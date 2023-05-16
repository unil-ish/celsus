import os
import tempfile
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader

APP_NAME = "Celsus Library"

st.set_page_config(
    page_title="Celsus Homepage",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="expanded",
)

# To avoid any resets due to interactions
if "valid_inputs_received" not in st.session_state:
    st.session_state["valid_inputs_received"] = False

# The page's title
st.title("Welcome to Celsus Library")


def q_a(file, query):
    """Use of the OpenAI models to answer questions on a given uploaded file.

    Args:
        file (str): Path to the PDF file that was uploaded.
        query (str): User's question that will need to be answered.

    Returns:
        dict: Returns a dictionary that holds the query(user's question)
        and the answer generated for the specific question.
    """

    # Load PDF file and split text
    loader = PyPDFLoader(file[0])
    texts = loader.load_and_split()

    # Use of the OpenAI Embeddings
    embeddings = OpenAIEmbeddings()

    # Use of Chroma to analyse texts with the OpenAI embeddings
    docsearch = Chroma.from_documents(texts, embeddings)

    # Answer chain
    q_a_c = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True
    )
    result = q_a_c({"query": query})
    return result


container = st.container()

# Shaping the page by structuring all important elements inside a container
with container:
    # Bypassing the need to create an account
    # Use of OpenAI API key to be able to use the Q&A Bot
    api_key = st.text_input(
        'API Key',
        type='password',
        help="Please enter your OpenAI API key. You may obtain your personal API key at: "
             "https://platform.openai.com/account/api-keys"
    )

    # File input field allowing user to upload their pdf file
    file = st.file_uploader(
        "Please upload your pdf file",
        type="pdf",
        key='pdf_file',
        accept_multiple_files=False
    )

    # Input for user Question
    prompt = st.text_input("Enter your question/request regarding your document.")

    # The following lines were greatly influenced by
    # https://colab.research.google.com/#fileId=https%3A//huggingface.co/spaces/sophiamyang/Panel_PDF_QA/blob/main/LangChain_QA_Panel_App.ipynb
    submit_button = st.button("Submit Question.")
    if submit_button:
        os.environ["OPENAI_API_KEY"] = api_key
        if file:
            with tempfile.TemporaryDirectory() as temp_dir:
                if file is not None:
                    with open(os.path.join(temp_dir, file.name), 'wb') as f:
                        f.write(file.read())
                prompt_text = prompt
                # If user input
                if prompt_text:
                    # Gathering of Q&A pair to publish it on the webpage
                    res = q_a(file=[os.path.join(temp_dir, file.name)],
                              query=prompt_text)
                    answer = res['result']
                    st.write(f"😊: {prompt_text}")
                    st.write("🤖:" + answer)
                    st.write("Relevant source text:")
                    source_text = []
                    # Quoting the direct text after the AI generated answer
                    for doc in res.get("source_documents"):
                        st.write(doc.page_content)
                        st.write("---")
                        source_text.append(doc.page_content)

                    # Button allowing user to download the answer and quoted text
                    combined_text = answer + "\n\n" + "\n\n".join(source_text)
                    st.download_button(
                        label="Download Answer",
                        data=combined_text,
                        file_name="answer_and_source.txt",
                        mime="text/plain"
                    )

    # Warning message if no api_key was entered
    if submit_button and not api_key:
        st.warning("Please input your OpenAI API key in order to proceed.")
        st.session_state.valid_inputs_received = False
        st.stop()

    # Warning message if there is no prompt
    elif submit_button and file and not prompt:
        st.warning("Please enter your question.")
        st.session_state.valid_inputs_received = False
        st.stop()

    # Warning message if there is/are no file/s uploaded
    elif submit_button and prompt and not file:
        st.warning("A document must first be uploaded.")
        st.session_state.valid_inputs_received = False
        st.stop()

    # Error message if no prompt and no file/s uploaded
    elif submit_button and not prompt and not file:
        st.error("Celsus is not a mindreader. Please upload your file/s and input your question.")
        st.session_state.valid_inputs_received = False
        st.stop()

    st.markdown("##")

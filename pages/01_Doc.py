import streamlit as st
from pathlib import Path

# Page containing all useful links
st.set_page_config(
    page_title="Doc",
    page_icon="📋",
    layout="centered",
)

st.title("User Guide")


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


intro_markdown = read_markdown_file(r'md_files\doc.md')
st.markdown(intro_markdown, unsafe_allow_html=True)

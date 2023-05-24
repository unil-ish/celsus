import streamlit as st
from pathlib import Path

# Terms of service page

st.set_page_config(
    page_title="Terms of service",
    page_icon="❗",
    layout="centered",
)

st.title("Terms of service")


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


intro_markdown = read_markdown_file(r'md_files\rules.md')
st.markdown(intro_markdown, unsafe_allow_html=True)

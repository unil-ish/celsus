import streamlit as st
import os
from pathlib import Path

# Page containing all useful links
st.set_page_config(
    page_title="Links",
    page_icon="🔗",
    layout="centered",
)

st.title("Useful Links")


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


intro_markdown = read_markdown_file(r'md_files\links.md')
st.markdown(intro_markdown, unsafe_allow_html=True)

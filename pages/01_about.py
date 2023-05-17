import streamlit as st
import base64
import os
from PIL import Image
from pathlib import Path

# Page containing all the information about Celsus

st.set_page_config(
    page_title="About Celsus",
    page_icon="❓",
    layout="centered",
)

st.title("What is Celsus Library?")


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


intro_markdown = read_markdown_file(r'md_files\about.md')
st.markdown(intro_markdown, unsafe_allow_html=True)


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

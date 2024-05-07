import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Coffee Sales", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Dashboard Coffee Sales")
st.subheader(":student: Muhammad Rifqi Naufal Irsyad - 09010622010")
st.markdown(
    "<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True
)
# Upload file
fl = st.file_uploader(":file_folder: Upload a File", type=["xlsx", "xls"])

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(fl)
else:
    st.warning("Upload file bernama 'jabodetabek_house_price.xlsx'")
    st.stop()
    try:
        df = pd.read_excel("jabodetabek_house_price.xlsx")
    except FileNotFoundError:
        st.error("File 'jabodetabek_house_price.xlsx' tidak ditemukan.")

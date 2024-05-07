import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Jabodetabek House Price", page_icon=":bar_chart:", layout="wide"
)
st.title(":bar_chart: Jabodetabek House Price")
st.subheader(":male-student: Ageng Putra Pratama - 09010622001")
st.subheader(":male-student: Muhammad Rifqi Naufal Irsyad - 09010622010")
st.subheader(":female-student: Rizki Cahyani Fitonah - 09010622010")
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

if not df.empty:
    st.write(df.head())

    # Exploratory Data Analysis (EDA)
    st.subheader("Exploratory Data Analysis (EDA)")

    # Summary Statistics
    st.write("Deskripsi Data:")
    st.write(df.describe())

    # Missing Values
    st.write("Jumlah Missing Values per Kolom:")
    st.write(df.isnull().sum())

    #bar chart
    st.subheader("Bar Chart")
    bar_chart = px.bar(df, x='city', y='price_in_rp', title='Harga Properti di Jabodetabek', labels={'city': 'Kota/Kabupaten', 'price_in_rp': 'Harga (IDR)'})
    st.plotly_chart(bar_chart)

    
    # Visualisasi distribusi harga properti dalam rupiah
    st.subheader("Distribusi Harga Properti")
    hist_chart = px.histogram(df, x='price_in_rp', nbins=30, title='Distribusi Harga Properti')
    st.plotly_chart(hist_chart)

    # Visualisasi distribusi jumlah kamar tidur dan kamar mandi
    st.subheader("Distribusi Jumlah Kamar Tidur dan Kamar Mandi")
    bedroom_chart = px.histogram(df, x='bedrooms', title='Distribusi Jumlah Kamar Tidur')
    bathroom_chart = px.histogram(df, x='bathrooms', title='Distribusi Jumlah Kamar Mandi')
    st.plotly_chart(bedroom_chart)
    st.plotly_chart(bathroom_chart)

    # Visualisasi distribusi luas tanah dan luas bangunan
    st.subheader("Distribusi Luas Tanah dan Luas Bangunan")
    land_size_chart = px.histogram(df, x='land_size_m2', nbins=30, title='Distribusi Luas Tanah (m2)')
    building_size_chart = px.histogram(df, x='building_size_m2', nbins=30, title='Distribusi Luas Bangunan (m2)')
    st.plotly_chart(land_size_chart)
    st.plotly_chart(building_size_chart)

    # Menghapus kolom non-numerik
    df_numeric = df.drop(columns=['url', 'title', 'address', 'district', 'city'])

    # Mengubah tipe data kolom yang tersisa ke numerik
    df_numeric = df_numeric.apply(pd.to_numeric, errors='coerce')

    # Menghapus baris yang mengandung nilai NaN
    df_numeric = df_numeric.dropna()

    # Korelasi antara harga properti dengan property_condition
    st.subheader("Korelasi antara Harga Properti dengan Kondisi Properti")
    correlation = df_numeric[['price_in_rp', 'property_condition']].corr()
    fig = px.imshow(correlation, labels=dict(x="Variabel", y="Variabel", color="Korelasi"), x=correlation.index, y=correlation.columns)
    st.plotly_chart(fig)
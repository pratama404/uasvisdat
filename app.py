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
st.text("Ageng Putra Pratama - 09010622001")
st.text("Muhammad Rifqi Naufal Irsyad - 09010622010")
st.text("Rizki Cahyani Fitonah")
st.markdown(
    "<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True
)
# Upload file
fl = st.file_uploader(":file_folder: Upload a File", type=["xlsx", "xls"])

try:
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_excel(fl)
    else:
        df = pd.read_excel("jabodetabek_house_price.xlsx")
except FileNotFoundError:
    st.error(
        "File not found. Please make sure you have uploaded the correct file or provide the correct path to the default file."
    )
except Exception as e:
    st.error(f"An error occurred: {e}")

if st.sidebar.checkbox("Lihat EDA dulu !"):
    # Exploratory Data Analysis (EDA)
    st.subheader("Exploratory Data Analysis (EDA)")
    st.write(df.head())

    # Summary Statistics
    st.write("Deskripsi Data:")
    st.write(df.describe())

    # Missing Values
    st.write("Jumlah Missing Values per Kolom:")
    st.write(df.isnull().sum())


# Filter
st.sidebar.header("Filter:")

city = st.sidebar.multiselect(":world_map: Kota", df["city"].dropna().unique())
if not city:
    df_filtered = df.copy()
else:
    df_filtered = df[df["city"].isin(city)]

district = st.sidebar.multiselect(
    ":cityscape: Kawasan", df["district"].dropna().unique()
)
if not district:
    df_filtered = df.copy()
else:
    df_filtered = df[df["district"].isin(district)]

alamat = st.sidebar.multiselect("📌 Alamat", df["address"].dropna().unique())
if not alamat:
    df_filtered = df.copy()
else:
    df_filtered = df[df["address"].isin(alamat)]

# Sertifikat Filter
sertifikat = st.sidebar.multiselect(
    "📜 Jenis Sertifikat", df["certificate"].dropna().unique()
)
if not sertifikat:
    df_filtered = df.copy()
else:
    df_filtered = df[df["certificate"].isin(sertifikat)]


# Mengambil semua kemungkinan fasilitas yang tidak kosong
all_facilities = set()
for facilities_list in df["facilities"]:
    facilities = facilities_list.split(", ")
    all_facilities.update(facilities)

# Mengurutkan fasilitas yang tidak kosong dalam bentuk daftar
all_facilities = sorted([facility for facility in all_facilities if facility])

selected_facilities = st.sidebar.multiselect("🎱 Fasilitas", all_facilities)

if not selected_facilities:
    df_filtered = df.copy()
else:
    mask = df["facilities"].apply(
        lambda x: any(facility in x for facility in selected_facilities)
    )
    df_filtered = df[mask & (df["facilities"] != "")]


# Harga
min_price_column, max_price_column = st.sidebar.columns(2)

min_price = min_price_column.number_input("💵 Harga Minimum", min_value=0, value=0)

max_price = max_price_column.number_input(
    "💶 Harga Maksimum", min_value=0, value=df["price_in_rp"].max()
)

# Menerapkan filter
df_filtered = df[(df["price_in_rp"] >= min_price) & (df["price_in_rp"] <= max_price)]

# Expander untuk Advanced Filters
with st.sidebar.expander("Advanced Filters", expanded=True):
    min_building_age, max_building_age = st.columns(2)
    min_building_age = min_building_age.number_input(
        "Usia Bangunan Minimum (Tahun)", min_value=0, value=0
    )
    max_building_age = max_building_age.number_input(
        "Usia Bangunan Maksimum (Tahun)",
        min_value=0,
        value=int(df["building_age"].max()),
    )
    df_filtered = df[
        (df["building_age"] >= min_building_age)
        & (df["building_age"] <= max_building_age)
    ]

    # Filter Tahun Pembangunan
    min_year_built, max_year_built = st.columns(2)
    min_year_built = min_year_built.number_input(
        "Tahun Pembangunan Minimum",
        min_value=int(df["year_built"].min()),
        max_value=int(df["year_built"].max()),
        value=int(df["year_built"].min()),
    )
    max_year_built = max_year_built.number_input(
        "Tahun Pembangunan Maksimum",
        min_value=int(df["year_built"].min()),
        max_value=int(df["year_built"].max()),
        value=int(df["year_built"].max()),
    )

    df_filtered = df[
        (df["year_built"] >= min_year_built) & (df["year_built"] <= max_year_built)
    ]

    # Filter Luas Tanah
    min_land_size, max_land_size = st.columns(2)
    min_land_size = min_land_size.number_input(
        "Luas Tanah Minimum (m^2)", min_value=0, value=0
    )
    max_land_size = max_land_size.number_input(
        "Luas Tanah Maksimum (m^2)", min_value=0, value=int(df["land_size_m2"].max())
    )
    df_filtered_land_size = df[
        (df["land_size_m2"] >= min_land_size) & (df["land_size_m2"] <= max_land_size)
    ]

    # Filter Luas Bangunan
    min_building_size, max_building_size = st.columns(2)
    min_building_size = min_building_size.number_input(
        "Luas Bangunan Minimum (m^2)", min_value=0, value=0
    )
    max_building_size = max_building_size.number_input(
        "Luas Bangunan Maksimum (m^2)",
        min_value=0,
        value=int(df["building_size_m2"].max()),
    )
    df_filtered_building_size = df[
        (df["building_size_m2"] >= min_building_size)
        & (df["building_size_m2"] <= max_building_size)
    ]
    floors = st.multiselect("🪜 Jumlah Lantai", df["floors"].dropna().unique())
    if floors:
        df_filtered = df[df["floors"].isin(floors)]
    else:
        df_filtered = df.copy()

    listrik = st.multiselect(
        "🔌 Kelistrikan", df["electricity"].dropna().unique()
    )
    if listrik:
        df_filtered = df[df["electricity"].isin(listrik)]
    else:
        df_filtered = df.copy()

    kondisi = st.multiselect(
        "🏡 Kondisi", df["property_condition"].dropna().unique()
    )
    if kondisi:
        df_filtered = df[df["property_condition"].isin(kondisi)]
    else:
        df_filtered = df.copy()

    orientasi = st.multiselect(
        "🧭 Orientasi Bangunan", df["building_orientation"].dropna().unique()
    )
    if orientasi:
        df_filtered = df[df["building_orientation"].isin(orientasi)]
    else:
        df_filtered = df.copy()

    furnish = st.multiselect("🪑 Perabotan", df["furnishing"].dropna().unique())
    if furnish:
        df_filtered = df[df["furnishing"].isin(furnish)]
    else:
        df_filtered = df.copy()

    bedrooms = st.multiselect(
        "🛏️ Jumlah Kamar Tidur", df["bedrooms"].dropna().unique()
    )
    if bedrooms:
        df_filtered = df[df["bedrooms"].isin(bedrooms)]
    else:
        df_filtered = df.copy()

    bathrooms = st.multiselect(
        "🛁 Jumlah Kamar Mandi", df["bathrooms"].dropna().unique()
    )
    if bathrooms:
        df_filtered = df[df["bathrooms"].isin(bathrooms)]
    else:
        df_filtered = df.copy()

    carports = st.multiselect(
        "🏎 Jumlah Carport", df["carports"].dropna().unique()
    )
    if carports:
        df_filtered = df[df["carports"].isin(carports)]
    else:
        df_filtered = df.copy()

    maid_bedrooms = st.multiselect(
        "🛏 Jumlah Kamar Pembantu", df["maid_bedrooms"].dropna().unique()
    )
    if maid_bedrooms:
        df_filtered = df[df["maid_bedrooms"].isin(maid_bedrooms)]
    else:
        df_filtered = df.copy()

    maid_bathrooms = st.multiselect(
        "🚽 Jumlah Kamar Mandi Pembantu", df["maid_bathrooms"].dropna().unique()
    )
    if maid_bathrooms:
        df_filtered = df[df["maid_bathrooms"].isin(maid_bathrooms)]
    else:
        df_filtered = df.copy()

    garages = st.multiselect("🏎️ Jumlah Garasi", df["garages"].dropna().unique())
    if garages:
        df_filtered = df[df["garages"].isin(garages)]
    else:
        df_filtered = df.copy()

if not df.empty:
    # bar chart
    st.subheader("Bar Chart")
    bar_chart = px.bar(
        df,
        x="city",
        y="price_in_rp",
        title="Harga Properti di Jabodetabek",
        labels={"city": "Kota/Kabupaten", "price_in_rp": "Harga (IDR)"},
    )
    st.plotly_chart(bar_chart)

    # Visualisasi distribusi harga properti dalam rupiah

    st.subheader("Distribusi Harga Properti")
    hist_chart = px.histogram(
        df, x="price_in_rp", nbins=30, title="Distribusi Harga Properti"
    )
    st.plotly_chart(hist_chart)

    # Visualisasi distribusi jumlah kamar tidur dan kamar mandi
    st.subheader("Distribusi Jumlah Kamar Tidur dan Kamar Mandi")
    bedroom_chart = px.histogram(
        df, x="bedrooms", title="Distribusi Jumlah Kamar Tidur"
    )
    bathroom_chart = px.histogram(
        df, x="bathrooms", title="Distribusi Jumlah Kamar Mandi"
    )
    st.plotly_chart(bedroom_chart)
    st.plotly_chart(bathroom_chart)

    # Visualisasi distribusi luas tanah dan luas bangunan
    st.subheader("Distribusi Luas Tanah dan Luas Bangunan")
    land_size_chart = px.histogram(
        df, x="land_size_m2", nbins=30, title="Distribusi Luas Tanah (m2)"
    )
    building_size_chart = px.histogram(
        df, x="building_size_m2", nbins=30, title="Distribusi Luas Bangunan (m2)"
    )
    st.plotly_chart(land_size_chart)
    st.plotly_chart(building_size_chart)

    # Menghapus kolom non-numerik
    df_numeric = df.drop(columns=["url", "title", "address", "district", "city"])

    # Mengubah tipe data kolom yang tersisa ke numerik
    df_numeric = df_numeric.apply(pd.to_numeric, errors="coerce")

    # Menghapus baris yang mengandung nilai NaN
    df_numeric = df_numeric.dropna()

    # Korelasi antara harga properti dengan property_condition
    st.subheader("Korelasi antara Harga Properti dengan Kondisi Properti")
    correlation = df_numeric[["price_in_rp", "property_condition"]].corr()
    fig = px.imshow(
        correlation,
        labels=dict(x="Variabel", y="Variabel", color="Korelasi"),
        x=correlation.index,
        y=correlation.columns,
    )
    st.plotly_chart(fig)

    # Scatter Plot
    st.subheader("Scatter Plot")
    scatter_plot = px.scatter(
        df,
        x="building_size_m2",
        y="price_in_rp",
        title="Hubungan Antara Luas Bangunan dan Harga Properti",
    )
    st.plotly_chart(scatter_plot)

    # Line Plot
    st.subheader("Line Plot")
    line_plot = px.line(
        df,
        x="year_built",
        y="price_in_rp",
        title="Trend Harga Properti Berdasarkan Tahun Pembangunan",
    )
    st.plotly_chart(line_plot)

    # Pie Chart
    st.subheader("Pie Chart")
    pie_chart = px.pie(
        df, names="property_condition", title="Persentase Kondisi Properti"
    )
    st.plotly_chart(pie_chart)

    # Histogram
    st.subheader("Histogram")
    histogram = px.histogram(df, x="price_in_rp", title="Distribusi Harga Properti")
    st.plotly_chart(histogram)

    # Box Plot
    st.subheader("Box Plot")
    box_plot = px.box(df, y="price_in_rp", title="Box Plot Harga Properti")
    st.plotly_chart(box_plot)

    # Density Contour Plot
    st.subheader("Density Contour Plot")
    density_contour = px.density_contour(
        df,
        x="building_size_m2",
        y="land_size_m2",
        title="Density Contour Plot Luas Bangunan vs Luas Tanah",
    )
    st.plotly_chart(density_contour)

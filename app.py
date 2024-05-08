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


try:
    df = pd.read_excel("jabodetabek_house_price.xlsx")
except FileNotFoundError:
    st.error(
        "File not found. Please make sure you have uploaded the correct file or provide the correct path to the default file."
    )
except Exception as e:
    st.error(f"An error occurred: {e}")


# Filter function
def apply_filters(data_frame):
    # Filter
    st.sidebar.header("Filter:")

    city = st.sidebar.multiselect(
        ":world_map: Kota", data_frame["city"].dropna().unique()
    )
    if not city:
        df_filtered = data_frame.copy()
    else:
        df_filtered = data_frame[data_frame["city"].isin(city)]

    district = st.sidebar.multiselect(
        ":cityscape: Kawasan", df_filtered["district"].dropna().unique()
    )
    if not district:
        df_filtered = df_filtered.copy()
    else:
        df_filtered = df_filtered[df_filtered["district"].isin(district)]

    alamat = st.sidebar.multiselect(
        "📌 Alamat", df_filtered["address"].dropna().unique()
    )
    if not alamat:
        df_filtered = df_filtered.copy()
    else:
        df_filtered = df_filtered[df_filtered["address"].isin(alamat)]

    # Sertifikat Filter
    sertifikat = st.sidebar.multiselect(
        "📜 Jenis Sertifikat", df_filtered["certificate"].dropna().unique()
    )
    if not sertifikat:
        df_filtered = df_filtered.copy()
    else:
        df_filtered = df_filtered[df_filtered["certificate"].isin(sertifikat)]

    # Mengambil semua kemungkinan fasilitas yang tidak kosong
    all_facilities = set()
    for facilities_list in df_filtered["facilities"]:
        facilities = facilities_list.split(", ")
        all_facilities.update(facilities)

    # Mengurutkan fasilitas yang tidak kosong dalam bentuk daftar
    all_facilities = sorted(
        [facility for facility in all_facilities if facility]
    )  # changed 'if facility' from 'if facility in all_facilities'

    selected_facilities = st.sidebar.multiselect(
        "🎱 Fasilitas", all_facilities
    )  # changed 'all_facilities' from 'df_filtered'

    if not selected_facilities:
        df_filtered = df_filtered.copy()
    else:
        mask = df_filtered["facilities"].apply(
            lambda x: any(facility in x for facility in selected_facilities)
        )
        df_filtered = df_filtered[mask & (df_filtered["facilities"] != "")]

    # Harga
    min_price_column, max_price_column = st.sidebar.columns(2)

    min_price = min_price_column.number_input("💵 Harga Minimum", min_value=0, value=0)

    max_price = max_price_column.number_input(
        "💶 Harga Maksimum", min_value=0, value=df_filtered["price_in_rp"].max()
    )

    # Menerapkan filter
    df_filtered = df_filtered[
        (df_filtered["price_in_rp"] >= min_price)
        & (df_filtered["price_in_rp"] <= max_price)
    ]

    # Expander untuk Advanced Filters
    with st.sidebar.expander("Advanced Filters", expanded=True):
        min_building_age, max_building_age = st.columns(2)
        min_building_age = min_building_age.number_input(
            "Usia Bangunan Minimum (Tahun)", min_value=0, value=0
        )
        max_building_age = max_building_age.number_input(
            "Usia Bangunan Maksimum (Tahun)",
            min_value=0,
            value=int(df_filtered["building_age"].max()),
        )
        df_filtered = df_filtered[
            (df_filtered["building_age"] >= min_building_age)
            & (df_filtered["building_age"] <= max_building_age)
        ]

        # Filter Tahun Pembangunan
        min_year_built, max_year_built = st.columns(2)
        min_year_built = min_year_built.number_input(
            "Tahun Pembangunan Minimum",
            min_value=int(df_filtered["year_built"].min()),
            max_value=int(df_filtered["year_built"].max()),
            value=int(df_filtered["year_built"].min()),
        )
        max_year_built = max_year_built.number_input(
            "Tahun Pembangunan Maksimum",
            min_value=int(df_filtered["year_built"].min()),
            max_value=int(df_filtered["year_built"].max()),
            value=int(df_filtered["year_built"].max()),
        )

        df_filtered = df_filtered[
            (df_filtered["year_built"] >= min_year_built)
            & (df_filtered["year_built"] <= max_year_built)
        ]

        # Filter Luas Tanah
        min_land_size, max_land_size = st.columns(2)
        min_land_size = min_land_size.number_input(
            "Luas Tanah Minimum (m²)", min_value=0, value=0
        )
        max_land_size = max_land_size.number_input(
            "Luas Tanah Maksimum (m²)",
            min_value=0,
            value=int(df_filtered["land_size_m2"].max()),
        )
        df_filtered_land_size = df_filtered[
            (df_filtered["land_size_m2"] >= min_land_size)
            & (df_filtered["land_size_m2"] <= max_land_size)
        ]

        # Filter Luas Bangunan
        min_building_size, max_building_size = st.columns(2)
        min_building_size = min_building_size.number_input(
            "Luas Bangunan Minimum (m²)", min_value=0, value=0
        )
        max_building_size = max_building_size.number_input(
            "Luas Bangunan Maksimum (m²)",
            min_value=0,
            value=int(df_filtered["building_size_m2"].max()),
        )
        df_filtered_building_size = df_filtered[
            (df_filtered["building_size_m2"] >= min_building_size)
            & (df_filtered["building_size_m2"] <= max_building_size)
        ]
        floors = st.multiselect(
            "🪜 Jumlah Lantai", df_filtered["floors"].dropna().unique()
        )
        if not floors:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["floors"].isin(floors)]

        listrik = st.multiselect(
            "🔌 Kelistrikan", df_filtered["electricity"].dropna().unique()
        )
        if not listrik:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["electricity"].isin(listrik)]

        kondisi = st.multiselect(
            "🏡 Kondisi", df_filtered["property_condition"].dropna().unique()
        )
        if not kondisi:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["property_condition"].isin(kondisi)]

        orientasi = st.multiselect(
            "🧭 Orientasi Bangunan",
            df_filtered["building_orientation"].dropna().unique(),
        )
        if not orientasi:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[
                df_filtered["building_orientation"].isin(orientasi)
            ]

        furnish = st.multiselect(
            "🪑 Perabotan", df_filtered["furnishing"].dropna().unique()
        )
        if not furnish:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["furnishing"].isin(furnish)]

        bedrooms = st.multiselect(
            "🛏️ Jumlah Kamar Tidur", df_filtered["bedrooms"].dropna().unique()
        )
        if not bedrooms:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["bedrooms"].isin(bedrooms)]

        bathrooms = st.multiselect(
            "🛁 Jumlah Kamar Mandi", df_filtered["bathrooms"].dropna().unique()
        )
        if not bathrooms:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["bathrooms"].isin(bathrooms)]

        carports = st.multiselect(
            "🏎 Jumlah Carport", df_filtered["carports"].dropna().unique()
        )
        if not carports:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["carports"].isin(carports)]

        maid_bedrooms = st.multiselect(
            "🛏 Jumlah Kamar Pembantu",
            df_filtered["maid_bedrooms"].dropna().unique(),
        )
        if not maid_bedrooms:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["maid_bedrooms"].isin(maid_bedrooms)]

        maid_bathrooms = st.multiselect(
            "🚽 Jumlah Kamar Mandi Pembantu",
            df_filtered["maid_bathrooms"].dropna().unique(),
        )
        if not maid_bathrooms:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[
                df_filtered["maid_bathrooms"].isin(maid_bathrooms)
            ]

        garages = st.multiselect("🏎️ Jumlah Garasi", df["garages"].dropna().unique())
        if not garages:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["garages"].isin(garages)]

    return df_filtered


# Apply filters
df_filtered = apply_filters(df)

if st.checkbox("Show EDA"):
    # Exploratory Data Analysis (EDA)
    st.header("Exploratory Data Analysis (EDA)")
    st.write(df_filtered.head())

    # Summary Statistics
    st.subheader("Deskripsi Data:")
    st.write(df_filtered.describe())

    # Missing Values
    st.subheader("Jumlah Missing Values per Kolom:")
    st.write(df_filtered.isnull().sum())

st.subheader("Bar Chart")
bar_chart = px.bar(
    df_filtered,
    x="city",
    y="price_in_rp",
    title="Harga Properti di Jabodetabek",
    labels={"city": "Kota/Kabupaten", "price_in_rp": "Harga (IDR)"},
)
st.plotly_chart(bar_chart)

# Visualisasi distribusi harga properti dalam rupiah

st.subheader("Distribusi Harga Properti")
hist_chart = px.histogram(
    df_filtered, x="price_in_rp", nbins=30, title="Distribusi Harga Properti"
)
st.plotly_chart(hist_chart)

# Visualisasi distribusi jumlah kamar tidur dan kamar mandi
st.subheader("Distribusi Jumlah Kamar Tidur dan Kamar Mandi")
bedroom_chart = px.histogram(
    df_filtered, x="bedrooms", title="Distribusi Jumlah Kamar Tidur"
)
bathroom_chart = px.histogram(
    df_filtered, x="bathrooms", title="Distribusi Jumlah Kamar Mandi"
)
st.plotly_chart(bedroom_chart)
st.plotly_chart(bathroom_chart)

# Visualisasi distribusi luas tanah dan luas bangunan
st.subheader("Distribusi Luas Tanah dan Luas Bangunan")
land_size_chart = px.histogram(
    df_filtered, x="land_size_m2", nbins=30, title="Distribusi Luas Tanah (m2)"
)
building_size_chart = px.histogram(
    df_filtered,
    x="building_size_m2",
    nbins=30,
    title="Distribusi Luas Bangunan (m2)",
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
    df_filtered,
    x="building_size_m2",
    y="price_in_rp",
    title="Hubungan Antara Luas Bangunan dan Harga Properti",
)
st.plotly_chart(scatter_plot)

# Line Plot
st.subheader("Line Plot")
line_plot = px.line(
    df_filtered,
    x="year_built",
    y="price_in_rp",
    title="Trend Harga Properti Berdasarkan Tahun Pembangunan",
)
st.plotly_chart(line_plot)

# Pie Chart
st.subheader("Pie Chart")
pie_chart = px.pie(
    df_filtered, names="property_condition", title="Persentase Kondisi Properti"
)
st.plotly_chart(pie_chart)

# Histogram
st.subheader("Histogram")
histogram = px.histogram(
    df_filtered, x="price_in_rp", title="Distribusi Harga Properti"
)
st.plotly_chart(histogram)

# Box Plot
st.subheader("Box Plot")
box_plot = px.box(df_filtered, y="price_in_rp", title="Box Plot Harga Properti")
st.plotly_chart(box_plot)

# Density Contour Plot
st.subheader("Density Contour Plot")
density_contour = px.density_contour(
    df_filtered,
    x="building_size_m2",
    y="land_size_m2",
    title="Density Contour Plot Luas Bangunan vs Luas Tanah",
)
st.plotly_chart(density_contour)

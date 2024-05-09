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
    all_facilities = sorted([facility for facility in all_facilities if facility])

    selected_facilities = st.sidebar.multiselect("🎱 Fasilitas", all_facilities)

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

    # Filter Usia Bangunan
    min_building_age, max_building_age = st.sidebar.slider(
        "Usia Bangunan (Tahun)",
        min_value=0,
        max_value=int(df_filtered["building_age"].max()),
        value=(0, int(df_filtered["building_age"].max())),
    )

    df_filtered = df_filtered[
        (df_filtered["building_age"] >= min_building_age)
        & (df_filtered["building_age"] <= max_building_age)
    ]

    # Filter Tahun Pembangunan
    min_year_built, max_year_built = st.sidebar.slider(
        "Tahun Pembangunan",
        min_value=int(df_filtered["year_built"].min()),
        max_value=int(df_filtered["year_built"].max()),
        value=(
            int(df_filtered["year_built"].min()),
            int(df_filtered["year_built"].max()),
        ),
    )

    df_filtered = df_filtered[
        (df_filtered["year_built"] >= min_year_built)
        & (df_filtered["year_built"] <= max_year_built)
    ]

    # Filter Luas Tanah
    min_land_size, max_land_size = st.sidebar.slider(
        "Luas Tanah (m²)",
        min_value=0,
        max_value=int(df_filtered["land_size_m2"].max()),
        value=(0, int(df_filtered["land_size_m2"].max())),
    )

    df_filtered = df_filtered[
        (df_filtered["land_size_m2"] >= min_land_size)
        & (df_filtered["land_size_m2"] <= max_land_size)
    ]

    # Filter Luas Bangunan
    min_building_size, max_building_size = st.sidebar.slider(
        "Luas Bangunan (m²)",
        min_value=0,
        max_value=int(df_filtered["building_size_m2"].max()),
        value=(0, int(df_filtered["building_size_m2"].max())),
    )

    df_filtered = df_filtered[
        (df_filtered["building_size_m2"] >= min_building_size)
        & (df_filtered["building_size_m2"] <= max_building_size)
    ]

    if df_filtered.empty:
        st.warning("Data tidak ditemukan dengan filter yang diterapkan.")
        return df_filtered
    # Expander untuk Advanced Filters
    with st.sidebar.expander("Advanced Filters", expanded=True):

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

        garages = st.multiselect(
            "🏎️ Jumlah Garasi", df_filtered["garages"].dropna().unique()
        )
        if not garages:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["garages"].isin(garages)]

    return df_filtered


# Apply filters
df_filtered = apply_filters(df)


st.sidebar.button("Clear All Filters")


def Home(df_filtered):
    jumlah_rumah = df_filtered["url"].nunique()
    avg_harga = df_filtered["price_in_rp"].mean()
    max_harga = df_filtered["price_in_rp"].max()
    min_harga = df_filtered["price_in_rp"].min()

    # Ubah harga ke dalam satuan miliar
    avg_harga_miliar = avg_harga / 1e9
    max_harga_miliar = max_harga / 1e9
    min_harga_juta = min_harga / 1e6

    # Menampilkan summary
    total1, total2, total3, total4 = st.columns(4, gap="large")
    with total1:
        st.info(":pencil: Jumlah Rumah yang Dijual")
        st.metric(label="Count of Houses", value=f"{jumlah_rumah:.2f}")
    with total2:
        st.info(":pencil: Rata-Rata Harga Rumah")
        st.metric(label="Average of Price", value=f"${avg_harga_miliar:.2f}B")
    with total3:
        st.info(":pencil: Harga Rumah Tertinggi")
        st.metric(label="Max of Price", value=f"${max_harga_miliar}B")
    with total4:
        st.info(":pencil: Harga Rumah Terdendah")
        st.metric(label="Min of Price", value=f"${min_harga_juta}M")


# Panggil method yang sudah dibuat dengan DataFrame yang sudah difilter
Home(df_filtered)

# Visualisasi data
st.header("Visualisasi Data")

col1, col2 = st.columns((2))

# persentase Properti Berdasarkan kota
with col1:
    fig_persentase_kota = px.pie(
        df_filtered["city"].value_counts(),
        values=df_filtered["city"].value_counts().values,
        names=df_filtered["city"].value_counts().index,
        title="Persentase Properti Berdasarkan Kota",
    )
    fig_persentase_kota.update_traces(textinfo="label+percent", textposition="outside")
    fig_persentase_kota.update_layout(showlegend=False)
    st.plotly_chart(fig_persentase_kota, use_container_width=True)

# persentase Properti Berdasarkan Tipe Sertifikat
with col2:
    fig_persentase_sertifikat = px.pie(
        df_filtered["certificate"].value_counts(),
        values=df_filtered["certificate"].value_counts().values,
        names=df_filtered["certificate"].value_counts().index,
        title="Persentase Properti Berdasarkan Tipe Sertifikat",
    )
    # fig_distribusi_sertifikat.update_traces(textinfo="label+percent", textposition="outside")
    st.plotly_chart(fig_persentase_sertifikat, use_container_width=True)

# persentase Properti Berdasarkan Orientas Bangunan
with col1:
    fig_persentase_kondisi_bangunan = px.pie(
        df_filtered["building_orientation"].value_counts(),
        values=df_filtered["building_orientation"].value_counts().values,
        names=df_filtered["building_orientation"].value_counts().index,
        title="Distribusi Properti Berdasarkan Orientasi Bangunan",
    )
    fig_persentase_kondisi_bangunan.update_traces(
        textinfo="label+percent", textposition="outside"
    )
    fig_persentase_kondisi_bangunan.update_layout(showlegend=False)
    st.plotly_chart(fig_persentase_kondisi_bangunan, use_container_width=True)

# persentase Properti Berdasarkan Kondisi Bangunan
with col2:
    fig_persentase_orientasi_bangunan = px.pie(
        df_filtered["property_condition"].value_counts(),
        values=df_filtered["property_condition"].value_counts().values,
        names=df_filtered["property_condition"].value_counts().index,
        title="Distribusi Properti Berdasarkan Kondisi Bangunan",
    )
    fig_persentase_orientasi_bangunan.update_traces(
        textinfo="label+percent", textposition="outside"
    )
    fig_persentase_orientasi_bangunan.update_layout(showlegend=False)
    st.plotly_chart(fig_persentase_orientasi_bangunan, use_container_width=True)

# BARRRRRRR
# BARRRRRRR
# BARRRRRRR
# BARRRRRRR
# BARRRRRRR


# KOTAAAAAAA
with col1:
    fig = px.bar(
        df_filtered,
        x="city",
        y="price_in_rp",
        title="Harga Properti di Jabodetabek Berdasarkan Kota",
        labels={"city": "Kota", "price_in_rp": "Harga (IDR)"},
        color="city",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        df_filtered["city"].value_counts(),
        x=df_filtered["city"].value_counts().index,
        y=df_filtered["city"].value_counts().values,
        title="Banyaknya Properti yang Dijual Berdasarkan Kota",
        labels={"x": "Kota", "y": "Jumlah Properti"},
    )
    fig.update_traces(
        text=df_filtered["city"].value_counts().values, textposition="outside"
    )
    st.plotly_chart(fig, use_container_width=True)

# TIPE SERTIFIKAT
with col1:
    fig = px.bar(
        df_filtered,
        x="certificate",
        y="price_in_rp",
        title="Harga Properti di Jabodetabek Berdasarkan Tipe Sertifikat",
        labels={"certificate": "Tipe Sertifikat", "price_in_rp": "Harga (IDR)"},
        color="certificate",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        df_filtered["certificate"].value_counts(),
        x=df_filtered["certificate"].value_counts().index,
        y=df_filtered["certificate"].value_counts().values,
        title="Banyaknya Properti yang Dijual Berdasarkan Tipe Sertifikat",
        labels={"x": "Tipe Sertifikat", "y": "Jumlah Properti"},
    )
    fig.update_traces(
        text=df_filtered["certificate"].value_counts().values, textposition="outside"
    )
    st.plotly_chart(fig, use_container_width=True)

# Orientasi Bangunan
with col1:
    fig = px.bar(
        df_filtered,
        x="building_orientation",
        y="price_in_rp",
        title="Harga Properti di Jabodetabek Berdasarkan Orientasi Properti",
        labels={
            "building_orientation": "Orientasi Properti",
            "price_in_rp": "Harga (IDR)",
        },
        color="building_orientation",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        df_filtered["building_orientation"].value_counts(),
        x=df_filtered["building_orientation"].value_counts().index,
        y=df_filtered["building_orientation"].value_counts().values,
        title="Banyaknya Properti yang Dijual Berdasarkan Orientasi Properti",
        labels={"x": "Building Orientation", "y": "Jumlah Properti"},
    )
    fig.update_traces(
        text=df_filtered["building_orientation"].value_counts().values,
        textposition="outside",
    )
    st.plotly_chart(fig, use_container_width=True)

# KONDISIIIIIIIII
with col1:
    fig = px.bar(
        df_filtered,
        x="property_condition",
        y="price_in_rp",
        title="Harga Properti di Jabodetabek Berdasarkan Kondisi Properti",
        labels={"property_condition": "Kondisi Bangunan", "price_in_rp": "Harga (IDR)"},
        color="property_condition",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        df_filtered["property_condition"].value_counts(),
        x=df_filtered["property_condition"].value_counts().index,
        y=df_filtered["property_condition"].value_counts().values,
        title="Banyaknya Properti yang Dijual Berdasarkan Kondisi Properti",
        labels={"x": "Kondisi Properti", "y": "Jumlah Properti"},
    )
    fig.update_traces(
        text=df_filtered["property_condition"].value_counts().values,
        textposition="outside",
    )
    st.plotly_chart(fig, use_container_width=True)


# BOX PLOT
#
#
#
#

df_filtered["count_bedrooms"] = df_filtered.groupby("bedrooms")["bedrooms"].transform(
    "count"
)

# Korelasi Antara Harga Properti dan Jumlah Kamar Tidur
with col1:
    fig_corr_harga_kamar_tidur = px.scatter(
        df_filtered,
        x="bedrooms",
        y="price_in_rp",
        title="Korelasi Antara Harga Properti dan Jumlah Kamar Tidur",
    )
    st.plotly_chart(fig_corr_harga_kamar_tidur, use_container_width=True)

# Korelasi Antara Harga Properti dan Jumlah Kamar Mandi
with col2:
    fig_corr_harga_kamar_mandi = px.scatter(
        df_filtered,
        x="bathrooms",
        y="price_in_rp",
        title="Korelasi Antara Harga Properti dan Jumlah Kamar Mandi",
    )
    st.plotly_chart(fig_corr_harga_kamar_mandi, use_container_width=True)

# Korelasi Antara Harga Properti dan Luas Tanah
with col1:
    fig_corr_harga_luas_tanah = px.scatter(
        df_filtered,
        x="land_size_m2",
        y="price_in_rp",
        title="Korelasi Antara Harga Properti dan Luas Tanah",
    )
    st.plotly_chart(fig_corr_harga_luas_tanah, use_container_width=True)

# Korelasi Antara Harga Properti dan Luas Bangunan
with col2:
    fig_corr_harga_luas_bangunan = px.scatter(
        df_filtered,
        x="building_size_m2",
        y="price_in_rp",
        title="Korelasi Antara Harga Properti dan Luas Bangunan",
    )
    st.plotly_chart(fig_corr_harga_luas_bangunan, use_container_width=True)


# Tren Harga Properti dari Waktu ke Waktu
linechartHarga = df_filtered.groupby("year_built")["price_in_rp"].sum().reset_index()
fig_tren_harga_waktu = px.area(
    linechartHarga,
    x="year_built",
    y="price_in_rp",
    title="Tren Harga Properti berdasarkan Tahun Pembangunan",
)
st.plotly_chart(fig_tren_harga_waktu, use_container_width=True)

with st.expander("TimeSeries Harga Bangunan"):
    st.write(linechartHarga.T.style.background_gradient(cmap="Blues"))
    csv = linechartHarga.to_csv(index=False).encode("UTf-8")
    st.download_button(
        "Download Data", data=csv, file_name="TimeSeriesHarga.csv", mime="text/csv"
    )
# -----------------------------------------------------------------

# Hitung jumlah properti yang dijual berdasarkan tahun pembangunan
properti_per_tahun = df_filtered["year_built"].value_counts().reset_index()
properti_per_tahun.columns = ["year_built", "jumlah_properti"]

# Tren Banyaknya Properti dijual dari Waktu ke Waktu
fig = px.area(
    properti_per_tahun,
    x="year_built",
    y="jumlah_properti",
    title="Tren Banyaknya Properti Dijual berdasarkan Tahun Pembangunan",
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("TimeSeries Jumlah Properti"):
    st.write(properti_per_tahun.T.style.background_gradient(cmap="Blues"))
    csv = properti_per_tahun.to_csv(index=False).encode("UTf-8")
    st.download_button(
        "Download Data",
        data=csv,
        file_name="TimeSeriesJumlahProperti.csv",
        mime="text/csv",
    )


# TREE MAP
# TREE MAP
jumlahByKotaDist = (
    df.groupby(["city", "district", "certificate"])
    .size()
    .reset_index(name="jumlah_rumah")
)

st.subheader("Tree Map Banyaknya Properti yang Dijual")
figTree = px.treemap(
    jumlahByKotaDist,
    path=["city", "district", "certificate"],
    values="jumlah_rumah",
    hover_data=["city", "district", "certificate", "jumlah_rumah"],
    color="certificate",
)
figTree.update_layout(width=800, height=1500)
st.plotly_chart(figTree, use_container_width=True)
# ------------------------


# Distribusi Properti Berdasarkan Koordinat Geografis
df_filtered["address_count"] = df_filtered.groupby(["lat", "long"])[
    "address"
].transform(
    "size"
)  # Hitung jumlah alamat untuk setiap baris
fig_scatter_mapbox = px.scatter_mapbox(
    df_filtered,
    lat="lat",
    lon="long",
    hover_name="address",
    color="city",
    size="address_count",  # Gunakan kolom 'address_count' sebagai ukuran
    mapbox_style="carto-positron",
    zoom=10,
    title="Peta Distribusi Geografis Properti Menurut Jumlah Rumah yang Dijual",
)
st.plotly_chart(fig_scatter_mapbox, use_container_width=True)

fig_scatter_mapbox = px.scatter_mapbox(
    df_filtered,
    lat="lat",
    lon="long",
    hover_name="address",
    color="city",
    size="price_in_rp",
    mapbox_style="carto-positron",
    zoom=10,
    title="Peta Distribusi Geografis Properti Berdasarkan Harga Porperti",
)

st.plotly_chart(fig_scatter_mapbox, use_container_width=True)

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Data Rumah yang Dijual"):
        jumlahByKotaDist = (
            df.groupby(["city", "district"]).size().reset_index(name="jumlah_rumah")
        )
        st.write(jumlahByKotaDist.style.background_gradient(cmap="Blues"))
        csv = jumlahByKotaDist.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Data",
            data=csv,
            file_name="Data Rumah.csv",
            mime="text/csv",
            help="Tekan untuk download data dalam bentuk CSV",
        )

with cl2:
    with st.expander("Data Harga"):
        city = df_filtered.groupby(by="city", as_index=False)["price_in_rp"].sum()
        st.write(city.style.background_gradient(cmap="Oranges"))
        csv = city.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Data",
            data=csv,
            file_name="Data Harga.csv",
            mime="text/csv",
            help="Tekan untuk download data dalam bentuk CSV",
        )

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="🏠 Jabodetabek House Price", layout="wide")
st.title("🏠 Jabodetabek House Price")
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
            lambda x: all(facility in x for facility in selected_facilities)
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

        building_age = st.multiselect(
            "🏗 Umur Bangunan (Tahun)", df_filtered["building_age"].dropna().unique()
        )
        if not building_age:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["building_age"].isin(building_age)]

        year_built = st.multiselect(
            "📆 Tahun Pembangunan", df_filtered["year_built"].dropna().unique()
        )
        if not year_built:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["year_built"].isin(year_built)]

        land_size = st.multiselect(
            "🪨 Luas Tanah (m²)", df_filtered["land_size_m2"].dropna().unique()
        )
        if not land_size:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[df_filtered["land_size_m2"].isin(land_size)]

        building_size = st.multiselect(
            "🧱 Luas Bangunan (m²)", df_filtered["building_size_m2"].dropna().unique()
        )
        if not building_size:
            df_filtered = df_filtered.copy()
        else:
            df_filtered = df_filtered[
                df_filtered["building_size_m2"].isin(building_size)
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
        st.info(":pencil: Jumlah Properti yang Dijual")
        st.metric(label="Count of Houses", value=f"{jumlah_rumah:.2f}")
    with total2:
        st.info(":pencil: Rata-Rata Harga Properti")
        st.metric(label="Average of Price", value=f"${avg_harga_miliar:.2f}B")
    with total3:
        st.info(":pencil: Harga Properti Tertinggi")
        st.metric(label="Max of Price", value=f"${max_harga_miliar}B")
    with total4:
        st.info(":pencil: Harga Properti Terdendah")
        st.metric(label="Min of Price", value=f"${min_harga_juta}M")


# Panggil method yang sudah dibuat dengan DataFrame yang sudah difilter
Home(df_filtered)


Top_5, persentase, bar_chart, korelasiDist, tren, mapping = st.tabs(
    ["Summary", "Persentase", "Bar Chart", "Korelasi & Distribusi", "Tren", "Mapping"]
)
with Top_5:
    col1, col2 = st.columns((2))
    # TOP CHART HARGA
    topChartHarga = df_filtered.groupby(by="district", as_index=False)[
        "price_in_rp"
    ].sum()
    topChartHarga = topChartHarga.sort_values(by="price_in_rp", ascending=True)
    topChartHarga = topChartHarga.tail(5)

    with col1:
        fig = px.bar(
            topChartHarga,
            x="price_in_rp",
            y="district",
            title="Top 5 Kecamatan dengan Total Harga Properti Tertinggi",
            template="seaborn",
            barmode="group",
            text="price_in_rp",
            labels={"price_in_rp": "", "district": ""},
        )
        fig.update_traces(texttemplate="%{text}", textposition="inside")
        st.plotly_chart(fig, use_container_width=True)

    # TopChartJumlah
    topChartJumlah = (
        df_filtered.groupby(["district"]).size().reset_index(name="jumlah_rumah")
    )
    topChartJumlah = topChartJumlah.sort_values(by="jumlah_rumah", ascending=True)
    topChartJumlah = topChartJumlah.tail(5)

    with col2:
        fig = px.bar(
            topChartJumlah,
            x="jumlah_rumah",
            y="district",
            title="Top 5 Kecamatan dengan Jumlah Properti yang Dijual Tertinggi",
            template="seaborn",
            barmode="group",
            text="jumlah_rumah",
            labels={"jumlah_rumah": "", "district": ""},
        )
        fig.update_traces(texttemplate="%{text}", textposition="inside")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Data Rumah Sesuai Filter"):
        st.write(df_filtered.style.background_gradient(cmap="Blues"))
        csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Data",
            data=csv,
            file_name="Data Full Data.csv",
            mime="text/csv",
            help="Tekan untuk download data dalam bentuk CSV",
        )
# PIECHART
# persentase Properti Berdasarkan kota
with persentase:
    col1, col2 = st.columns((2))
    with col1:
        fig_persentase_kota = px.pie(
            df_filtered["city"].value_counts(),
            values=df_filtered["city"].value_counts().values,
            names=df_filtered["city"].value_counts().index,
            title="Persentase Jumlah Properti Berdasarkan Kota",
        )
        fig_persentase_kota.update_traces(textinfo="percent", textposition="outside")
        st.plotly_chart(fig_persentase_kota, use_container_width=True)

    # persentase Properti Berdasarkan Tipe Sertifikat
    with col2:
        fig_persentase_sertifikat = px.pie(
            df_filtered["certificate"].value_counts(),
            hole=0.7,
            values=df_filtered["certificate"].value_counts().values,
            names=df_filtered["certificate"].value_counts().index,
            title="Persentase Jumlah Properti Berdasarkan Tipe Sertifikat",
        )
        fig_persentase_sertifikat.add_annotation(
            dict(
                x=0.5,
                y=0.5,
                align="center",
                xref="paper",
                yref="paper",
                showarrow=False,
                font_size=30,
                text="Certificate",
            )
        )
        st.plotly_chart(fig_persentase_sertifikat, use_container_width=True)

    # persentase Properti Berdasarkan Orientasi Bangunan
    with col1:
        fig_persentase_orientasi_bangunan = px.pie(
            df_filtered["building_orientation"].value_counts(),
            values=df_filtered["building_orientation"].value_counts().values,
            names=df_filtered["building_orientation"].value_counts().index,
            title="Persentase Jumlah Properti Berdasarkan Orientasi Bangunan",
        )
        fig_persentase_orientasi_bangunan.update_traces(
            textinfo="percent", textposition="outside"
        )
        st.plotly_chart(fig_persentase_orientasi_bangunan, use_container_width=True)

    # persentase Properti Berdasarkan Kondisi Bangunan
    with col2:
        fig_persentase_kondisi_bangunan = px.pie(
            df_filtered["property_condition"].value_counts(),
            values=df_filtered["property_condition"].value_counts().values,
            names=df_filtered["property_condition"].value_counts().index,
            title="Persentase Jumlah Properti Berdasarkan Kondisi Bangunan",
        )
        fig_persentase_kondisi_bangunan.update_traces(
            textinfo="label+percent", textposition="outside"
        )
        fig_persentase_kondisi_bangunan.update_layout(showlegend=False)
        st.plotly_chart(fig_persentase_kondisi_bangunan, use_container_width=True)

    # persentase Properti Berdasarkan Kondisi Perabotan
    with col1:
        fig = px.pie(
            df_filtered["furnishing"].value_counts(),
            values=df_filtered["furnishing"].value_counts().values,
            names=df_filtered["furnishing"].value_counts().index,
            title="Persentase Jumlah Properti Berdasarkan Kondisi Perabotan",
        )
        fig.update_traces(textinfo="label+percent", textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Sunburst Chart

    fig_sunburst = px.sunburst(
        df_filtered,
        width=1000,
        height=1000,
        path=["city", "district"],
        values="price_in_rp",
    )
    fig_sunburst.update_layout(title="Harga Properti Berdasarkan Kota dan Kecamatan")
    st.plotly_chart(fig_sunburst)

    # Sunburst Chart
    jumlahByKotaDist = (
        df_filtered.groupby(["city", "district"])
        .size()
        .reset_index(name="jumlah_rumah")
    )
    fig_sunburst = px.sunburst(
        jumlahByKotaDist,
        width=1000,
        height=1000,
        path=["city", "district"],
        values="jumlah_rumah",
    )
    fig_sunburst.update_layout(title="Jumlah Properti Berdasarkan Kota dan Kecamatan")
    st.plotly_chart(fig_sunburst)


with bar_chart:
    col1, col2 = st.columns((2))
    # BARRRRRRR
    # BARRRRRRR
    # BARRRRRRR
    # BARRRRRRR
    # BARRRRRRR

    # KOTAAAAAAA
    with col1:
        cityPrice = df_filtered.groupby(by="city", as_index=False)["price_in_rp"].mean()
        cityPrice = cityPrice.sort_values(by="price_in_rp", ascending=False)
        fig = px.bar(
            cityPrice,
            width=400,
            height=600,
            x="city",
            y="price_in_rp",
            text="price_in_rp",
            title="Harga Properti di Jabodetabek Berdasarkan Kota",
            labels={"city": "", "price_in_rp": ""},
        )
        fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df_filtered["city"].value_counts(),
            width=400,
            height=600,
            x=df_filtered["city"].value_counts().index,
            y=df_filtered["city"].value_counts().values,
            title="Banyaknya Properti yang Dijual Berdasarkan Kota",
            labels={"x": "", "y": ""},
        )
        fig.update_traces(
            text=df_filtered["city"].value_counts().values, textposition="outside"
        )
        st.plotly_chart(fig, use_container_width=True)

    # TIPE SERTIFIKAT
    with col1:
        certiPrice = df_filtered.groupby(by=["certificate", "city"], as_index=False)[
            "price_in_rp"
        ].sum()
        certiPrice = certiPrice.sort_values(by="price_in_rp", ascending=False)
        fig = px.bar(
            certiPrice,
            width=400,
            height=600,
            x="certificate",
            y="price_in_rp",
            color="city",
            text="price_in_rp",
            title="Harga Properti di Jabodetabek Berdasarkan Tipe Sertifikat",
            labels={"certificate": "", "price_in_rp": ""},
        )
        fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df_filtered["certificate"].value_counts(),
            width=400,
            height=600,
            x=df_filtered["certificate"].value_counts().index,
            y=df_filtered["certificate"].value_counts().values,
            title="Banyaknya Properti yang Dijual Berdasarkan Tipe Sertifikat",
            labels={"x": "", "y": ""},
        )
        fig.update_traces(
            text=df_filtered["certificate"].value_counts().values,
            textposition="outside",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Orientasi Bangunan
    with col1:
        OrientPrice = df_filtered.groupby(
            by=["building_orientation", "city"], as_index=False
        )["price_in_rp"].sum()
        OrientPrice = OrientPrice.sort_values(by="price_in_rp", ascending=False)
        fig = px.bar(
            OrientPrice,
            width=400,
            height=600,
            x="building_orientation",
            y="price_in_rp",
            color="city",
            text="price_in_rp",
            title="Harga Properti di Jabodetabek Berdasarkan Orientasi Properti",
            labels={"building_orientation": "", "price_in_rp": ""},
        )
        fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df_filtered["building_orientation"].value_counts(),
            width=400,
            height=600,
            x=df_filtered["building_orientation"].value_counts().index,
            y=df_filtered["building_orientation"].value_counts().values,
            title="Banyaknya Properti yang Dijual Berdasarkan Orientasi Properti",
            labels={"x": "", "y": ""},
        )
        fig.update_traces(
            text=df_filtered["building_orientation"].value_counts().values,
            textposition="outside",
        )
        st.plotly_chart(fig, use_container_width=True)

    # KONDISIIIIIIIII
    with col1:
        CondiPrice = df_filtered.groupby(
            by=["property_condition", "city"], as_index=False
        )["price_in_rp"].sum()
        CondiPrice = CondiPrice.sort_values(by="price_in_rp", ascending=False)
        fig = px.bar(
            CondiPrice,
            width=400,
            height=600,
            x="property_condition",
            y="price_in_rp",
            color="city",
            text="price_in_rp",
            title="Harga Properti di Jabodetabek Berdasarkan Kondisi Properti",
            labels={"property_condition": "", "price_in_rp": ""},
        )
        fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df_filtered["property_condition"].value_counts(),
            width=400,
            height=600,
            x=df_filtered["property_condition"].value_counts().index,
            y=df_filtered["property_condition"].value_counts().values,
            title="Banyaknya Properti yang Dijual Berdasarkan Kondisi Properti",
            labels={"x": "", "y": ""},
        )
        fig.update_traces(
            text=df_filtered["property_condition"].value_counts().values,
            textposition="outside",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col1:
        CondiPrice = df_filtered.groupby(by=["furnishing", "city"], as_index=False)[
            "price_in_rp"
        ].sum()
        CondiPrice = CondiPrice.sort_values(by="price_in_rp", ascending=False)
        fig = px.bar(
            CondiPrice,
            width=400,
            height=600,
            x="furnishing",
            y="price_in_rp",
            color="city",
            text="price_in_rp",
            title="Harga Properti di Jabodetabek Berdasarkan Kondisi Perabotan",
            labels={"furnishing": "", "price_in_rp": ""},
        )
        fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df_filtered["furnishing"].value_counts(),
            width=400,
            height=600,
            x=df_filtered["furnishing"].value_counts().index,
            y=df_filtered["furnishing"].value_counts().values,
            title="Banyaknya Properti yang Dijual Berdasarkan Kondisi Perabotan",
            labels={"x": "", "y": ""},
        )
        fig.update_traces(
            text=df_filtered["furnishing"].value_counts().values,
            textposition="outside",
        )
        st.plotly_chart(fig, use_container_width=True)


with korelasiDist:
    col1, col2 = st.columns((2))
    df_filtered["count_bedrooms"] = df_filtered.groupby("bedrooms")[
        "bedrooms"
    ].transform("count")

    # Korelasi Antara Harga Properti dan Luas Tanah
    with col1:
        fig_corr_harga_luas_tanah = px.scatter(
            df_filtered,
            x="land_size_m2",
            y="price_in_rp",
            color="city",
            title="Korelasi Antara Harga Properti dengan Luas Tanah",
            labels={"land_size_m2": "Luas Tanah", "price_in_rp": "Harga Properti"},
        )
        st.plotly_chart(fig_corr_harga_luas_tanah, use_container_width=True)

    # Korelasi Antara Harga Properti dan Luas Bangunan
    with col2:
        fig_corr_harga_luas_bangunan = px.scatter(
            df_filtered,
            x="building_size_m2",
            y="price_in_rp",
            color="city",
            title="Korelasi Antara Harga Properti dengan Luas Bangunan",
            labels={
                "building_size_m2": "Luas Bangunan",
                "price_in_rp": "Harga Properti",
            },
        )
        st.plotly_chart(fig_corr_harga_luas_bangunan, use_container_width=True)


    # DensityPLOT
    # DensityPLOT
    # DensityPLOT
    # DensityPLOT
    # DensityPLOT
    # DensityPLOT

    with col1:
        jumlahByKota = (
            df_filtered.groupby(["city"]).size().reset_index(name="Jumlah_Properti")
        )
        fig = px.density_contour(
            jumlahByKota,
            x="city",
            y="Jumlah_Properti",
            title="Korelasi Antara Jumlah Properti dengan Kota",
            labels={"city": "", "Jumlah_Properti": ""},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        jumlahByCertificate = (
            df_filtered.groupby(["certificate"])
            .size()
            .reset_index(name="Jumlah_Certificate")
        )
        fig = px.density_contour(
            jumlahByCertificate,
            x="certificate",
            y="Jumlah_Certificate",
            title="Korelasi Antara Jumlah Properti dengan Jenis Sertifikat",
            labels={"certificate": "", "Jumlah_Certificate": ""},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col1:
        jumlahByKondisi = (
            df_filtered.groupby(["property_condition"])
            .size()
            .reset_index(name="Jumlah_Kondisi")
        )
        fig = px.density_contour(
            jumlahByKondisi,
            x="property_condition",
            y="Jumlah_Kondisi",
            title="Korelasi Antara Jumlah Properti dengan Kondisi Properti",
            labels={"property_condition": "", "Jumlah_Kondisi": ""},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        jumlahByOrientasi = (
            df_filtered.groupby(["building_orientation"])
            .size()
            .reset_index(name="Jumlah_Orientasi")
        )
        fig = px.density_contour(
            jumlahByOrientasi,
            x="building_orientation",
            y="Jumlah_Orientasi",
            title="Korelasi Antara Jumlah Properti dengan Orientasi Bangunan",
            labels={"building_orientation": "", "Jumlah_Orientasi": ""},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col1:
        jumlahByFurnish = (
            df_filtered.groupby(["furnishing"])
            .size()
            .reset_index(name="Jumlah_Furnish")
        )
        fig = px.density_contour(
            jumlahByFurnish,
            x="furnishing",
            y="Jumlah_Furnish",
            title="Korelasi Antara Jumlah Properti dengan Kondisi Perabotan",
            labels={"furnishing": "", "Jumlah_Furnish": ""},
        )
        st.plotly_chart(fig, use_container_width=True)

    # Box Plot
    fig_box = px.box(
        df_filtered,
        x="city",
        y="price_in_rp",
        title="Box Plot Harga Properti Berdasarkan Kota",
        template="seaborn",
    )
    fig_box.update_layout(xaxis_title="", yaxis_title="")
    fig_box.update_xaxes(tickangle=45)
    st.plotly_chart(fig_box, use_container_width=True)

    # Violin Plot Harga Properti Berdasarkan Kota
    jumlahByKotaDist = (
        df_filtered.groupby(["city", "district", "certificate"])
        .size()
        .reset_index(name="jumlah_rumah")
    )

    fig_violin = px.violin(
        jumlahByKotaDist,
        x="city",
        y="jumlah_rumah",
        title="Violin Plot Harga Properti Berdasarkan Kota",
        template="seaborn",
    )
    fig_violin.update_layout(xaxis_title="", yaxis_title="")
    fig_violin.update_xaxes(tickangle=45)
    st.plotly_chart(fig_violin, use_container_width=True)

with tren:
    col1, col2 = st.columns((2))

    linechartHarga = df_filtered.groupby("year_built")["price_in_rp"].mean().reset_index()
    linechartHarga2 = df_filtered.groupby("year_built")["price_in_rp"].mean().reset_index()

    linechartHarga['year_built'] = linechartHarga['year_built'].astype(str).str[:4]
    linechartHarga['price_in_rp'] = (linechartHarga['price_in_rp'] / 1_000_000_000).map('{:.2f}'.format)
    
    linechartHarga2['year_built'] = linechartHarga2['year_built'].astype(str).str[:4]
    linechartHarga2['price_in_rp'] = (linechartHarga2['price_in_rp'] / 1_000_000_000).map('{:.2f}'.format) + ' Miliar'

    fig_tren_harga_waktu = px.area(
        linechartHarga,
        x="year_built",
        y="price_in_rp",
        title="Tren Rata-Rata Harga Properti berdasarkan Tahun Pembangunan",
        labels={"year_built": "Tahun Pembangunan", "price_in_rp": "Harga (dalam Miliar Rp)"}
    )

    st.plotly_chart(fig_tren_harga_waktu, use_container_width=True)

    with st.expander("TimeSerie Rata-Rata Harga Bangunan"):
        st.write(linechartHarga2.T.style.background_gradient(cmap="Blues"))
        csv = linechartHarga.to_csv(index=False).encode("UTF-8")
        st.download_button(
            "Download Data", data=csv, file_name="TimeSeriesHarga.csv", mime="text/csv"
        )

    properti_per_tahun = df_filtered["year_built"].value_counts().reset_index()
    properti_per_tahun.columns = ["year_built", "jumlah_properti"]

    # Tren Banyaknya Properti dijual dari Waktu ke Waktu
    fig = px.area(
        properti_per_tahun,
        x="year_built",
        y="jumlah_properti",
        title="Tren Banyaknya Properti Dijual berdasarkan Tahun Pembangunan",
        labels={"year_built": "", "jumlah_properti": ""},
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("TimeSeries Jumlah Properti"):
        st.write(properti_per_tahun.T.style.background_gradient(cmap="Blues"))
        csv = properti_per_tahun.to_csv(index=False).encode("UTF-8")
        st.download_button(
            "Download Data",
            data=csv,
            file_name="TimeSeriesJumlahProperti.csv",
            mime="text/csv",
        )

with mapping:
    col1, col2 = st.columns((2))
    # TREE MAP
    # TREE MAP
    jumlahByKotaDist = (
        df_filtered.groupby(["city", "district", "certificate"])
        .size()
        .reset_index(name="jumlah_rumah")
    )

    figTree = px.treemap(
        jumlahByKotaDist,
        path=["city", "district", "certificate"],
        values="jumlah_rumah",
        hover_data=["city", "district", "certificate", "jumlah_rumah"],
        color="certificate",
        color_discrete_sequence=[
            "#CDE8E5",
            "#EEF7FF",
            "#7AB2B2",
            "#4D869C",
        ],
        title="Tree Map Banyaknya Properti yang Dijual",
    )
    figTree.update_layout(width=800, height=1500)
    st.plotly_chart(figTree, use_container_width=True)

    #
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

    cl1, cl2 = st.columns(2)
    with cl1:
        with st.expander("Data Rumah yang Dijual"):
            jumlahByKotaDist = (
                df_filtered.groupby(["city", "district"])
                .size()
                .reset_index(name="jumlah_rumah")
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

    # Heatmap
    # serti

    fig_heatmap = px.density_heatmap(
        df_filtered,
        x="city",
        y="certificate",
        z="price_in_rp",
        title="Heatmap Harga Properti Antara Kota dan Jenis Sertifikat",
        marginal_x="rug",
        marginal_y="histogram",
        color_continuous_scale=["#006769", "#40A578", "#9DDE8B", "#E6FF94"],
    )
    fig_heatmap.update_xaxes(title=None, tickangle=45)
    fig_heatmap.update_yaxes(title=None)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    heatmap_data = (
        df_filtered.groupby(["city", "certificate"]).size().reset_index(name="count")
    )
    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="city",
        y="certificate",
        z="count",
        title="Heatmap Jumlah Properti Antara Kota dan Jenis Sertifikat",
        marginal_x="rug",
        marginal_y="histogram",
    )
    fig_heatmap.update_xaxes(title=None, tickangle=45)
    fig_heatmap.update_yaxes(title=None)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Kondisi
    fig_heatmap = px.density_heatmap(
        df_filtered,
        x="city",
        y="property_condition",
        z="price_in_rp",
        title="Heatmap Harga Properti Antara Kota dan Kondisi Bangunan",
        marginal_x="rug",
        marginal_y="histogram",
        color_continuous_scale=["#006769", "#40A578", "#9DDE8B", "#E6FF94"],
    )
    fig_heatmap.update_xaxes(title=None, tickangle=45)
    fig_heatmap.update_yaxes(title=None)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    heatmap_data = (
        df_filtered.groupby(["city", "property_condition"])
        .size()
        .reset_index(name="count")
    )
    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="city",
        y="property_condition",
        z="count",
        title="Heatmap Jumlah Properti Antara Kota dan Kondisi Bangunan",
        marginal_x="rug",
        marginal_y="histogram",
    )
    fig_heatmap.update_xaxes(title=None, tickangle=45)
    fig_heatmap.update_yaxes(title=None)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # orientasi
    fig_heatmap = px.density_heatmap(
        df_filtered,
        x="city",
        y="building_orientation",
        z="price_in_rp",
        title="Heatmap Harga Properti Antara Kota dan Orientasi Bangunan",
        marginal_x="rug",
        marginal_y="histogram",
        color_continuous_scale=["#006769", "#40A578", "#9DDE8B", "#E6FF94"],
    )
    fig_heatmap.update_xaxes(title=None, tickangle=45)
    fig_heatmap.update_yaxes(title=None)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    heatmap_data = (
        df_filtered.groupby(["city", "building_orientation"])
        .size()
        .reset_index(name="count")
    )
    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="city",
        y="building_orientation",
        z="count",
        title="Heatmap Jumlah Properti Antara Kota dan Orientasi Bangunan",
        marginal_x="rug",
        marginal_y="histogram",
    )
    fig_heatmap.update_xaxes(title=None, tickangle=45)
    fig_heatmap.update_yaxes(title=None)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # furnish

    fig_heatmap = px.density_heatmap(
        df_filtered,
        x="city",
        y="furnishing",
        z="price_in_rp",
        title="Heatmap Harga Properti Antara Kota dan Kondisi Perabotan",
        marginal_x="rug",
        marginal_y="histogram",
        color_continuous_scale=["#006769", "#40A578", "#9DDE8B", "#E6FF94"],
    )
    fig_heatmap.update_xaxes(title=None, tickangle=45)
    fig_heatmap.update_yaxes(title=None)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    heatmap_data = (
        df_filtered.groupby(["city", "furnishing"]).size().reset_index(name="count")
    )
    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="city",
        y="furnishing",
        z="count",
        title="Heatmap Jumlah Properti Antara Kota dan Kondisi Perabotan",
        marginal_x="rug",
        marginal_y="histogram",
    )
    fig_heatmap.update_xaxes(title=None, tickangle=45)
    fig_heatmap.update_yaxes(title=None)
    st.plotly_chart(fig_heatmap, use_container_width=True)

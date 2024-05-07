import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import plotly.express as px

# Load data
data_url = "https://github.com/pratama404/uasvisdat/raw/main/jabodetabek_house_price.csv"
df = pd.read_csv(data_url)

# Preprocessing
df["building_size_m2"] = pd.to_numeric(df["building_size_m2"], errors="coerce")
df["price_in_rp"] = pd.to_numeric(df["price_in_rp"], errors="coerce")
df = df.dropna(subset=["land_size_m2", "building_size_m2", "price_in_rp"])

# Drop non-numeric columns
df_numeric = df.select_dtypes(include=['float64', 'int64'])

# Impute missing values
imputer = SimpleImputer(strategy='mean')
df_filled = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_numeric.columns)

# Feature selection
X = df_filled[["land_size_m2", "building_size_m2", "bedrooms", "bathrooms", "floors", "building_age"]]
y = df_filled["price_in_rp"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = LinearRegression()
model.fit(X_train, y_train)

# Model evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Streamlit app
st.title("Sistem Rekomendasi Properti")
st.sidebar.header("Masukkan Data Properti yang Dicari")

bedrooms = st.sidebar.number_input("Jumlah Kamar Tidur", min_value=1, max_value=10, value=1)
bathrooms = st.sidebar.number_input("Jumlah Kamar Mandi", min_value=1, max_value=10, value=1)
land_size = st.sidebar.number_input("Ukuran Tanah (m2)", min_value=10, max_value=10000, value=100)
building_size = st.sidebar.number_input("Ukuran Bangunan (m2)", min_value=10, max_value=10000, value=100)
floors = st.sidebar.number_input("Jumlah Lantai", min_value=1, max_value=10, value=1)
building_age = st.sidebar.number_input("Umur Bangunan (Tahun)", min_value=1, max_value=100, value=1)

input_data = [[land_size, building_size, bedrooms, bathrooms, floors, building_age]]
predicted_price = model.predict(input_data)[0]

st.subheader("Hasil Prediksi Harga Properti")
st.write(f"Prediksi Harga Properti: Rp {predicted_price:,.0f}")

st.subheader("Performa Model")
st.write(f"Mean Squared Error: {mse:.2f}")
st.write(f"R-squared: {r2:.2f}")

# Visualisasi harga aktual vs prediksi
df_result = pd.DataFrame({"Actual Price": y_test, "Predicted Price": y_pred})
fig = px.scatter(df_result, x="Actual Price", y="Predicted Price", trendline="ols")
fig.update_layout(title="Actual Price vs Predicted Price", xaxis_title="Actual Price", yaxis_title="Predicted Price")
st.plotly_chart(fig)

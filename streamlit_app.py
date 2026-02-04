import streamlit as st
import requests

API_URL = "https://house-price-prediction-api-ky9x.onrender.com/predict"

st.set_page_config(page_title="House Price Prediction", layout="centered")

st.title("House Price Prediction")
st.write("Enter property details to estimate the house price.")

location = st.selectbox("Location", ["CityB", "CityC", "CityD"])
size = st.number_input("Size (sq ft)", min_value=100, max_value=10000, value=2000)
bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=2)
bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=1)
year_built = st.number_input("Year Built", min_value=1900, max_value=2025, value=2014)
condition = st.selectbox("Condition", ["Poor", "Fair", "Good", "Excellent"])
property_type = st.selectbox("Property Type", ["Single Family", "Townhouse", "Condominium"])
date_sold = st.date_input("Sale Date")

if st.button("Predict Price"):
    payload = {
        "location": location,
        "size": size,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "year_built": year_built,
        "condition": condition,
        "type": property_type,
        "date_sold": str(date_sold)
    }

    with st.spinner("Predicting..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        price = response.json()["predicted_price"]
        st.success(f"Estimated Price: ₹ {price:,.2f}")
    else:
        st.error("Failed to get prediction from API")

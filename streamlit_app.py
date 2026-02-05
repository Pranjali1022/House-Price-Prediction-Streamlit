import streamlit as st
import requests
from datetime import date

API_URL = "https://house-price-prediction-api-zj3e.onrender.com/predict"

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered"
)
st.markdown("""
    <h1 style='text-align:center; color:#2c3e50;'>🏠 House Price Prediction</h1>
    <h4 style='text-align:center; color:#34495e;'>
        ML-powered real estate valuation
    </h4>
    <br>
    """,
    unsafe_allow_html=True)

st.info("Enter property details below and click **Predict House Price** to get an estimated value.")
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        size = st.number_input("House Size (sq ft)", min_value=300, max_value=10000, step=50)
        bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, step=1)
        bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, step=1)
        year_built = st.number_input("Year Built", min_value=1900, max_value=date.today().year, step=1)
    with col2:
        location = st.selectbox("Location",["CityA", "CityB", "CityC", "CityD"])
        condition = st.selectbox("Condition", ["Poor", "Fair", "Good", "New"])
        property_type = st.selectbox("Property Type", ["Condominium", "Single Family", "Townhouse"])
        date_sold = st.date_input("Sale Date", value=date(2019, 1, 1))
    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("Predict House Price", use_container_width=True)
if submit_btn:
    payload = {
        "location": location,
        "size": size,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "year_built": year_built,
        "condition": condition,
        "type": property_type,
        "date_sold": date_sold.strftime("%Y-%m-%d")
    }
    with st.spinner("Waking up the server and predicting price..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=120)
            if response.status_code == 200:
                result = response.json()
                if "predicted_price" in result:
                    price = result["predicted_price"]
                    st.success("Prediction successful")
                    st.metric(label="Estimated House Price", value=f"₹ {price:,.2f}")
                elif "error" in result:
                    st.error("Prediction failed on server.")
                    st.write("Details:", result.get("details", "No details provided"))
                else:
                    st.error("Unexpected API response.")
                    st.write(result)
            else:
                st.error("Failed to get prediction from API.")
        except requests.exceptions.ReadTimeout:
            st.warning("The API is waking up (cold start). "
                "Please click **Predict** again in a few seconds.")
        except requests.exceptions.ConnectionError:
            st.error(
                "Unable to connect to the API. "
                "Please check the API status or try again later.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("About this project"):
    st.markdown(
        """
        **House Price Prediction App**
        - Built using **Machine Learning (XGBoost Regressor)**
        - Trained on **log-transformed house prices** for stable & positive predictions
        - Backend API built with **FastAPI**
        - Deployed on **Render**
        - Frontend developed using **Streamlit**

        This project demonstrates an **end-to-end ML workflow**:
        data preprocessing → model training → API deployment → UI integration.
        """
    )

st.markdown(
    """
    <hr>
    <p style="text-align:center; color:gray;">
        Built with love using Python, FastAPI, Streamlit & Machine Learning
    </p>
    """,
    unsafe_allow_html=True
)

import streamlit as st
import requests

st.title("Insurance Premium Prediction")
st.write("Enter your details")

age = st.number_input("Age", value=30)
weight = st.number_input("Weight (in kgs)", value=70.0)
height = st.number_input("Height (in cm)", value=170.0)
income = st.number_input("Income (in lakhs per annum)", value=5.0)
smoker = st.checkbox("Are you a smoker?")
city = st.text_input("City of residence", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    [
        "retired", "freelancer", "student",
        "government_job", "business_owner",
        "unemployed", "private_job"
    ]
)

if st.button("Predict Premium"):

    data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=data
        )

        result = response.json()

        st.success(
            f"Predicted Insurance Premium Category: {result['predicted_premium']}"
        )

    except Exception as e:
        st.error("Error in prediction. Please try again.")
        st.code(str(e))

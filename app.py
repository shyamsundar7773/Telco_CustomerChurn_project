import streamlit as st
import pickle
import pandas as pd

# 🔹 Load model and columns
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.title("Customer Churn Prediction")

# 🔹 Inputs
tenure = st.slider("Tenure", 1, 72)
monthly = st.number_input("Monthly Charges")

contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
dependents = st.selectbox("Dependents", ["No", "Yes"])

# 🔹 Create input structure
input_data = pd.DataFrame(columns=columns)
input_data.loc[0] = 0

# 🔹 Fill values
input_data["tenure"] = tenure
input_data["MonthlyCharges"] = monthly

if contract == "One year":
    input_data["Contract_One year"] = 1
elif contract == "Two year":
    input_data["Contract_Two year"] = 1

if dependents == "Yes":
    input_data["Dependents_Yes"] = 1

# 🔹 Prediction
if st.button("Predict"):
    prediction = model.predict(input_data)
    prob = model.predict_proba(input_data)

    st.write("### 🔍 Prediction Result")

    if prediction[0] == 1:
        st.error("Customer will churn")
    else:
        st.success("Customer will stay")

    # ✅ NEW: Probability
    st.write(f"Churn Probability: {prob[0][1]:.2f}")

    # ✅ NEW: Explanation
    st.write("### 💡 Insight")
    st.write(
        "Customers with lower tenure, higher monthly charges, "
        "and month-to-month contracts are more likely to churn."
    )
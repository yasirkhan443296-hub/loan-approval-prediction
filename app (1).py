
import streamlit as st
import pickle

st.title("Loan Approval Prediction")

try:
    model = pickle.load(open("model.pkl", "rb"))
    columns = pickle.load(open("columns.pkl", "rb"))

    st.success("Model Loaded Successfully")
    st.write("Number of features:", len(columns))
    st.write(columns)

 except Exception as e:
                       st.error(e)
                        


import streamlit as st
import pickle

st.title("Loan Approval Prediction")

with open('model(1).pkl', 'rb') as file:
    model = pickle.load(file)

    st.write("Model Loaded Successfully")
    

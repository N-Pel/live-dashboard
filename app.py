import streamlit as st
import pandas as pd

SHEET_ID = "1YZW1ENJdB1n910lvtCilbG776d0HrudGV163XZzsQqA"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/1YZW1ENJdB1n910lvtCilbG776d0HrudGV163XZzsQqA/edit?usp=sharing"

st.title("📊 Live Dashboard")

@st.cache_data(ttl=30)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

st.metric("Total Rows", len(df))

if "Revenue" in df.columns:
    st.metric("Total Revenue", df["Revenue"].sum())
    st.line_chart(df["Revenue"])

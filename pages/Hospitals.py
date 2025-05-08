import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Hospitals", layout="wide")

st.title("🏥 Hospitals Overview")

df = pd.read_csv("data.csv")

# Example: Number of patients by Hospital
hospital_chart = df.groupby("Hospital")["patient_id"].nunique().reset_index()
hospital_chart.columns = ["Hospital", "Patient Count"]

chart = alt.Chart(hospital_chart).mark_bar(size=15, color="#F58518").encode(
    x=alt.X("Hospital:N", title="Hospital"),
    y=alt.Y("Patient Count:Q", title="Patients"),
    tooltip=["Hospital:N", "Patient Count:Q"]
).properties(
    height=300,
    title="👥 Patients by Hospital"
).configure_view(
    stroke=None
).configure_axis(
    grid=False
)

st.altair_chart(chart, use_container_width=True)

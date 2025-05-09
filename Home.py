import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Patient Overview", layout="wide")

# Load and cache the dataset
@st.cache_data
def load_patient_data():
    return pd.read_csv("data.csv")

data = load_patient_data()

# Convert selected columns to numeric for analysis
numeric_columns = ["length_of_stay", "age", "lace_score", "cci_score"]
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")

# Dashboard Title
st.title("🧑‍⚕️ Patient Overview Dashboard")

# Summary Metrics
total_patients = data["patient_id"].nunique()
total_admissions = data["admission_id"].nunique()
average_los = data["length_of_stay"].mean()
average_age = data["age"].mean()
average_lace = data["lace_score"].mean()
average_cci = data["cci_score"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Patients", total_patients)
col2.metric("Total Admissions", total_admissions)
col3.metric("Avg. Length of Stay", f"{average_los:.2f} days")

col4, col5, col6 = st.columns(3)
col4.metric("Average Age", f"{average_age:.1f} years")
col5.metric("Average LACE Score", f"{average_lace:.2f}")
col6.metric("Average CCI Score", f"{average_cci:.2f}")

# Helper to create bar charts with optional binning
def create_bar_chart(column, label, use_bins=False, bins=None):
    if use_bins and bins:
        binned_data = data.copy()
        binned_data[column] = pd.cut(binned_data[column], bins=bins, right=False)
        binned_data[column] = binned_data[column].apply(lambda x: f"{int(x.left)}–{int(x.right - 1)}")
        chart_data = binned_data.groupby(column, observed=False)["patient_id"].nunique().reset_index()
    else:
        chart_data = data.groupby(column)["patient_id"].nunique().reset_index()

    chart_data.columns = [label, "Patient Count"]

    return alt.Chart(chart_data).mark_bar(size=15, color="#4C78A8").encode(
        x=alt.X(f"{label}:N", title=label, sort='-y', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("Patient Count:Q", title="Patients"),
        tooltip=[f"{label}:N", "Patient Count:Q"]
    ).properties(
        height=300,
        title=f"👥 Patients by {label}"
    ).configure_view(
        stroke=None
    ).configure_axis(
        grid=False,
        labelFontSize=12,
        titleFontSize=14,
        labelColor="#555",
        titleColor="#222"
    ).configure_title(
        fontSize=18,
        anchor='start',
        font='Helvetica',
        color='#333'
    )

# Pie chart for categorical data (used for gender)
def create_pie_chart(column, label):
    chart_data = data[column].value_counts().reset_index()
    chart_data.columns = [label, "Count"]

    return alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(f"{label}:N", legend=alt.Legend(title=label)),
        tooltip=[f"{label}:N", "Count:Q"]
    ).properties(
        width=350,
        height=350,
        title=f"🍰 Patients by {label}"
    ).configure_title(
        fontSize=18,
        anchor='middle',
        font='Helvetica',
        color='#333'
    )

# Bin definitions
age_bins = list(range(0, 101, 10))
los_bins = list(range(0, 51, 5))
cci_bins = list(range(0, 21, 2))
lace_bins = list(range(0, 21, 2))

# Generate visualizations
age_chart = create_bar_chart("age", "Age", use_bins=True, bins=age_bins)
gender_chart = create_pie_chart("gender", "Gender")
race_chart = create_bar_chart("race", "Race")
admission_type_chart = create_bar_chart("admission_type", "Admission Type")
admission_location_chart = create_bar_chart("admission_location", "Admission Location")
discharge_location_chart = create_bar_chart("discharge_location", "Discharge Location")
los_chart = create_bar_chart("length_of_stay", "Length of Stay", use_bins=True, bins=los_bins)
cci_chart = create_bar_chart("cci_score", "CCI Score", use_bins=True, bins=cci_bins)
lace_chart = create_bar_chart("lace_score", "LACE Score", use_bins=True, bins=lace_bins)
hospital_chart = create_bar_chart("Hospital", "Hospital")

# Layout the visual sections
st.markdown("### 🧬 Demographics")
col1, col2 = st.columns(2)
col1.altair_chart(age_chart, use_container_width=True)
col2.altair_chart(gender_chart, use_container_width=True)
st.altair_chart(race_chart, use_container_width=True)

st.markdown("### 🏥 Admissions and Locations")
col3, col4 = st.columns(2)
col3.altair_chart(admission_type_chart, use_container_width=True)
col4.altair_chart(admission_location_chart, use_container_width=True)
st.altair_chart(discharge_location_chart, use_container_width=True)

st.markdown("### 📈 Scores and Stay")
col5, col6 = st.columns(2)
col5.altair_chart(los_chart, use_container_width=True)
col6.altair_chart(cci_chart, use_container_width=True)
st.altair_chart(lace_chart, use_container_width=True)

st.altair_chart(hospital_chart, use_container_width=True)

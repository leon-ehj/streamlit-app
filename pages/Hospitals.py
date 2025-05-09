import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Hospital Overview", layout="wide")

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# Convert to numeric
df["length_of_stay"] = pd.to_numeric(df["length_of_stay"], errors="coerce")
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["lace_score"] = pd.to_numeric(df["lace_score"], errors="coerce")
df["cci_score"] = pd.to_numeric(df["cci_score"], errors="coerce")

# Dashboard title
st.title("🏥 Hospital Overview Dashboard")

# Dropdown to select hospital for metrics
hospital_list = df["Hospital"].dropna().unique()
selected_hospital = st.selectbox("🏥 Select a Hospital", sorted(hospital_list))

# Filter the data for the selected hospital (for metrics only)
df_hospital = df[df["Hospital"] == selected_hospital]

# Basic metrics for the selected hospital
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Patients", df_hospital["patient_id"].nunique())
with col2:
    st.metric("Total Admissions", df_hospital["admission_id"].nunique())
with col3:
    st.metric("Average Length of Stay", f"{df_hospital['length_of_stay'].mean():.2f} days")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("Average Age", f"{df_hospital['age'].mean():.1f} years")
with col5:
    st.metric("Average LACE Score", f"{df_hospital['lace_score'].mean():.2f}")
with col6:
    st.metric("Average CCI Score", f"{df_hospital['cci_score'].mean():.2f}")

# Function to create a bar chart
def create_bar_chart(group_column, title, bin=False, custom_bins=None, df_to_use=None):
    if bin and custom_bins:
        df_grouped = df_to_use.copy()  # Use provided dataframe (either selected or all hospitals)
        df_grouped[group_column] = pd.cut(df_grouped[group_column], bins=custom_bins, right=False)
        df_grouped[group_column] = df_grouped[group_column].apply(lambda x: f"{int(x.left)}–{int(x.right - 1)}")
        group_counts = df_grouped.groupby(group_column, observed=False)["patient_id"].nunique().reset_index()
    else:
        group_counts = df_to_use.groupby(group_column)["patient_id"].nunique().reset_index()

    group_counts.columns = [group_column, "Patient Count"]
    group_counts = group_counts[group_counts["Patient Count"] > 0]

    chart = alt.Chart(group_counts).mark_bar(size=15, color="#4C78A8").encode(
        x=alt.X(f"{group_column}:N", title=title, sort='-y', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("Patient Count:Q", title="Patients"),
        tooltip=[f"{group_column}:N", "Patient Count:Q"]
    ).properties(
        height=300,
        title=f"👥 Patients by {title}"
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

    return chart

# Define custom bins
age_bins = list(range(0, 101, 10))      # 0–9, 10–19, ..., 90–99
los_bins = list(range(0, 51, 5))        # 0–4, 5–9, ..., 45–49
cci_bins = list(range(0, 21, 2))        # 0–1, 2–3, ..., 18–19
lace_bins = list(range(0, 21, 2))       # 0–1, 2–3, ..., 18–19

# Create the charts using the selected hospital's data for all but the last chart
age_chart = create_bar_chart('age', 'Age', bin=True, custom_bins=age_bins, df_to_use=df_hospital)
gender_chart = create_bar_chart('gender', 'Gender', df_to_use=df_hospital)
race_chart = create_bar_chart('race', 'Race', df_to_use=df_hospital)
admission_type_chart = create_bar_chart('admission_type', 'Admission Type', df_to_use=df_hospital)
admission_location_chart = create_bar_chart('admission_location', 'Admission Location', df_to_use=df_hospital)
discharge_location_chart = create_bar_chart('discharge_location', 'Discharge Location', df_to_use=df_hospital)
length_of_stay_chart = create_bar_chart('length_of_stay', 'Length of Stay', bin=True, custom_bins=los_bins, df_to_use=df_hospital)
cci_score_chart = create_bar_chart('cci_score', 'CCI Score', bin=True, custom_bins=cci_bins, df_to_use=df_hospital)
lace_score_chart = create_bar_chart('lace_score', 'LACE Score', bin=True, custom_bins=lace_bins, df_to_use=df_hospital)

# Create the chart for all hospitals (final chart)
hospital_chart = create_bar_chart('Hospital', 'Hospital', df_to_use=df)

# Display charts in sections
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
col5.altair_chart(length_of_stay_chart, use_container_width=True)
col6.altair_chart(cci_score_chart, use_container_width=True)

st.altair_chart(lace_score_chart, use_container_width=True)

# Display the final chart showing data for all hospitals
st.markdown("### 🏥 Patients by Hospital")
st.altair_chart(hospital_chart, use_container_width=True)

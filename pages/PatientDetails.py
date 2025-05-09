import streamlit as st
import pandas as pd

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# Fetch query parameters
query_params = st.query_params
patient_id = query_params.get("patient_id", [None])[0]

# If no patient is selected, show a message and a back link
if patient_id is None:
    st.write("❗ No patient selected. Please go back and select a patient.")
    st.markdown("[Go back to the Patient Overview](./Patients.py)")
else:
    # Fetch the patient details for the selected patient_id
    patient_details = df[df["patient_id"] == int(patient_id)]

    if patient_details.empty:
        st.write("❗ Patient not found.")
    else:
        st.title(f"Patient Details - ID: {patient_id}")

        # Display patient details
        st.write("### Personal Information")
        st.write(f"**Age**: {patient_details['age'].values[0]}")
        st.write(f"**Gender**: {patient_details['gender'].values[0]}")
        st.write(f"**Race**: {patient_details['race'].values[0]}")

        st.write("### Health Scores")
        st.write(f"**LACE Score**: {patient_details['lace_score'].values[0]}")
        st.write(f"**CCI Score**: {patient_details['cci_score'].values[0]}")

        st.write("### Admission Details")
        st.write(f"**Admission Type**: {patient_details['admission_type'].values[0]}")
        st.write(f"**Admission Location**: {patient_details['admission_location'].values[0]}")
        st.write(f"**Discharge Location**: {patient_details['discharge_location'].values[0]}")

        # You can add more details as needed

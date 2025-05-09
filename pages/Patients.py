import streamlit as st
import pandas as pd

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# Convert necessary columns to numeric
df["length_of_stay"] = pd.to_numeric(df["length_of_stay"], errors="coerce")
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["lace_score"] = pd.to_numeric(df["lace_score"], errors="coerce")
df["cci_score"] = pd.to_numeric(df["cci_score"], errors="coerce")

# Dashboard title
st.title("🧑‍⚕️ Patients Overview")

# ---- Search and Filters Section ----
st.subheader("🔍 Search and Filters")

# Input field to search by patient ID
search_id = st.text_input("Search by Patient ID")

# ---- Apply Filters ----
filtered_df = df.copy()

# Filter by patient ID if a search term is provided
if search_id:
    filtered_df = filtered_df[filtered_df["patient_id"].astype(str).str.contains(search_id)]

# Display filtered patient data
if search_id:
    st.subheader("🔎 Filtered Patients")
    filtered_table = filtered_df[[
        "patient_id", "age", "gender", "length_of_stay",
        "diagnosis_description", "cci_score", "lace_score"
    ]].dropna()

    # Rename columns for better readability
    filtered_table.columns = [
        "Patient ID", "Age", "Gender", "Length of Stay",
        "Diagnosis", "CCI Score", "LACE Score"
    ]

    # Generate the table with clickable Patient IDs as markdown links
    for i, row in filtered_table.iterrows():
        patient_id = row["Patient ID"]
        patient_link = f"[{patient_id}](./PatientDetails.py?patient_id={patient_id})"
        filtered_table.at[i, "Patient ID"] = patient_link

    # Render the table row by row as markdown
    for _, row in filtered_table.iterrows():
        row_markdown = " | ".join([f"{col}: {row[col]}" for col in filtered_table.columns])
        st.markdown(row_markdown)

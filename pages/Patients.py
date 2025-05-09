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

# Calculate averages for filtering
avg_lace_score = df["lace_score"].mean()
avg_cci_score = df["cci_score"].mean()
avg_length_of_stay = df["length_of_stay"].mean()

# Filters for high scores
high_lace_filter = st.checkbox(f"Filter by High LACE Score (> {avg_lace_score:.2f})", value=True)
high_cci_filter = st.checkbox(f"Filter by High CCI Score (> {avg_cci_score:.2f})", value=True)
high_los_filter = st.checkbox(f"Filter by High Length of Stay (> {avg_length_of_stay:.2f} days)", value=True)

# Apply Filters
filtered_df = df.copy()

# Filter by patient ID if a search term is provided
if search_id:
    filtered_df = filtered_df[filtered_df["patient_id"].astype(str).str.contains(search_id)]

# Filter by high LACE score
if high_lace_filter:
    filtered_df = filtered_df[filtered_df["lace_score"] > avg_lace_score]

# Filter by high CCI score
if high_cci_filter:
    filtered_df = filtered_df[filtered_df["cci_score"] > avg_cci_score]

# Filter by high LOS
if high_los_filter:
    filtered_df = filtered_df[filtered_df["length_of_stay"] > avg_length_of_stay]

# Display filtered patient data
if not filtered_df.empty:
    st.subheader("🔎 Filtered Patients")
    
    # Select the relevant columns
    filtered_table = filtered_df[[
        "patient_id", "age", "gender", "length_of_stay",
        "diagnosis_description", "cci_score", "lace_score"
    ]].dropna()

    # Rename columns for better readability
    filtered_table.columns = [
        "Patient ID", "Age", "Gender", "Length of Stay",
        "Diagnosis", "CCI Score", "LACE Score"
    ]

    # Display the filtered table
    st.dataframe(filtered_table)  # This will display the table in the UI
    
else:
    st.write("No patients found with the selected filters.")

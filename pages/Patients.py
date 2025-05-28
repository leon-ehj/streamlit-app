import streamlit as st
import pandas as pd
import os

# Load and merge data from ETL output
def load_data():
    output_dir = "etl_output"
    
    dim_patient = pd.read_csv(os.path.join(output_dir, "dim_patient.csv"))
    dim_hospital = pd.read_csv(os.path.join(output_dir, "dim_hospital.csv"))
    dim_diagnosis = pd.read_csv(os.path.join(output_dir, "dim_diagnosis.csv"))
    fact_admissions = pd.read_csv(os.path.join(output_dir, "fact_admissions.csv"))
    
    df = fact_admissions.merge(dim_patient, on="patient_key", how="left") \
                        .merge(dim_hospital, on="hospital_key", how="left") \
                        .merge(dim_diagnosis, on="diagnosis_key", how="left")
    
    race_grouped = {
        'White': ['WHITE', 'WHITE - OTHER EUROPEAN', 'WHITE - RUSSIAN', 'WHITE - BRAZILIAN', 'WHITE - EASTERN EUROPEAN'],
        'Black': ['BLACK/AFRICAN AMERICAN', 'BLACK/CARIBBEAN ISLAND', 'BLACK/AFRICAN', 'BLACK/CAPE VERDEAN'],
        'Hispanic': ['HISPANIC/LATINO - PUERTO RICAN', 'HISPANIC/LATINO - HONDURAN', 'HISPANIC/LATINO - DOMINICAN', 'HISPANIC/LATINO - MEXICAN', 'HISPANIC/LATINO - SALVADORAN', 'HISPANIC/LATINO - GUATEMALAN', 'HISPANIC/LATINO - COLUMBIAN', 'HISPANIC/LATINO - CUBAN', 'HISPANIC/LATINO - CENTRAL AMERICAN', 'HISPANIC OR LATINO'],
        'Asian': ['ASIAN - SOUTH EAST ASIAN', 'ASIAN', 'ASIAN - CHINESE', 'ASIAN - KOREAN', 'ASIAN - ASIAN INDIAN'],
        'Other': ['OTHER', 'UNKNOWN', 'UNABLE TO OBTAIN', 'PATIENT DECLINED TO ANSWER', 'SOUTH AMERICAN', 'PORTUGUESE', 'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER', 'AMERICAN INDIAN/ALASKA NATIVE']
    }

    def group_races(race_value):
        for category, races in race_grouped.items():
            if race_value in races:
                return category
        return 'Other/Unknown'

    df['race_category'] = df['race'].apply(group_races)
    df['gender_label'] = df['gender'].map({'M': 'Male', 'F': 'Female'})
    
    return df

# Load merged data
df = load_data()

st.title("Patients Overview")
st.subheader("Search and Filters")

# input field to search by patient ID
search_id = st.text_input("Search by Patient ID")

# calculate averages and add filters for higher than average scores
avg_lace_score = df["lace_score"].mean()
avg_cci_score = df["cci_score"].mean()
avg_length_of_stay = df["length_of_stay"].mean()

high_lace_filter = st.checkbox(f"Filter by High LACE Score (> {avg_lace_score:.2f})", value=True)
high_cci_filter = st.checkbox(f"Filter by High CCI Score (> {avg_cci_score:.2f})", value=True)
high_los_filter = st.checkbox(f"Filter by High Length of Stay (> {avg_length_of_stay:.2f} days)", value=True)

filtered_df = df.copy()

# search for patient ID
if search_id:
    filtered_df = filtered_df[filtered_df["patient_id"].astype(str).str.contains(search_id)]

# high lace
if high_lace_filter:
    filtered_df = filtered_df[filtered_df["lace_score"] > avg_lace_score]

# high cci
if high_cci_filter:
    filtered_df = filtered_df[filtered_df["cci_score"] > avg_cci_score]

# high los
if high_los_filter:
    filtered_df = filtered_df[filtered_df["length_of_stay"] > avg_length_of_stay]

# filter
if not filtered_df.empty:
    st.subheader("Filtered Patients")
    
    filtered_table = filtered_df[[
        "patient_id", "age", "gender", "length_of_stay",
        "diagnosis_description", "cci_score", "lace_score"
    ]].dropna()

    # rename columns for visual clarity
    filtered_table.columns = [
        "Patient ID", "Age", "Gender", "Length of Stay",
        "Diagnosis", "CCI Score", "LACE Score"
    ]

    # show filtered table
    st.dataframe(filtered_table) 
    
    # searched patient id doesnt exist
else:
    st.write("No patients found with the selected filters.")

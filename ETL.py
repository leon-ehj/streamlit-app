import pandas as pd
import os

output_dir = "etl_output"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv("data.csv")

dim_patient = df[['patient_id', 'gender', 'age', 'race']].drop_duplicates().reset_index(drop=True)
dim_patient['patient_key'] = dim_patient.index + 1 

dim_hospital = df[['Hospital']].drop_duplicates().reset_index(drop=True)
dim_hospital['hospital_key'] = dim_hospital.index + 1

dim_diagnosis = df[['icd_code', 'icd_version', 'diagnosis_description']].drop_duplicates().reset_index(drop=True)
dim_diagnosis['diagnosis_key'] = dim_diagnosis.index + 1

fact_admissions = df.merge(dim_patient, on=['patient_id', 'gender', 'age', 'race'], how='left')

fact_admissions = fact_admissions.merge(dim_hospital, on='Hospital', how='left')

fact_admissions = fact_admissions.merge(dim_diagnosis, on=['icd_code', 'icd_version', 'diagnosis_description'], how='left')

fact_admissions = fact_admissions[[
    'admission_id', 'patient_key', 'hospital_key', 'diagnosis_key',
    'admission_type', 'admission_location', 'discharge_location',
    'admittime', 'dischtime', 'length_of_stay',
    'cci_score', 'ed_visit_count',
    'lace_l_score', 'lace_a_score', 'lace_e_score', 'lace_score'
]]

dim_patient.to_csv(os.path.join(output_dir, "dim_patient.csv"), index=False)
dim_hospital.to_csv(os.path.join(output_dir, "dim_hospital.csv"), index=False)
dim_diagnosis.to_csv(os.path.join(output_dir, "dim_diagnosis.csv"), index=False)
fact_admissions.to_csv(os.path.join(output_dir, "fact_admissions.csv"), index=False)

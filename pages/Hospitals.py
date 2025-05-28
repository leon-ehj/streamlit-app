import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Patient Dashboard", layout="wide")

def load_data():
    import pandas as pd
    import os

    output_dir = "etl_output"  # folder where your ETL CSVs are saved

    # Load dimension tables
    dim_patient = pd.read_csv(os.path.join(output_dir, "dim_patient.csv"))
    dim_hospital = pd.read_csv(os.path.join(output_dir, "dim_hospital.csv"))
    dim_diagnosis = pd.read_csv(os.path.join(output_dir, "dim_diagnosis.csv"))

    # Load fact table
    fact_admissions = pd.read_csv(os.path.join(output_dir, "fact_admissions.csv"))

    # Merge dimensions to fact table to reconstruct original columns needed for dashboard
    df = fact_admissions.merge(dim_patient, on="patient_key", how="left") \
                        .merge(dim_hospital, on="hospital_key", how="left") \
                        .merge(dim_diagnosis, on="diagnosis_key", how="left")

    # Add race_category and gender_label as before
    race_grouped = {
        'White': [
            'WHITE', 
            'WHITE - OTHER EUROPEAN', 
            'WHITE - RUSSIAN', 
            'WHITE - BRAZILIAN', 
            'WHITE - EASTERN EUROPEAN'
        ],
        'Black': [
            'BLACK/AFRICAN AMERICAN', 
            'BLACK/CARIBBEAN ISLAND', 
            'BLACK/AFRICAN', 
            'BLACK/CAPE VERDEAN'
        ],
        'Hispanic': [
            'HISPANIC/LATINO - PUERTO RICAN', 
            'HISPANIC/LATINO - HONDURAN', 
            'HISPANIC/LATINO - DOMINICAN', 
            'HISPANIC/LATINO - MEXICAN', 
            'HISPANIC/LATINO - SALVADORAN', 
            'HISPANIC/LATINO - GUATEMALAN', 
            'HISPANIC/LATINO - COLUMBIAN', 
            'HISPANIC/LATINO - CUBAN', 
            'HISPANIC/LATINO - CENTRAL AMERICAN', 
            'HISPANIC OR LATINO'
        ],
        'Asian': [
            'ASIAN - SOUTH EAST ASIAN', 
            'ASIAN', 
            'ASIAN - CHINESE', 
            'ASIAN - KOREAN', 
            'ASIAN - ASIAN INDIAN'
        ],
        'Other': [
            'OTHER', 
            'UNKNOWN', 
            'UNABLE TO OBTAIN', 
            'PATIENT DECLINED TO ANSWER', 
            'SOUTH AMERICAN', 
            'PORTUGUESE',
            'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER',
            'AMERICAN INDIAN/ALASKA NATIVE'
        ]
    }

    def group_races(race_value):
        for category, races in race_grouped.items():
            if race_value in races:
                return category
        return 'Other/Unknown'

    df['race_category'] = df['race'].apply(group_races)
    df['gender_label'] = df['gender'].map({'M': 'Male', 'F': 'Female'})

    return df

df_all = load_data()

hospital_list = df_all["Hospital"].dropna().unique()
selected_hospital = st.selectbox("Select a Hospital", sorted(hospital_list))
df = df_all[df_all["Hospital"] == selected_hospital]

df = df.dropna(subset=['length_of_stay', 'age', 'lace_score', 'cci_score'])

race_grouped = {
    'White': [
        'WHITE', 
        'WHITE - OTHER EUROPEAN', 
        'WHITE - RUSSIAN', 
        'WHITE - BRAZILIAN', 
        'WHITE - EASTERN EUROPEAN'
    ],
    'Black': [
        'BLACK/AFRICAN AMERICAN', 
        'BLACK/CARIBBEAN ISLAND', 
        'BLACK/AFRICAN', 
        'BLACK/CAPE VERDEAN'
    ],
    'Hispanic': [
        'HISPANIC/LATINO - PUERTO RICAN', 
        'HISPANIC/LATINO - HONDURAN', 
        'HISPANIC/LATINO - DOMINICAN', 
        'HISPANIC/LATINO - MEXICAN', 
        'HISPANIC/LATINO - SALVADORAN', 
        'HISPANIC/LATINO - GUATEMALAN', 
        'HISPANIC/LATINO - COLUMBIAN', 
        'HISPANIC/LATINO - CUBAN', 
        'HISPANIC/LATINO - CENTRAL AMERICAN', 
        'HISPANIC OR LATINO'
    ],
    'Asian': [
        'ASIAN - SOUTH EAST ASIAN', 
        'ASIAN', 
        'ASIAN - CHINESE', 
        'ASIAN - KOREAN', 
        'ASIAN - ASIAN INDIAN'
    ],
    'Other': [
        'OTHER', 
        'UNKNOWN', 
        'UNABLE TO OBTAIN', 
        'PATIENT DECLINED TO ANSWER', 
        'SOUTH AMERICAN', 
        'PORTUGUESE',
        'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER',
        'AMERICAN INDIAN/ALASKA NATIVE'
    ]
}

def group_races(race_value):
    for category, races in race_grouped.items():
        if race_value in races:
            return category
    return 'Other/Unknown'
df['race_category'] = df['race'].apply(group_races)

def create_bar(group_column, title, bar_size=20, data=None):
    if data is None:
        data = df
    group_counts = df.groupby(group_column)["patient_id"].nunique().reset_index()
    group_counts.columns = [group_column, "Patient Count"]
    group_counts = group_counts.sort_values(by=group_column, ascending=True)

    chart = alt.Chart(group_counts).mark_bar(size=bar_size, color="#56B4E9").encode(
        x=alt.X(f"{group_column}:N", title=title, sort='ascending', axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Patient Count:Q", title="Patients"),
        tooltip=[f"{group_column}:N", "Patient Count:Q"]
    ).properties(
        height=425,
        width=350,
        title=f"Patients by {title}"
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

df['gender_label'] = df['gender'].map({'M': 'Male', 'F': 'Female'})

def gender_pie(df, title):
    gender_counts = df['gender_label'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    chart = alt.Chart(gender_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(
            'Gender:N',
            scale=alt.Scale(domain=['Male', 'Female'], range=['#0000FF', '#FFC0CB']),
            legend=alt.Legend(title=title, titleFontSize=20, labelFontSize=18)
        ),
        tooltip=['Gender:N', 'Count:Q']
    ).properties(title=f"Patients by {title}").configure_title(
        fontSize=18,
        anchor='middle',
        font='Helvetica',
        color='#333'
    )
    return chart

def create_pie(group_column, title):
    group_counts = df[group_column].value_counts().reset_index()
    group_counts.columns = [group_column, "Count"]

    chart = alt.Chart(group_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(
        f"{group_column}:N",
        legend=alt.Legend(title=title, titleFontSize=20, labelFontSize=18)
    ),
        tooltip=[f"{group_column}:N", "Count:Q"]).properties(title=f"Patients by {title}").configure_title(
        fontSize=18,
        anchor='middle',
        font='Helvetica',
        color='#333'
    )
    return chart

def bar_hospitals(column_name, title):
    counts = df_all[column_name].value_counts().reset_index()
    counts.columns = [column_name, "Count"]

    chart = alt.Chart(counts).mark_bar(size=20, color="#56B4E9").encode(
        x=alt.X("Count:Q", title="Patients"),
        y=alt.Y(f"{column_name}:N", sort='-x', title=title),
        tooltip=[f"{column_name}:N", "Count:Q"]
    ).properties(
        width=500,
        height=400,
        title=f"Patients by {title}"
    ).configure_axis(
        labelLimit=200
    )
    return chart

# checking if df_all displayed hospitals correctly 
# st.write(df_all["Hospital"].value_counts())


age_histogram = alt.Chart(df).mark_bar(color="#56B4E9").encode(
    alt.X("age:Q", bin=alt.Bin(maxbins=20), title="Age"),
    alt.Y("count():Q", title="Number of Patients"),
    tooltip=["age:Q", "count():Q"]
).properties(
    height=400,
    width=400,
    title="Age Distribution of Patients"
).configure_view(
    stroke=None
).configure_axis(
    grid=False,
    labelFontSize=16,
    titleFontSize=18,
    labelColor="#555",
    titleColor="#222"
).configure_title(
    fontSize=20,
    anchor='start',
    font='Helvetica',
    color='#333'
)

# title
st.title("Patient Overview Dashboard")
# metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Patients", df["patient_id"].nunique())
with col2:
    st.metric("Total Admissions", df["admission_id"].nunique())
with col3:
    st.metric("Average Length of Stay", f"{df['length_of_stay'].mean():.2f} days")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("Average Age", f"{df['age'].mean():.1f} years")
with col5:
    st.metric("Average LACE Score", f"{df['lace_score'].mean():.2f}")
with col6:
    st.metric("Average CCI Score", f"{df['cci_score'].mean():.2f}")

# creating charts
gender_chart = gender_pie(df, 'Gender')

race_pie_chart = create_pie('race_category', 'Race')

admission_type_chart = create_bar('admission_type', 'Admission Type', bar_size=30)

admission_location_chart = create_bar('admission_location', 'Admission Location', bar_size=25)

discharge_location_chart = create_bar('discharge_location', 'Discharge Location')

length_of_stay_chart = create_bar('length_of_stay', 'Length of Stay', bar_size=10)

cci_score_chart = create_bar('cci_score', 'CCI Score', bar_size=48)

lace_score_chart = create_bar('lace_score', 'LACE Score', bar_size=35)

hospital_chart = bar_hospitals('Hospital', 'Hospital')

# flip axes, allow for longer labels so they dont get cut off, sort by x to show distribution better
admission_type_chart = admission_type_chart.encode(
    x=alt.X("Patient Count:Q", title="Patients"),
    y=alt.Y('admission_type:N', title='Admission Type',sort='-x',axis=alt.Axis(labelLimit=200)))
admission_location_chart = admission_location_chart.encode(
    x=alt.X("Patient Count:Q", title="Patients"),
    y=alt.Y('admission_location:N', title='Admission Location',sort='-x',axis=alt.Axis(labelLimit=200)))
discharge_location_chart = discharge_location_chart.encode(
    x=alt.X("Patient Count:Q", title="Patients"),
    y=alt.Y('discharge_location:N', title='Discharge Location',sort='-x',axis=alt.Axis(labelLimit=200)))

# separate columns

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Admissions and Locations")
    st.altair_chart(admission_type_chart, use_container_width=True)
    st.altair_chart(admission_location_chart, use_container_width=True)
    st.altair_chart(discharge_location_chart, use_container_width=True)
    st.altair_chart(hospital_chart, use_container_width=True)

with col2:
    st.markdown("### Demographics")
    st.altair_chart(age_histogram, use_container_width=True)
    st.altair_chart(gender_chart, use_container_width=True)
    st.altair_chart(race_pie_chart, use_container_width=True)

    st.markdown("### Additional Details")
    st.altair_chart(length_of_stay_chart, use_container_width=True)
    st.altair_chart(cci_score_chart, use_container_width=True)
    st.altair_chart(lace_score_chart, use_container_width=True)

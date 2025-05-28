import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Patient Dashboard", layout="wide")

<<<<<<< HEAD
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
    
    # Now df contains columns from all dims and fact; rename 'Hospital' for consistency
    df.rename(columns={"Hospital": "Hospital"}, inplace=True)
    
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

df = load_data()

# bar chart
def create_bar(group_column, title, bar_size=20):
    group_counts = df.groupby(group_column)["patient_id"].nunique().reset_index()
    group_counts.columns = [group_column, "Patient Count"]
    group_counts = group_counts.sort_values(by=group_column, ascending=True)
    
    chart = alt.Chart(group_counts).mark_bar(size=bar_size, color="#56B4E9").encode(
        x=alt.X(f"{group_column}:N", title=title, sort='ascending', axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Patient Count:Q", title="Patients"),
        tooltip=[f"{group_column}:N", "Patient Count:Q"]
    ).properties(
        height=425,
        width=400,
        title=f"Patients by {title}"
    ).configure_view(
        stroke=None
    ).configure_axis(
        grid=False,
        labelFontSize=11,
        titleFontSize=14,
        labelColor="#555",
        titleColor="#222"
    ).configure_title(
        fontSize=20,
        anchor='start',
        font='Helvetica',
        color='#333'
    )
    return chart

# pie chart for race
def race_pie(group_column, title):
    group_counts = df[group_column].value_counts().reset_index()
    group_counts.columns = [group_column, "Count"]

    chart = alt.Chart(group_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(
        f"{group_column}:N",
        legend=alt.Legend(title=title, titleFontSize=20, labelFontSize=18)
    ),
        tooltip=[f"{group_column}:N", "Count:Q"]
    ).properties(title=f"Patients by {title}").configure_title(
        fontSize=18,
        anchor='middle',
        font='Helvetica',
    )
    return chart

# pie chart for genders (male blue and female pink), mapped M to male and F to female for visual clarity on chart

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
    ).properties(
        width=350,
        height=350,
        title=f"Patients by {title}"
    ).configure_title(
        fontSize=18,
        anchor='middle',
        font='Helvetica',
        color='#333'
    )
    return chart

# histogram for age (bar chart looked bad)
age_histogram = alt.Chart(df).mark_bar(color="#56B4E9").encode(
    alt.X("age:Q", bin=alt.Bin(maxbins=20), title="Age"),
    alt.Y("count():Q", title="Number of Patients"),
    tooltip=["age:Q", "count():Q"]
).properties(
    height=400,
    width=350,
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
    fontSize=18,
    anchor='start',
    font='Helvetica',
    color='#333'
)

# title
st.title("Patient Overview Dashboard")

# metrics
=======
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
st.title("🏥 Patient Overview Dashboard")

# basic metrics
>>>>>>> 88ddf07edf562a45d4aa0016551a44b907822a0d
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

<<<<<<< HEAD
# creating charts 
gender_chart = gender_pie(df, 'Gender')

race_pie_chart = race_pie('race_category', 'Race')

admission_type_chart = create_bar('admission_type', 'Admission Type', bar_size=30)

admission_location_chart = create_bar('admission_location', 'Admission Location', bar_size=25)

discharge_location_chart = create_bar('discharge_location', 'Discharge Location')

length_of_stay_chart = create_bar('length_of_stay', 'Length of Stay', bar_size=7)

cci_score_chart = create_bar('cci_score', 'CCI Score', bar_size=40)

lace_score_chart = create_bar('lace_score', 'LACE Score', bar_size=30)

hospital_chart = create_bar('Hospital', 'Hospital', bar_size=25)

# flip axes, allow for longer labels so they dont get cut off, sort by x to show distribution better
admission_type_chart = admission_type_chart.encode(
    x=alt.X("Patient Count:Q", title="Patients"),
    y=alt.Y('admission_type:N', title='Admission Type',sort='-x',axis=alt.Axis(labelLimit=200))
)

admission_location_chart = admission_location_chart.encode(
    x=alt.X("Patient Count:Q", title="Patients"),
    y=alt.Y('admission_location:N', title='Admission Location',sort='-x',axis=alt.Axis(labelLimit=200))
)

discharge_location_chart = discharge_location_chart.encode(
    x=alt.X("Patient Count:Q", title="Patients"),
    y=alt.Y('discharge_location:N', title='Discharge Location',sort='-x',axis=alt.Axis(labelLimit=200))
)

hospital_chart = hospital_chart.encode(
    x=alt.X("Patient Count:Q", title="Patients"),
    y=alt.Y('Hospital:N', title='Hospital',sort='-x',axis=alt.Axis(labelLimit=200))
)

# format columns (idk how to make it look good, the odd number of charts underneath each header is awkward)

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
=======
# Function to create a bar chart for grouping by different columns
def create_bar_chart(group_column, title):
    group_counts = df.groupby(group_column)["patient_id"].nunique().reset_index()
    group_counts.columns = [group_column, "Patient Count"]
    
    # Filter out groups with zero patients (optional)
    group_counts = group_counts[group_counts["Patient Count"] > 0]
    
    # Bar chart
    chart = alt.Chart(group_counts).mark_bar(size=15, color="#4C78A8").encode(
        x=alt.X(f"{group_column}:N", title=title),
        y=alt.Y("Patient Count:Q", title="Patients"),
        tooltip=[f"{group_column}:N", "Patient Count:Q"]
    ).properties(
        height=300,
        title=f"👥 Patients by {title}"
    ).configure_view(
        stroke=None
    ).configure_axis(
        grid=False
    )
    
    return chart

# Create the charts for each category
age_chart = create_bar_chart('age', 'Age')
gender_chart = create_bar_chart('gender', 'Gender')
race_chart = create_bar_chart('race', 'Race')
admission_type_chart = create_bar_chart('admission_type', 'Admission Type')
admission_location_chart = create_bar_chart('admission_location', 'Admission Location')
discharge_location_chart = create_bar_chart('discharge_location', 'Discharge Location')
length_of_stay_chart = create_bar_chart('length_of_stay', 'Length of Stay')
cci_score_chart = create_bar_chart('cci_score', 'CCI Score')
lace_score_chart = create_bar_chart('lace_score', 'LACE Score')
hospital_chart = create_bar_chart('Hospital', 'Hospital')

# Display the charts using Streamlit
st.altair_chart(age_chart, use_container_width=True)
st.altair_chart(gender_chart, use_container_width=True)
st.altair_chart(race_chart, use_container_width=True)
st.altair_chart(admission_type_chart, use_container_width=True)
st.altair_chart(admission_location_chart, use_container_width=True)
st.altair_chart(discharge_location_chart, use_container_width=True)
st.altair_chart(length_of_stay_chart, use_container_width=True)
st.altair_chart(cci_score_chart, use_container_width=True)
st.altair_chart(lace_score_chart, use_container_width=True)
st.altair_chart(hospital_chart, use_container_width=True)
>>>>>>> 88ddf07edf562a45d4aa0016551a44b907822a0d

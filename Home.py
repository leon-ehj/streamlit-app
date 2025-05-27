import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Patient Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

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
    'Hispanic/Latino': [
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

def create_bar(group_column, title, bar_size=20):
    group_counts = df.groupby(group_column)["patient_id"].nunique().reset_index()
    group_counts.columns = [group_column, "Patient Count"]
    group_counts = group_counts.sort_values(by=group_column, ascending=True)
    
    chart = alt.Chart(group_counts).mark_bar(size=bar_size, color="#4C78A8").encode(
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

def create_pie(group_column, title):
    group_counts = df[group_column].value_counts().reset_index()
    group_counts.columns = [group_column, "Count"]

    chart = alt.Chart(group_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(
        f"{group_column}:N",
        legend=alt.Legend(title=title)
    ),
        tooltip=[f"{group_column}:N", "Count:Q"]
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

age_histogram = alt.Chart(df).mark_bar(color="#4C78A8").encode(
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
gender_chart = create_pie('gender', 'Gender')
race_pie_chart = create_pie('race_category', 'Race')
admission_type_chart = create_bar('admission_type', 'Admission Type', bar_size=30)
admission_location_chart = create_bar('admission_location', 'Admission Location', bar_size=25)
discharge_location_chart = create_bar('discharge_location', 'Discharge Location')
length_of_stay_chart = create_bar('length_of_stay', 'Length of Stay', bar_size=7)
cci_score_chart = create_bar('cci_score', 'CCI Score', bar_size=35)
lace_score_chart = create_bar('lace_score', 'LACE Score', bar_size=30)
hospital_chart = create_bar('Hospital', 'Hospital', bar_size=25)

# flip axes
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

    st.markdown("### Additional Metrics")
    st.altair_chart(length_of_stay_chart, use_container_width=True)
    st.altair_chart(cci_score_chart, use_container_width=True)
    st.altair_chart(lace_score_chart, use_container_width=True)

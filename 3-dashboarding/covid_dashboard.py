import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np



### CONFIG
st.set_page_config(
    page_title="Covid dashboard",
    page_icon="😷",
    layout="wide"
  )

### TITLE AND TEXT
st.title("Covid dashboard")
st.markdown("Voici quelques données concernant les cas de COVID et les décès apparentés à ce virus dans le monde.")

### LOAD AND CACHE DATA
DATA_URL = ('https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv')

@st.cache_data # this lets the 
def load_data():
    data = pd.read_csv(DATA_URL)
    data['date'] = pd.to_datetime(data['dateRep'], dayfirst=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


st.markdown("World evolution covid cases")

data_global=data.iloc[:,[4,11]].groupby('date')['cases'].sum().reset_index(drop=False)
fig = px.histogram(data_global, x="date", y="cases")
fig.update_layout(bargap=0.2)
st.plotly_chart(fig, use_container_width=True)


#### CREATE TWO COLUMNS
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Average covid cases**")

    with st.form("average_covid_cases_per_country"):
        country = st.selectbox("Select a country", data["countriesAndTerritories"].sort_values().unique())
        start_period = st.date_input("Select a start date you want to see your metric")
        end_period = st.date_input("Select an end date you want to see your metric")
        submit = st.form_submit_button("submit")

        if submit:
            avg_period_country_cases = data[(data["countriesAndTerritories"]==country)]
            start_period, end_period = pd.to_datetime(start_period), pd.to_datetime(end_period)
            mask = (avg_period_country_cases["date"] > start_period) & (avg_period_country_cases["date"] < end_period)
            avg_period_country_cases_mask = avg_period_country_cases[mask]
            moyenne = avg_period_country_cases_mask['cases'].mean()
            st.metric(f"Average covid cases during selected period for {country} ", np.round(moyenne, 2))
    
            fig = px.histogram(avg_period_country_cases_mask, x="date", y="cases")
            fig.update_layout(bargap=0.2)
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            avg_period_country_cases = data[(data["countriesAndTerritories"]=='France')]
            start_period, end_period = pd.to_datetime('2020-11-01'), pd.to_datetime('2020-12-31')
            mask = (avg_period_country_cases["date"] > start_period) & (avg_period_country_cases["date"] < end_period)
            avg_period_country_cases_mask = avg_period_country_cases[mask]
            moyenne = avg_period_country_cases_mask['cases'].mean()
            st.metric(f"Average covid cases during selected period for France ", np.round(moyenne, 2))
    
            fig = px.histogram(avg_period_country_cases_mask, x="date", y="cases")
            fig.update_layout(bargap=0.2)
            st.plotly_chart(fig, use_container_width=True)


with col2:
    st.markdown("**Average covid deaths**")

    with st.form("average_covid_deaths_per_country"):
        country = st.selectbox("Select a country", data["countriesAndTerritories"].sort_values().unique())
        start_period = st.date_input("Select a start date you want to see your metric")
        end_period = st.date_input("Select an end date you want to see your metric")
        submit = st.form_submit_button("submit")

        if submit:
            avg_period_country_deaths = data[(data["countriesAndTerritories"]==country)]
            start_period, end_period = pd.to_datetime(start_period), pd.to_datetime(end_period)
            mask = (avg_period_country_deaths["date"] > start_period) & (avg_period_country_deaths["date"] < end_period)
            avg_period_country_deaths_mask = avg_period_country_deaths[mask]
            moyenne = avg_period_country_deaths_mask['deaths'].mean()
            st.metric(f"Average covid deaths during selected period for {country} ", np.round(moyenne, 2))
    
            fig = px.histogram(avg_period_country_deaths_mask, x="date", y="deaths")
            fig.update_layout(bargap=0.2)
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            avg_period_country_deaths = data[(data["countriesAndTerritories"]=='France')]
            start_period, end_period = pd.to_datetime('2020-11-01'), pd.to_datetime('2020-12-31')
            mask = (avg_period_country_deaths["date"] > start_period) & (avg_period_country_deaths["date"] < end_period)
            avg_period_country_deaths_mask = avg_period_country_deaths[mask]
            moyenne = avg_period_country_deaths_mask['deaths'].mean()
            st.metric(f"Average covid deaths during selected period for France ", np.round(moyenne, 2))
    
            fig = px.histogram(avg_period_country_cases_mask, x="date", y="deaths")
            fig.update_layout(bargap=0.2)
            st.plotly_chart(fig, use_container_width=True)
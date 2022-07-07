import pandas as pd
import requests
from pandas import json_normalize
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from line import Line
from map import Map


st.set_page_config(page_title="streamlit_project", page_icon=":mask:", layout="centered")
st.sidebar.title(":mask: Corona Dashboard")
st.sidebar.markdown("##")


@st.cache
def get_data():
    # url = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/json/"
    # response = requests.get(url)
    # dictr = response.json()
    # records = dictr['records']
    # dataframe = json_normalize(records)
    dataframe = pd.read_csv("../streamlit_corona/corona_data.csv")
    dataframe['dateRep'] = pd.to_datetime(dataframe['dateRep'], format="%d/%m/%Y")
    return dataframe


df = get_data()

plot_type = st.sidebar.radio(
    "Please select a plot type",
    ('Line Plot', 'Geo Plot')
)

if plot_type == 'Line Plot':
    line = Line(df)
    line.line_app()

elif plot_type == "Geo Plot":
    map = Map(df)
    map.map_app()

import pandas as pd
import streamlit as st
from line import Line
from map import Map


def do_stuff_on_page_load():
    st.set_page_config(layout="wide")


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


do_stuff_on_page_load()
st.sidebar.title(":mask: Dashboard :mask:")
st.sidebar.markdown("##")
df = get_data()

plot_type = st.sidebar.radio(
    "Please select a plot type :",
    ('Line Plot', 'Geo Plot')
)

if plot_type == 'Line Plot':
    line = Line(df)
    line.line_app()

elif plot_type == "Geo Plot":
    map = Map(df)
    map.map_app()

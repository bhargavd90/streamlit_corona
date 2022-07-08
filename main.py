import pandas as pd
import streamlit as st
from line import Line
from map import Map


def do_stuff_on_page_load():
    # To set the page layout to wide on page load
    st.set_page_config(layout="wide")


@st.cache
def get_data(path: str) -> pd.DataFrame:
    # Fetches the data from the given url and returns a dataframe
    # url = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/json/"
    # response = requests.get(url)
    # dictr = response.json()
    # records = dictr['records']
    # dataframe = json_normalize(records)
    dataframe = pd.read_csv(path)
    dataframe['dateRep'] = pd.to_datetime(dataframe['dateRep'], format="%d/%m/%Y")
    dataframe["popData2020"] = dataframe["popData2020"].astype(float)
    return dataframe


do_stuff_on_page_load()
st.sidebar.title(":mask: Dashboard :mask:")
st.sidebar.markdown("##")

file_path = "../streamlit_corona/corona_data.csv"
df = get_data(file_path)

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

import streamlit as st
import plotly.express as px
import pandas as pd
import datetime


def plot_line(df_sub, time_line):
    if time_line == "Cases To Deaths":
        df_group_1 = df_sub.groupby(['dateRep'])["cases"].agg('sum').reset_index(name='total_cases')
        df_group_2 = df_sub.groupby(['dateRep'])["deaths"].agg('sum').reset_index(name='total_deaths')
        df_group = pd.merge(df_group_1, df_group_2, on='dateRep')
        df_group["total_cases_deaths"] = df_group["total_cases"] / df_group["total_deaths"]
    elif time_line == "Cases":
        df_group = df_sub.groupby(['dateRep'])["cases"].agg('sum').reset_index(name='total_cases_deaths')
    elif time_line == "Deaths":
        df_group = df_sub.groupby(['dateRep'])["deaths"].agg('sum').reset_index(name='total_cases_deaths')
    plot = px.area(df_group, x="dateRep", y="total_cases_deaths")
    plot.update_xaxes(showgrid=False)
    plot.update_yaxes(showgrid=False)
    st.plotly_chart(plot)


class Line:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def line_app(self):
        date_range = st.date_input(
            label="Date Range",
            value=[self.dataframe["dateRep"].min(), self.dataframe["dateRep"].max()],
            min_value=self.dataframe["dateRep"].min(),
            max_value=self.dataframe["dateRep"].max(),
        ),

        countriesAndTerritories = st.selectbox("Select Country: ",
                                               options=self.dataframe["countriesAndTerritories"].unique(),
                                               index=0)

        try:
            df_sub = self.dataframe.query("dateRep>=@date_range[0][0] & dateRep<=@date_range[0][1] & "
                                          "countriesAndTerritories==@countriesAndTerritories")
            total_cases = int(df_sub["cases"].sum())
            total_deaths = int(df_sub["deaths"].sum())
            first_column, second_column, third_column = st.columns(3)
            with first_column:
                st.subheader("Total Cases:")
                st.subheader(total_cases)
            with second_column:
                st.subheader("Total Deaths:")
                st.subheader(total_deaths)
            with third_column:
                st.subheader("Cases To Deaths:")
                st.subheader(round(total_cases / total_deaths, 2))
            st.markdown("___")
            time_line = st.selectbox("Select Timeline Plot: ", options=["Cases", "Deaths", "Cases To Deaths"], index=0)
            plot_line(df_sub, time_line)
        except Exception as e:
            st.markdown("Please select a valid date range")




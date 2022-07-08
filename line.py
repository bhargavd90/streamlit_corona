import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def plot_line(df_sub: pd.DataFrame, time_line: str, cumulative_checkbox: bool) -> None:
    if time_line == "Deaths/Cases":
        df_group_1 = df_sub.groupby(['dateRep'])["cases"].agg('sum').reset_index(name='total_cases')
        df_group_2 = df_sub.groupby(['dateRep'])["deaths"].agg('sum').reset_index(name='total_deaths')
        df_group = pd.merge(df_group_1, df_group_2, on='dateRep')
        df_group["total_cases_deaths"] = df_group["total_deaths"] / df_group["total_cases"]
    elif time_line == "Cases":
        df_group = df_sub.groupby(['dateRep'])["cases"].agg('sum').reset_index(name='total_cases_deaths')
    elif time_line == "Deaths":
        df_group = df_sub.groupby(['dateRep'])["deaths"].agg('sum').reset_index(name='total_cases_deaths')
    if cumulative_checkbox:
        df_group["total_cases_deaths"] = df_group.total_cases_deaths.cumsum()
    plot = px.area(df_group, x="dateRep", y="total_cases_deaths", labels={
        "dateRep": "date slider",
        "total_cases_deaths": time_line
    }, )
    plot.update_xaxes(showgrid=False)
    plot.update_yaxes(showgrid=False)
    plot.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    plot.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    st.plotly_chart(plot, use_container_width=True)


def plot_pie(df_sub: pd.DataFrame, time_line: str) -> None:
    df_group_1 = df_sub.groupby(['popData2020', "countriesAndTerritories"])['cases'].agg('sum').reset_index(
        name='total_cases')
    df_group_2 = df_sub.groupby(['popData2020'])['deaths'].agg('sum').reset_index(name='total_deaths')
    df_group = pd.merge(df_group_1, df_group_2, on='popData2020')
    df_group["no_total_cases"] = df_group["popData2020"] - df_group["total_cases"]
    df_group["no_total_deaths"] = df_group["total_cases"] - df_group["total_deaths"]
    df_group["total_cases_pie"] = round(df_group["total_cases"] * 100 / df_group["popData2020"], 2)
    df_group["no_total_cases_pie"] = 100 - df_group["total_cases_pie"]
    df_group["total_deaths_pie"] = round(
        df_group["total_deaths"] * df_group["total_cases_pie"] / df_group["total_cases"], 2)
    df_group["no_total_deaths_pie"] = df_group["total_cases_pie"] - df_group["total_deaths_pie"]
    plot_1 = go.Figure(go.Sunburst(
        labels=["population", "positive", "negative", "deaths", "no_deaths"],
        parents=["", "population", "population", "positive", "positive"],
        values=[100, df_group["total_cases_pie"].iloc[0], df_group["no_total_cases_pie"].iloc[0],
                df_group["total_deaths_pie"].iloc[0], df_group["no_total_deaths_pie"].iloc[0]],
        branchvalues="total",
    ))
    #plot_1.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    df_sub["Day_of_Week"] = df_sub.dateRep.dt.day_name()
    if time_line != "Deaths/Cases":
        if time_line == "Cases":
            df_day = df_sub.groupby(['Day_of_Week'])["cases"].agg('sum').reset_index(name='per_day')
        elif time_line == "Deaths":
            df_day = df_sub.groupby(['Day_of_Week'])["deaths"].agg('sum').reset_index(name='per_day')
        plot_2 = px.pie(df_day, values='per_day', names='Day_of_Week')

    column_3_0, column_3_1 = st.columns(2)
    with column_3_0:
        st.subheader("piechart w/r to population")
        st.markdown("##")
        st.plotly_chart(plot_1, use_container_width=True)
    with column_3_1:
        if time_line != "Deaths/Cases":
            st.subheader("piechart w/r to day of week")
            st.markdown("##")
            st.plotly_chart(plot_2, use_container_width=True)
        else:
            pass


class Line:

    # First page

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def line_app(self):
        st.title(":mask: Timeline per country")
        date_range = st.date_input(
            label="Date Range :",
            value=[self.dataframe["dateRep"].min(), self.dataframe["dateRep"].max()],
            min_value=self.dataframe["dateRep"].min(),
            max_value=self.dataframe["dateRep"].max(),
        ),

        countriesAndTerritories = st.selectbox("Country :",
                                               options=self.dataframe["countriesAndTerritories"].unique(),
                                               index=0)

        try:
            df_sub = self.dataframe.query("dateRep>=@date_range[0][0] & dateRep<=@date_range[0][1] & "
                                          "countriesAndTerritories==@countriesAndTerritories")
            total_cases = int(df_sub["cases"].sum())
            total_deaths = int(df_sub["deaths"].sum())
            column_0_0, column_0_1, column_0_2 = st.columns(3)
            with column_0_0:
                st.subheader("Cases:")
                st.subheader(total_cases)
            with column_0_1:
                st.subheader("Deaths:")
                st.subheader(total_deaths)
            with column_0_2:
                st.subheader("Deaths/Cases:")
                st.subheader(round(total_deaths / total_cases, 2))
            st.markdown("___")
            column_1_0, column_1_1, column_1_2 = st.columns(3)
            with column_1_0:
                time_line = st.selectbox("Timeline Plot: ", options=["Cases", "Deaths", "Deaths/Cases"], index=0)
            with column_1_1:
                cumulative_checkbox = st.checkbox('cumulative')
            with column_1_2:
                piechart_checkbox = st.checkbox('plot pie')
            plot_line(df_sub, time_line, cumulative_checkbox)
            st.markdown("___")
            if piechart_checkbox:
                plot_pie(df_sub, time_line)
                st.markdown("___")
            st.subheader("Tabular data")
            st.markdown("##")
            st.dataframe(df_sub)
        except Exception as e:
            print(e)
            st.error("insufficient data to display the plot")

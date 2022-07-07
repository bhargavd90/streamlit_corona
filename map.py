import plotly.graph_objects as go
import streamlit as st


class Map:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def map_app(self):
        date_range = st.date_input(
            label="Date Range",
            value=[self.dataframe["dateRep"].min(), self.dataframe["dateRep"].max()],
            min_value=self.dataframe["dateRep"].min(),
            max_value=self.dataframe["dateRep"].max(),
        ),

        try:
            df_sub = self.dataframe.query("dateRep>=@date_range[0][0] & dateRep<=@date_range[0][1]")
            df_group = df_sub.groupby(['countriesAndTerritories'])['cases'].agg('sum').reset_index(
                name='total_cases')
            plot = go.Figure(data=go.Choropleth(
                locationmode="country names",
                locations=df_group["countriesAndTerritories"],
                z=df_group["total_cases"].astype(float),
                colorscale="Reds",
                colorbar_title="Cases in million",
                # text=df_group_2["total_cases"].astype(str)
            )
            )
            plot.update_layout(
                title_text='Europe map with corona cases',
                geo=dict(
                    scope='europe',
                ),
                height=800,
                width=800,
                dragmode=False
            )
            st.plotly_chart(plot)
        except Exception as e:
            st.markdown("Please select a valid date range")


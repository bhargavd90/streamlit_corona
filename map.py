import streamlit as st


class Map:

    # Second page

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def map_app(self):
        st.title(":mask: Map view of corona cases")
        date_range = st.date_input(
            label="Date Range :",
            value=[self.dataframe["dateRep"].min(), self.dataframe["dateRep"].max()],
            min_value=self.dataframe["dateRep"].min(),
            max_value=self.dataframe["dateRep"].max(),
        ),
        column_0_0, column_0_1 = st.columns(2)
        with column_0_0:
            time_line = st.selectbox("Timeline Plot: ", options=["Cases", "Deaths"], index=0)
        with column_0_1:
            population_checkbox = st.checkbox('per population')
        try:
            df_sub = self.dataframe.query("dateRep>=@date_range[0][0] & dateRep<=@date_range[0][1]")
            if time_line == "Cases":
                df_group = df_sub.groupby(['countriesAndTerritories', 'popData2020'])['cases'].agg('sum').reset_index(
                    name='total_cases_deaths')
            elif time_line == "Deaths":
                df_group = df_sub.groupby(['countriesAndTerritories', 'popData2020'])['deaths'].agg('sum').reset_index(
                    name='total_cases_deaths')
            df_group["total_cases_deaths_population"] = (df_group["total_cases_deaths"] * 100) / df_group["popData2020"]
            if population_checkbox:
                z_name = "total_cases_deaths_population"
            else:
                z_name = "total_cases_deaths"

            data = [dict(type='choropleth',
                         locationmode="country names",
                         locations=df_group["countriesAndTerritories"],
                         z=df_group[z_name].astype(float),
                         colorscale="Reds")]
            layout = dict(geo=dict(scope='europe'),
                          height=800,
                          width=800,
                          dragmode=False
                          # sliders=slider
                          )
            plot = dict(data=data, layout=layout)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)
            st.error("insufficient data to display the plot or error while plotting")

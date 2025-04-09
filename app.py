import streamlit as st

from Top_10_Earthquakes_map.data_treatment import DataTreatment
from Top_10_Earthquakes_map.graphs import EarthquakeVisualizer

df = DataTreatment()
df_top_10 = df.top_10_df


visualizer = EarthquakeVisualizer(df_top_10)

st.set_page_config(layout="wide")

st.title("Dashboard de Terremotos - Top 10 por Magnitude")

visualizer.plot_map()
import plotly.express as px
import pandas as pd
import streamlit as st

class EarthquakeVisualizer:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def plot_map(self)->None:
        df = self.df
        fig = px.scatter_geo(
            df, 
            lon='lon', 
            lat='lat', 
            hover_name='place', 
            size='mag',
            color='mag',  # Cores baseadas na magnitude
            color_continuous_scale='YlOrRd',
            hover_data={
                'mag': True,
                'depth': True,
                'time': True,
                'tsunami': True,  # Adiciona essa informação no hover
                'lon': False,
                'lat': False
            },
            title='Mapa interativo de terremotos'
        )

        fig.update_layout(
            width=1200,
            height=700,
            geo=dict(
                showland=True,
                landcolor='LightGreen',
                showcountries=True,
                showocean=True,
                oceancolor='LightBlue'
            )
        )

        st.plotly_chart(fig)


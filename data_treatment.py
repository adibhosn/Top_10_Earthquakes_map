import pandas as pd
import requests
import plotly.express as px



class DataTreatment:
    def __init__(self) -> None:
        self.url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson'
        self.data = self.get_data()

        if self.data is None:
            raise ValueError("Erro ao obter os dados da URL.")

        self.raw_df = self.extract_raw_dataframe()
        self.cleaned_df = self.extract_properties_fields(self.raw_df)
        self.top_10_df = self.get_top_10_by_magnitude(self.cleaned_df)

    def get_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()

            return data

        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")

    def extract_raw_dataframe(self) -> pd.DataFrame:
        """
        Converte os dados brutos no dicionário 'features' em um DataFrame.
        """
        bruto = pd.DataFrame.from_dict(self.data, orient='index').reset_index()
        features_list = bruto.loc[bruto['index'] == 'features'].values

        if not features_list.any():
            raise ValueError("Nenhum dado de 'features' encontrado.")

        features_dict  = features_list[0][1]
        df = pd.DataFrame.from_dict(features_dict)
        df = df.drop(['type', 'id'], axis=1)
        return df
    
    def extract_properties_fields(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Extrai campos importantes da coluna 'properties' e trata o campo de tempo.
        """
        df = df.copy()

        # Extrair coordenadas (lon, lat)
        df[['lon', 'lat', 'depth']] = df['geometry'].apply(lambda x: pd.Series([
            x['coordinates'][0],  # longitude
            x['coordinates'][1],  # latitude
            x['coordinates'][2]   # profundidade
        ]))

        campos = ['mag', 'place', 'tsunami', 'type', 'title']

        for campo in campos:
            df[campo] = df['properties'].apply(lambda x: x.get(campo))

        # Tratar 'time' separadamente porque precisa de conversão
        df['time'] = df['properties'].apply(lambda x: pd.to_datetime(x.get('time'), unit='ms'))

        #dropando colunas antigas
        df = df.drop(['properties', 'geometry'], axis=1)
        return df
    
    def get_top_10_by_magnitude(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Retorna os 10 terremotos com maior magnitude.
        """
        df_top_10 = df.sort_values(by='mag', ascending=False).head(10).reset_index(drop=True)
        return df_top_10


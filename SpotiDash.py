# Run this app with `python DASH2.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Création de l'application
app = dash.Dash(__name__)

################################## LECTURE FICHIER ##################################

# Lien vers le fichier
link = 'https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/API_SPOTIFY/df_spotify_1754.zip'

# Lecture fichier
df = pd.read_csv(link)

list_artiste = sorted(df['artist_name'].unique().tolist())


################################## APPLICATION ##################################

fig = px.bar(data_frame=df[['album_name', 'artist_name', 'total_tracks']][df['artist_name'] == ''],
    x='artist_name'
    )

fig2 = px.bar(data_frame=df[['album_name', 'artist_name', 'total_tracks']][df['artist_name'] == ''],
    x='album_name',
    y='total_tracks'
    )

# Titres et textes
app.layout = html.Div([
    html.H1(children = "Stats Spotify",
            style={
            'textAlign': 'center'}
            ), # pour le titre
    dcc.Dropdown(list_artiste,
                id='input_search',
                value=''
            ),
    dcc.Graph(  figure=fig,
                id="fig_test"
            ),
    dcc.Graph(  figure=fig2,
                id="fig_test2"
            ) # affichage du graph# affichage du graph
])


################################## APPEL DES COMPOSANTS ##################################


@app.callback(
    [Output(component_id="fig_test", component_property="figure"),
    Output(component_id="fig_test2", component_property="figure")],
    Input(component_id="input_search", component_property="value")
)

def update_graph(value):
    
  # Utilisez Plotly Express pour créer un graphique en barres des 10 premiers livres, en affichant le nombre de pages par titre.
    fig = px.bar(data_frame=df[['album_name', 'artist_name', 'total_tracks']][df['artist_name'] == value],
       x='album_name'
       )
    fig.update_layout(title="Test", xaxis_title="Albums", yaxis_title = "Nb de titres")  

    return fig

def update_graph2(value):
    
  # Utilisez Plotly Express pour créer un graphique en barres des 10 premiers livres, en affichant le nombre de pages par titre.
    fig2 = px.bar(data_frame=df[['album_name', 'artist_name', 'total_tracks']][df['artist_name'] == ''],
                    x='album_name',
                    y='total_tracks'
    )
    fig.update_layout(title="Test", xaxis_title="Albums", yaxis_title = "Nb de titres")  

    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)
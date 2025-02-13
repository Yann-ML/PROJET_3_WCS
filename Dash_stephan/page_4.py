from dash import dcc, html
from navbar import create_navbar
import pandas as pd
from app import app
from dash.dependencies import Input, Output

nav = create_navbar()

header = html.H3("Partie choix d'un titre")

# on récupère le dataframe

df = pd.read_csv('https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/API_SPOTIFY/df_spotify_1754.zip')

list_artiste = sorted(df['artist_name'].unique().tolist())



def create_page_4():
    # layout = html.Div([
    #     # html.H1("Mon Lecteur Spotify"),
    #     # html.Iframe(
    #     # src="https://open.spotify.com/embed/track/57tzAvfPHXHzCHUNp9AUBm?utm_source=generator",
    #     # width="25%",
    #     # height="25%",
    #     # allow="encrypted-media",)
    # ]),
    layout = html.Div(
    children=[
        nav,
        header,
        html.Div(
            children="Vous voulez écouter un morceau ?",
            style={"font-style": "italic", "font-weight": "bold", 'margin-bottom': '50px'},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    list_artiste,
                    id="input_search",
                    placeholder="Choisissez un titre :",
                ),
                html.Div(id="dd-output-container"),
            ],
            style={"width": "50%"},
        ),
        html.Div(
            style={'margin-bottom': '50px'},  # pour les écarts verticaux
        ),
        html.Div(
            style={'padding-top': '50px'},  # pour les écarts horizontaux
        ),
        html.Div(
            [
                dcc.Dropdown(
                    list_artiste,
                    id="search_album",
                    placeholder="Choisissez un album :",
                ),
                html.Div(id="dd-output-container"),
            ],
            style={"width": "50%"},
        ),
    ]
    )
    return layout

@app.callback(
    Output(component_id="fig_test", component_property="figure"),
    Input(component_id="input_search", component_property="value")
)

def update_graph(value):
    
  # Utilisez Plotly Express pour créer un graphique en barres des 10 premiers livres, en affichant le nombre de pages par titre.
    fig = px.bar(data_frame=df[['album_name', 'artist_name', 'total_tracks']][df['artist_name'] == value],
       x='album_name'
       )
    fig.update_layout(title="Test", xaxis_title="Albums", yaxis_title = "Nb de titres")  

    return fig
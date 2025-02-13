# Run this app with `python DASH2.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc 
import google.generativeai as genai  #IA
from dotenv import load_dotenv  # IA
import os  # IA
import plotly.express as px
import pandas as pd

# Création de l'application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


################################## CHARGEMENT VARIABLE ENVIRONNEMENT ##################################

load_dotenv()

################################## CONNEXION GOOGLE CHATBOT ##################################

genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

################################## LECTURE FICHIER ##################################


# Lien vers le fichier
link = 'https://raw.githubusercontent.com/Yann-ML/PROJET_3_WCS/main/API_SPOTIFY/df_spotify_1754.zip'

# Lecture fichier
df = pd.read_csv(link)

list_artiste = sorted(df['artist_name'].unique().tolist())

# nettoyage de la colonne genre car vue comme du str
df['genres_artist_clean'] = df['genres_artist'].apply(lambda x: x.replace('[', '').replace(']', '').replace("'", ""))


################################## STYLE DES AFFICHAGES ##################################


button_style = {
    'padding': '10px 20px',
    'margin': '5px',
    'background-color': '#007bff',
    'color': 'white',
    'border': 'none',
    'border-radius': '5px',
    'cursor': 'pointer',
    'font-size': '16px',
    'text-align': 'center',
    'display': 'inline-block'
}


################################## APPLICATION ##################################


# Titres et textes
app.layout = html.Div([
    
    # Titre de la page
    html.H1(['SpotiDash'],
           style={'textAlign': 'center'}),

    # Affichage bulle informations éléments du DF
    html.Div([

        # Affichage nb artistes
        html.Div(children=[
                html.Label(f'{len(df["artist_id"].unique())} artistes',
                           style=button_style),
                    ], style={'padding': 10, 'flex': 1}),

        # Affichage nb albums
        html.Div(children=[        
                html.Label(f'{len(df["album_id"].unique())} albums',
                           style=button_style)
                    ], style={'padding': 10, 'flex': 1}),

        # Affichage nb titres
        html.Div(children=[        
                html.Label(f'{len(df["track_id"].unique())} titres',
                           style=button_style)
                    ], style={'padding': 10, 'flex': 1}),

        # Affichage nb genres
        html.Div(children=[
                # On explose la liste des genres, dont on récupère les valeurs uniques, et on prend ensuite la longueur de la liste
                html.Label(children=f"{len(df['genres_artist_clean'].apply(lambda x: x.split(',')).explode().drop_duplicates())} genres",
                          style=button_style)
                    ], style={'padding': 10, 'flex': 1})

    # Affichage pour avoir les 4 éléments visibles sur la même ligne
    ], style={'display': 'flex', 'flexDirection': 'row'}),

    # Case de sélection de la donnée ('artiste' dans le cas présent)
    dcc.Dropdown(list_artiste,
                id='input_search',
                value=''),

    # Affichage photo artiste et popularité
    html.Div([
        html.Img(
             style={'height': '8%','width': '8%'},
            id='img_artist'),
        html.Label(
            id='pop_artist')
        ], style={'display': 'flex', 'flexDirection': 'row'}),

    
    # En fonction de l'artiste recherché, récupère ses albums triés par popularité et affiche l'url de l'album
    
    # Bloc affichage Album à gauche et titre à droite
    html.Div([

        # top 3 pochette album + titre album
        html.Div([
        
        # Ligne affichage album 1
        html.Div([
            html.Img(
                     style={'height': '8%','width': '8%'},
                    id='img_album1'),
            html.Label(
                    id='title_album1')
                ], style={'display': 'flex', 'flexDirection': 'row'}),

        # Ligne affichage album 2
        html.Div([
            html.Img(
                     style={'height': '8%','width': '8%'},
                    id='img_album2'),
            html.Label(
                    id='title_album2')
                ], style={'display': 'flex', 'flexDirection': 'row'}),
        
        # Ligne affichage album 3
        html.Div([
            html.Img(
                     style={'height': '8%','width': '8%'},
                    id='img_album3'),
            html.Label(
                    id='title_album3')
                ], style={'display': 'flex', 'flexDirection': 'row'}),

    # affichage en colonne du bloc album+titre
    ], style={'display': 'flex', 'flexDirection': 'column'}), 

    # bloc affichage top tracks à droite du bloc album
    html.Div([

        # affichage des titres en colonne
        html.Div([
            html.Label('Top_track 1'),
            html.Label('Top_track 2'),
            html.Label('Top_track 3'),
            html.Label('Top_track 4')
                ], style={'display': 'flex', 'flexDirection': 'column'})
        
            ], style={'display': 'flex', 'flexDirection': 'column'})
             
    # affichage bloc album+titre en ligne
    ], style={'display': 'flex', 'flexDirection': 'row'}),
    
    # affichage biographie par le chat
    html.Div([
        html.Label(
                id='bio_artist'
                )       
            ])
])


################################## APPEL DES COMPOSANTS ##################################


# callback d'appel des images artistes, pochette albums, puis biographie par le chat
@app.callback(
    [Output(component_id="img_artist", component_property='src'),
     Output(component_id="pop_artist", component_property='children'),
     Output(component_id="img_album1", component_property='src'),
     Output(component_id="title_album1", component_property='children'),
     Output(component_id="img_album2", component_property='src'),
     Output(component_id="title_album2", component_property='children'),
     Output(component_id="img_album3", component_property='src'),
     Output(component_id="title_album3", component_property='children'),
     Output(component_id='bio_artist', component_property='children')],
        
    Input(component_id="input_search", component_property="value")
)

# fonction d'appel des éléments à récupérer dans le DF
def update_album_image(value):
    if value:
        
        # récup 3 albums les plus populaires de l'artiste sélectionné
        album_info = df[['album_name', 'popularity_album', 'popularity_artist', 'image_artist', 'artist_name', 'url_image_album']][df['artist_name'] == value].drop_duplicates().sort_values(by='popularity_album', ascending=False).iloc[0:3]
        
        # gestion si moins de 3 albums
        album1 = album_info.iloc[0] if len(album_info) > 0 else None
        album2 = album_info.iloc[1] if len(album_info) > 1 else None
        album3 = album_info.iloc[2] if len(album_info) > 2 else None

        # récup pochette et titres albums
        img_album1 = album1['url_image_album'] if album1 is not None else ' '
        title_album1 = album1['album_name'] if album1 is not None else ' '
        
        img_album2 = album2['url_image_album'] if album2 is not None else ' '
        title_album2 = album2['album_name'] if album2 is not None else ' '
        
        img_album3 = album3['url_image_album'] if album3 is not None else ' '
        title_album3 = album3['album_name'] if album3 is not None else ' '

        # récup image et popularité artiste
        artist_info = df[df['artist_name'] == value].iloc[0]
        img_artist = artist_info['image_artist']
        pop_artist = f"Popularité : {artist_info['popularity_artist']}"
        
        # génération du modèle d'IAG
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # définition du prompt
        prompt = f"Peux tu m'afficher le maximum d'informations sur {value} dans un style biographie d'artiste ? Je veux un bloc de 10 lignes maximum, je ne veux pas de MarkDown dans le texte. soit si tu veux afficher un mot en gras mets le en gras directement"
        
        # réponse du prompt et génération
        reponse = model.generate_content(prompt)
        texte = html.P(reponse.text) 
        
        return img_artist, pop_artist,\
                img_album1, title_album1,\
                img_album2, title_album2,\
                img_album3, title_album3,\
                texte
        
    return ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '  # Si aucun artiste n'est sélectionné, ne pas afficher d'image

if __name__ == '__main__':
    app.run_server(debug=True)
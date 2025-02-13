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
app = dash.Dash(__name__)


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
    
    ####################### TITRE PAGE #######################
    
    html.H1(['SpotiDash'],
           style={'textAlign': 'center'}),

    ####################### BULLE INFOS DF #######################
    
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
                    ], style={'padding': 10, 'flex': 1}),
        
        # Affichage nb labels
        html.Div(children=[
                html.Label(children=f'{len(df["label"].unique())} labels',
                          style=button_style)
                    ], style={'padding': 10, 'flex': 1})

    # Affichage pour avoir les 4 éléments visibles sur la même ligne
    ], style={'display': 'flex', 'flexDirection': 'row'}),

    ########################### CASE DE SELECTION ARTISTE ###########################

    dcc.Dropdown(list_artiste,
                id='input_search',
                value=''),

    ########################### ARTISTE SELECTIONNE / BIOGRAPHIE, PHOTO ###########################
    
    html.Div([
        
        html.Div([
            html.Label(
                id='pop_artist',
                style={'flex' : '2'}),
            html.Label(
                id='bio_artist',
                style={'flex' : '6'}),
                ], style={'display' : 'flex',
                          'flexDirection': 'column',
                          'gap' : '2px'}),
        html.Img(
            style={'height': '15%',
                   'width': '15%',
                   'borderRadius' : '50%'},
            id='img_artist'),
        
        ], style={'display': 'flex', 
                  'flexDirection': 'row'}),
    
    ########################### TOP 3 ALBUMS ###########################

    # Ligne affichage album 1
    html.Div([
        html.Img(
                id='img_album1',
                style={'height': '15%',
                       'width': '15%',
                       'flex': '2'}),
        
        # colonne affichage infos album 1
        html.Div([
            html.Label(id='title_album1'),
            html.Label(id='pop_album1'),
            html.Label(id='release_album1'),
            html.Label(id='label_album1')
                ], style={'display': 'flex',
                            'flexDirection': 'column',
                            'flex' : '2',
                            'gap' : '5px'}),
        
        # affichage infos album demandé au chat
        html.Label(
                id='info_album1',
                style={'flex' : '8'})
        
            ], style={'display': 'flex',
                      'flexDirection': 'row',
                      'alignItems' : 'center',
                      'justifyContent' : 'space-between',
                      'width' : '100%',
                      'gap' : '20px',
                      'padding' : '20px'}),

    # Ligne affichage album 2
    html.Div([
        html.Img(
                id='img_album2',
                style={'height': '15%',
                       'width': '15%',
                       'flex': '2'}),
        
        # colonne affichage infos album 2
        html.Div([
            html.Label(id='title_album2'),
            html.Label(id='pop_album2'),
            html.Label(id='release_album2'),
            html.Label(id='label_album2')
                ], style={'display': 'flex',
                            'flexDirection': 'column',
                            'flex' : '2',
                            'gap' : '5px'}),
        
        # affichage infos album demandé au chat
        html.Label(
                id='info_album2',
                style={'flex' : '8'})
        
            ], style={'display': 'flex',
                      'flexDirection': 'row',
                      'alignItems' : 'center',
                      'justifyContent' : 'space-between',
                      'width' : '100%',
                      'gap' : '20px',
                      'padding' : '20px'}),
        
    # Ligne affichage album 3
     html.Div([
        html.Img(
                id='img_album3',
                style={'height': '15%',
                       'width': '15%',
                       'flex': '2'}),
        
        # colonne affichage infos album 3
        html.Div([
            html.Label(id='title_album3'),
            html.Label(id='pop_album3'),
            html.Label(id='release_album3'),
            html.Label(id='label_album3')
                ], style={'display': 'flex',
                            'flexDirection': 'column',
                            'flex' : '2',
                            'gap' : '5px'}),
        
        # affichage infos album demandé au chat
        html.Label(
                id='info_album3',
                style={'flex' : '8'})
        
            ], style={'display': 'flex',
                      'flexDirection': 'row',
                      'alignItems' : 'center',
                      'justifyContent' : 'space-between',
                      'width' : '100%',
                      'gap' : '20px',
                      'padding' : '20px'})
    
])

################################## APPEL DES COMPOSANTS ##################################


# callback d'appel des images artistes, pochette albums, puis biographie par le chat
@app.callback(
    [Output(component_id="img_artist", component_property='src'),
     Output(component_id="pop_artist", component_property='children'),
     Output(component_id='bio_artist', component_property='children'),
     
     Output(component_id="img_album1", component_property='src'),
     Output(component_id="title_album1", component_property='children'),
     Output(component_id="pop_album1", component_property='children'),
     Output(component_id="release_album1", component_property='children'),
     Output(component_id="label_album1", component_property='children'),
     Output(component_id="info_album1", component_property='children'),
     
     Output(component_id="img_album2", component_property='src'),
     Output(component_id="title_album2", component_property='children'),
     Output(component_id="pop_album2", component_property='children'),
     Output(component_id="release_album2", component_property='children'),
     Output(component_id="label_album2", component_property='children'),
     Output(component_id="info_album2", component_property='children'),
          
     Output(component_id="img_album3", component_property='src'),
     Output(component_id="title_album3", component_property='children'),
     Output(component_id="pop_album3", component_property='children'),
     Output(component_id="release_album3", component_property='children'),
     Output(component_id="label_album3", component_property='children'),
     Output(component_id="info_album3", component_property='children')],
        
    Input(component_id="input_search", component_property="value")
)

# fonction d'appel des éléments à récupérer dans le DF
def update_album_image(value):
    if value:
        
        # récup 3 albums les plus populaires de l'artiste sélectionné
        album_info = df[['album_name', 'popularity_album', 'release_date', 'label', 'popularity_artist', 'image_artist', 'artist_name', 'url_image_album']][df['artist_name'] == value].drop_duplicates().sort_values(by='popularity_album', ascending=False).iloc[0:3]
        
        # gestion si moins de 3 albums
        album1 = album_info.iloc[0] if len(album_info) > 0 else None
        album2 = album_info.iloc[1] if len(album_info) > 1 else None
        album3 = album_info.iloc[2] if len(album_info) > 2 else None

        # récup pochette et titres albums
        img_album1 = album1['url_image_album'] if album1 is not None else ' '
        title_album1 = album1['album_name'] if album1 is not None else ' '
        pop_album1 = f"Popularité : {album1['popularity_album']}" if album1 is not None else ' '
        release_album1 = f"Date de sortie : {album1['release_date']}" if album1 is not None else ' '
        label_album1 = f"Label : {album1['label']}" if album1 is not None else ' '
        
        img_album2 = album2['url_image_album'] if album2 is not None else ' '
        title_album2 = album2['album_name'] if album2 is not None else ' '
        pop_album2 = f"Popularité : {album2['popularity_album']}" if album2 is not None else ' '
        release_album2 = f"Date de sortie : {album2['release_date']}" if album2 is not None else ' '
        label_album2 = f"Label : {album2['label']}" if album2 is not None else ' '
               
        img_album3 = album3['url_image_album'] if album3 is not None else ' '
        title_album3 = album3['album_name'] if album3 is not None else ' '
        pop_album3 = f"Popularité : {album3['popularity_album']}" if album3 is not None else ' '
        release_album3 = f"Date de sortie : {album3['release_date']}" if album3 is not None else ' '
        label_album3 = f"Label : {album3['label']}" if album3 is not None else ' '
        
        # récup image et popularité artiste
        artist_info = df[df['artist_name'] == value].iloc[0]
        img_artist = artist_info['image_artist']
        pop_artist = f"Popularité : {artist_info['popularity_artist']}"
        
        ##################### PROMPT INFOS ARTISTE #####################
        
        # génération du modèle d'IAG
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # définition du prompt
        prompt = f"Peux tu m'afficher le maximum d'informations sur {value} dans un style biographie d'artiste ? Je veux un bloc de 10 lignes maximum, je ne veux pas de MarkDown dans le texte. soit si tu veux afficher un mot en gras mets le en gras directement"
        reponse = model.generate_content(prompt) # génération de la réponse du prompt
        texte = html.P(reponse.text) # transformation en texte de la réponse et affichage
        
        ##################### PROMPT INFOS ALBUM #####################
        
        prompt2 = f"Peux-tu me raconter l'histoire de l'album {title_album1} de l'artiste {value} en 10 lignes ?"
        reponse2 = model.generate_content(prompt2) # génération de la réponse du prompt
        info_album1 = html.P(reponse2.text) # transformation en texte de la réponse et affichage
        
        prompt3 = f"Peux-tu me raconter l'histoire de l'album {title_album2} de l'artiste {value} en 10 lignes ?"
        reponse3 = model.generate_content(prompt3) # génération de la réponse du prompt
        info_album2 = html.P(reponse3.text) # transformation en texte de la réponse et affichage
        
        prompt4 = f"Peux-tu me raconter l'histoire de l'album {title_album3} de l'artiste {value} en 10 lignes ?"
        reponse4 = model.generate_content(prompt4) # génération de la réponse du prompt
        info_album4 = html.P(reponse4.text) # transformation en texte de la réponse et affichage
        
        return img_artist, pop_artist, texte, \
                img_album1, title_album1, pop_album1, release_album1, label_album1, info_album1, \
                img_album2, title_album2, pop_album2, release_album2, label_album2, info_album2,\
                img_album3, title_album3, pop_album3, release_album3, label_album3, info_album4\
                
    # si aucun artiste sélectionné, ne rien afficher (autant de ' ' que de return attendus)
    return ' ', ' ', ' ', \
            ' ', ' ', ' ', ' ', ' ', ' ',\
            ' ', ' ', ' ', ' ', ' ', ' ',\
            ' ', ' ', ' ', ' ', ' ', ' '

if __name__ == '__main__':
    app.run_server(debug=True)
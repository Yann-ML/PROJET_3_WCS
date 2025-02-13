from dash import html
from navbar import create_navbar
import google.generativeai as genai  #IA
from dotenv import load_dotenv  # IA
import os  # IA

# CHARGER LES VARIABLES D'ENVIRONNEMENT DEPUIS .env pour récupérer le google_api_key
load_dotenv()

# CONFIGURATION DE LA CONNEXION
genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))


nav = create_navbar()

header = html.H3('Welcome to page 3!')

test =         html.Div([
            html.P('Dash converts Python classes into HTML'),
            html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
        ])

image = html.Img(
                src='https://i.scdn.co/image/ab67616d0000b273a1dd49dc930832be23c88409',
                title='ma Photo',
                style={'height': '30%','width': '30%'},
            )

artiste = "Moby"

# partie génération d'un prompt
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = f"Peux tu m'afficher le maximum d'informations sur {artiste} dans un style biographie d'artiste ? Je veux un bloc de 10 lignes maximum, je ne veux pas de MarkDown dans le texte. soit si tu veux afficher un mot en gras mets le en gras directement"
reponse = model.generate_content(prompt)

texte = html.P(reponse.text)


def create_page_3():
    layout = html.Div([
        nav,
        header,
        test,
        image,
        texte,

    ],style={
            'textAlign': 'center'})
    return layout
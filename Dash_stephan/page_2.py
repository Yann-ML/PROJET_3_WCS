
from dash import html
from navbar import create_navbar

nav = create_navbar()

header = html.H3('Welcome to page 2!')


def create_page_2():
    layout = html.Div([
        nav,
        header,
        html.H1("Mon Lecteur Spotify"),
        html.Iframe(
        src="https://open.spotify.com/embed/track/57tzAvfPHXHzCHUNp9AUBm?utm_source=generator",
        width="25%",
        height="25%",
        allow="encrypted-media",)
    ])
    return layout
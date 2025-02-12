from dash import html
from navbar import create_navbar

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

def create_page_3():
    layout = html.Div([
        nav,
        header,
        test,
        image,

    ],style={
            'textAlign': 'center'})
    return layout
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('./data/clean_adj_sale_prices.csv')

sales_count = len(df)


fig = px.bar(df, x="sale_year", y="sale_price_adj", color='sale_location', barmode='group', title='Sales by year colored by location')

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(
    style={'backgroundColor': colors['background']},

    children=[
    html.H1(
        children='Phillips Auction House Historical Sales',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Historical auction results from Phillips auction house.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='Sales by year colored by location',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
import csv
import json
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from app import dash_app


# Info about each category
# 0 = grijs
# 1 = groen
# 2 = geel
# 3 = oranje
# 4 = rood
ubo_info = [
    {
        'title': 'UBO implementation status',
        'status': {
            'implemented': 1,
            'not implemented': 4
        },
        'description': 'As required by the 4th and 5th European Union’s Anti-Money Laundering Directive (AMLD) EU countries need to have established beneficial ownership registers by 10 January 2020. Which ones have done so, and which ones have failed to do so?',
    },
    {
        'title': 'Who has access?',
        'status': {
            'N/A': 0,
            'public': 1,
            'general public with legitimate interest': 2,
            'public only nationals and EU citizens': 3,
            'not public': 4
        },
        'description': 'EU countries are obliged to provide public access to beneficial ownership according to AMLD 5. Many countries do not comply. They restrict access to this data by closing off these registers to the public, only allowing public authorities to access them, only granting people access after disclosing their purpose of accessing beneficial ownership data or requiring e-identification or a national tax identification from users.',
    },
    {
        'title': 'Paywall',
        'status': {
            'N/A': 0,
            'no': 1,
            'yes': 4
        },
        'description': 'A threshold in accessing beneficial ownership data is enforcing a paywall. To access a beneficial ownership extract of a company, most EU countries charge a fee. Prices of beneficial ownership extracts (legal entity or person) fall in the range of €2,50 to €27,- per extract.',
    },
    {
        'title': 'Registration required',
        'status': {
            'N/A': 0,
            'no': 1,
            'yes': 4
        },
        'description': 'To keep track of who uses beneficial ownership registers, EU countries have implemented complicated registration systems. People that want to access these registers in many cases need a national digital identification document. This limits foreign authorities or persons to access and use beneficial ownership data.',
    },
    {
        'title': 'Structured data in machine readable format',
        'status': {
            'N/A': 0,
            'yes': 1,
            'no': 4
        },
        'description': 'How data is published determines its (re)usability. Only two countries publish data in their registers as structured data and in machine readable formats (Denmark and Latvia). These countries allow (re)users to download the full dataset and access individual data through an A.P.I. Most EU countries still publish beneficial ownership extracts in PDF format instead of open data formats, limiting its reusability.',
    },
    {
        'title': 'Search for persons/legal entities',
        'status': {
            'N/A': 0,
            'legal entity and person': 1,
            'legal entity': 3
        },
        'description': 'The usability of beneficial ownership registers is also determined by their functionalities, for example how data can be searched. In almost all EU countries users can only search by company name, and on a name of a beneficial owner. Only in five countries it is possible to search by company name and beneficial owner.',
    }
]


# Map the results to their colors
color_map = {
    0: '#9AC0D8',
    1: '#0BCEAB',
    2: '#F6FF7A',
    3: '#FFD17A',
    4: '#FF4E4E',
}


# Load the data containing the results of all categories and countries
ubo_data = []
with open('data/data.csv') as IN:
    ubo_data = list(csv.DictReader(IN))


# Load the data containing the tooltips for results
ubo_data_tooltips = []
with open('data/data_tooltips.csv') as IN:
    ubo_data_tooltips = list(csv.DictReader(IN))


def create_legend(i):
    return i
    ''.join([html.P(x) for x in ubo_info[i]['status'].keys()])


# Update a collapse item (part of the category menu accordion on the left)
def update_collapse_item(i):
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        ubo_info[i]['title'],
                        color='link',
                        id=f'group-{i}-toggle',
                        className='collapse-button',
                        style={'textAlign': 'left'}
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    [
                        ubo_info[i]['description'],
                        html.Br(),
                        html.Br(),
                    ] + [
                            html.Div(
                                [
                                    html.Div('', className='legend-color', style={'background-color': f"{color_map[value]}"}),
                                    html.Span(' ' + key)
                                ]
                            ) for key, value in ubo_info[i]['status'].items()
                        ]
                ),
                id=f"collapse-{i}",
            ),
        ]
    )


# Data from https://geojson-maps.ash.ms/: medium resolution (50m),
# Europe, deselected countries we don't need and included Cyprus
with open('data/custom.geo-50m-europe41.json') as IN:
    countries = json.load(IN)


# Update the choropleth map
def update_choropleth(current_result):
    # Results value for each country, e.g. [1, 1, 4, 3, ...]
    results = [ubo_info[current_result]['status'][x[ubo_info[current_result]['title']]] for x in ubo_data]
    return {
        'data': [
            go.Choropleth(
                # This specifies that we provide our own geojson
                locationmode='geojson-id',
                # Provide our own custom geojson
                geojson=countries,
                # Specify the key in the geojson containing the country
                # ISO 3166-1 alpha-3 code
                featureidkey='properties.iso_a3',
                # ISO 3166-1 alpha-3 code of the countries we want to show,
                # e.g., ['AUT', 'BEL', 'BGR', ...]
                locations=[x['Country code'] for x in ubo_data],
                z=results,
                showscale=False,
                # Only retrieve the colors that are actually used in a map,
                # otherwise gradients of the colors might be used
                colorscale=[color_map[x] for x in list(set(sorted(results)))],
                # Provide text for the tooltips
                text=[
                    '<b>{0}</b>: {1}<br>{2}'.format(
                            x['Country'],
                            # Result
                            x[ubo_info[current_result]['title']],
                            # Retrieve any extra tooltip info
                            ubo_data_tooltips[idx][ubo_info[current_result]['title']]
                        ) for idx, x in enumerate(ubo_data)
                ],
                hoverinfo="text",
            )
        ],
        'layout': go.Layout(
            geo={
                'scope': 'europe',
                'domain': {
                    'x': [0, 1],
                    'y': [0, 1]
                },
                'lataxis': {'range': [38, 70]},
                'lonaxis': {'range': [-24, 34]},
                'showcoastlines': False,
                'resolution': 50,
                'showframe': False,
                'projection': {'type': 'mercator'},
                'showland': False,
                'showocean': True,
                'oceancolor': '#FFF0E6',
            },
            showlegend=False,
            height=900,
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            font={'family': "'Montserrat', sans-serif"},
        )
    }


# Main layout of the dash app
dash_app.layout = html.Div(
    [
        # Needed for page routing
        dcc.Location(id='url', refresh=False),

        # Navbar
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("About", href="/about")),
            ],
            brand="UBO Atlas",
            brand_href="/",
            color="#204C72",
            dark=True,
        ),

        # The page content is added here
        html.Div(id='page-content'),

        # The page content is added here
        html.Footer(
            [
                html.Div('logo', className="osf"),
                html.Div('contact', className="lower-footer")
            ]
        )
    ]
)


# Layout of the about page
about_layout = html.Div(
    [
        html.Br(),
        html.H1('About UBO Atlas'),
        html.P(
            'Anonymous companies and other legal entities are vehicles that are frequently used by malicious individuals to commit financial crimes such as money laundering, cross-border corruption, environmental crimes and even human trafficking. The Panama Papers and LuxLeaks have proven this to be the case. And because of the anonymous character of these companies, the real individuals behind these entities are often not held accountable for their harmful and illegal actions.'
        ),
        html.P(
            'To combat this, the European Union has taken significant steps to increase the transparency in company ownership with the 4th and 5h Anti Money Laundering Directive (AMLD). One of the instruments of the AMLD is enforcing member states to open up their beneficial ownership registers to the public. This recognizes the value of public oversight and scrutiny of who owns a company and who is pulling the strings. Not only to fight financial crime, but also to ensure public trust in the financial system and ensure that companies can easily find out who they are in business with.'
        ),
        html.P(
            [
                'Three years after the adoption of AMLD 5 and a year after the deadline for member states to install and open up the beneficial ownership registers, the UBO Atlas showcases the current state of play in the European Union. It showcases the specifics regarding the implementation and accessibility of beneficial ownership registers in EU member states. The UBO Atlas builds upon ',
                html.A(
                    'research executed by TaxJustice Europe and Transparency International',
                    href='https://www.transparency.org/en/publications/access-denied-availability-accessibility-beneficial-ownership-registers-data-european-union'
                ),
                '. Over the course of the next couple of months more details about these beneficial ownerships will be added to the UBO Atlas.'
            ]
        ),
        html.P(
            [
                'If information is incorrect or not up to date anymore - please contact ',
                html.A(
                    'jesse@openstate.eu',
                    href='mailto:jesse@openstate.eu'
                ),
                ' with supporting evidence. This will be analysed and if sufficient proof is available the data presented in the UBO Atlas will be updated.'
            ]
        ),
        html.Br(),
    ],
    className="container"
)


# Page routing callback
@dash_app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    # About page
    if pathname == '/about':
        return about_layout
    # Home page
    else:
        return html.Div(
            [
                html.Div(
                    [
                        # Category menu on the left
                        html.Div([update_collapse_item(x) for x in range(0, len(ubo_info))], className="accordion col-4"),

                        # Choropleth
                        dcc.Graph(
                            id='choropleth',
                            config={'displayModeBar': False},
                            className="col-8"
                        )
                    ],
                    className="row"
                )
            ],
            className="container-fluid"
        )


# Callback that changes the choropleth and category menu based on a
# click on an item in the category menu
@dash_app.callback(
    [Output('choropleth', 'figure')] + [Output(f"collapse-{i}", "is_open") for i in range(0, len(ubo_info))],
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(0, len(ubo_info))],
)
def update_home_page(*args):
    ctx = dash.callback_context

    # Output for the default state when the page is first rendered, i.e.
    # open the first category and show its corresponding map
    if not ctx.triggered:
        return (update_choropleth(0), True,) + (False,) * (len(ubo_info) - 1)
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Depending on the clicked category, open that category and show that map
    group_number = int(re.match(r'group-(\d+)-toggle', button_id).group(1))
    return (update_choropleth(group_number),) + tuple(True if group_number == x else False for x in range(0, len(ubo_info)))


if __name__ == "__main__":
    app.run(threaded=True)

import csv
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
        'title': 'Status Implementation',
        'status': {
            'implemented': 1,
            'not implemented': 4
        },
        'description': 'Description of this category',
    },
    {
        'title': 'All UBO info accessible for',
        'status': {
            'N/A': 0,
            'public': 1,
            'general public with legitimate interest': 2,
            'public only nationals and EU citizens': 3,
            'not public': 4
        },
        'description': 'Description of this category',
    },
    {
        'title': 'Paywall',
        'status': {
            'N/A': 0,
            'no': 1,
            'yes': 4
        },
        'description': 'Description of this category',
    },
    {
        'title': 'Registration to get access required',
        'status': {
            'N/A': 0,
            'no': 1,
            'yes': 4
        },
        'description': 'Description of this category',
    },
    {
        'title': 'Available as open data',
        'status': {
            'N/A': 0,
            'no': 1,
            'yes': 4
        },
        'description': 'Description of this category',
    },
    {
        'title': 'Search by person/entity',
        'status': {
            'N/A': 0,
            'entity and person': 1,
            'legal entity': 3
        },
        'description': 'Description of this category',
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


# Update the choropleth map
def update_choropleth(current_result):
    results = [ubo_info[current_result]['status'][x[ubo_info[current_result]['title']]] for x in ubo_data]
    return {
        'data': [go.Choropleth(
            locations=[x['Country code'] for x in ubo_data],
            z=results,
            showscale=False,
            # Only retrieve the colors that are actually used in a map,
            # otherwise gradients of the colors might be used
            colorscale=[color_map[x] for x in list(set(sorted(results)))],
            text=['<b>{0}</b>: {1}'.format(x['Country'], x[ubo_info[current_result]['title']]) for x in ubo_data],
            hoverinfo="text",
        )],
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

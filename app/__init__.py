#/usr/bin/env python
# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
from flask import Flask

app = Flask(__name__)

external_stylesheets = ['/static/dash.css', dbc.themes.BOOTSTRAP]

dash_app = dash.Dash(__name__, server=app, url_base_pathname="/", external_stylesheets=external_stylesheets)

dash_app.config['suppress_callback_exceptions'] = True

dash_app.title = 'UBO Atlas - an overview of Ultimate Beneficial Ownership registers across the EU'

dash_app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Mulish:wght@500&display=swap" rel="stylesheet">
        <!-- Matomo -->
            <script type="text/javascript">
              var _paq = window._paq = window._paq || [];
              /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
              _paq.push(['trackPageView']);
              _paq.push(['enableLinkTracking']);
              (function() {
                var u="//analytics.openstate.eu/";
                _paq.push(['setTrackerUrl', u+'matomo.php']);
                _paq.push(['setSiteId', '2']);
                var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
                g.type='text/javascript'; g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
              })();
            </script>
        <!-- End Matomo Code -->
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

from app import routes

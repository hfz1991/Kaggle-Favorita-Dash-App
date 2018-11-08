import dash
import os

from flask import send_from_directory


app = dash.Dash()
server = app.server
app.config.supress_callback_exceptions = True

external_css = [
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'
]
for css in external_css:
    app.css.append_css({"external_url": css})


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

from flask import Flask, flash, redirect, render_template, request, session, abort
from bokeh.embed import server_document
# import bokeh
app = Flask(__name__)

@app.route("/")
def chart():
    # script=server_document(model=None,app_path="/app",url="http://localhost:5006")
    script=server_document("http://localhost:5006/bokeh-sliders")
    print(script)
    return render_template('chart.html',bokS=script)

if __name__ == "__main__":
    app.run(debug=True)
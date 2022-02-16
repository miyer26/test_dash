import altair as alt
from vega_datasets import data
from dash import Dash, dcc, html, Output, Input



iris = data.iris()


app = Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)


app = Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        html.Div("Iris dash", style={"fontSize": 30}),
        dcc.Dropdown(
            id="ycol",
            value="sepalLength",
            options=[{"label": i, "value": i} for i in iris.columns],
        ),
        html.Iframe(
            id="scatter",
            style={"border-width": "0", "width": "100%", "height": "400px"},
        ),
        dcc.RangeSlider(1.5, 4.5, 0.1, id="rslider", value=[1.5, 4.5]),
    ],
)


@app.callback(
    Output("scatter", "srcDoc"), Input("ycol", "value"), Input("rslider", "value")
)
def plot_altair(ycol, xrange, df=iris.copy()):
    xmin = xrange[0]
    xmax = xrange[1]
    chart = (
        alt.Chart(df[(df["sepalWidth"] < xmax) & (df["sepalWidth"] > xmin)])
        .mark_point()
        .encode(x="sepalWidth", y=ycol)
    )
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)

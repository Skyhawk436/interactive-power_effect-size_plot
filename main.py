# This project is using plotly to create my interactive power curve figure from jupyter.
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Output, Input
from statsmodels.stats.power import TTestIndPower

power_plot_app = Dash(__name__)

effect_size = 0.6
alpha = 0.05
sample_sizes = np.arange(5,100)
slider_range = np.arange(0.1, 2.0, 0.1, dtype=float)

power_plot_app.layout = html.Div(children=[
    html.H1(children='Power Plot App',style={'textAlign':'center'}),

    html.Div(children='''
        Interactive plot to explore the relationship between sample size, effect size and statistical power.
    ''', style={'textAlign':'center'}),

    dcc.Graph(
        id='power-plot'
    ),
    dcc.Slider(id='effect_size_slider',min=0.1, max=2.0, step=0.1, value=0.6),

    html.H3(children='Select effect size', style={'textAlign':'center'})
])


@power_plot_app.callback(Output('power-plot', 'figure'),(Input('effect_size_slider', 'value')))
def update_plot(selected_es_value):
    powers = []
    for s in sample_sizes:
        analysis = TTestIndPower()
        res = analysis.solve_power(nobs1=s, effect_size=selected_es_value, alpha=alpha)
        powers.append(res)

    fig = px.line(x=sample_sizes, y=powers, labels={'x': "sample size", 'y':'power at alpha=.05'})
    return fig


if __name__ == '__main__':
    power_plot_app.run_server(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

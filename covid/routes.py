from covid import app
import json, plotly
# from flask import render_template
from wrangling_scripts.wrangle_data import return_figures, get_dynamic_fig
import pandas as pd
from flask import Flask, render_template,request
import plotly.graph_objs as go

import numpy as np


@app.route('/')
@app.route('/index')
def index():
    
    figures = return_figures()
#     dynamic_fig = get_dynamic_fig()
    

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON
                           )



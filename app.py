
# coding: utf-8


import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect
import requests
import datetime

import bokeh
from bokeh.plotting import figure
from bokeh.io import show,output_notebook
from bokeh.embed import components
from bokeh.models import HoverTool
bv = bokeh.__version__

#create flask instance
app = Flask(__name__)
app.vars={}


# In[74]:

@app.route('/')
def main():
    return redirect('/index')


# In[75]:

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['start_date'] = request.form['start_date']
        return redirect('/graph')


# In[76]:

@app.route('/graph', methods=['GET', 'POST'])
def graph():

    def bokeh_plot(pred_df, actual_df, item, color1, color2):
        p = figure(plot_width=800, plot_height=500,
                   title="Two-Week Projection for {} start from {}".format(item, app.vars['start_date']), x_axis_type="datetime")
        p.line(pred_df.iloc[:, 0], pred_df.iloc[:, 1], line_width=3,
               line_color=color1, legend='Predicted {}'.format(item))
        p.line(actual_df.iloc[:, 0], actual_df.iloc[:, 1], line_width=3,
               line_color=color2, legend='Actual {}'.format(item))
        p.xaxis.axis_label = "Date"
        p.yaxis.axis_label = "Projection"
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_style = 'bold'
        p.xaxis.bounds = (pred_df.date.iloc[-1], pred_df.date.iloc[0])
        script, div = components(p)
        return script, div

    def generate_plots(no):
        pred_df = pd.read_csv('pred_{}.csv'.format(no))
        actual_df = pd.read_csv('actual_{}.csv'.format(no))
        pred_df['date'] = pred_df['date'].apply(
            lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
        actual_df['date'] = actual_df['date'].apply(
            lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

        # for sales
        pred_sales = pred_df[['date', 'pred_sales']]
        actual_sales = actual_df[['date', 'Net_Sales']]
        script_sales, div_sales = bokeh_plot(
            pred_sales, actual_sales, 'Net Sales', "#658b33", "#dbc69d")

        # for trans
        pred_trans = pred_df[['date', 'pred_trans']]
        actual_trans = actual_df[['date', 'Trans']]
        script_trans, div_trans = bokeh_plot(
            pred_trans, actual_trans, 'Transactions', "#658b33", "#dbc69d")

        # for visits
        pred_visits = pred_df[['date', 'pred_visits']]
        actual_visits = actual_df[['date', 'Visits']]
        script_visits, div_visits = bokeh_plot(
            pred_visits, actual_visits, 'Visits', "#658b33", "#dbc69d")

        return script_sales, div_sales, script_trans, div_trans, script_visits, div_visits

    if app.vars['start_date'] == '2014-05-01':
        script_sales, div_sales, script_trans, div_trans, script_visits, div_visits = generate_plots(1)
        
        return render_template('graph.html', bv=bv, period=app.vars['start_date'],
                               script_sales=script_sales, div_sales=div_sales,
                               script_trans=script_trans, div_trans=div_trans,
                               script_visits=script_visits, div_visits=div_visits
                               )
    

    elif app.vars['start_date'] == '2014-11-14':
        script_sales, div_sales, script_trans, div_trans, script_visits, div_visits = generate_plots(2)
        
        return render_template('graph.html', bv=bv, period=app.vars['start_date'],
                               script_sales=script_sales, div_sales=div_sales,
                               script_trans=script_trans, div_trans=div_trans,
                               script_visits=script_visits, div_visits=div_visits
                               )
        

    else:
        script_sales, div_sales, script_trans, div_trans, script_visits, div_visits = generate_plots(3)    

        return render_template('graph.html', bv=bv, period=app.vars['start_date'],
                               script_sales=script_sales, div_sales=div_sales,
                               script_trans=script_trans, div_trans=div_trans,
                               script_visits=script_visits, div_visits=div_visits
                               )



if __name__ == '__main__':
    
    #run the app
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)





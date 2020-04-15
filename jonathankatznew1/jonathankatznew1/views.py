"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from jonathankatznew1 import app
from jonathankatznew1.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


from jonathankatznew1.Models.QueryFormStructure import QueryFormStructure 
from jonathankatznew1.Models.QueryFormStructure import LoginFormStructure 
from jonathankatznew1.Models.QueryFormStructure import UserRegistrationFormStructure 
from jonathankatznew1.Models.QueryFormStructure import Covid19 


from jonathankatznew1.Models.Forms import ExpandForm
from jonathankatznew1.Models.Forms import CollapseForm



from os import path
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/datamodel')
def datamodel():
    """Renders the datamodel page."""
    return render_template(
        'datamodel.html',
        title='datamodel',
        year=datetime.now().year,
        message='Your datamodel page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )
@app.route('/Data')
def Data():
    """Renders the Data page."""
    return render_template(
        'Data.html',
        title='Data',
        year=datetime.now().year,
        message='Your Data page.'
    )

@app.route('/data/deaths' , methods = ['GET' , 'POST'])
def deaths():

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    # df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\deaths.csv'))
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/deaths.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    
    return render_template(
        'deaths.html',  
        title='Deaths',
        year=datetime.now().year,
        message='Death Cases dataset page.',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/data/recovered' , methods = ['GET' , 'POST'])
def recovered():

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/recovered.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    
    return render_template(
        'recovered.html',
        title='recovered Cases',
        year=datetime.now().year,
        message='recovered Cases dataset page.',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/data/confirmed' , methods = ['GET' , 'POST'])
def confirmed():

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/confirmed.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    
    return render_template(
        'confirmed.html',
        title='confirmed',
        year=datetime.now().year,
        message='confirmed Cases dataset page.',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )
@app.route('/dataquery' , methods = ['GET' , 'POST'])
def dataquery():

    

    form1 = Covid19()
    
    chart = ''
    chart_deaths = ''
    chart_recovered = ''
   
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/confirmed.csv'))
    df = df.drop(['Lat' , 'Long' , 'Province/State'], 1)
    df = df.rename(columns={'Country/Region': 'Country'})
    df = df.groupby('Country').sum()
    l = df.index
    m = list(zip(l , l))

    form1.countries.choices = m       
  
    df_deaths = pd.read_csv(path.join(path.dirname(__file__), 'static/data/deaths.csv'))
    df_deaths = df_deaths.drop(['Lat' , 'Long' , 'Province/State'], 1)
    df_deaths = df_deaths.rename(columns={'Country/Region': 'Country'})
    df_deaths = df_deaths.groupby('Country').sum()

    df_recovered = pd.read_csv(path.join(path.dirname(__file__), 'static/data/recovered.csv'))
    df_recovered = df_recovered.drop(['Lat' , 'Long' , 'Province/State'], 1)
    df_recovered = df_recovered.rename(columns={'Country/Region': 'Country'})
    df_recovered = df_recovered.groupby('Country').sum()

    if request.method == 'POST':
        countries = form1.countries.data 
        start_date = form1.start_date.data
        end_date = form1.end_date.data
       
        df = df.loc[countries]
        df = df.transpose()
        df.index = pd.to_datetime(df.index)
        df=df[start_date:end_date]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'line' , figsize = (32, 14) , fontsize = 22 , grid = True)
        chart = plot_to_img(fig)

       
        df_deaths = df_deaths.loc[countries]
        df_deaths = df_deaths.transpose()
        df_deaths.index = pd.to_datetime(df_deaths.index)
        df_deaths=df_deaths[start_date:end_date]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df_deaths.plot(ax = ax , kind = 'line' , figsize = (32, 14) , fontsize = 22 , grid = True)
        chart_deaths = plot_to_img(fig)


        df_recovered = df_recovered.loc[countries]
        df_recovered = df_recovered.transpose()
        df_recovered.index = pd.to_datetime(df_recovered.index)
        df_recovered = df_recovered[start_date:end_date]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df_recovered.plot(ax = ax , kind = 'line' , figsize = (32, 14) , fontsize = 22 , grid = True)
        chart_recovered = plot_to_img(fig)


    return render_template(
        'dataquery.html',
        form1 = form1,
        chart = chart,
        chart_deaths = chart_deaths,
        chart_recovered = chart_recovered

        
    )
def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

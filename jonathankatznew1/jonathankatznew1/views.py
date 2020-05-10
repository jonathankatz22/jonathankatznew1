"""
Routes and views for the flask application.
"""

from datetime import datetime
from jonathankatznew1 import app
from jonathankatznew1.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from flask   import Flask, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError
 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from jonathankatznew1.Models.QueryFormStructure import LoginFormStructure 
from jonathankatznew1.Models.QueryFormStructure import UserRegistrationFormStructure 
from jonathankatznew1.Models.QueryFormStructure import Covid19 

from jonathankatznew1.Models.Forms import ExpandForm
from jonathankatznew1.Models.Forms import CollapseForm

from os import path
from flask_bootstrap import Bootstrap


bootstrap = Bootstrap(app) #start bootstrap suppurt

db_Functions = create_LocalDatabaseServiceRoutines() #create a conection to the service routines

# The home() function that renders the Home page
@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

# The contact() function that renders the Contact page
@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
    )

# The about() function that renders the About page
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
    )

# The Register() function that renders the Register page, receives from the user a form with user registration
# details using UserRegistrationFormStrucute, checks if the user already exists (retrun error) or not (registers
# a new user with the details provided)
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            
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

# The Login() function that renders the Login page, receives from the user a form with the login 
# details (username and password) using LoginFormStructure, checks if the login data is correct using IsLoginGood
# and if so redirects to the DataQuery page. If not, a login error message is displayed and the user is asked to
# to Login again
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
         
             return redirect('/dataquery')

        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to Data Analysis',
        year=datetime.now().year,
        )

# The Data() function that renders the Data page which has links to the three Corona Virus Datasets (Deaths, Confirmed, Recovered)
@app.route('/Data')
def Data():
    """Renders the Data page."""
    return render_template(
        'Data.html',
          year=datetime.now().year,
        )

# The deaths() function that renders the Deaths Dataset page. The deaths() function reads the COVID-19 death cases dataset CSV file into
# a panda dataframe. Then, the dataframe is reduced to the first 10 and last 10 rows - a total of 20 rows. The user has the option to select 
# either Expand using form1 (show the 20 rows table in HTML) or Collapse using form2 (hide the table). The function redners the Deaths page 
# and returns to it the presentation of raw_data_table either in Expand (20 tows table) or Collapse (empty).

@app.route('/data/deaths' , methods = ['GET' , 'POST'])
def deaths():

    form1 = ExpandForm()
    form2 = CollapseForm()

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/deaths.csv'))
    df = pd.concat([df.head(10),df.tail(10)])
    raw_data_table = ''
    

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    
    return render_template(
        'deaths.html',  
        year=datetime.now().year,
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

# The recovered() function that renders the Recovered Dataset page. The recovered() function reads the COVID-19 recovered cases dataset CSV file into
# a panda dataframe. Then, the dataframe is reduced to the first 10 and last 10 rows - a total of 20 rows. The user has the option to select 
# either Expand using form1 (show the 20 rows table in HTML) or Collapse using form2 (hide the table). The function redners the Recovered page
# and returns to it the presentation of raw_data_table either in Expand (20 tows table) or Collapse (empty).
@app.route('/data/recovered' , methods = ['GET' , 'POST'])
def recovered():

    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/recovered.csv'))
    df = pd.concat([df.head(10),df.tail(10)])
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    
    return render_template(
        'recovered.html',
        year=datetime.now().year,
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

# The confirmed() function that renders the Confirmed Dataset page. The confirmed() function reads the COVID-19 Confirmed cases dataset CSV file into
# a panda dataframe. Then, the dataframe is reduced to the first 10 and last 10 rows - a total of 20 rows. The user has the option to select 
# either Expand using form1 (show the 20 rows table in HTML) or Collapse using form2 (hide the table). The function redners the Confirmed page and
# and returns to it the presentation of raw_data_table either in Expand (20 tows table) or Collapse (empty).
@app.route('/data/confirmed' , methods = ['GET' , 'POST'])
def confirmed():

    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/confirmed.csv'))
    df = pd.concat([df.head(10),df.tail(10)])
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    
    return render_template(
        'confirmed.html',
        year=datetime.now().year,
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

# The dataquery() function that renders the DataQuery page. The dataquery() function uses the COVID19 form that cotains start_Date,
# end_date, miltiple_countries and submit. The function reads into 3 dataframes the 3 CSV files/datasets (confirmed, deaths, recovered)
# The three dataframes data (df_deatha, df_confirmed, df_recovered) is organized such that all cases per country are grouped and unnecssary columns are removed/dropped. 
# The organized dataframes are then plotted as a line graph allowing multipe graphs (one graph for every country selected using the object ax = fig.add_subplot(111))
# The dataquery() function renders then the dataquery page and returns to it the 3 graphs (each with or more selected countries) 
@app.route('/dataquery' , methods = ['GET' , 'POST'])
def dataquery():

    form1 = Covid19()
    
    chart_confirmed = ''
    chart_deaths = ''
    chart_recovered = ''
   
    plt.rc('legend',fontsize=22)

    df_confirmed = pd.read_csv(path.join(path.dirname(__file__), 'static/data/confirmed.csv'))
    df_confirmed = df_confirmed.drop(['Lat' , 'Long' , 'Province/State'], 1)
    df_confirmed = df_confirmed.rename(columns={'Country/Region': 'Country'})
    df_confirmed = df_confirmed.groupby('Country').sum()
    l = df_confirmed.index
    m = list(zip(l , l))

    form1.countries.choices = m       
  
    
    if (request.method == 'POST'):
        countries = form1.countries.data 
        start_date = form1.start_date.data
        end_date = form1.end_date.data
       
        df_confirmed = df_confirmed.loc[countries]
        df_confirmed = df_confirmed.transpose()
        df_confirmed.index = pd.to_datetime(df_confirmed.index)
        df_confirmed=df_confirmed[start_date:end_date]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df_confirmed.plot(ax = ax , kind = 'line' , figsize = (32, 14) , fontsize = 22 , grid = True)
        chart_confirmed = plot_to_img(fig)


        #להסביר את השורות
        df_deaths = pd.read_csv(path.join(path.dirname(__file__), 'static/data/deaths.csv'))
        df_deaths = df_deaths.drop(['Lat' , 'Long' , 'Province/State'], 1)
        df_deaths = df_deaths.rename(columns={'Country/Region': 'Country'})
        df_deaths = df_deaths.groupby('Country').sum()
        df_deaths = df_deaths.loc[countries]
        df_deaths = df_deaths.transpose()
        df_deaths.index = pd.to_datetime(df_deaths.index)
        df_deaths=df_deaths[start_date:end_date]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df_deaths.plot(ax = ax , kind = 'line' , figsize = (32, 14) , fontsize = 22 , grid = True)
        chart_deaths = plot_to_img(fig)
        
        #להסביר את השורות
        df_recovered = pd.read_csv(path.join(path.dirname(__file__), 'static/data/recovered.csv'))
        df_recovered = df_recovered.drop(['Lat' , 'Long' , 'Province/State'], 1)
        df_recovered = df_recovered.rename(columns={'Country/Region': 'Country'})
        df_recovered = df_recovered.groupby('Country').sum()
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
        year=datetime.now().year,
        form1 = form1,
        chart_confirmed = chart_confirmed,
        chart_deaths = chart_deaths,
        chart_recovered = chart_recovered

        
    )

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

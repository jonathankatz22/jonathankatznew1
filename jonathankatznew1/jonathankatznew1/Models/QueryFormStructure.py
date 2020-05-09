
### ----------------------------------------------------------- ###
### --- include all software packages and libraries needed ---- ###
### ----------------------------------------------------------- ###
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField,SelectMultipleField
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired

### ----------------------------------------------------------- ###
## This class have the fields that are part of the Login form.
##   This form will get from the user a 'username' and a 'password' and sent to the server
##   to check if this user is authorised to continue
## You can see three fields:
##   the 'username' field - will be used to get the username
##   the 'password' field - will be used to get the password
##   the 'submit' button - the button the user will press to have the 
##   form be "posted" (sent to the server for process)

class LoginFormStructure(FlaskForm):
    username   = StringField('Username:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')



## This class have the fields of a registration form
##   This form is where the user can register himself. It will have sll the information
##   we want to save on a user (general information) and the username ans PW the new user want to have
## You can see three fields:
##   the 'FirstName' field - will be used to get the first name of the user
##   the 'LastName' field - will be used to get the last name of the user
##   the 'PhoneNum' field - will be used to get the phone number of the user
##   the 'EmailAddr' field - will be used to get the E-Mail of the user
##   the 'username' field - will be used to get the username
##   the 'password' field - will be used to get the password
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNum   = StringField('Phone number:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('Username:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

## This class has the fields that the user can set for the query of parameters 
## for analysing the data (using Pandas etc.)
## Following are the fields we are using (with format paramaters and validation):
##   the Countries - selecting one or more countries with validation
##   the Start_date - the start date for the query, format paramter and validation
##   the end_date - the end date for the query, format paramter and validation
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
 

class Covid19(FlaskForm):
    countries = SelectMultipleField('Select one or multiple contries:' , validators = [DataRequired] )
    start_date = DateField('Start Date (From 1/22/2020 ):' , format='%Y-%m-%d' , validators = [DataRequired])
    end_date = DateField('End Date (Until 08/05/2020):' , format='%Y-%m-%d' , validators = [DataRequired])
    submit = SubmitField('submit')





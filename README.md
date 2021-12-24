# data_rep_project
# Cian Hogan G00387860
# Data Representation Module Big Project
# HIGHER DIPLOMA IN SCIENCE IN COMPUTING (DATA ANALYTICS)

This repository stores the relevant files and instructions for the Final Assessment Project for the Data Representation and Querying Module for the HIGHER DIPLOMA IN SCIENCE IN COMPUTING (DATA ANALYTICS) through GMIT.
The aim of this project, as described in [Assessment Instructions](https://learnonline.gmit.ie/pluginfile.php/457695/mod_resource/content/8/Project%20Description.pdf), is to create a Web application in Flask that has a RESTful API, the application should link to one or more database tables.
***
App hosted on Python Anywhere: [http://cianhogan.eu.pythonanywhere.com/](http://cianhogan.eu.pythonanywhere.com/)
***
# Using the app
## Rep Max Calculator home page
The app allows users to calculate an estimated one-rep maximum for a given exercise based on the number of repetitions they achieve with sub-maximal weights.
One-repetition maximum (one rep maximum or 1RM) in weight training is the maximum amount of weight that a person can possibly lift for only one repetition.

The user enters their weight in KG and number of reps between 1-12, and that information is passed to a formula within the app.py via AJAX and Jquery, which calculates an estimated 1RM.

A table is also presented with estimated weights for each rep amount between 1-12. The table is hidden until the calculator is used and the result returned from the app.

## Login and Register
Users have the option to login via the login page if they already have an account.
If the user is not already registered they can register through the register page.

Once logged in the user is directed to their Dashboard page.

## Dashboard page
The dashboard page can only be accessed by a logged in user.
The dashboard page displays the users saved maximal weights between 1-5 reps for the Bench, Squat and Deadlift exercises.

At the bottom of the dashboard page the user has the option to logout.

From the table of records there are buttons leading to the pages to submit new or delete the current records listed on the dashboard.

## logMaxs (Submit records)
The logmaxs page allows the user to select an exercise and submit their record weights for 1-5 repetitions. Once a record is submitted they are directed back to the dashboard page. 

If the new records are larger than the previous records they will be displayed in the tables. The records are saved in the app database so are there if the user logs out and back in.

## Delete
On the delete page the user can delete the current records for a given exercise. After deleting a record they are redirected to the dashboard and that exercise table should now be empty.

## logout
The logout route logs the current user out of their session and redirects them to the login page.

***
# App.py
The Web App has a main python file called app.py which executes the Flask framework to create a web application. The app creates a number of pages, linking to html templates through the Flask @app.route method.
The app uses SQLALCHEMY to manage the database for the application. SQLALCHEMY uses object relational mapping as opposed to the classic SQL select where statements.

Many different Flask modules are used to provide extra functionality. FLask Forms are used for managing user input, FlaskLogin used for managing user sessions, Bcrypt is used for encrypting/hashing user passwords.

Any app dependencies are listed in the requirements.txt file.

# base.html
This file acts as a template for all other html files.
This file contains the nav bar is the same across all pages so can be added to the bae file and inherited across all other files.
Within the base file we add blocks using Jinja {{}}. This allows us to fill our title, page content and any javascript needed to to the other files which extend the base.
We can also add our scripts and style sheet links for implementing bootstrap styling to the app.

# Other html files
All other html files extend base.html but customize the content using jinja syntax.
Variables are base to the given template via the app routes in app.py

home.html also uses Ajax and Jquery to post data to '/process' route within app.py. This allows app.py to perform calculations and return a JSON object to the AJAX function and the page is manipulated based on that information.

# requirements.txt
The requirements.txt file holds a list of any python modules needed for this app to run.
The app was set up and runs on Python 3.8.3 but may run on other versions of python.
The app is running on Flask 2.0.2, but may run on other versions as well.

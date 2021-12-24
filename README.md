# data_rep_project
Data Representation Module Big Project

This repository stores the relevant files and instructions for the Final Assesment Project for the Data Representation and Querying Module for the HIGHER DIPLOMA IN SCIENCE IN COMPUTING (DATA ANALYTICS) through GMIT 
The aim of this project, as described in (assessment instructions)[https://learnonline.gmit.ie/pluginfile.php/457695/mod_resource/content/8/Project%20Description.pdf], is to create a Web application in Flask that has a RESTful API, the application should link to one or more database tables.

Python Anywhere: (http://cianhogan.eu.pythonanywhere.com/)[http://cianhogan.eu.pythonanywhere.com/]

# Using the app
## Rep Max Calculator home page
The app allows users to calculate an estimated one-rep maximum for a given exercise based on the number of repitions they achieve with sub-maximal wieghts.
One-repetition maximum (one rep maximum or 1RM) in weight training is the maximum amount of weight that a person can possibly lift for one repetition.
The user enters their weight in KG and number of reps between 1-12, and that information is passed to a formula which caluclates an estimated 1RM.
A table is also presented with estimated wiehgts for each rep amount between 1-12.

## Login and Register
Users have the option to login via the login page if they already have an account.
If the user is not already registered they can register through the register page.

Once logged in the user is directed to their Dashboard page.

## Dashboard page
The dashboard page can only be accessed by a logged in user.
The dashboard page displays the users saved maximal weights between 1-5 reps for the Bench, Squat and Deadlift exercises.

At the bottom of the dashboard page the user has the option to logout

From the table of records there are buttons leading to the pages to submit new or delete the current records listed on the dashboard

## logMaxs (Submit records)
The logmaxs page allows the user to select an exercise and submit their record weights for 1-5 repitions. Once a record is submitted they are directed back to the dashboard page. If the new records are larger than the previous records they will be displayed in the tables.

## Delete
On the delete page the user can delete the current records for a given exercise. After deleting a record they are redirected to the dashboard and that exercise table should now be empty.

## logout
The logout route logs the current user out of their session and redirects them to the login page.

# App.py
The Web App has a main python file called app.py whichexecutes the Flask framework to create a web application. The app creates a number of pages, linking to html templates.

The app creates 6 different pages or routes:
- home: This is the main landing page. home describes what the application is about and how to use it. It links to the other pages where a user can register and login.

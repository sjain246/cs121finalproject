Data:
    The data for our database comes from the github link provided 
    (https://github.com/awesomedata/awesome-public-datasets). 
    The specific link for the airline on-time performance dataset is 
    https://community.amstat.org/jointscsg-section/dataexpo/dataexpo2009. 
    This dataset, although large, is very thoughtfully organized, with a separate spreadsheet 
    for each year of data(from 1987 to 2008), in addition to extra spreadsheets for more 
    specific details about carriers, airports, plane data, and variable descriptions. With 
    all of this data, we can not only provide a lot of useful queried information to 
    potential users about flight cancellations, but also make relatively accurate predictions
    and recommendations on what flights to take based on historical patterns.

How to load data from command-line:
    Please run the following steps before running app.py to initialize the database and load in the data:
    $ cd your-files
    $ mysql
    mysql> CREATE DATABASE flightdb;
    mysql> USE flightdb;
    mysql> source setup.sql;
    mysql> source load-data.sql;
    mysql> source setup-passwords.sql;
    mysql> source setup-routines.sql;
    mysql> source grant-permissions.sql;
    mysql> source queries.sql;
    mysql> quit;
    $ python3 app.py

How to run Python program:


Additional features:
    We have provided a few additional features to the setup-passwords.sql file to facilitate 
    the use of our database through the Python UI.
    We have made a distinction between administrative users and client users in terms of 
    levels of access to the database. All administrative users can access all functionalities 
    of the database that clients can, with additional capabilities to modify the database.
    Specifically, administrators have the capability to downgrade an administrator's role 
    to that of a client, as well as the capability to upgrade a client's role to that of an 
    administrator, giving them full access to the program.
    Additionally, administrators are able to insert new flight route entries into the database 
    whereas clients may only view them.

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
    We pruned the data due to its extremely large size, and kept 993 records from the entire 
    dataset in which to store in our database. This represents 993 individual records of 
    US domestic flights and their corresponding information.

Downloading data files:
Please proceed to the github link https://github.com/sjain246/cs121finalprojdata (also included in link-to-data.txt) and download all csv
files from this repo. Files included are:
    airline.csv
    airport.csv
    delay_info.csv
    plane.csv
    routes.csv
Prior to loading the data, please ensure that all .csv files are in cr format,
    and not lf format. .csv files in lf format will not properly load.

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

How to run Python program:
    After loading the data, please use the following steps to run the Python program
    $ python3 app.py
    The program works as follows:
        Users are greeted by a home page, where they can exit or login with their credentials
    Initial users, as specified in the adding users section of setup-passwords are:
        Username: 'eyhan', Password: 'password11219', Role: Client
        Username: 'sjain3', Password: 'strongpass383', Role: Admin
    If user is a client, a limited version of the menu is displayed with all available 
    functionalities to them.
    If user is an administrator, a full version of the menu is displayed with all functionalities 
    for clients and additional functionalities for updating the database and updating 
    user roles.

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

Additional notes:
Note that for setup-passwords, we were given permission by Prof. Hovik
to modify the structure of the procedures to accept a third attribute of role.

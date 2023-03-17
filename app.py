"""
TODO: Student name(s):
TODO: Student email(s):
TODO: High-level program overview
******************************************************************************
This is a template you may start with for your Final Project application.
You may choose to modify it, or you may start with the example function
stubs (most of which are incomplete).
Some sections are provided as recommended program breakdowns, but are optional
to keep, and you will probably want to extend them based on your application's
features.
TODO:
- Make a copy of app-template.py to a more appropriately named file. You can
  either use app.py or separate a client vs. admin interface with app_client.py,
  app_admin.py (you can factor out shared code in a third file, which is
  recommended based on submissions in 22wi).
- For full credit, remove any irrelevant comments, which are included in the
  template to help you get started. Replace this program overview with a
  brief overview of your application as well (including your name/partners name).
  This includes replacing everything in this *** section!
******************************************************************************
"""
# TODO: Make sure you have these installed with pip3 if needed
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True
# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn(role):
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    if role == 1:
        usern = 'appclient'
        passw = 'clientpw'
    elif role == 2:
        usern = 'appadmin'
        passw = 'adminpw'
    else:
        sys.stderr('An internal error occurred, please contact the administrator.')
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user=usern,
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password=passw,
          database='flightdb' # replace this with your database name
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)
def authenticate(maybeusername, maybepassword):
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='adminpw',
          database='flightdb' # replace this with your database name
        )

        cursor = conn.cursor()
        sql = "SELECT authenticate(%s, %s)" % (maybeusername, maybepassword)
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            sys.stderr("Username does not exist!")
        else:
            (col1val) = (rows) # tuple unpacking!
            if col1val == 0:
                sys.stderr("Username does not exist!")
            return col1val
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)
# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def get_avg_delays():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    sql = """SELECT airline_name, AVG(total_delay) AS avg_delay
             FROM route NATURAL LEFT JOIN airline
             GROUP BY carrier_code;"""
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred, give something useful for clients...')
def count_port_pairs():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    sql = """SELECT a1.port_name AS origin_name, a2.port_name AS dest_name, 
             COUNT(*) AS num_routes
         FROM (route JOIN airport AS a1 
             ON route.origin_code = a1.port_code)
             JOIN airport AS a2
             ON route.destination_code = a2.port_code
         GROUP BY origin_code, destination_code;"""
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred, give something useful for clients...')
def get_min_avg_day():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    sql = """SELECT day_of_week
             FROM
                 (SELECT day_of_week, AVG(total_delay) AS avg_delay
                 FROM route
                 GROUP BY day_of_week) AS delays
             ORDER BY avg_delay ASC LIMIT 1;"""
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred, give something useful for clients...')
def min_avg_port_pair():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    sql = """SELECT origin_name, dest_name 
             FROM 
                 (SELECT a1.port_name AS origin_name, a2.port_name AS dest_name, 
                     AVG(total_delay) AS avg_delay
                 FROM (route LEFT JOIN airport AS a1 
                     ON route.origin_code = a1.port_code)
                     LEFT JOIN airport AS a2
                     ON route.destination_code = a2.port_code
                 GROUP BY origin_code, destination_code) AS route_pairs
             ORDER BY avg_delay ASC LIMIT 1;"""
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred, give something useful for clients...')
def max_avg_port_pair():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    sql = """SELECT origin_name, dest_name 
             FROM 
                 (SELECT a1.port_name AS origin_name, a2.port_name AS dest_name, 
                     AVG(total_delay) AS avg_delay
                 FROM (route LEFT JOIN airport AS a1 
                     ON route.origin_code = a1.port_code)
                     LEFT JOIN airport AS a2
                     ON route.destination_code = a2.port_code
                 GROUP BY origin_code, destination_code) AS route_pairs
             ORDER BY avg_delay DESC LIMIT 1;"""
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred, give something useful for clients...')
def get_model_avgs():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    sql = """SELECT manufacturer, model, AVG(total_delay) AS avg_delay
             FROM route NATURAL LEFT JOIN plane
             GROUP BY manufacturer, model;"""
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred, give something useful for clients...')
def get_min_airline():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    sql = """SELECT airline_name 
             FROM 
                 (SELECT airline_name, AVG(total_delay) AS avg_delay
                 FROM route NATURAL LEFT JOIN airline
                 GROUP BY carrier_code) AS delays
             ORDER BY avg_delay ASC LIMIT 1;"""
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred, give something useful for clients...')
def get_avg_dist_airline():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    sql = """SELECT airline_name, AVG(distance) AS avg_dist
             FROM route NATURAL LEFT JOIN airline
             GROUP BY carrier_code;"""
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred, give something useful for clients...')
def get_dist_vs_delay():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    sql = """SELECT distance, AVG(total_delay)
             FROM route
             GROUP BY distance
             ORDER BY distance ASC;"""
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred, give something useful for clients...')
# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)
# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
# TODO: Please change these!
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort)
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    print('  (TODO: provide command-line options)')
    print('  (a) - get average delay time for across all airlines')
    print('  (d) - get the day of the week with the lowest average delay')
    print('  (c) - gets the number of appearances of distinct origin/destination airport pairs')
    print('  (lp) - gets the origin/destination airport pair with the lowest average delay')
    print('  (hp) - gets the origin/destination airport pair with the highest average delay')
    print('  (m) - gets the average delay time for every aircraft model produced by all mnanufacturers')
    print('  (l) - gets the airline with the lowest average delay')
    print('  (d) - gets the average distance travelled per flight for all airlines')
    print('  (v) - gets a list of flight distances vs their corresponding average delay')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        get_avg_delays()
    elif ans == 'd':
        get_min_avg_day()
    elif ans == 'c':
        count_port_pairs()
    elif ans == 'lp':
        min_avg_port_pair()
    elif ans == 'hp':
        max_avg_port_pair()
    elif ans == 'm':
        get_model_avgs()
    elif ans == 'l':
        get_min_airline()
    elif ans == 'd':
        get_avg_dist_airline()
    elif ans == 'v':
        get_dist_vs_delay()
# Another example of where we allow you to choose to support admin vs. 
# client features  in the same program, or
# separate the two as different app_client.py and app_admin.py programs 
# using the same database.
def show_admin_options():
    """
    Displays options specific for admins, such as adding new data <x>,
    modifying <x> based on a given id, removing <x>, etc.
    """
    print('What would you like to do? ')
    print('  (x) - something nifty for admins to do')
    print('  (x) - another nifty thing')
    print('  (x) - yet another nifty thing')
    print('  (x) - more nifty things!')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == '':
        pass

def home_screen():
    """
    Displays options specific for admins, such as adding new data <x>,
    modifying <x> based on a given id, removing <x>, etc.
    """
    print('Welcome to FlightDB, an interface for interacting with US domestic airline data ')
    print('  (l) - Login with my credentials')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'l':
        maybeusername = input("Enter your username: ")
        maybepassword = input("Enter your password: ")
        role = authenticate(maybeusername, maybepassword)
        if role == 0:
            print("Login Failed!")
        else:
            conn = get_conn(role)
            main(role)

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()
def main(role):
    """
    Main function for starting things up.
    """
    if role == 1:
        show_options()
    elif role == 2:
        show_admin_options()
    else:
        sys.stderr("An internal error occurred, please contact the administrator.")
        quit_ui()
if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>
    conn = 0
    home_screen()
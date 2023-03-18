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
        sql = "SELECT authenticate(%s, %s)" % ("\'" + maybeusername + "\'", "\'" + maybepassword + "\'")
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
            sys.stderr('An error occurred while calculating average delays')
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
            sys.stderr('An error occurred while counting airports')
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
            sys.stderr('An error occurred when finding the day of the week with the smallest delay')
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
            sys.stderr('An error occurred while finding airports with the lowest delay')
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
            sys.stderr('An error occurred while finding airports with the highest delay')
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
            sys.stderr('An error occurred while computing aircraft model averages')
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
            sys.stderr('An error occurred while finding the airline with the shortest delay')
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
            sys.stderr('An error occurred while accessing the data')
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
            sys.stderr('An error occurred while accessing distances and delays')
def add_new_route():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    flight_num = input("Enter the flight number: ")
    flight_num = flight_num.strip()
    if not (flight_num.is_digit()):
        return "Invalid flight number"
    flight_num = (int)(flight_num)
    
    carrier_code = input("Enter the carrier code: ")
    carrier_code = carrier_code.strip()
    if not (carrier_code.is_digit() and len(carrier_code) <= 3):
        return "Invalid carrier code: at most 3 digits"
    
    depart_time = input("Enter the departure time: ")
    depart_time = depart_time.strip()

    arriv_time = input("Enter the arrial time: ")
    arriv_time = arriv_time.strip()

    tail_num = input("Enter the tail number: ")
    tail_num = tail_num.strip()
    if not (len(tail_num) <= 6):
        return "Invalid tail number: at most 6 digits"
    
    is_cancelled = input("Cancellation (Y/N): ")
    is_cancelled = is_cancelled.strip()
    if is_cancelled == 'Y':
        is_cancelled = 1
    elif is_cancelled == 'N':
        is_cancelled = 0
    else:
        return "Invalid input for cancellation"
    
    origin_code = input("IATA code of origin airport: ")
    origin_code = origin_code.strip()
    if not (len(origin_code) == 6):
        return "Invalid code: must be 3 digits"
    
    destination_code = input("IATA code of destination airport: ")
    destination_code = destination_code.strip()
    if not (len(destination_code) == 6):
        return "Invalid code: must be 3 digits"
    
    distance = input("Distance of flight: ")
    distance = distance.strip()
    if not (distance.is_digit()):
        return "Must be a number"
    distance = (int)(distance)

    day_of_week = input("Day of the week (0:Sunday, 1:Monday, ..., 6: Saturday): ")
    day_of_week = day_of_week.strip()
    if day_of_week not in ['0','1','2','3','4','5','6']:
        return "Must be a valid day of the week"
    day_of_week = (int)(day_of_week)

    departure_delay = input("Time of delay at departure: ")
    departure_delay = departure_delay.strip()
    if departure_delay == "":
        departure_delay = "0"
    if not departure_delay.is_digit():
        return "Must be a valid day of the week"
    departure_delay = (int)(departure_delay)

    arrival_delay = input("Time of delay at arrival: ")
    arrival_delay = arrival_delay.strip()
    if arrival_delay == "":
        arrival_delay = "0"
    if not arrival_delay.is_digit():
        return "Must be a valid day of the week"
    arrival_delay = (int)(arrival_delay)

    airline_delay = input("Time of delay due to airline: ")
    airline_delay = departure_delay.strip()
    if airline_delay == "":
        airline_delay = "0"
    if not airline_delay.is_digit():
        return "Must be a valid day of the week"
    airline_delay = (int)(airline_delay)

    weather_delay = input("Time of delay due to weather: ")
    weather_delay = weather_delay.strip()
    if weather_delay == "":
        weather_delay = "0"
    if not weather_delay.is_digit():
        return "Must be a valid day of the week"
    weather_delay = (int)(weather_delay)

    aircraft_delay = input("Time of delay due to aircraft: ")
    aircraft_delay = aircraft_delay.strip()
    if aircraft_delay == "":
        aircraft_delay = "0"
    if not aircraft_delay.is_digit():
        return "Must be a valid day of the week"
    aircraft_delay = (int)(aircraft_delay)

    NAS_delay = input("Time of delay due to NAS: ")
    NAS_delay = NAS_delay.strip()
    if NAS_delay == "":
        NAS_delay = "0"
    if not NAS_delay.is_digit():
        return "Must be a valid day of the week"
    NAS_delay = (int)(NAS_delay)

    security_delay = input("Time of delay due to security: ")
    security_delay = security_delay.strip()
    if security_delay == "":
        security_delay = "0"
    if not security_delay.is_digit():
        return "Must be a valid day of the week"
    security_delay = (int)(security_delay)
    
    sql = "CALL sp_newroute (%d, \'%s\', \'%s\', \'%s\', \'%s\', %d, \'%s\', \'%s\', %d, %d, %d, %d, %d, %d, %d, %d, %d)" % flight_num, carrier_code, depart_time, arriv_time, tail_num, is_cancelled, origin_code, destination_code, distance, day_of_week, departure_delay, arrival_delay, airline_delay, weather_delay, aircraft_delay, NAS_delay, security_delay
    try:
        cursor.execute(sql)
        conn.commit()
        # row = cursor.fetchone()
        # rows = cursor.fetchall()
        # if not rows:
        #     return "No results found!"
        # for row in rows:
        #     (col1val) = (row) # tuple unpacking!
        #     print(col1val)
            # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while inserting a new route entry into the database')
def add_new_client():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    new_uname = input("New username: ")
    new_uname = new_uname.strip()
    new_pw = input("New password: ")
    new_pw = new_pw.strip()
    sql = "CALL sp_add_user(\'%s\', \'%s\', 1);" % new_uname, new_pw
    try:
        cursor.execute(sql)
        conn.commit()
        # row = cursor.fetchone()
        # rows = cursor.fetchall()
        # if not rows:
        #     return "No results found!"
        # for row in rows:
        #     (col1val) = (row) # tuple unpacking!
        #     print(col1val)
        #     # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while creating a new client')
def add_new_admin():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    new_uname = input("New username: ")
    new_uname = new_uname.strip()
    new_pw = input("New password: ")
    new_pw = new_pw.strip()
    sql = "CALL sp_add_user(\'%s\', \'%s\', 2);" % new_uname, new_pw
    try:
        cursor.execute(sql)
        conn.commit()
        # row = cursor.fetchone()
        # rows = cursor.fetchall()
        # if not rows:
        #     return "No results found!"
        # for row in rows:
        #     (col1val) = (row) # tuple unpacking!
        #     print(col1val)
        #     # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while creating a new administrator')
def client_to_admin():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    uname = input("Client's username: ")
    uname = uname.strip()
    fsql = "SELECT * FROM user_info WHERE username = \'%s\'" % uname
    try:
        cursor.execute(fsql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        if len(rows) > 1:
            return "Too many users with this username!"
        (col1val) = (rows[0]) # tuple unpacking!
        if col1val[2] == 2:
            return "User is already an administrator"
        else:
            ssql = "CALL sp_upgrade_client(\'%s\');" % uname
            cursor.execute(ssql)
            conn.commit()
        # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while fetching data to upgrade client to admin')
def admin_to_client():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    uname = input("Administrator's username: ")
    uname = uname.strip()
    fsql = "SELECT * FROM user_info WHERE username = \'%s\'" % uname
    try:
        cursor.execute(fsql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        if len(rows) > 1:
            return "Too many users with this username!"
        (col1val) = (rows[0]) # tuple unpacking!
        if col1val[2] == 1:
            return "User is already a client"
        else:
            ssql = "CALL sp_downgrade_admin(\'" + uname + "\');"
            cursor.execute(ssql)
            conn.commit()
        # do stuff with row data
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            # TODO: Please actually replace this :) 
            sys.stderr('An error occurred while fetching data to downgrade admin to client')
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
    print('  (AC) - add a new client to the database')
    print('  (AA) - add a new admin to the database')
    print('  (UC) - upgrade an existing client to an admin')
    print('  (DA) - downgrade an existing admin to a client')
    print('  (I) - insert a new route')
    
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
    elif ans == 'ac':
        add_new_client()
    elif ans == 'aa':
        add_new_admin()
    elif ans == 'uc':
        client_to_admin()
    elif ans == 'da':
        admin_to_client()
    elif ans == 'i':
        add_new_route()

    elif ans == 'q':
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
        role = authenticate(maybeusername, maybepassword) [0][0]
        if role == 0:
            print("Login Failed!")
        return role

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
    r = home_screen()
    if r == 1 or r == 2:
        conn = get_conn(r)
        main(r)
"""
TODO: Student name(s): Eric Han, Sahil Jain
TODO: Student email(s): eyhan@caltech.edu, sjain3@caltech.edu
TODO: High-level program overview
******************************************************************************
User Interface to connect to flightDB database from Python.
Using command-line arguments to make connections to the database and retrieve 
information as needed.
Users are greeted by a home page, where they can exit or login with their credentials
If user is a client, a limited version of the menu is displayed with all available 
functionalities to them.
If user is an administrator, a full version of the menu is displayed with all functionalities 
for clients and additional functionalities for updating the database and updating 
user roles.
******************************************************************************
"""
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

# Makes the appropriate connection to the database based on the given role
# of the connecting user.
# Inputs: role -> integer indicating the role of the user
# Output: conn -> database connection object
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
          port='3306', 
          password=passw,
          database='flightdb'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
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

# Makes a local connection to the database to authenticate the user
# Determines if the user is in the database, and if so, whether they are 
# a client or an admin
# Inputs: maybeusername -> string indicating the username to be authenticated
#         maybepassword -> string indicating the password to be authenticated
# Output: col1val -> role of the user if they exist
def authenticate(maybeusername, maybepassword):
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          port='3306',
          password='adminpw',
          database='flightdb'
        )

        cursor = conn.cursor()
        sql = "SELECT authenticate(%s, %s)" % ("\'" + maybeusername + "\'", "\'" + maybepassword + "\'")
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            sys.stderr("Username does not exist!")
        else:
            (col1val) = (rows) # tuple unpacking!
            if col1val == 0:
                sys.stderr("Username does not exist!")
            return col1val
    except mysql.connector.Error as err:
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
# Calculates the average delay time across all airlines in the database.
# Prints results to user
# Inputs: N/A
# Output: N/A
def get_avg_delays():
    param1 = ''
    cursor = conn.cursor()
    sql = """SELECT airline_name, AVG(total_delay) AS avg_delay
             FROM route NATURAL LEFT JOIN airline
             GROUP BY carrier_code;"""
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while calculating average delays')

# Counts the number of origin/destination airport pairs
# Prints results to user
# Inputs: N/A
# Output: N/A
def count_port_pairs():
    param1 = ''
    cursor = conn.cursor()
    sql = """SELECT a1.port_name AS origin_name, a2.port_name AS dest_name, 
             COUNT(*) AS num_routes
         FROM (route JOIN airport AS a1 
             ON route.origin_code = a1.port_code)
             JOIN airport AS a2
             ON route.destination_code = a2.port_code
         GROUP BY origin_code, destination_code;"""
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while counting airports')

# Calculates the day of the week with the least delay
# Prints results to user
# Inputs: N/A
# Output: N/A
def get_min_avg_day():
    param1 = ''
    cursor = conn.cursor()
    sql = """SELECT day_of_week
             FROM
                 (SELECT day_of_week, AVG(total_delay) AS avg_delay
                 FROM route
                 GROUP BY day_of_week) AS delays
             ORDER BY avg_delay ASC LIMIT 1;"""
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when finding the day of the week with the smallest delay')

# Finds the origin/destination pair with the lowest delay time
# Prints results to user
# Inputs: N/A
# Output: N/A
def min_avg_port_pair():
    param1 = ''
    cursor = conn.cursor()
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
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while finding airports with the lowest delay')

# Finds the origin/destination pair with the highest delay time
# Prints results to user
# Inputs: N/A
# Output: N/A
def max_avg_port_pair():
    param1 = ''
    cursor = conn.cursor()
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
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while finding airports with the highest delay')

# Calculates the average delay time based on the airplane model
# Prints results to user
# Inputs: N/A
# Output: N/A
def get_model_avgs():
    param1 = ''
    cursor = conn.cursor()
    sql = """SELECT manufacturer, model, AVG(total_delay) AS avg_delay
             FROM route NATURAL LEFT JOIN plane
             GROUP BY manufacturer, model;"""
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while computing aircraft model averages')

# Finds the airline with the lowest amount of delays
# Prints results to user
# Inputs: N/A
# Output: N/A
def get_min_airline():
    param1 = ''
    cursor = conn.cursor()
    sql = """SELECT airline_name 
             FROM 
                 (SELECT airline_name, AVG(total_delay) AS avg_delay
                 FROM route NATURAL LEFT JOIN airline
                 GROUP BY carrier_code) AS delays
             ORDER BY avg_delay ASC LIMIT 1;"""
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while finding the airline with the shortest delay')

# Calculates the average distance travelled per flight for each airline
# Prints results to user
# Inputs: N/A
# Output: N/A
def get_avg_dist_airline():
    param1 = ''
    cursor = conn.cursor()
    sql = """SELECT airline_name, AVG(distance) AS avg_dist
             FROM route NATURAL LEFT JOIN airline
             GROUP BY carrier_code;"""
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while accessing the data')

# Calculates the average delay for each distance of flight travelled
# Prints results to user
# Inputs: N/A
# Output: N/A
def get_dist_vs_delay():
    param1 = ''
    cursor = conn.cursor()
    sql = """SELECT distance, AVG(total_delay)
             FROM route
             GROUP BY distance
             ORDER BY distance ASC;"""
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            return "No results found!"
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            print(col1val)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while accessing distances and delays')

# Adds a new route and all its associated information to the database
# If no delay times are entered, they default to 0
# Inputs: N/A
# Output: N/A
def add_new_route():
    param1 = ''
    cursor = conn.cursor()
    flight_num = input("Enter the flight number: ")
    flight_num = flight_num.strip()
    if flight_num == "" or not (flight_num.isdigit()):
        return "Invalid flight number"
    flight_num = (int)(flight_num)
    
    carrier_code = input("Enter the 2-3 character carrier code: ")
    carrier_code = carrier_code.strip()
    if not (len(carrier_code) <= 3 and len(carrier_code) > 0):
        return "Invalid carrier code: at most 3 digits"
    
    depart_time = input("Enter the departure time in YYYY-MM-DD HH:MM:SS format: ")
    depart_time = depart_time.strip()

    arriv_time = input("Enter the arrial time in YYYY-MM-DD HH:MM:SS format: ")
    arriv_time = arriv_time.strip()

    tail_num = input("Enter the upto 6 character tail number: ")
    tail_num = tail_num.strip()
    if not (len(tail_num) <= 6 and len(tail_num) > 0):
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
    if not (len(origin_code) == 3):
        return "Invalid code: must be 3 digits"
    
    destination_code = input("IATA code of destination airport: ")
    destination_code = destination_code.strip()
    if not (len(destination_code) == 3):
        return "Invalid code: must be 3 digits"
    
    distance = input("Distance of flight: ")
    distance = distance.strip()
    if not (distance.isdigit()):
        return "Must be a number"
    distance = (int)(distance)

    day_of_week = input("Day of the week (1:Monday, 2:Tuesday, ..., 7: Sunday): ")
    day_of_week = day_of_week.strip()
    if day_of_week not in ['1','2','3','4','5','6', '7']:
        return "Must be a valid day of the week"
    day_of_week = (int)(day_of_week)

    departure_delay = input("Time of delay at departure: ")
    departure_delay = departure_delay.strip()
    if departure_delay == "":
        departure_delay = "0"
    if not departure_delay.isdigit():
        return "Must be a valid day of the week"
    departure_delay = (int)(departure_delay)

    arrival_delay = input("Time of delay at arrival: ")
    arrival_delay = arrival_delay.strip()
    if arrival_delay == "":
        arrival_delay = "0"
    if not arrival_delay.isdigit():
        return "Must be a valid day of the week"
    arrival_delay = (int)(arrival_delay)

    airline_delay = input("Time of delay due to airline: ")
    airline_delay = airline_delay.strip()
    if airline_delay == "":
        airline_delay = "0"
    if not airline_delay.isdigit():
        return "Must be a valid day of the week"
    airline_delay = (int)(airline_delay)

    weather_delay = input("Time of delay due to weather: ")
    weather_delay = weather_delay.strip()
    if weather_delay == "":
        weather_delay = "0"
    if not weather_delay.isdigit():
        return "Must be a valid day of the week"
    weather_delay = (int)(weather_delay)

    aircraft_delay = input("Time of delay due to aircraft: ")
    aircraft_delay = aircraft_delay.strip()
    if aircraft_delay == "":
        aircraft_delay = "0"
    if not aircraft_delay.isdigit():
        return "Must be a valid day of the week"
    aircraft_delay = (int)(aircraft_delay)

    NAS_delay = input("Time of delay due to NAS: ")
    NAS_delay = NAS_delay.strip()
    if NAS_delay == "":
        NAS_delay = "0"
    if not NAS_delay.isdigit():
        return "Must be a valid day of the week"
    NAS_delay = (int)(NAS_delay)

    security_delay = input("Time of delay due to security: ")
    security_delay = security_delay.strip()
    if security_delay == "":
        security_delay = "0"
    if not security_delay.isdigit():
        return "Must be a valid day of the week"
    security_delay = (int)(security_delay)
    
    sql = "CALL sp_new_route (%d, \'%s\', \'%s\', \'%s\', \'%s\', %d, \'%s\', \'%s\', %d, %d, %d, %d, %d, %d, %d, %d, %d);" % (flight_num, carrier_code, depart_time, arriv_time, tail_num, is_cancelled, origin_code, destination_code, distance, day_of_week, departure_delay, arrival_delay, airline_delay, weather_delay, aircraft_delay, NAS_delay, security_delay)
    try:
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while inserting a new route entry into the database')

# Adds a new client, including their username and password to the database
# Inputs: N/A
# Output: N/A
def add_new_client():
    param1 = ''
    cursor = conn.cursor()
    new_uname = input("New username: ")
    new_uname = new_uname.strip()
    new_pw = input("New password: ")
    new_pw = new_pw.strip()
    sql = "CALL sp_add_user(\'%s\', \'%s\', 1);" % new_uname, new_pw
    try:
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while creating a new client')

# Adds a new admin, including their username and password to the database
# Inputs: N/A
# Output: N/A
def add_new_admin():
    param1 = ''
    cursor = conn.cursor()
    new_uname = input("New username: ")
    new_uname = new_uname.strip()
    new_pw = input("New password: ")
    new_pw = new_pw.strip()
    sql = "CALL sp_add_user(\'%s\', \'%s\', 2);" % new_uname, new_pw
    try:
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while creating a new administrator')

# Upgrades the role of a given client to that of an admin
# Inputs: N/A
# Output: N/A
def client_to_admin():
    param1 = ''
    cursor = conn.cursor()
    uname = input("Client's username: ")
    uname = uname.strip()
    fsql = "SELECT * FROM user_info WHERE username = \'%s\'" % uname
    try:
        cursor.execute(fsql)
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
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred while fetching data to upgrade client to admin')

# Downgrades the role of a given client to that of an admin
# Inputs: N/A
# Output: N/A
def admin_to_client():
    param1 = ''
    cursor = conn.cursor()
    uname = input("Administrator's username: ")
    uname = uname.strip()
    fsql = "SELECT * FROM user_info WHERE username = \'%s\'" % uname
    try:
        cursor.execute(fsql)
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
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
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
def show_options():
    """
    Displays options users can choose in the application
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
    Displays options specific for admins
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
    Displays options available before logging in
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
    r = home_screen()
    if r == 1 or r == 2:
        conn = get_conn(r)
        main(r)
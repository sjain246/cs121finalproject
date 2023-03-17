DROP TABLE IF EXISTS route;
DROP TABLE IF EXISTS delay_info;
DROP TABLE IF EXISTS airline;
DROP TABLE IF EXISTS plane;
DROP TABLE IF EXISTS airport;

-- Stores information about each airline
CREATE TABLE airline(
    -- the airline carrier code, which is of length 2 or 3
    carrier_code VARCHAR(3),
    -- the name of the airline
    airline_name VARCHAR(200),
    -- the carrier code will be used to uniqely identify airlines
    PRIMARY KEY (carrier_code)
);


-- Stores information about different aircrafts
CREATE TABLE plane (
    -- tail number of the aircraft
    tail_num VARCHAR(6),
    -- manufacturer of the aircraft (ie. Boeing or Airbus)
    manufacturer VARCHAR(100), 
    -- date issued
    issue_date DATE,
    -- aircraft model
    model VARCHAR(50),
    -- status of the aircraft
    status SMALLINT, 
    -- type of the aircraft
    aircraft_type VARCHAR (50),
    -- type of the engine used in the aircraft
    engine_type VARCHAR (25),
    -- the tail number will be used to uniqely identify planes
    PRIMARY KEY (tail_num)
);

-- Stores information about delays
CREATE TABLE delay_info (
    -- delay at departure in minutes
    departure_delay INT, 
    -- delay at arrival in minutes
    arrival_delay INT,
    -- delay due to airline in minutes
    airline_delay INT,
    -- delay due to weather in minutes
    weather_delay INT,
    -- delay due to late aircraft in minutes
    aircraft_delay INT,
    -- delay due to national aerospace systems in minutes
    NAS_delay INT,
    -- delay due to security in minutes
    security_delay INT,
    -- generated ID for delay_info entries
    delay_info_id INT AUTO_INCREMENT,
    -- the delay_info id will be used to uniquely identify delay information
    PRIMARY KEY (delay_info_id)
);

-- Stores information about each airport
CREATE TABLE airport (
    -- 3 digit IATA airport code
    port_code CHAR(3),
    -- name of the airport 
    port_name VARCHAR(100),
    -- country of the airport
    port_country CHAR(3),
    -- city of the airport
    port_city VARCHAR(50),
    -- state of the airport (all flights will be domestic)
    port_state CHAR(2),
    -- latitudinal coordinate of airport
    port_lat DOUBLE,
    -- longitudinial coordinate of airport
    port_long DOUBLE,
    -- the airport IATA code will be used to uniquely identify airports
    PRIMARY KEY (port_code)
);

-- Stores information about aircraft routes
CREATE TABLE route (
    -- at least 2 characters
    carrier_code VARCHAR(3) NOT NULL, 
    -- the associated number of the flight
    flight_num SMALLINT,
    -- scheduled time of departure
    depart_time TIMESTAMP, 
    -- scheduled time of arrival
    arrival_time TIMESTAMP,
    -- total calculated sum of delay times
    total_delay INT DEFAULT NULL,
    -- tail number of the aircraft
    tail_num VARCHAR(6) NOT NULL,
    -- stores if the flight was cancelled
    is_cancelled BOOLEAN,
    -- 3 digit IATA airport code of the origin airport
    origin_code CHAR(3) NOT NULL,
    -- 3 digit IATA airport code of the destination airport
    destination_code CHAR(3) NOT NULL,
    -- distance traveled by the route in miles
    distance INT, 
    -- day of the week of departure
    day_of_week TINYINT,
    -- ID of entry containing delay information
    delay_info_id INT AUTO_INCREMENT NOT NULL,
    -- the carrier code, flight number, and departure time
    -- will be used to uniqely identify routes
    PRIMARY KEY (carrier_code, flight_num, depart_time),
    FOREIGN KEY (carrier_code) REFERENCES airline(carrier_code),
    FOREIGN KEY (tail_num) REFERENCES plane(tail_num),
    FOREIGN KEY (delay_info_id) REFERENCES delay_info(delay_info_id),
    FOREIGN KEY (origin_code) REFERENCES airport(port_code),
    FOREIGN KEY (destination_code) REFERENCES airport(port_code)
);

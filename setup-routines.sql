-- File for Password Management section of Final Project
DROP PROCEDURE IF EXISTS sp_all_routes_update_total_delay;
DROP TRIGGER IF EXISTS trg_route_insert;
DROP TRIGGER IF EXISTS trg_route_update;
DROP PROCEDURE IF EXISTS sp_new_route;
DROP PROCEDURE IF EXISTS sp_upd_total_delay;
DROP FUNCTION IF EXISTS tot_delay_route;
DROP FUNCTION IF EXISTS tot_delay;

SET max_sp_recursion_depth = 1;

-- Set the "end of statement" character to ! so we don't confuse MySQL
DELIMITER !

-- Given a delay_info_id, returns the total delay from the delay_info db
CREATE FUNCTION tot_delay(delay_id INT) 
    RETURNS INT DETERMINISTIC
BEGIN
  DECLARE res INT;

  -- Get the total delay by taking a sum of all of the delay types 
  -- for the delay entity specified from the derived delay_id.
  SELECT departure_delay + arrival_delay + airline_delay + aircraft_delay + 
    weather_delay + NAS_delay + security_delay 
  INTO res
  FROM delay_info
  WHERE delay_info_id = delay_id;

  RETURN res;

END !


-- Given a flight route's carrier_code, flight_num, and depart_time,
-- returns the total delay in that route (via the delay_info db).
CREATE FUNCTION tot_delay_route(f_num SMALLINT, c_code VARCHAR(3), d_time TIMESTAMP) 
    RETURNS INT DETERMINISTIC
BEGIN
  DECLARE res INT;
  DECLARE delay_id INT;

  -- Get the delay_info_id for the flight route uniquely identified
  -- by the given flight number, carrier code, and departure time.
  SELECT delay_info_id 
  INTO delay_id
  FROM route
  WHERE carrier_code = c_code AND flight_num = f_num AND depart_time = d_time;

  -- Get the total delay from the derived delay_id via the tot_delay function.
  SELECT tot_delay(delay_id) 
  INTO res;

  RETURN res;

END !

-- Back to the standard SQL delimiter
DELIMITER ;


-- Set the "end of statement" character to ! so we don't confuse MySQL
DELIMITER !

-- A procedure to execute when inserting or updating a route
-- that will set its corresponding total delay depending on 
-- the delay values in 

CREATE PROCEDURE sp_upd_total_delay(
    new_flight_num SMALLINT,
    new_carrier_code VARCHAR(3),
    new_depart_time TIMESTAMP
)
BEGIN 
    DECLARE new_total INT;

    -- Gets the total delay for the flight route uniquely indetified by the 
    -- given carrier_code, flight_num, and depart_time.
    SELECT tot_delay_route(new_flight_num, new_carrier_code, new_depart_time)
    INTO new_total;

    -- Updates the route by setting the total delay to be 
    -- the derived total delay.
    UPDATE route
    SET total_delay = new_total
    WHERE carrier_code = new_carrier_code AND flight_num = new_flight_num AND 
        depart_time = new_depart_time;
END !

-- A procedure called immediately after adding initial values
-- to the database to update all of the rows in route with their 
-- respective total delays.
CREATE PROCEDURE sp_all_routes_update_total_delay()
BEGIN 
    DECLARE curr_depart_date TIMESTAMP;
    DECLARE curr_flight_num SMALLINT;
    DECLARE curr_carrier_code VARCHAR(3);

    DECLARE done INT DEFAULT 0;
    -- Define a cursor to get the flight number, carrier code,
    -- and depart time for each flight route in the route db.
    DECLARE cur CURSOR FOR
        SELECT flight_num, carrier_code, depart_time 
        FROM route;
    -- When fetch is complete, handler sets flag
    -- 02000 is MySQL error for "zero rows fetched"
    DECLARE CONTINUE HANDLER FOR SQLSTATE '02000'
        SET done = 1;
    OPEN cur;
    WHILE NOT done DO
        -- Fetch the next group of flight number, carrier code,
        -- and depart time from the cursor
        FETCH cur INTO curr_flight_num, curr_carrier_code, curr_depart_date;
        IF NOT done THEN
            -- Call the procedure defined above to set the total delay for
            -- the route uniquely identified by the provided parameters.
            CALL sp_upd_total_delay(curr_flight_num, curr_carrier_code, 
                curr_depart_date);
        END IF;
    END WHILE;
    CLOSE cur; -- don't forget to close the cursor
END !

-- Handles new rows added to route table (immediately after adding the 
-- corresponding delay_info row) and updates their total_delay
-- attribute accordingly. 
CREATE TRIGGER trg_route_insert BEFORE INSERT
       ON route FOR EACH ROW
BEGIN
    DECLARE new_total INT;
    DECLARE new_ind INT;

    -- Gets the current delay_info_id in the delay_info, which represents
    -- the delay_info_id for the route since the corresponding route row 
    -- is always immediately added after the delay_info row
    SELECT `AUTO_INCREMENT` - 1
    INTO new_ind
    FROM  INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'flightdb'
    AND   TABLE_NAME   = 'delay_info'; 

    -- Gets the total delay for the flight route based on its delay id.
    -- SELECT tot_delay(NEW.delay_info_id) 
    SELECT tot_delay(new_ind)
    INTO new_total;
    -- Updates the route by setting the total delay to be 
    -- the derived total delay.
    SET NEW.total_delay = new_total;
END !

-- Procedure to use when creating a new route to set the route's
-- attributes in both the delay_info and route tables. 
CREATE PROCEDURE sp_new_route(
    new_flight_num SMALLINT,
    new_carrier_code VARCHAR(3),
    new_depart_time TIMESTAMP,
    new_arriv_time TIMESTAMP,
    new_tail_num VARCHAR(6),
    new_is_cancelled BOOLEAN,
    new_origin_code CHAR(3),
    new_destination_code CHAR(3),
    new_distance INT, 
    new_day_of_week TINYINT,
    new_departure_delay INT, 
    new_arrival_delay INT,
    new_airline_delay INT,
    new_weather_delay INT,
    new_aircraft_delay INT,
    new_NAS_delay INT,
    new_security_delay INT
)
BEGIN 
    -- Inserts a new delay_info row based on inputted parameters
    INSERT INTO delay_info 
    VALUES (new_departure_delay, new_arrival_delay, new_airline_delay, 
        new_weather_delay, new_aircraft_delay, new_NAS_delay, 
        new_security_delay, 0);
    -- Inserts a new route row based on inputted parameters
    INSERT INTO route 
    VALUES (new_carrier_code, new_flight_num, new_depart_time, new_arriv_time, 
        0, new_tail_num, new_is_cancelled, new_origin_code, 
        new_destination_code, new_distance, new_day_of_week, 0);
END !

-- Back to the standard SQL delimiter
DELIMITER ;

-- Calling sp_all_newroutes immediately after adding initial values
-- to the database to update all of the rows in route with their 
-- respective total delays.
CALL sp_all_routes_update_total_delay();

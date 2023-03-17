-- File for Password Management section of Final Project
DROP PROCEDURE IF EXISTS sp_all_newroutes;
DROP TRIGGER IF EXISTS trg_route_insert;
DROP TRIGGER IF EXISTS trg_route_update;
DROP PROCEDURE IF EXISTS sp_newroute;
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

CREATE PROCEDURE sp_newroute(
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
CREATE PROCEDURE sp_all_newroutes()
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
            CALL sp_newroute(curr_flight_num, curr_carrier_code, 
                curr_depart_date);
        END IF;
    END WHILE;
    CLOSE cur; -- don't forget to close the cursor
END !


-- Handles new rows added to route table, updates their total_delay
-- attribute accordingly
CREATE TRIGGER trg_route_insert BEFORE INSERT
       ON route FOR EACH ROW
BEGIN
    DECLARE new_total INT;

    -- Gets the total delay for the flight route based on its delay id.
    SELECT tot_delay(NEW.delay_info_id) 
    INTO new_total;
    -- Updates the route by setting the total delay to be 
    -- the derived total delay.
    SET NEW.total_delay = new_total;
END !

-- Handles rows updated in route table, updates their total_delay
-- attribute accordingly
CREATE TRIGGER trg_route_update BEFORE UPDATE
       ON route FOR EACH ROW
BEGIN
    DECLARE new_total INT;

    -- Gets the total delay for the flight route based on its delay id.
    SELECT tot_delay(NEW.delay_info_id) 
    INTO new_total;
    -- Updates the route by setting the total delay to be 
    -- the derived total delay.
    SET NEW.total_delay = new_total;
END !
-- Back to the standard SQL delimiter
DELIMITER ;

-- Calling sp_all_newroutes immediately after adding initial values
-- to the database to update all of the rows in route with their 
-- respective total delays.
CALL sp_all_newroutes();

-- Queries equivalent to RA expressions:
-- [Query 1]
-- Query to get the average delay across all routes for each airline.
SELECT airline_name, AVG(total_delay) AS avg_delay
FROM route NATURAL LEFT JOIN airline
GROUP BY carrier_code;

-- [Query 2]
-- Query to get the number of times each origin/destination airport
-- pair/route is present in the database, with the names of the airports 
-- present in the result instead of the IATA code to amplify user experience
SELECT a1.port_name AS origin_name, a2.port_name AS dest_name, 
    COUNT(*) AS num_routes
FROM (route JOIN airport AS a1 
    ON route.origin_code = a1.port_code)
    JOIN airport AS a2
    ON route.destination_code = a2.port_code
GROUP BY origin_code, destination_code;

-- Query to get the day of the week where there is the 
-- minimum average amount of delay. This query would
-- be very useful for potential passengers to decide
-- when they should optimally book their flight.
-- Output is in integer form, with 1 representing
-- Monday all the way up to 7 representing Sunday.
SELECT day_of_week
FROM
    (SELECT day_of_week, AVG(total_delay) AS avg_delay
    FROM route
    GROUP BY day_of_week) AS delays
ORDER BY avg_delay ASC LIMIT 1;

-- Query to get the origin/destination airport pair
-- where there is the least amount of average delay.
SELECT origin_name, dest_name 
FROM 
    (SELECT a1.port_name AS origin_name, a2.port_name AS dest_name, 
        AVG(total_delay) AS avg_delay
    FROM (route LEFT JOIN airport AS a1 
        ON route.origin_code = a1.port_code)
        LEFT JOIN airport AS a2
        ON route.destination_code = a2.port_code
    GROUP BY origin_code, destination_code) AS route_pairs
ORDER BY avg_delay ASC LIMIT 1;

-- Query to get the origin/destination airport pair
-- where there is the greatest amount of average delay.
SELECT origin_name, dest_name 
FROM 
    (SELECT a1.port_name AS origin_name, a2.port_name AS dest_name, 
        AVG(total_delay) AS avg_delay
    FROM (route LEFT JOIN airport AS a1 
        ON route.origin_code = a1.port_code)
        LEFT JOIN airport AS a2
        ON route.destination_code = a2.port_code
    GROUP BY origin_code, destination_code) AS route_pairs
ORDER BY avg_delay DESC LIMIT 1;


-- Query to get the average delay for each 
-- aircraft manufacturer and model pair.
SELECT manufacturer, model, AVG(total_delay) AS avg_delay
FROM route NATURAL LEFT JOIN plane
GROUP BY manufacturer, model;



-- Query to get the airline with the lowest average total delay.
-- Useful to recommend to users what airline they should choose.
SELECT airline_name 
FROM 
    (SELECT airline_name, AVG(total_delay) AS avg_delay
    FROM route NATURAL LEFT JOIN airline
    GROUP BY carrier_code) AS delays
ORDER BY avg_delay ASC LIMIT 1;

-- Query to get the average distance (in miles) that flight routes cover
-- for each airline

SELECT airline_name, AVG(distance) AS avg_dist
FROM route NATURAL LEFT JOIN airline
GROUP BY carrier_code;

-- Query to get the average total delay for each route distance (in miles), 
-- which can be used to see how route distance affects delay
SELECT distance, AVG(total_delay)
FROM route
GROUP BY distance
ORDER BY distance ASC;
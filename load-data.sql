LOAD DATA LOCAL INFILE 'seattle_hosts.csv' INTO TABLE airline
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'seattle_hosts.csv' INTO TABLE route
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'seattle_hosts.csv' INTO TABLE plane
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'seattle_hosts.csv' INTO TABLE delay_info
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'seattle_hosts.csv' INTO TABLE airport
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS; -- If your CSV file has a row with column names

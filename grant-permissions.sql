DROP USER IF EXISTS 'appadmin'@'localhost';
DROP USER IF EXISTS 'appclient'@'localhost';

CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'clientpw';
-- Can add more users or refine permissions
GRANT ALL PRIVILEGES ON flightdb.* TO 'appadmin'@'localhost';
GRANT SELECT ON flightdb.* TO 'appclient'@'localhost';
FLUSH PRIVILEGES;
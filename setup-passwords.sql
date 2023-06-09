-- File for Password Management section of Final Project

-- Note that for setup-passwords, we were given permission by Prof. Hovik
-- to modify the structure of the procedures to accept a third attribute of 
-- role.
DROP TABLE IF EXISTS user_info;
DROP PROCEDURE IF EXISTS sp_add_user;
DROP PROCEDURE IF EXISTS sp_upgrade_client;
DROP PROCEDURE IF EXISTS sp_downgrade_admin;
DROP FUNCTION IF EXISTS authenticate;
DROP TABLE IF EXISTS make_salt;

-- (Provided) This function generates a specified number of characters for using as a
-- salt in passwords.
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT) 
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

-- Provided (you may modify if you choose)
-- This table holds information for authenticating users based on
-- a password.  Passwords are not stored plaintext so that they
-- cannot be used by people that shouldn't have them.
-- You may extend that table to include an is_admin or role attribute if you 
-- have admin or other roles for users in your application 
-- (e.g. store managers, data managers, etc.)
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,

    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,

    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL,
    -- integer representing the role of the user
    -- 1 indicates a client
    -- 2 indicates an admin
    role TINYINT NOT NULL
);

-- [Problem 1a]
-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table. 
-- Note that for setup-passwords, we were given permission by Prof. Hovik
-- to modify the structure of the procedures to accept a third attribute of 
-- role.
DELIMITER !
CREATE PROCEDURE sp_add_user(new_username VARCHAR(20), password VARCHAR(20), role TINYINT)
BEGIN
  DECLARE salt VARCHAR(20) DEFAULT '';
  SET salt = make_salt(8);
  INSERT INTO user_info VALUES 
    (new_username, salt, SHA2(CONCAT(salt, password), 256), role);
END !
DELIMITER ;

DELIMITER !
CREATE PROCEDURE sp_upgrade_client(new_username VARCHAR(20))
BEGIN
  UPDATE user_info
  SET role = 2
  WHERE username = new_username;
END !
DELIMITER ;

DELIMITER !
CREATE PROCEDURE sp_downgrade_admin(new_username VARCHAR(20))
BEGIN
  UPDATE user_info
  SET role = 1
  WHERE username = new_username;
END !
DELIMITER ;

-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user is a client, and 2 if the 
-- user is a admin, and the specified password hashes to the value for the 
-- user. Otherwise returns 0.
-- Note that for setup-passwords, we were given permission by Prof. Hovik
-- to modify the structure of the procedures to accept a third attribute of 
-- role.
DELIMITER !
CREATE FUNCTION authenticate(usern VARCHAR(20), passw VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
  -- TODO
  DECLARE temp INT DEFAULT 0;
  DECLARE rtemp INT DEFAULT 0;
  SELECT COUNT(username), role INTO temp, rtemp
  FROM user_info 
  WHERE user_info.username = usern AND 
    user_info.password_hash = SHA2(CONCAT(user_info.salt, passw), 256)
  GROUP BY username;
  IF temp = 0 THEN
	  RETURN 0;
  END IF;
  IF temp = 1 AND rtemp = 1 THEN
    RETURN 1;
  END IF;
  IF temp = 1 AND rtemp = 2 THEN
    RETURN 2;
  END IF;
END !
DELIMITER ;

-- [Problem 1c]
-- Add at least two users into your user_info table so that when we run this file,
-- we will have examples users in the database.
-- Note that for setup-passwords, we were given permission by Prof. Hovik
-- to modify the structure of the procedures to accept a third attribute of 
-- role.
CALL sp_add_user('eyhan', 'password11219', 1);
CALL sp_add_user('sjain3', 'strongpass383', 2);

-- [Problem 1d]
-- Optional: Create a procedure sp_change_password to generate a new salt and change the given
-- user's password to the given password (after salting and hashing)

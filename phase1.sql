CREATE DATABASE IF NOT EXISTS photoshare;
USE photoshare;

CREATE TABLE Users (
    user_id int4 AUTO_INCREMENT,
    email varchar(255) UNIQUE,
    password varchar(255),
    fname varchar(255), 
    lname varchar(255), 
    dob date, 
    hometown varchar(255), 
    gender varchar(255),
    PRIMARY KEY (user_id)
);

CREATE TABLE Albums ( 
	album_id int4 auto_increment, 
    album_name varchar(255),
    user_id int4 REFERENCES Users(user_id) ON DELETE CASCADE, 
    date_ofc date, 
    PRIMARY KEY (album_id)
);

CREATE TABLE Friends ( 
    friend_email varchar(255),
    email int4 REFERENCES Users(email) ON DELETE CASCADE,
    PRIMARY KEY (friend_email, email)
);

CREATE TABLE Pictures (
  picture_id int4  AUTO_INCREMENT,
  album_id int4,
  imgdata longblob ,
  caption varchar(255),
  INDEX upid_idx (album_id),
  PRIMARY KEY (picture_id)
);

CREATE TABLE Comments (
	comm_id int4 auto_increment,
    friend_email int4 REFERENCES Friends(friend_email) ON DELETE CASCADE,
    comm_text varchar(255), 
    comm_date date,
    PRIMARY KEY (comm_id)
);

CREATE TABLE Tags ( 
	tag_id int4,
	word varchar(255), 
    PRIMARY KEY (tag_id)
);

CREATE TABLE Makes (
	user_id int4 REFERENCES Users(user_id) ON DELETE CASCADE, 
    album_id int4 REFERENCES Albums(album_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, album_id)
);

CREATE TABLE Contain (
	album_id int4 REFERENCES Albums(album_id) ON DELETE CASCADE, 
    picture_id int4 REFERENCES Pictures(picture_id) ON DELETE CASCADE,
    PRIMARY KEY (picture_id, album_id)
);

CREATE TABLE Comm_On (
	comm_id int4 REFERENCES Comments(comm_id) ON DELETE CASCADE, 
    picture_id int4 REFERENCES Pictures(picture_id) ON DELETE CASCADE,
    PRIMARY KEY (comm_id, picture_id)
);

CREATE TABLE Comm (
	comm_id int4 REFERENCES Comments(comm_id) ON DELETE CASCADE, 
    friend_email int4 REFERENCES Friends(friend_email) ON DELETE CASCADE,
    PRIMARY KEY (comm_id, friend_email)
);

CREATE TABLE Associated (
	picture_id int4 REFERENCES Pictures(picture_id) ON DELETE CASCADE, 
    tag_id int4 REFERENCES Tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (picture_id, tag_id)
);

CREATE TABLE Liked (
	friend_email int4 REFERENCES Friends(friend_email) ON DELETE CASCADE, 
    picture_id int4 REFERENCES Pictures(picture_id) ON DELETE CASCADE,
    PRIMARY KEY (friend_email, picture_id)
);


INSERT INTO Users (email, password) VALUES ('test@bu.edu', 'test');
INSERT INTO Users (email, password) VALUES ('test1@bu.edu', 'test');

CREATE DATABASE photoshare;
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
	# album_id int4 auto_increment, 
    album_name varchar(255),
    user_id int4 REFERENCES Users(user_id) ON DELETE CASCADE, 
    date_ofc date, 
    PRIMARY KEY (album_name, user_id)
);

CREATE TABLE Friends ( 
    friend_email varchar(255),
    email varchar(255) REFERENCES Users(email) ON DELETE CASCADE,
    PRIMARY KEY (friend_email, email)
);

CREATE TABLE Pictures (
  picture_id int4  AUTO_INCREMENT,
  album_name varchar(255) REFERENCES ALbums(album_name),
  imgdata longblob ,
  caption varchar(255),
  user_id int4 REFERENCES Users(user_id) ON DELETE CASCADE, 
#  INDEX upid_idx (album_id),
  PRIMARY KEY (picture_id, user_id, album_name)
);

CREATE TABLE Comments (
	comm_id int4 auto_increment,
    friend_email varchar(255) REFERENCES Friends(friend_email) ON DELETE CASCADE,
    comm_text varchar(255), 
    comm_date date,
    picture_id int4 REFERENCES Pictures(picture_id) ON DELETE CASCADE,
    PRIMARY KEY (comm_id, picture_id)
);

CREATE TABLE Tags (
	word varchar(255), 
    picture_id int4 REFERENCES Pictures(picture_id) ON DELETE CASCADE,
    PRIMARY KEY (word, picture_id)
);


CREATE TABLE Liked (
	friend_email varchar(255) REFERENCES Friends(friend_email) ON DELETE CASCADE, 
    picture_id int4 REFERENCES Pictures(picture_id) ON DELETE CASCADE,
    PRIMARY KEY (friend_email, picture_id)
);



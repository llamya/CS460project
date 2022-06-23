CREATE DATABASE IF NOT EXISTS photoshare;
USE photoshare;
DROP TABLE IF EXISTS Pictures CASCADE;
DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE Users (
    user_id int4  AUTO_INCREMENT,
    email varchar(255) UNIQUE,
    password varchar(255),
    fname varchar(255), 
    lname varchar(255), 
    dob date, 
    hometown varchar(255), 
    gender varchar (255),
    PRIMARY KEY (user_id)
);
CREATE TABLE Album ( 
	album_id int4 auto_increment, 
    album_name VARCHAR(255),
    user_id int4 REFERENCES Users(user_id) ON DELETE CASCADE, 
    date_ofc date, 
    PRIMARY KEY (album_id)
);
CREATE TABLE Friends ( 
	friend_id int4, 
    user_id int4 REFERENCES Users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (friend_id)
);
CREATE TABLE Pictures(
  picture_id int4  AUTO_INCREMENT,
  album_id int4,
  imgdata longblob ,
  caption VARCHAR(255),
  INDEX upid_idx (album_id),
  PRIMARY KEY (picture_id)
);
CREATE TABLE Comments(
	comm_id int4 auto_increment,
    friend_id int4 REFERENCES Friends(friend_id) ON DELETE CASCADE,
    comm_text varchar (255), 
    comm_date date,
    PRIMARY KEY (comm_id)
);
CREATE TABLE Tags( 
	tag_id int4,
	word varchar (255), 
    PRIMARY KEY (tag_id)
);
CREATE TABLE Makes(
	user_id int4 REFERENCES Users(user_id) ON DELETE CASCADE, 
    album_id int4 REFERENCES Album(album_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, album_id)
);
CREATE TABLE contain(
	album_id int4 REFERENCES Album(album_id) ON DELETE CASCADE, 
    photo_id int4 REFERENCES Photos(photo_id) ON DELETE CASCADE,
    PRIMARY KEY (photo_id, album_id)
);
CREATE TABLE comm_on(
	comm_id int4 REFERENCES Comments(comm_id) ON DELETE CASCADE, 
    picture_id int4 REFERENCES Album(album_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, album_id)
);
CREATE TABLE comm(
	comm_id int4 REFERENCES Comments(comm_id) ON DELETE CASCADE, 
    friend_id int4 REFERENCES Friend(friend_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, album_id)
);
CREATE TABLE associated(
	photo_id int4 REFERENCES Photo(photo_id) ON DELETE CASCADE, 
    tag_id int4 REFERENCES Tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (photo_id, tag_id)
);

CREATE TABLE liked(
	friend_id int4 REFERENCES Friends(friend_id) ON DELETE CASCADE, 
    picture_id int4 REFERENCES Album(picture_id) ON DELETE CASCADE,
    PRIMARY KEY (friend_id, picture_id)
);


INSERT INTO Users (email, password) VALUES ('test@bu.edu', 'test');
INSERT INTO Users (email, password) VALUES ('test1@bu.edu', 'test');

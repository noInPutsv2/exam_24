CREATE TABLE user_logs (
log_id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
id int NOT NULL,
time_stamp DATETIME NOT NULL,
log_in BIT NOT NULL,
CONSTRAINT id FOREIGN KEY (id) REFERENCES dbo.users(id)
);
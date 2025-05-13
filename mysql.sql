/*These are mysql Queries , copy and paste in your mysql database terminal.*/

CREATE DATABASE smart_farming;

USE smart_farming;

CREATE TABLE IF NOT EXISTS crop_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    soil_moisture INT,
    recommended_crop VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);






/*
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='your_mysql_username',
        password='your_mysql_password',
        database='smart_farming',
        cursorclass=pymysql.cursors.DictCursor
    )
*/
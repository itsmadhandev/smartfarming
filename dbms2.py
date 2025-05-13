import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
import random
from datetime import datetime

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user=' ',     #database username
        password=' ',    #database password
        database=' ',   #database name
        cursorclass=pymysql.cursors.DictCursor
    )

def initialize_db():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crop_recommendations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                temperature FLOAT,
                humidity FLOAT,
                soil_moisture INT,
                recommended_crop VARCHAR(50),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

#this is logic
def recommend_crop(temp, hum, moisture):
    if moisture > 600 and temp > 25 and hum > 70:
        return "Rice"
    elif 400 < moisture <= 600 and 15 < temp < 25 and 50 < hum < 70:
        return "Wheat"
    elif moisture < 400 and temp > 28 and hum < 50:
        return "Cotton"
    elif 400 < moisture <= 600 and 20 < temp <= 30 and 50 <= hum <= 70:
        return "Maize"
    else:
        return "No strong match"

#inserting values to database 
def simulate_and_recommend():
    temp = round(random.uniform(15, 35), 2)
    hum = round(random.uniform(40, 90), 2)
    moisture = random.randint(300, 800)
    crop = recommend_crop(temp, hum, moisture)

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO crop_recommendations (temperature, humidity, soil_moisture, recommended_crop)
                VALUES (%s, %s, %s, %s)
            """, (temp, hum, moisture, crop))
        conn.commit()
        conn.close()

        messagebox.showinfo("Crop Recommendation",
                            f"Simulated Data:\nTemp: {temp}°C\nHumidity: {hum}%\nSoil Moisture: {moisture}\n\nRecommended Crop: {crop}")
        load_recommendations()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def load_recommendations():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM crop_recommendations ORDER BY timestamp DESC LIMIT 10")
            rows = cursor.fetchall()
        conn.close()

        for i in tree.get_children():
            tree.delete(i)
        for row in rows:
            tree.insert("", "end", values=(row['id'], row['temperature'], row['humidity'], row['soil_moisture'], row['recommended_crop'], row['timestamp']))
    except Exception as e:
        messagebox.showerror("Error", str(e))

initialize_db()

#graphical user interface - tkinter
root = tk.Tk()
root.title("Smart Farming - Crop Recommender")
root.geometry("950x500") #display size resolution

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Crop Recommendation System", font=("Helvetica", 16)).pack(pady=10)

btn = tk.Button(frame, text="Simulate & Recommend Crop", command=simulate_and_recommend, width=30, height=2)
btn.pack(pady=10)

columns = ("ID", "Temperature", "Humidity", "Soil Moisture", "Recommended Crop", "Timestamp")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=150)
tree.pack(pady=20, fill=tk.BOTH, expand=True)

load_recommendations()
root.mainloop()
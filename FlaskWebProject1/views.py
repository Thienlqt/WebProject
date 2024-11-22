"""
Routes and views for the flask application.
"""


import email
from flask import render_template
from FlaskWebProject1 import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask import Flask, render_template, request
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField
# from wtforms.validators import InputRequired, Email, Length

import math
from datetime import datetime, timedelta
import json

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'home.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Our contact'
    )

@app.route('/tracking')
def tracking():
    """Renders the contact page."""
    return render_template(
        'input.html',
        title='Tracking',
        year=datetime.now().year,
        message='Your tracking system'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/login')
def login():
    """Renders the login page."""
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/Registration')
def Registration():
    """Renders the registration page."""
    return render_template(
        'Registration.html',
        title='Registration',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/Checklogin', methods=['POST'])
def CheckLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Received email: {email}, password: {password}")  # Debugging statement
        
        if check_credentials(email, password):
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Please try again."

@app.route('/CheckRegister', methods=['POST'])
def CheckRegister():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Received email: {email}, password: {password}")  # Debugging statement
        
        if register_user(email, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Email may already be in use."

def check_credentials(email, password):
    with open('users.txt', 'r') as file:
        for line in file:
            stored_email, stored_password = line.strip().split(',')
            if email == stored_email and password == stored_password:
                return True
    return False

def register_user(email, password):
    if not user_exists(email):
        with open('users.txt', 'a') as file:
            file.write(f"{email},{password}\n")
        return True
    return False

def user_exists(email):
    with open('users.txt', 'r') as file:
        for line in file:
            stored_email = line.strip().split(',')[0]
            if email == stored_email:
                return True
    return False
    

def parse_timestamp(time_str):
        time_str = time_str[:-1]
        if '.' in time_str:
            base, fraction = time_str.split('.')
            time_str = f"{base}.{fraction[:6]}"
        return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")
def convert_time_to_int(dt):
        return dt.hour * 100 + dt.minute

def add_minutes(dt, minutes):
        return dt + timedelta(minutes=minutes)

def haversine_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in kilometers

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
        dlat = lat2 - lat1
        dlon = lon2 - lon1
    
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
    
        result = R * c
        return result

def calculate_calories_burned(weight_kg, distance_km, time_minutes):
        # Assuming walking at a moderate pace (3-4 mph)
        # MET value for moderate walking is approximately 3.5
        met = 3.5
    
        # Calorie calculation formula: calories = MET * weight (kg) * time (hours)
        time_hours = time_minutes / 60
        calories = met * weight_kg * time_hours
    
        return calories
@app.route('/Calculate', methods=['POST','GET'])
def Calculate():
    minutes = request.form['minute']
    kg = request.form['kg']
    minutes_to_add = int(minutes)
    weight_kg = float(kg)
    first_time = None
    first_position = None
    last_time = None
    last_position = None

    # Read the CSV file
    with open("iPhoneThingGps.csv", 'r') as file:
    # Skip the header
        next(file)
    
        for line in file:
                # Split the line manually
            time_str, value_str = line.strip().split(',', 1)
        
            dt = parse_timestamp(time_str)
            position = json.loads(value_str)
        
            if first_time is None:
                first_time = dt
                first_position = position
        
            if dt >= add_minutes(first_time, minutes_to_add):
                last_time = dt
                last_position = position
                break

    # If we didn't find a matching end time, use the last row
    if last_time is None:
        last_time = dt
        last_position = position

    # Calculate the distance
    distance = haversine_distance(
        first_position['lat'], first_position['lon'],
        last_position['lat'], last_position['lon']
    )

    # Calculate time difference in minutes
    time_diff = (last_time - first_time).total_seconds() / 60

    # Calculate calories burned
    calories_burned = calculate_calories_burned(weight_kg, distance, time_diff)
    
    if request.method == 'POST':
        return redirect(url_for("result", calories_burned = calories_burned, distance = distance, time_diff = time_diff ))
    else:
        return redirect(url_for("input"))



@app.route('/result/<calories_burned>/<distance>/<time_diff>')
def result(calories_burned, distance, time_diff):
    """Renders the about page."""
    return render_template(
        'result.html',calories_burned = calories_burned, distance = distance, time_diff = time_diff, 
        title='result',
        year=datetime.now().year,
        message='Your application description page.'
    )
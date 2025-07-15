from flask import Flask, render_template, request, redirect, flash
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flashing messages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/consult', methods=['GET', 'POST'])
def consult():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        message = request.form.get('message')

        if not name or not email or not date:
            flash('Please fill out all required fields.')
            return redirect('/consult')

        # Save to CSV
        with open('form_data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, email, date, message])

        flash('Your consultation request has been submitted!')
        return redirect('/consult')
    
    return render_template('consult.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

mail = Mail(app)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultations.db'
db = SQLAlchemy(app)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date = db.Column(db.String(20))
    message = db.Column(db.Text)

# Create the table once
with app.app_context():
    db.create_all()

import requests

recaptcha_response = request.form['g-recaptcha-response']
verify_url = f"https://www.google.com/recaptcha/api/siteverify"
payload = {'secret': 'YOUR_SECRET_KEY', 'response': recaptcha_response}
response = requests.post(verify_url, data=payload)
result = response.json()

if not result.get('success'):
    flash('reCAPTCHA failed. Try again.')
    return redirect('/consult')

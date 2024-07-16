from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///climate_db2.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ClimateData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
class ClimateForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    temperature = StringField('Temperature (°C)', validators=[DataRequired()])
    humidity = StringField('Humidity (%)', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class ConferenceAttendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    
class ConferenceAttendeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

    
@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')
    

@app.route('/record_data', methods=['GET', 'POST'])
def record_data():
    form = ClimateForm()
    if form.validate_on_submit():
        location = form.location.data
        temperature = float(form.temperature.data)
        humidity = float(form.humidity.data)
        new_entry = ClimateData(location=location, temperature=temperature, humidity=humidity)
        db.session.add(new_entry)
        db.session.commit()
        flash('Data submitted successfully!', 'success')
        return redirect(url_for('climate_data'))
    return render_template('./record_data.html', form=form)

@app.route('/attend_conference', methods=['GET', 'POST'])
def attend_conference():
    form = ConferenceAttendeeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        new_entry = ConferenceAttendee(name=name, email=email)
        db.session.add(new_entry)
        db.session.commit()
        flash('Attendance submitted successfully!', 'success')
        return redirect(url_for('conference_attendee'))
    return render_template('./attend_conference.html', form=form)

@app.route('/data')
def climate_data():
    data = ClimateData.query.all()
    return render_template('data.html', data=data)

@app.route('/conference')
def conference_attendee():
    data = ConferenceAttendee.query.all()
    return render_template('conferece_attendees.html', data=data)



# @app.route('/secure')
# def secure_page():
#     # Implement secure page logic here
#     return 'Secure page content'


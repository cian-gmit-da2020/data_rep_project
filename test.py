from flask import Flask, render_template, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, Optional
from flask_bcrypt import Bcrypt
from datetime import datetime


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbtest.db'
app.config['SECRET_KEY'] = 'secretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RepMaxs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fiveRM = db.Column(db.Integer)
    fourRM = db.Column(db.Integer)
    threeRM = db.Column(db.Integer)
    twoRM = db.Column(db.Integer)
    oneRM = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


db.create_all()


class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username= username.data).first()
            
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please Choose a different username")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")

class logMaxs(FlaskForm):
    exercise = SelectField("Exercises", choices=[('Bench', 'Bench'), ('Squat', 'Squat'), 
    ('Deadlift', 'Deadlift')])
    fiveRM = IntegerField(render_kw={"placeholder": "5 RM"}, validators=[Optional()])
    fourRM = IntegerField(render_kw={"placeholder": "4 RM"}, validators=[Optional()])
    threeRM = IntegerField(render_kw={"placeholder": "3 RM"}, validators=[Optional()])
    twoRM = IntegerField(render_kw={"placeholder": "2 RM"}, validators=[Optional()])
    oneRM = IntegerField(render_kw={"placeholder": "1 RM"}, validators=[Optional()])

    submit = SubmitField("Submit")

class deleteRecord(FlaskForm):
    exercise = SelectField("Exercises", choices=[('Bench', 'Bench'), ('Squat', 'Squat'), 
    ('Deadlift', 'Deadlift')])
    #reps = SelectField("Reps No", choices=[("fiveRM", '5 RM'), ("fourRM", '4 RM'), 
    #("threeRM", '3 RM'), ("twoRM", '2 RM'), ("oneRM", '1 RM')])

    submit = SubmitField("Delete")

         

@app.route("/")
def home():
    return render_template("home.html")



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return  redirect(url_for('dashboard'))
    return render_template("login.html", form=form)



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route('/logMaxs',  methods=['GET', 'POST'])
@login_required
def logMaxsPage():
    form = logMaxs()
    if form.validate_on_submit():
        post = RepMaxs(exercise=form.exercise.data, fiveRM=form.fiveRM.data, fourRM=form.fourRM.data,
        threeRM=form.threeRM.data, twoRM=form.twoRM.data, oneRM=form.oneRM.data, user_id=current_user.get_id())
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('logMaxs.html', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    id = current_user.get_id()

    form = deleteRecord()
    if form.validate_on_submit():
        record = RepMaxs.query.filter_by(exercise=form.exercise.data,  user_id=id).delete()
        db.session.commit()

        return redirect(url_for('dashboard'))
    
    return render_template('delete.html', form=form)



@app.route('/dashboard',  methods=['GET', 'POST'])
@login_required
def dashboard():

    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    #squat = RepMaxs.query.filter_by(exercise='Squat', user_id=id).all()
    #deadlift = RepMaxs.query.filter_by(exercise='Deadlift', user_id=id).all()

    benchReturn = []
    
    bench = RepMaxs.query.filter_by(exercise='Bench', user_id=id).order_by(desc(RepMaxs.fiveRM)).first()
    if bench != None:
        benchReturn.append(bench.fiveRM)
    else: 
        benchReturn.append(None)
    bench = RepMaxs.query.filter_by(exercise='Bench', user_id=id).order_by(desc(RepMaxs.fourRM)).first()
    if bench != None:
        benchReturn.append(bench.fourRM)
    else: 
        benchReturn.append(None)
    bench = RepMaxs.query.filter_by(exercise='Bench', user_id=id).order_by(desc(RepMaxs.threeRM)).first()
    if bench != None:
        benchReturn.append(bench.threeRM)
    else: 
        benchReturn.append(None)
    bench = RepMaxs.query.filter_by(exercise='Bench', user_id=id).order_by(desc(RepMaxs.twoRM)).first()
    if bench != None:
        benchReturn.append(bench.twoRM)
    else: 
        benchReturn.append(None)
    bench = RepMaxs.query.filter_by(exercise='Bench', user_id=id).order_by(desc(RepMaxs.oneRM)).first()
    if bench != None:
        benchReturn.append(bench.oneRM)
    else: 
        benchReturn.append(None)

    squatReturn = []
    
    squat = RepMaxs.query.filter_by(exercise='Squat', user_id=id).order_by(desc(RepMaxs.fiveRM)).first()
    if squat != None:
        squatReturn.append(squat.fiveRM)
    else: 
        squatReturn.append(None)
    squat = RepMaxs.query.filter_by(exercise='Squat', user_id=id).order_by(desc(RepMaxs.fourRM)).first()
    if squat != None:
        squatReturn.append(squat.fourRM)
    else: 
        squatReturn.append(None)
    squat = RepMaxs.query.filter_by(exercise='Squat', user_id=id).order_by(desc(RepMaxs.threeRM)).first()
    if squat != None:
        squatReturn.append(squat.threeRM)
    else: 
        squatReturn.append(None)
    squat = RepMaxs.query.filter_by(exercise='Squat', user_id=id).order_by(desc(RepMaxs.twoRM)).first()
    if squat != None:
        squatReturn.append(squat.twoRM)
    else: 
        squatReturn.append(None)
    squat = RepMaxs.query.filter_by(exercise='Squat', user_id=id).order_by(desc(RepMaxs.oneRM)).first()
    if squat != None:
        squatReturn.append(squat.oneRM)
    else: 
        squatReturn.append(None)

    deadliftReturn = []
    
    deadlift = RepMaxs.query.filter_by(exercise='Deadlift', user_id=id).order_by(desc(RepMaxs.fiveRM)).first()
    if deadlift != None:
        deadliftReturn.append(deadlift.fiveRM)
    else: 
        deadliftReturn.append(None)
    deadlift = RepMaxs.query.filter_by(exercise='Deadlift', user_id=id).order_by(desc(RepMaxs.fourRM)).first()
    if deadlift != None:
        deadliftReturn.append(deadlift.fourRM)
    else: 
        deadliftReturn.append(None)
    deadlift = RepMaxs.query.filter_by(exercise='Deadlift', user_id=id).order_by(desc(RepMaxs.threeRM)).first()
    if deadlift != None:
        deadliftReturn.append(deadlift.threeRM)
    else: 
        deadliftReturn.append(None)
    deadlift = RepMaxs.query.filter_by(exercise='Deadlift', user_id=id).order_by(desc(RepMaxs.twoRM)).first()
    if deadlift != None:
        deadliftReturn.append(deadlift.twoRM)
    else: 
        deadliftReturn.append(None)
    deadlift = RepMaxs.query.filter_by(exercise='Deadlift', user_id=id).order_by(desc(RepMaxs.oneRM)).first()
    if deadlift != None:
        deadliftReturn.append(deadlift.oneRM)
    else: 
        deadliftReturn.append(None)

    return render_template('dash.html', user=user, bench=benchReturn, squat=squatReturn, deadlift=deadliftReturn)


if __name__ == "__main__":
    app.run(debug=True)
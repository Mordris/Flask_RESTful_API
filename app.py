import psycopg2
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from forms import LoginForm, RegistrationForm
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/Flask_RESTful_API_DB'

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Establish the PostgreSQL database connection
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="Flask_RESTful_API_DB",
    user="postgres",
    password="123456"
)

# Load the user object for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Routes and view functions
@app.route('/')
def index():
    return 'Welcome to the Flask Login Example'

@app.route('/register', methods=['GET', 'POST'])
def register():
    from models import User

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Create a new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from models import User

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            # Log in the user
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    from models import User

    # Log out the user
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)

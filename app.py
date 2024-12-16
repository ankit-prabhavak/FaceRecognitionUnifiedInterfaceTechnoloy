
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
import face_recognition
import numpy as np
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image
from scipy.spatial.distance import cosine  # For face encoding comparison

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for session management

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'users.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure image upload folder
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    face_encoding = db.Column(db.PickleType, nullable=True)  # Store face encoding


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        branch = request.form['branch']
        roll_number = request.form['roll_number']
        address = request.form['address']
        image_data = request.form['image_data']  # For webcam capture

        if image_data:
            # Convert base64 image data to image
            image_data = image_data.split(',')[1]  # Remove "data:image/png;base64,"
            image_data = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_data))

            # Save image to disk
            filename = secure_filename(f"{username}_profile.png")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)

            # Process face encoding
            image = face_recognition.load_image_file(filepath)
            face_encoding = face_recognition.face_encodings(image)

            if face_encoding:
                face_encoding = face_encoding[0]  # Get the first face encoding
            else:
                return "No face detected. Please try again with a clearer image."

            # Check if username already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return "Username already taken. Please choose a different username."

            # Create a new user with the face encoding (convert to list for Pickle)
            new_user = User(username=username, password=password, name=name, branch=branch, 
                            roll_number=roll_number, address=address, face_encoding=face_encoding.tolist())
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if the request contains the 'username' and 'password' fields for credential login
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('welcome'))

        # Check if the request contains 'image_data' for face login
        elif 'image_data' in request.form:
            image_data = request.form['image_data']

            if image_data:
                # Process the base64-encoded image
                image_data = image_data.split(',')[1]  # Remove the base64 prefix
                image_data = base64.b64decode(image_data)

                # Convert image data to a file-like object for face_recognition
                image = face_recognition.load_image_file(BytesIO(image_data))  # Pass byte stream to load_image_file
                face_encoding = face_recognition.face_encodings(image)

                if face_encoding:
                    face_encoding = face_encoding[0]  # Get the first face encoding
                    users = User.query.all()  # Get all users
                    for u in users:
                        if u.face_encoding is not None:
                            # Convert stored encoding to numpy array
                            stored_encoding = np.array(u.face_encoding)
                            # Compare using cosine distance (lower value means closer match)
                            distance = cosine(stored_encoding, face_encoding)
                            if distance < 0.06:  # Threshold for comparison 0.6
                                session['user_id'] = u.id
                                return redirect(url_for('welcome'))

                    # If no match was found, display an error
                    return "User not registered or face mismatch"

        # If we reach here, no valid login method was used
        return "Invalid login method or data."

    return render_template('login.html')

# Route for welcome page
@app.route('/welcome')
def welcome():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login if user is not authenticated

    user = User.query.get(user_id)
    return render_template('welcome.html', user=user)


# Logout route to clear session
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Clear the session
    return render_template('logout.html')
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)

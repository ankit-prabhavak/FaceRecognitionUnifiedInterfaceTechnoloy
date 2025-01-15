# Project Details: Flask Authentication with Face Recognition

## Overview
This Flask application offers a flexible and secure user authentication system. It supports two types of login methods: traditional username/password authentication and a more innovative face recognition system using webcam images. The system integrates both methods to provide users with multiple ways to securely access the platform.

## Features
- **User Registration**: Users can register by entering personal details and uploading a profile image. The image is processed for face recognition.
- **Two Login Methods**:
  - **Username/Password Login**: Users can log in using traditional credentials.
  - **Face Recognition Login**: Users can log in by submitting a webcam image for face recognition.
- **Face Recognition**: Uses the `face_recognition` library to generate unique face encodings, ensuring secure identification.
- **Session Management**: Secure session handling to keep users logged in across pages and ensure secure logouts.
- **Image Handling**: Proper security measures to sanitize and restrict image uploads.

## Project Structure
FRUITS/<br>
├── instance/<br>
│   └── users.db<br>
├── static/<br>
│   ├── images/<br>
│   ├── js/<br>
│   ├── Home.css<br>
│   ├── Login.css<br>
│   ├── RegisterPage.css<br>
│   ├── Logout.css<br>
│   ├── Welcome.css<br>
│   ├── Logo.jpg<br>
│   └── TitleLogo.ico<br>
├── templates/<br>
│   ├── home.html<br>
│   ├── login.html<br>
│   ├── logout.html<br>
│   ├── register.html<br>
│   └── welcome.html<br>
├── app.py<br>
├── local.py<br>
├── requirements.txt<br>
├── README.md<br>
└── venv/<br>


## Requirements
- **Flask**: Lightweight WSGI web application framework.
- **face_recognition**: A Python library for face recognition, which leverages dlib.
- **SQLAlchemy**: ORM for interacting with the SQLite database.
- **Werkzeug**: Provides utilities like `secure_filename` for file uploads.

You can install the necessary dependencies by running:


## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/flask-face-recognition-auth.git
    cd flask-face-recognition-auth
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Flask app**:
    ```bash
    python app.py
    ```

The app should now be running at `http://127.0.0.1:5000`.

## Application Flow

### 1. User Registration
- When a new user registers:
  - They enter personal information (username, password, name, etc.).
  - A profile picture is captured via webcam.
  - The image is processed to generate a face encoding using the `face_recognition` library.
  - The face encoding (a unique 128-dimensional vector) is saved in the database along with other user details.

### 2. User Login
- **Username/Password Login**:
  - The user enters their username and password.
  - The app checks the database for matching credentials. If successful, the user is logged in and redirected to the welcome page.
- **Face Recognition Login**:
  - The user submits an image captured via their webcam.
  - The app generates a face encoding from the captured image and compares it with the stored encodings in the database.
  - If a match is found (based on cosine similarity), the user is logged in and redirected to the welcome page.

### 3. Face Recognition and Cosine Similarity
- The app uses `face_recognition` to generate a unique face encoding for each user.
- During login, the face encoding of the captured image is compared to stored encodings using cosine similarity.
- A match is considered valid if the cosine distance between the two encodings is below a threshold (e.g., 0.8).

### 4. Image Handling and Security
- Profile images are uploaded and saved to the `static/images/` folder.
- **Sanitizing filenames**: We use `secure_filename()` from `Werkzeug` to ensure that file names are safe and free from malicious elements.
- **Allowed file types**: Only PNG, JPG, and JPEG images are accepted to prevent harmful file uploads.

### 5. Session Management and Logout
- After successful login, the user’s session is maintained using Flask’s session management.
- On logout, the session is cleared to ensure no sensitive data remains accessible.

### 6. Database and Models
- The user data, including face encodings, are stored in an SQLite database using SQLAlchemy.
- The **User** model defines the structure of the database, with fields such as username, password, and face_encoding.
- **Face Encoding** is stored as a serialized object (PickleType), allowing easy retrieval and comparison.

## Security Measures
- **Sanitizing File Names**: All uploaded images are sanitized using `secure_filename` to avoid malicious file uploads.
- **Restricting File Types**: Only PNG, JPG, and JPEG file formats are allowed.
- **Session Management**: The app ensures secure login sessions and clear logout procedures, protecting against unauthorized access.

## Conclusion
This Flask app offers a versatile authentication system by combining both traditional username/password login and modern face recognition. By utilizing Flask’s session management and securing the image upload process, we ensure both user convenience and security.

## Future Improvements
- Integrate email verification during registration.
- Implement more advanced face recognition algorithms for higher accuracy.
- Support multi-factor authentication (MFA) for enhanced security.

**NOTE**:  
For setting the cosine similarity, use the `local.py` file to determine the supported threshold on your device's webcam and update that in `app.py`.


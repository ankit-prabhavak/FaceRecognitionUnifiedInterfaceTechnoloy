import face_recognition
import numpy as np
from scipy.spatial.distance import cosine

# Example paths to your images
image_path_1 = "C:/Users/ankit/OneDrive/Pictures/Camera Roll/kavy1.jpg"
image_path_2 = "C:/Users/ankit/OneDrive/Pictures/Camera Roll/kavy2.jpg"

# Load images and get their face encodings
image_1 = face_recognition.load_image_file(image_path_1)
image_2 = face_recognition.load_image_file(image_path_2)

# Get face encodings (there should be exactly one face per image)
encoding_1 = face_recognition.face_encodings(image_1)[0]
encoding_2 = face_recognition.face_encodings(image_2)[0]

# Compute the cosine distance between the two face encodings
distance = cosine(encoding_1, encoding_2)

print(f"Cosine distance between the faces: {distance}")

import face_recognition # type: ignore
import cv2
import numpy as np
import os
from pathlib import Path

class FaceDetector:
    def __init__(self, known_faces_dir):
        """
        Initialize the face detector with known faces
        Args:
            known_faces_dir: Directory containing folders with known person's faces
        """
        self.known_faces_dir = known_faces_dir
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load and encode all known faces from the directory"""
        for person_name in os.listdir(self.known_faces_dir):
            person_dir = os.path.join(self.known_faces_dir, person_name)
            
            if not os.path.isdir(person_dir):
                continue
            
            for image_name in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_name)
                
                try:
                    # Load image
                    image = face_recognition.load_image_file(image_path)
                    
                    # Get face encodings
                    face_encodings = face_recognition.face_encodings(image)
                    
                    for face_encoding in face_encodings:
                        self.known_face_encodings.append(face_encoding)
                        self.known_face_names.append(person_name)
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")
        
        print(f"✓ Loaded {len(self.known_face_encodings)} face encodings")
    
    def recognize_faces(self, frame):
        """
        Detect and recognize faces in a frame
        Args:
            frame: Image frame from video/camera
        
        Returns:
            List of recognized face information
        """
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        face_distances = []
        
        for face_encoding in face_encodings:
            # Compare with known faces
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding, 
                tolerance=0.6
            )
            name = "Unknown"
            distance = 1.0
            
            # Use face distance to determine best match
            face_distances_array = face_recognition.face_distance(
                self.known_face_encodings, 
                face_encoding
            )
            
            if len(face_distances_array) > 0:
                best_match_index = np.argmin(face_distances_array)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    distance = face_distances_array[best_match_index]
            
            face_names.append(name)
            face_distances.append(distance)
        
        return face_locations, face_names, face_distances
import cv2
import csv
import os
from datetime import datetime
from face_detector import FaceDetector
import pandas as pd

class AttendanceSystem:
    def __init__(self, known_faces_dir, attendance_file="attendance/attendance.csv"):
        """
        Initialize the attendance system
        Args:
            known_faces_dir: Directory with known faces
            attendance_file: CSV file to store attendance records
        """
        self.face_detector = FaceDetector(known_faces_dir)
        self.attendance_file = attendance_file
        self.marked_today = set()
        self.ensure_attendance_file()
    
    def ensure_attendance_file(self):
        """Create attendance file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.attendance_file), exist_ok=True)
        
        if not os.path.exists(self.attendance_file):
            with open(self.attendance_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Date', 'Time', 'Status'])
    
    def mark_attendance(self, name):
        """
        Mark attendance for a person
        Args:
            name: Name of the person
        """
        if name == "Unknown":
            return
        
        # Avoid marking same person multiple times in a short period
        if name in self.marked_today:
            return
        
        current_datetime = datetime.now()
        date = current_datetime.strftime("%Y-%m-%d")
        time = current_datetime.strftime("%H:%M:%S")
        
        with open(self.attendance_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, date, time, 'Present'])
        
        self.marked_today.add(name)
        print(f"✓ Attendance marked for {name} at {time}")
    
    def reset_daily_attendance(self):
        """Reset attendance tracking for a new day"""
        self.marked_today.clear()
    
    def get_attendance_report(self, date=None):
        """
        Get attendance report for a specific date
        Args:
            date: Date in format YYYY-MM-DD (defaults to today)
        
        Returns:
            DataFrame with attendance records
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if not os.path.exists(self.attendance_file):
            return None
        
        df = pd.read_csv(self.attendance_file)
        return df[df['Date'] == date]
    
    def run_camera(self, camera_id=0):
        """
        Run the attendance system using webcam
        Args:
            camera_id: Camera device ID (usually 0 for default camera)
        """
        video_capture = cv2.VideoCapture(camera_id)
        
        if not video_capture.isOpened():
            print("❌ Error: Cannot access camera")
            return
        
        # Set camera resolution
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("=" * 50)
        print("✓ Face Detection Attendance System Started")
        print("=" * 50)
        print("Controls:")
        print("  'q' - Quit application")
        print("  'r' - Reset daily attendance")
        print("  'p' - Print today's attendance")
        print("=" * 50)
        
        frame_count = 0
        
        while True:
            ret, frame = video_capture.read()
            
            if not ret:
                print("❌ Error reading frame from camera")
                break
            
            frame_count += 1
            
            # Detect and recognize faces (process every other frame for performance)
            if frame_count % 2 == 0:
                face_locations, face_names, face_distances = self.face_detector.recognize_faces(frame)
                
                # Draw results on frame
                for (top, right, bottom, left), name, distance in zip(
                    face_locations, face_names, face_distances
                ):
                    # Scale back up face locations
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    
                    # Determine color based on recognition
                    if name == "Unknown":
                        color = (0, 0, 255)  # Red for unknown
                    else:
                        color = (0, 255, 0)  # Green for known
                        self.mark_attendance(name)
                    
                    # Draw box
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    
                    # Draw label
                    label = f"{name} ({distance:.2f})"
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                    cv2.putText(
                        frame, label, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1
                    )
            
            # Add info text
            cv2.putText(frame, "Press 'q' to quit, 'r' to reset, 'p' for report", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow("Face Detection Attendance System", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n✓ Exiting application...")
                break
            elif key == ord('r'):
                self.reset_daily_attendance()
                print("✓ Daily attendance reset")
            elif key == ord('p'):
                report = self.get_attendance_report()
                if report is not None and len(report) > 0:
                    print("\n📋 Today's Attendance Report:")
                    print(report.to_string())
                else:
                    print("\n📋 No attendance records for today")
        
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create attendance system
    system = AttendanceSystem(known_faces_dir="known_faces")
    
    # Run with camera
    system.run_camera()
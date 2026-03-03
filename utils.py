import os
import cv2

def capture_face_images(person_name, known_faces_dir="known_faces", num_images=10):
    """
    Capture face images for a new person
    Args:
        person_name: Name of the person
        known_faces_dir: Directory to store faces
        num_images: Number of images to capture
    """
    person_dir = os.path.join(known_faces_dir, person_name)
    os.makedirs(person_dir, exist_ok=True)
    
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        print("❌ Error: Cannot access camera")
        return
    
    print(f"\n📷 Capturing {num_images} images for {person_name}")
    print("Instructions:")
    print("  'c' - Capture image")
    print("  'q' - Quit capture")
    print("\nTip: Try different angles and lighting conditions\n")
    
    count = 0
    
    while count < num_images:
        ret, frame = video_capture.read()
        
        if not ret:
            print("❌ Error reading frame")
            break
        
        # Add counter text
        cv2.putText(frame, f"Images captured: {count}/{num_images}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'c' to capture, 'q' to quit", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow(f"Capture Face - {person_name}", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            filename = os.path.join(person_dir, f"{person_name}_{count}.jpg")
            cv2.imwrite(filename, frame)
            print(f"✓ Captured image {count + 1}/{num_images}")
            count += 1
        elif key == ord('q'):
            print("Capture cancelled")
            break
    
    video_capture.release()
    cv2.destroyAllWindows()
    
    if count == num_images:
        print(f"✓ Successfully captured {num_images} images for {person_name}\n")

def list_known_faces(known_faces_dir="known_faces"):
    """List all registered people"""
    if not os.path.exists(known_faces_dir):
        print("No known_faces directory found")
        return
    
    people = [p for p in os.listdir(known_faces_dir) 
              if os.path.isdir(os.path.join(known_faces_dir, p))]
    
    if not people:
        print("No registered people found")
        return
    
    print("\n👥 Registered People:")
    for i, person in enumerate(people, 1):
        person_dir = os.path.join(known_faces_dir, person)
        num_images = len(os.listdir(person_dir))
        print(f"  {i}. {person} ({num_images} images)")
    print()
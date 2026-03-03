"""
Setup script to easily add new people to the attendance system
Run this script to capture faces for new people
"""

from utils import capture_face_images, list_known_faces

def main():
    while True:
        print("\n" + "="*50)
        print("👤 Face Capture Setup")
        print("="*50)
        print("1. Capture new person")
        print("2. List registered people")
        print("3. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            person_name = input("Enter person's name: ").strip()
            if person_name:
                num_images = input("Number of images to capture (default 10): ").strip()
                num_images = int(num_images) if num_images.isdigit() else 10
                capture_face_images(person_name, num_images=num_images)
            else:
                print("❌ Name cannot be empty")
        
        elif choice == "2":
            list_known_faces()
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("❌ Invalid choice, please try again")

if __name__ == "__main__":
    main()
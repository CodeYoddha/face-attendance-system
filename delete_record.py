"""
Script to delete attendance records for a person
"""

import os
import pandas as pd

def delete_attendance_record(person_name, attendance_file="attendance/attendance.csv"):
    """
    Delete all attendance records for a person
    Args:
        person_name: Name of the person
        attendance_file: Path to attendance CSV file
    """
    if not os.path.exists(attendance_file):
        print("❌ Attendance file not found")
        return
    
    try:
        # Read the CSV file
        df = pd.read_csv(attendance_file)
        
        # Count records before deletion
        records_before = len(df[df['Name'] == person_name])
        
        if records_before == 0:
            print(f"❌ No records found for {person_name}")
            return
        
        # Remove records for this person
        df = df[df['Name'] != person_name]
        
        # Save back to CSV
        df.to_csv(attendance_file, index=False)
        
        print(f"✓ Deleted {records_before} record(s) for {person_name}")
        print(f"✓ Remaining records: {len(df)}")
    
    except Exception as e:
        print(f"❌ Error deleting records: {e}")

def delete_face_images(person_name, known_faces_dir="known_faces"):
    """
    Delete face images for a person
    Args:
        person_name: Name of the person
        known_faces_dir: Directory containing faces
    """
    person_dir = os.path.join(known_faces_dir, person_name)
    
    if not os.path.exists(person_dir):
        print(f"❌ No face directory found for {person_name}")
        return
    
    try:
        import shutil
        shutil.rmtree(person_dir)
        print(f"✓ Deleted all face images for {person_name}")
    except Exception as e:
        print(f"❌ Error deleting faces: {e}")

def delete_person_completely(person_name):
    """
    Delete a person completely (attendance records + face images)
    Args:
        person_name: Name of the person
    """
    print(f"\n🗑️  Deleting all data for {person_name}...")
    delete_attendance_record(person_name)
    delete_face_images(person_name)
    print(f"✓ {person_name} has been completely removed\n")

if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        print("🗑️  Delete Records")
        print("="*50)
        print("1. Delete attendance records only")
        print("2. Delete face images only")
        print("3. Delete person completely (records + images)")
        print("4. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            person_name = input("Enter person's name: ").strip()
            if person_name:
                delete_attendance_record(person_name)
            else:
                print("❌ Name cannot be empty")
        
        elif choice == "2":
            person_name = input("Enter person's name: ").strip()
            if person_name:
                delete_face_images(person_name)
            else:
                print("❌ Name cannot be empty")
        
        elif choice == "3":
            person_name = input("Enter person's name: ").strip()
            if person_name:
                confirm = input(f"Are you sure you want to delete ALL data for {person_name}? (yes/no): ").strip().lower()
                if confirm == "yes":
                    delete_person_completely(person_name)
                else:
                    print("❌ Deletion cancelled")
            else:
                print("❌ Name cannot be empty")
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("❌ Invalid choice, please try again")
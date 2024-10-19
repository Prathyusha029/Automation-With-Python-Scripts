import os
import pandas as pd
import shutil
from datetime import datetime

# Step 1: Identify all CSV files in the folder
def get_csv_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.csv')]

# Step 2: Clean the CSV files (remove duplicates and handle missing values)
def clean_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df_cleaned = df.drop_duplicates()  
        df_cleaned.ffill(inplace=True) 
        return df_cleaned
    except Exception as e:
        print(f"An error occurred while cleaning {file_path}: {e}")
        return None

# Step 3: Save cleaned files into a new directory
def save_cleaned_data(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

# Step 4: Organize files by archiving raw files after processing
def move_to_archive(file_path, archive_directory):
    if not os.path.exists(archive_directory):
        os.makedirs(archive_directory)  
    shutil.move(file_path, os.path.join(archive_directory, os.path.basename(file_path)))
    print(f"Moved {file_path} to {archive_directory}")

# Step 5: System maintenance - Clean up old logs or files
def delete_old_files(directory, days=30):
    now = datetime.now()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        file_age = now - datetime.fromtimestamp(os.path.getmtime(file_path))
        if file_age.days > days:
            os.remove(file_path)
            print(f"Deleted old file: {file_path}")

# Step 6: Unarchive files (Move files back from archive to the original folder)
def unarchive_files(archive_directory, destination_directory):
    if not os.path.exists(archive_directory):
        print(f"Archive directory {archive_directory} does not exist.")
        return
    
    for file_name in os.listdir(archive_directory):
        archived_file_path = os.path.join(archive_directory, file_name)
        destination_path = os.path.join(destination_directory, file_name)
        shutil.move(archived_file_path, destination_path)
        print(f"Moved {archived_file_path} back to {destination_directory}")

def automate_data_cleaning(input_directory, output_directory, archive_directory, unarchive=False):
    if unarchive:
        # Step 7: Unarchive files before starting cleaning
        unarchive_files(archive_directory, input_directory)
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory) 
    csv_files = get_csv_files(input_directory)
    
    for file_name in csv_files:
        input_path = os.path.join(input_directory, file_name)
        df_cleaned = clean_data(input_path)
        
        if df_cleaned is not None:
            output_path = os.path.join(output_directory, file_name)
            save_cleaned_data(df_cleaned, output_path)
            move_to_archive(input_path, archive_directory)  

    # Perform system maintenance by deleting files older than 30 days in the archive
    delete_old_files(archive_directory, days=30)

if __name__ == "__main__":
    input_directory = r"C:\Users\Yekam\OneDrive\Desktop\Task4\example\path\csv"  
    output_directory = r"C:\Users\Yekam\OneDrive\Desktop\Task4\cleaned_files"  
    archive_directory = r"C:\Users\Yekam\OneDrive\Desktop\Task4\archive"  

    automate_data_cleaning(input_directory, output_directory, archive_directory, unarchive=True)

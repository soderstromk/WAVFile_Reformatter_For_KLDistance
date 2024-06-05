import os
from datetime import datetime
from collections import defaultdict
from tkinter import Tk, filedialog

def get_modified_time(file_path):
    return os.path.getmtime(file_path)

def determine_day_range(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith('.wav')]

    if not files:
        return None, None, None

    modified_dates = [datetime.fromtimestamp(get_modified_time(os.path.join(folder_path, f))).date() for f in files]
    earliest_date = min(modified_dates)
    latest_date = max(modified_dates)
    relative_days = [(modified_date - earliest_date).days + 1 for modified_date in modified_dates]

    return earliest_date, latest_date, relative_days

def rename_files_by_modified_date(folder_path, bird_id):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith('.wav')]

    if not files:
        print("No .wav files found in the folder")
        return

    files.sort(key=lambda f: get_modified_time(os.path.join(folder_path, f)))

    day_file_dict = defaultdict(list)
    first_file_modified_time = get_modified_time(os.path.join(folder_path, files[0]))
    first_file_modified_date = datetime.fromtimestamp(first_file_modified_time).date()

    for file in files:
        file_path = os.path.join(folder_path, file)
        modified_time = get_modified_time(file_path)
        modified_date = datetime.fromtimestamp(modified_time).date()

        relative_day = str((modified_date - first_file_modified_date).days + 1)

        day_file_dict[relative_day].append(file)

    for day, files in day_file_dict.items():
        files.sort(key=lambda f: get_modified_time(os.path.join(folder_path, f)))
        for index, file in enumerate(files, start=1):
            new_name = f"{bird_id}_{int(day):02}_{index:05}.wav"
            while os.path.exists(os.path.join(folder_path, new_name)):
                index += 1
                new_name = f"{bird_id}_{int(day):02}_{index:05}.wav"
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed '{file}' to '{new_name}'")

def select_folder():
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path

if __name__ == "__main__":
    print("Welcome to the Bird Audio File Renamer!")
    print("This script will rename your .wav files based on their modification date.")
    folder_path = select_folder()
    if folder_path:
        bird_id = input("Enter Bird ID: ")
        earliest_date, latest_date, relative_days = determine_day_range(folder_path)
        if earliest_date and latest_date:
            print(f"Earliest date: {earliest_date}")
            print(f"Latest date: {latest_date}")
            print(f"Relative days: {relative_days}")
        rename_files_by_modified_date(folder_path, bird_id)
    else:
        print("No folder selected")

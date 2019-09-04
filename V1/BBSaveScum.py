import glob
import os
import time
import datetime

# Change the path of your folders with \\ as separator
savegame_path = "D:\\Users\\Admin\\Documents\\Battle Brothers\\savegames"
savescum_path = "D:\\Users\\Admin\\Documents\\Battle Brothers\\SaveScum Backups"
# Savegame file extension. Usually its sav
ext = "sav" 
# Save copy interval, in minutes
interval = 1
maxsaves = 30

# Initialization. Do not modify
saved_date = 0
savescum_counter = 0

# Create savescum path if it does not exist
if not os.path.isdir(savescum_path):
    os.mkdir(savescum_path)
    print("Created Folder" + savescum_path)

# Main
    
while True:

    savegames = glob.glob(savegame_path + "\\*." + ext)
    modification_time = []

    for savegame in savegames:
        modification_time.append(os.path.getmtime(savegame))

    latest_save = savegames[modification_time.index(max(modification_time))]
    latest_date = max(modification_time)
    latest_size = os.path.getsize(latest_save)

    file_name = latest_save.replace("." + ext, "").split("\\")[-1]
    folder_path = savescum_path + "\\" + file_name

    checkgames = glob.glob(folder_path + "\\*." + ext)
    savescum_mod_time = [0]
    
    for savegame in checkgames:
        savescum_mod_time.append(os.path.getmtime(savegame))
        savescum_counter+=1

    check_save = checkgames[savescum_mod_time.index(max(savescum_mod_time))-1] #-1 is required because how lists positions work in python
    check_date = max(savescum_mod_time)
    check_size = os.path.getsize(check_save)

    if savescum_counter > maxsaves:
        file_deleted = checkgames[savescum_mod_time.index(min(savescum_mod_time))]
        if os.path.isfile(file_deleted):
            os.remove(file_deleted)
            print("Deleted "+ file_deleted )

    if latest_date > check_date or latest_size != check_size:
            
        file_name = latest_save.replace("." + ext, "").split("\\")[-1]
        folder_path = savescum_path + "\\" + file_name

        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
            print("Created Folder" + folder_path)
            
        new_save = str(datetime.datetime.now().replace(microsecond=0).isoformat('.')).replace(":", ".")

        with open(latest_save, "rb") as save:
            with open(folder_path + "\\" + new_save + "." + file_name + "." + ext, "wb") as copy_save:
                copy_save.write(save.read())

        print("Created Backup", new_save) #.split("\\")[-1])
        
    else:
        
        print("No new Savegames")

    time.sleep(interval * 10)
    savescum_counter = 0


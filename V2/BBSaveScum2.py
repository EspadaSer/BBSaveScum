import glob
import os
import time
import datetime
import configparser

#Config file exists
config = configparser.RawConfigParser()
configFilePath = r'config.txt'

if not os.path.isfile(configFilePath):
    config['Settings'] = {'game_savegame_path' : 'D:\\Users\\Admin\\Documents\\Battle Brothers\\savegames',
                          'backup_path' : 'D:\\Users\\Admin\\Documents\\Battle Brothers\\SaveScum Backups',
                          'extension' : 'sav',
                          'interval_minutes' : '1',
                          'maximum_saves' : '30'}
    config.write(open('config.txt', 'w'))
    print("Config.txt not found. File created. Setup the file and run the program again")

if os.path.isfile(configFilePath):

    config.read(configFilePath)
    savegame_path = config.get('Settings', 'game_savegame_path')
    savescum_path = config.get('Settings', 'backup_path')
    ext = config.get('Settings', 'extension')
    interval = int(config.get('Settings', 'interval_minutes'))
    maxsaves = int(config.get('Settings', 'maximum_saves'))

# Initialization. Do not modify
saved_date = 0
savescum_counter = 0

# Create savesgame path if it does not exist
if not os.path.isdir(savegame_path):
    print("game_savegame_path does not exist. Change the path on config.txt and restart this program")
    input("Press ENTER to terminate this program")
    raise SystemExit(0)
    
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

    check_save = checkgames[savescum_mod_time.index(max(savescum_mod_time))-1]
    #-1 is required because how lists positions work in python
    check_date = max(savescum_mod_time)
    check_size = os.path.getsize(check_save)

    if maxsaves > 0 and savescum_counter > maxsaves:
        file_deleted = checkgames[savescum_mod_time.index(min(savescum_mod_time))]
        if os.path.isfile(file_deleted):
            os.remove(file_deleted)
            print("Deleted " + file_deleted)

    if latest_date > check_date or latest_size != check_size:
            
        file_name = latest_save.replace("." + ext, "").split("\\")[-1]
        folder_path = savescum_path + "\\" + file_name

        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
            print("Created Folder" + folder_path)
            
        timestamp = str(datetime.datetime.now().replace(microsecond=0).isoformat('.')).replace(":", "").replace("-", "").replace(".", "_")

        with open(latest_save, "rb") as save:
            with open(folder_path + "\\" + timestamp + "_" + file_name + "." + ext, "wb") as copy_save:
                copy_save.write(save.read())

        print("Created Backup", timestamp) #.split("\\")[-1])
        
    else:
        
        print("No new Savegames")

    time.sleep(interval * 60)
    savescum_counter = 0


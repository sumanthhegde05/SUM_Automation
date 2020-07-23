import errno, os, stat, shutil


path_to_dir  = 'C:\\Users\\Administrator\\AppData\\Local\\sum'  # path to directory you wish to remove
files_in_dir = os.listdir(path_to_dir)     # get list of files in the directory

for file in files_in_dir:                  # loop to delete each file in folder
    try:
        print(file)
        shutil.rmtree(path_to_dir+'\\'+file)
    except:
        continue
try:
    shutil.rmtree('C:\\Users\\Administrator\\AppData\\Local\\localsum')
except Exception:
    pass

try:
    shutil.rmtree('C:\\cpqsystem')
except Exception:
    pass


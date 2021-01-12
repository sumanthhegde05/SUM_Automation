
import errno, os, stat, shutil
import sys,time
def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

def clearall():
    try:
        os.system("taskkill /IM sum_service_x64.exe /f")
    except:
        pass
    try:
        os.system("taskkill /IM gatherlogs_x64.exe /f")
    except:
        pass
    time.sleep(5)
    '''try:
        os.system("taskkill /IM cmd.exe /f")
    except:
        pass'''


'''def clear_cmd():
    try:
        os.system("taskkill /IM cmd.exe /f > nul")
    except:
        pass'''

        #try:
            #os.chmod(first+'\\gatherlogs_x64.exe', stat.S_IWRITE)
        #except:
            #break
        #try:
            #os.chmod(first, stat.S_IWRITE)
            #shutil.rmtree(first, ignore_errors=False, onerror=handleRemoveReadonly)
        #except:
            #pass
def clear_log(first):
    path_to_dir  = first  # path to directory you wish to remove
    files_in_dir = os.listdir(path_to_dir)   
    for file in files_in_dir:                  # loop to delete each file in folder
        try:
            print(file)
            os.remove(path_to_dir+'\\'+file)
            shutil.rmtree(path_to_dir+'\\'+file)
        except:
            continue

    
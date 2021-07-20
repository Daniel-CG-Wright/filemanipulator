#This is the __init__ file for the filemanipulator package.
#Run it as the main script to replenish the README.txt file,
#and update the software (if it is available)
from update_check import checkForUpdates
from os.path import join as osjoin
from os import getcwd
import filemanipulator

pagelink = "https://raw.githubusercontent.com/Daniel-CG-Wright/File-manipulator-python-module-Py-3.9-/main/filemanipulator/filemanipulator.py"
updatepath = osjoin(getcwd(), "filemanipulator.py")

#Set this to True to have the module automatically update whenever it is
#imported, if an update is available.
autoupdates = False

if autoupdates == True:
    

    checkForUpdates(updatepath, pagelink)
    
if __name__ == "__main__":

    with open("README.txt", "w+", encoding="utf-8") as rm:

        rm.write("""Welcome to filemanipulator, a small module built to aid with some file operations which may be useful.
It's a simple module, but can sometimes come in useful, particularly with file management.

To update to the latest version, either set 'autoupdates' in the __init__.py file to True, for the module
to automatically update whenver a new version is available on GitHub, or run the __init__.py file as its own
script, triggering an automatic update.

Please ensure file editing permissions are granted to Python for this module to work properly.
""")

    check = checkForUpdates(updatepath, pagelink)




    if check:
        print("filemanipulator.py was updated to the latest version.")
    
    else:

        print("No updates found for filemanipulator.py")




    
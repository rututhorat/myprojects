import os #used to interact with files and folders.
import shutil #used to move or copy files.

path=input("Enter your path: ") #Asks the user to enter a folder path where the files are located.

files = os.listdir(path)#gives a list of all files and folders inside the given path.
#Here, files will store all the file names.

for file in files:                                  #os.path.splitext(file) → splits the file into name and extension.
                                                    #Example: "example.txt" → ("example", ".txt")
    filename,extension=os.path.splitext(file)       
    extension = extension[1:]                       #extension[1:] → removes the dot (.)
                                                    #Example: ".txt" → "txt"

    

    if os.path.exists(path+'/'+extension):                             #Checks if a folder with the same name as the extension already exists.
        shutil.move(path+'/'+file,path+'/'+extension+'/'+file)         #Example: if the file is "photo.jpg", it checks for a folder "jpg" inside the path.
    else:                                                              #If the folder exists → move the file into that folder.
        os.makedirs(path+'/'+extension)                                #If the folder does not exist → first create the folder, then move the file there.
        shutil.move(path+'/'+file,path+'/'+extension+'/'+file)

print("✅ Files organized successfully!")
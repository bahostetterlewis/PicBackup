import os
import re
import time
import shutil

#############################################################################################
#                                     CONSTANTS                                             #
#                                    DON'T MODIFY                                           #
#############################################################################################
#This string will match any file extension for an image (at least I think I got them all)
#NOTE - It only matches lowercase so be sure to make all extensions lowercase before 
#attempting a match
IMAGE_MATCH_STRING = "^((jpe?g)|(bmp)|(img)|(dds)|(dng)|(gif)|(png)|(psd)|(pspimage)|(tga)|(thm)|(tif)|(yuv))$"
#This matches most valid months - DOES NOT acct for number of days in a month
#only allows months 1-12, and dates 1
DATE_MATCH = "(\d\d-){2}(\d){4}"
#get the users desktop
#this is probably platform independant - as long as they have a desktop
DESTINATION_PATH = os.path.join(os.getcwd(), "My Pictures")
#############################################################################################
#                                   END CONSTANTS                                           #
#############################################################################################

## main program entry point
def Main():                           
  currentDirectory = os.getcwd()

  #walk over the directories
  for root, dirs, files in os.walk(currentDirectory):
    for file in files:#get all files in the current directory
      fileExtension = str.split(file, '.')[-1]

      if re.match(IMAGE_MATCH_STRING, fileExtension.lower()):
        filePath = os.path.join(root, file)

        if re.search(DATE_MATCH, str(filePath)):#if we are in a folder that is already organized skip
          continue

        #file name will have the following structure
        #originalFileName '_' The day abbreviation Mon-Day-Year (all as numbers) Hour;Minute;Second from a 24 hour clock - all times/dates are when file was created
        folderName = time.strftime("%m-%d-%Y", time.gmtime(os.path.getctime(filePath)))
        folderPath = os.path.join(DESTINATION_PATH, folderName)
        newFilePath = os.path.join(folderPath, file)

        if os.path.exists(newFilePath):#the picture already exists
          modifier = 1
          foundNumber = False
          while not foundNumber: #we are going to modify the name so that it has a number in it to differentiate them, causing overwrites to not happen
            fileParts = str.split(file, '.')
            fileParts[-2] = fileParts[-2] + '(' + str(modifier) + ')'
            possibleFilePath = os.path.join(folderPath, '.'.join(fileParts))
            if not os.path.exists(possibleFilePath):
              foundNumber = True
              newFilePath = possibleFilePath
            else:
              modifier += 1
        
        print ("Moving: " + file)
        try:#attempt to move the file
          shutil.move(filePath, newFilePath)
        except:#if there was an error 
          doCopy = False

          if not os.path.exists(folderPath):#the file wasn't there, make it and then redo the move
            print("creating folder: " + folderName)
            os.makedirs(folderPath)
            doCopy = True
            
          if doCopy:
            shutil.move(filePath, newFilePath)

#run program
if __name__ == '__main__':
  Main()

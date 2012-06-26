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
DATE_MATCH = "^(1[012]|0[1-9])-([12]\d|3[01]|0[1-9])-[12]\d{3}$"
#get the users desktop
#this is probably platform independant - as long as they have a desktop
DESTINATION_PATH = os.path.join(os.path.expanduser('~'),'Desktop','My_Pics')
#############################################################################################
#                                   END CONSTANTS                                           #
#############################################################################################

## main program entry point
def Main():                           
  currentDirectory = os.getcwd()

  #walk over the directories
  for root, dirs, files in os.walk(currentDirectory):
    for file in files:
      fileExtension = str.split(file, '.')[-1]

      if re.match(IMAGE_MATCH_STRING, fileExtension.lower()):
        filePath = os.path.join(root, file)
        #file name will have the following structure
        #originalFileName '_' The day abbreviation Mon-Day-Year (all as numbers) Hour;Minute;Second from a 24 hour clock - all times/dates are when file was created
        fileName = time.strftime("{0}_%a_%m-%d-%Y_%H;%M;%S.{1}".format(file, fileExtension), time.gmtime(os.path.getctime(filePath)))
        #this should be the date - allows more versitile user names for files that have underscores in them
        folderName = None
        try:
          folderName = next(section for section in str.split(fileName, '_') if re.match(DATE_MATCH, section))#get first match of the date value for folder name
        except:
          folderName = "Undated"
        folderPath = os.path.join(DESTINATION_PATH, folderName)
        filePath = os.path.join(folderPath, fileName)

        if not os.path.exists(filePath):#only copy when the file hasn't already been backed up
          print ("Backing up: " + file)
          try:#attempt to copy the file
            shutil.copy2(os.path.join(root, file), filePath)
          except IOError:#if there was an error 
            if not os.path.exists(folderPath):#the file wasn't there, make it and then redo the copy
              print("creating folder: " + folderName)
              os.makedirs(folderPath)
              shutil.copy2(os.path.join(root, file), filePath)
        else:
          print ("Not backing up: " + file)

#run program
if __name__ == '__main__':
  Main()


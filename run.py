import correctorlib
import os

def deleteContent(fName):
    with open(fName, "w"):
        pass

name = "output"
directory = "/home/mostafa/TrainData2/"
sh = 0
deleteContent("result.csv")
for filename in os.listdir(directory):
    if filename.endswith(".png"):
		#print directory+filename
		correctorlib.run(directory,filename,sh)
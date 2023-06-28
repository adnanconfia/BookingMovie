from movie_booking.settings import Img_url

def getImageFile(filename):
    fileName = filename.split('/')
    fileName = fileName[len(fileName)-1]
    file ={
        "fileName":fileName,"filePath":Img_url+"images/"+fileName
    }
    return file
import StringIO
import os

from django.conf import settings
from PIL import Image, ImageOps
from random import randint

class BookImageUtils:
    
    def __init__(self, uploadedImage, currDate):
        self.uploadedImage = uploadedImage
        self.currDate = currDate
        
        #Setting image name: <current date including milliseconds>+<random number>
        self.imgNewName = self.currDate.strftime("%Y%m%d%H%M%S%f") + str(randint(0,9))
        self.imgOldName = str(self.uploadedImage)
		
		# New image name should have old extension. rfind -> lastIndexOf
        self.imgExtension = self.imgOldName[self.imgOldName.rfind("."):] 
        self.imgName = self.imgNewName + self.imgExtension
        self.imageDynamicPath = str(currDate.year) + "/" + str(currDate.month) + "/" + str(currDate.day) + "/"
        self.imagePath = settings.UPLOAD_FOLDER + self.imageDynamicPath
		
        # Creates path to store image
        if not os.path.exists(self.imagePath):
            os.makedirs(self.imagePath)
            
            
    # Verifies if image format is in allowed list defined in settings.py
    def isValidFormat(self):
		if self.uploadedImage.content_type in settings.ALLOWED_IMAGE_UPLOAD:
			return True
		else:
			return False
        
        
    # Verifies if image size does not exceed the defined one
    def isValidSize(self):
		if self.uploadedImage._size < settings.ALLOWED_IMAGE_SIZE:
			return True
		else:
			return False
        
    
    # Resizes image by scale factor
    def resizeImage(self,image,maxWidth,maxHeight):
        (width, height) = image.size
        
        #checking image resolution
        resizingFactor = 1
        if (maxWidth/width < maxHeight/height):
            resizingFactor = float(maxHeight)/float(height)
        else:
            resizingFactor = float(maxWidth)/float(width)
                    
        if (resizingFactor < 1):
            newSize = ( int(width * resizingFactor), int(height * resizingFactor) )
            image = image.resize(newSize, Image.ANTIALIAS)
        
        return image
            
    
    # Uploads image to the disc
    def uploadImage(self):
        maxWidth = settings.ALLOWED_MAX_IMAGE_RESOLUTION[0]
        maxHeight =	settings.ALLOWED_MAX_IMAGE_RESOLUTION[1]
        
        imageStr = ""
        for chunk in self.uploadedImage.chunks():
            imageStr += chunk
          
        imagefile = StringIO.StringIO(imageStr)
        self.image = Image.open(imagefile)
        self.image = self.resizeImage(self.image, maxWidth, maxHeight)
        self.image.save(self.imagePath + self.imgName)
        
        
    # Generates image thumbnail if it does not exists. Called after uploadImage
    def generateThumnail(self):
        maxWidth = settings.IMAGE_THUMBNAIL[0]
        maxHeight =	settings.IMAGE_THUMBNAIL[1]
        
        self.imgNewNameThumb = self.imgNewName + "-thumbnail" + self.imgExtension
        
        self.image = self.resizeImage(self.image, maxWidth, maxHeight)
        self.image.save(self.imagePath + self.imgNewNameThumb)
        
    
    # Generates image thumbnail based on image of given path. Used in book edit mode
    # TODO: test
    def changeThumbnail(self, imagePath):
        maxWidth = settings.IMAGE_THUMBNAIL[0]
        maxHeight =	settings.IMAGE_THUMBNAIL[1]
        
        image = Image.open(imagePath)
        image = self.resizeImage(image, maxWidth, maxHeight)
        imgExtension = imagePath[imagePath.rfind("."):]
        #not sure if should be self.imgNewNameThumb or imgNewNameThumb
        self.imgNewNameThumb =  imagePath[:imagePath.rfind(".")] + "-thumbnail" + imgExtension 
        image.save(self.imgNewNameThumb)
		
# TODO: add deleteImage and moveImage functions -> data is obtained from database
# BookImage.imageDynamicPath | BookImage.imgName | BookImage.imgNewNameThumb

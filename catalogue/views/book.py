import logging

import os
import uuid
import StringIO
from PIL import Image, ImageOps
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from datetime import datetime
from random import randint
from django.conf import settings
from catalogue.entities import RU_ru
from catalogue.entities.ResponseMessage import ResponseMessage
from catalogue.models import User
from catalogue.utils.management.BookUtils import BookUtils

log = logging.getLogger("django")


def insertBook(request):
    
    bookUUIDVal =  uuid.uuid4()

    imagePath = settings.UPLOAD_FOLDER

    bookNameTxt = request.POST["book-name-txt"]
    bookAuthorTxt = request.POST["book-author-txt"]
    bookDescriptionTxt = request.POST["book-desc-txt"]
    
    bookCategorySelect = request.POST["category-select"]
    bookCoverSelect = request.POST["cover-select"]
    bookQualitySelect = request.POST["quality-select"]
    bookLanguageSelect = request.POST["language-select"]
    
    bookPriceTxt = request.POST["book-price-txt"]
    bookDiscountTxt = request.POST["book-discount-txt"]
    
    bookNotable = False
    if "book-is-with-priority" in request.POST.keys():
        bookNotable = True
    
    bookUploadedImages = request.FILES.getlist('file')
    
    bookId = request.POST["book-id"]
    
    
    status_code = 1 #1-ok, 2-warn, 3-error ---------------------
    
    resp = ResponseMessage(1,"success")

    try:
        
        bookImagesNames = []
        imageCounter = 1
        
        for uploadedImage in bookUploadedImages:
            
            # Setting image name: <current date including milliseconds>+<random number>
            currDate = datetime.today()
            imgNewName = currDate.strftime("%Y%m%d%H%M%S%f") + str(randint(0,9))
            imgOldName = str(uploadedImage)
            imgName = imgNewName + imgOldName[imgOldName.index("."):]
            imgNewNameThumb = imgNewName + "-thumbnail" + imgOldName[imgOldName.index("."):]
            imageDynamicPath = str(currDate.year) + "/" + str(currDate.month) + "/" + str(currDate.day) + "/"
            imagePath = imagePath + imageDynamicPath
            
            # Images are stored in YYYY/MM/DD folder structure
            print imagePath
            if not os.path.exists(imagePath):
                os.makedirs(imagePath)
                    
            if uploadedImage.content_type in settings.ALLOWED_IMAGE_UPLOAD:
                if uploadedImage._size < settings.ALLOWED_IMAGE_SIZE:
                    
                    # Uploading image to the server
                    bookImagesNames.append(imgName)
                    imageStr = ""
                    for chunk in uploadedImage.chunks():
                        imageStr += chunk
                        
                    imagefile  = StringIO.StringIO(imageStr)
                    image = Image.open(imagefile)
                    (width, height) = image.size
                        
                    #checking image resolution
                    resizingFactor = 1
                    if (settings.ALLOWED_MAX_IMAGE_RESOLUTION[0]/width < settings.ALLOWED_MAX_IMAGE_RESOLUTION[1]/height):
                        resizingFactor = float(settings.ALLOWED_MAX_IMAGE_RESOLUTION[1])/float(height)
                    else:
                        resizingFactor = float(settings.ALLOWED_MAX_IMAGE_RESOLUTION[0])/float(width)
                    
                    if (resizingFactor < 1):
                        newSize = ( int(width * resizingFactor), int(height * resizingFactor))
                        image = image.resize(newSize, Image.ANTIALIAS)
                        
                    image.save(imagePath + imgName)
                    
                    #generating image thumbnail
                    resizingFactorThumb = 1
                    if (settings.IMAGE_THUMBNAIL[0]/width < settings.IMAGE_THUMBNAIL[1]/height):
                        resizingFactorThumb = float(settings.IMAGE_THUMBNAIL[1])/float(height)
                    else:
                        resizingFactorThumb = float(settings.IMAGE_THUMBNAIL[0])/float(width)
                        
                    if (resizingFactorThumb < 1):
                        newSize = ( int(width * resizingFactorThumb), int(height * resizingFactorThumb))
                        image.thumbnail(newSize, Image.ANTIALIAS)
                    
                    image.save(imagePath + imgNewNameThumb)
                    
                    # When a new book is added with images, only the first image is defined as thumbnail. 
                    # Thumbnail can be chnaged in book item modification
                    if (imageCounter == 1):
                        bookThumbnail = imgNewNameThumb
                            
                    # It's allowod to upload only 15 valid images per book
                    if imageCounter >= settings.ALLOWED_IMAGE_QUANT:
                        resp = ResponseMessage(2, "wrong-image-quantity")
                        log.warning("Wrong image quantity! Only %d images are allowed. Other images will be discarded" % settings.ALLOWED_IMAGE_QUANT)
                        break;
                        
                    imageCounter += 1
                     
                else:
                    resp = ResponseMessage(3,"wrong-image-size")
                    log.warning("Wrong image size! Only %d KB images are allowed. The image %s will be discarded" %
                                ((settings.ALLOWED_IMAGE_SIZE / 1024), imgOldName) )
            else: 
                resp = ResponseMessage(3,"wrong-image-format")
                log.warning("Wrong image size! Only JPG and PNG images are allowed. The image %s will be discarded" % (imgOldName) )
            
            
        # Inserting other book data only if image data is correct if it is exists
        if resp.getErrorCode() == 1 or not bookUploadedImages:
            
            users = User.objects.filter(id=1) #TODO: hardcoded
        
            if len(users) > 0:
                modifyUser = users[0]
                            
                bookUtils = BookUtils()
                
                # Modify book category
                if len(bookId) > 0:
                    print "tmp------------"
                    
                # Add new book category
                else:
                    resp = bookUtils.addNewBook(bookUUIDVal, bookNameTxt, bookAuthorTxt, bookDescriptionTxt, bookCategorySelect, 
                            bookCoverSelect, bookQualitySelect, bookLanguageSelect, bookPriceTxt, 
                            bookDiscountTxt, bookNotable, imageDynamicPath, bookImagesNames, bookThumbnail, modifyUser)
                            
    except Exception as error:
        ResponseMessage(3,"internal-error")
        log.exception(error)
 
    
   
    
        
    
    return render_to_response(
                              'catalogue/templates/book-management.html', 
                              {
                               #'book_category_list': book_category_list, 
                               #'status': status_code,
                               'ResponseMessage': ResponseMessage,
                               'lang': RU_ru
                               })
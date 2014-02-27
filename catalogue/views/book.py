import logging

from django.shortcuts import render_to_response
from catalogue.entities import RU_ru

log = logging.getLogger("django")



def insertBook(request):

    bookNameTxt = request.POST["book-name-txt"]
    bookAuthorTxt = request.POST["book-author-txt"]
    bookDescriptionTxt = request.POST["book-desc-txt"]
    
    bookCategorySelect = request.POST["category-select"]
    bookCoverSelect = request.POST["cover-select"]
    bookQualitySelect = request.POST["quality-select"]
    bookLanguageSelect = request.POST["language-select"]
    
    bookPriceTxt = request.POST["book-price-txt"]
    bookDiscountTxt = request.POST["book-discount-txt"]
    
    bookIsPrioritized = False
    if "book-is-with-priority" in request.POST.keys():
        bookIsPrioritized = True
    
    bookUploadedImages = request.FILES.getlist('file')
    
    #https://docs.djangoproject.com/en/dev/topics/http/file-uploads/
    for uploadedImage in bookUploadedImages:
        with open('/home/andriy/Pictures/books-test/'+str(uploadedImage), 'wb+') as destination:
            for chunk in uploadedImage.chunks():
                destination.write(chunk)
    
    
    
    #book_category_id = request.POST["book-category-id"]
    
    
        
    
    return render_to_response(
                              'catalogue/templates/book-management.html', 
                              {
                               #'book_category_list': book_category_list, 
                               #'status': status_code,
                               'lang': RU_ru
                               })
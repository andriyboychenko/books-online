from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=50)
    active = models.BooleanField(default=1)
    def __unicode__(self):
        return self.role_name

class User(models.Model):
    name = models.CharField(max_length=50)
    user_type = models.ForeignKey(Role)
    db_insert_date = models.DateTimeField('date published')
    db_modify_date = models.DateTimeField('date published')
    db_modify_user = models.ForeignKey('self', null=True, blank=True)
    active = models.BooleanField(default=1)
    def __unicode__(self):
        return self.name

class BookCategory(models.Model):
    category_name = models.CharField(max_length=50)
    category_description = models.CharField(max_length=500)
    sub_category_of = models.ForeignKey('self', null=True, blank=True)
    db_insert_date = models.DateTimeField('date published')
    db_modify_date = models.DateTimeField('date published')
    db_modify_user = models.ForeignKey(User)
    active = models.BooleanField(default=1)
    def __unicode__(self):
        return self.category_name
 
class BookAttributeType(models.Model):
    type_name = models.CharField(max_length=50)
    db_insert_date = models.DateTimeField('date published')
    db_modify_date = models.DateTimeField('date published')
    db_modify_user = models.ForeignKey(User)
    active = models.BooleanField(default=1)
    def __unicode__(self):
        return self.type_name
    
class BookAttribute(models.Model):
    attribute_name = models.CharField(max_length=50)
    attribute_type = models.ForeignKey(BookAttributeType)
    attribute_description = models.CharField(max_length=500)
    db_insert_date = models.DateTimeField('date published')
    db_modify_date = models.DateTimeField('date published')
    db_modify_user = models.ForeignKey(User)
    active = models.BooleanField(default=1)
    def __unicode__(self):
        return self.attribute_name
    
class BookItem(models.Model):
    book_uuid = models.CharField(max_length=40)
    book_name = models.CharField(max_length=200)
    book_author = models.CharField(max_length=100)
    book_description = models.CharField(null=True, max_length=1000)
    book_category = models.ForeignKey(BookCategory)
    book_cover = models.ForeignKey(BookAttribute, related_name='book_cover')
    book_quality = models.ForeignKey(BookAttribute, related_name='book_quality')
    book_language = models.ForeignKey(BookAttribute, related_name='book_language')
    book_price = models.DecimalField(max_digits=10, decimal_places=2)
    book_discount = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    is_notable = models.BooleanField(default=0)
    book_images_path = models.CharField(null=True, max_length=200)
    book_images_names = models.CharField(null=True, max_length=1000)
    book_thumbnail = models.CharField(null=True, max_length=30)
    view_counter = models.BigIntegerField(null=True, default=0)
    search_hits_counter = models.BigIntegerField(null=True, default=0)
    db_insert_date = models.DateTimeField('date published')
    db_modify_date = models.DateTimeField('date published')
    db_modify_user = models.ForeignKey(User)
    active = models.BooleanField(default=1)
    def __unicode__(self):
        return self.book_name
    
    
    


from django.db import models

# Create your models here.

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
    


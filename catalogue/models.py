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

class BookCathegory(models.Model):
    cathegory_name = models.CharField(max_length=50)
    cathegory_description = models.CharField(max_length=500)
    sub_cathegory_of = models.ForeignKey('self', null=True, blank=True)
    db_insert_date = models.DateTimeField('date published')
    db_modify_date = models.DateTimeField('date published')
    db_modify_user = models.ForeignKey(User)
    active = models.BooleanField(default=1)
    def __unicode__(self):
        return self.cathegory_name
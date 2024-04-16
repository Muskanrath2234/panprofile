from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(null=True,max_length=200,blank=True)
    DOB = models.DateField(null=True,max_length=10,blank=True)
    Pan = models.CharField(null=True,max_length=10,blank=True)
    father_Name  = models.CharField(null=True,max_length=200,blank=True)
    Profile_img = models.ImageField(default="images/default_profile.png",upload_to='images',blank=True,null=True)




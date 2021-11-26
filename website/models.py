from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField
from django.utils.text import slugify


class Image(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content=models.CharField(max_length=2000,null=True)
    title=models.CharField(max_length=80 ,null=True)
    file=models.ImageField(upload_to="media")
    date_created=models.DateTimeField(auto_now_add=True ,null=True)
    slug = models.SlugField(null=True,blank=True)

    def __str__(self):
        return str(self.title)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Image,self).save(*args,**kwargs)

class UserDetails(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(null=True)

class UpdateProfileImage(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image=models.ImageField(upload_to="media", default="4568172.jpg")
    bio=models.CharField(max_length=250, null=True)
    date_created=models.DateTimeField(auto_now_add=True ,null=True)

    def __str__(self):
        return f"{self.user} profile"

class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    image=models.ForeignKey(Image, on_delete=models.CASCADE,null=True)
    comment=models.CharField(max_length=200)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

class Like(models.Model):
    id=models.AutoField(primary_key=True)
    image=models.ManyToManyField(Image,related_name="like")
    like=models.ManyToManyField(User,related_name="like")

class OTP(models.Model):
    user=OneToOneField(User,on_delete=models.CASCADE,null=True)
    mobile=models.CharField(max_length=15,null=True)
    otp=models.CharField(max_length=6,null=True)
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#------------------------------------------------------------------------
class MessageManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['content'])>200:
            errors["content"] = "content cannot be over 200 characters"
        if len(postData['content']) < 2:
            errors["content"] = "content cannot be less than 2 characters"
        return errors
    def Create_message(self,postData):
        this_user=User.objects.get(id=postData['hidden'])
        post = Message.objects.create(content=postData['content'],uploader=this_user)
        post.save()
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        user=User.objects.all().values().filter(email=postData['email'])
        if user:
            errors["user"] = "email already exists in database"
        if len(postData['firstname']) < 2:
            errors["firstname"] = "firstname cannot be less than 2 characters"
        if postData['firstname'].isalpha() is False:
            errors["firstname"] = "first name cannot contain numbers"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "last name must be longer than 2 characters" #ADD MAX LENGTH VALIDATIONS OM ALL
        if postData['lastname'].isalpha() is False:
            errors["lastname"] = "last name cannot contain numbers"
        if len(postData['password']) < 8 :
            errors["password"] = "password cannot be less than 8 characters"
        if postData['password'] != postData['passwordconf'] :
            errors["passwordconf"] = "passwords do not match"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "email is invalid"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['password']) < 1 :
            errors["password"] = "please enter your password"
        try:
            user=User.objects.all().values().get(email=postData['email'])
            if user:
                if bcrypt.checkpw(postData['password'].encode(), user['pwhash'].encode()):
                    print("password match")
                else:
                    errors["password"] = "passwords do not match"
                return errors
        except:
            errors['login']="user does not exist in database"
            return errors
    def Create_user(self,postData):
        user = User.objects.create()
       
        user.firstname = postData['firstname']
        user.lastname = postData['lastname']
        user.email = postData['email']
        user.pwhash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user.save()
#------------------------------------------------------------------------
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    pwhash = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # *************************
    # Connect an instance of UserManager to our User model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UserManager()
    # *************************
#------------------------------------------------------------------------
class Message(models.Model):
    content = models.CharField(max_length=255)
    likes= models.ManyToManyField(User, related_name='liked')
    uploader=models.ForeignKey(User,related_name='uploaded')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

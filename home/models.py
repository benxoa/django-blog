from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



from tinymce import models as ty_models
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=17)
    
    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    title = models.CharField( max_length=120)
    image = models.ImageField(upload_to="uploads/",default=1)
    date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    display_text = models.TextField(max_length=100)
    content = ty_models.HTMLField()
    
    def __str__(self) -> str:
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField("userimage/") # or whatever

    def __str__(self):
        return self.user.email

class Contact(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    subject = models.CharField( max_length=240, default=1)
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return f"{self.firstName } {self.lastName}"
    


    

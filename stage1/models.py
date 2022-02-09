from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    asin = models.CharField(max_length=100)

class Reviewer(models.Model):
    original_id = models.CharField(max_length=100)

class UserItem(models.Model):
    author = models.ForeignKey(User,on_delete=models.RESTRICT,null=False)
    item = models.ForeignKey(Item,on_delete=models.RESTRICT,null=False)
    done = models.BooleanField(default=False)

class Aspect(models.Model):
    name = models.CharField(max_length=100)

class Review(models.Model):
    item = models.ForeignKey(Item,on_delete=models.RESTRICT,null=False)
    reviewer = models.ForeignKey(Reviewer,on_delete=models.RESTRICT,null=False)

class ReviewSentence(models.Model):
    review = models.ForeignKey(Review,on_delete=models.RESTRICT,null=False)
    aspect = models.ForeignKey(Aspect,on_delete=models.RESTRICT,null=False)
    content = models.CharField(max_length=1000)

class Answer(models.Model):
    author = models.ForeignKey(User,on_delete=models.RESTRICT,null=False)
    item = models.ForeignKey(Item,on_delete=models.RESTRICT,null=False)
    sentence = models.ForeignKey(ReviewSentence,on_delete=models.RESTRICT,null=False)
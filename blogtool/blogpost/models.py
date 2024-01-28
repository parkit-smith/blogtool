from django.db import models
# Create your models here.

class BlogPost(models.Model):
    blog_post_title = models.CharField(max_length = 2000)
    blog_post_date = models.CharField(max_length = 2000)
    blog_post_image = models.ImageField(blank=True, null=True)
    blog_post_text = models.CharField(max_length = 100000)
    blog_card_title = models.CharField(max_length = 2000)
    blog_card_caption = models.CharField(max_length = 2000)
    blog_card_image = models.ImageField(blank=True,null=True)

class Ghat(models.Model):
    ghat = models.CharField(max_length = 200)

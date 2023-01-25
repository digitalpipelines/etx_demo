from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from articles.utils import slugify_instance_title
from django.urls import reverse
from django.db.models import Q
from django.conf import settings

USER = settings.AUTH_USER_MODEL

class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == '':
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self.db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(USER, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pubish = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    objects = ArticleManager()

    @property
    def name(self):
        return self.title
    
    def get_absolute_url(self):
        #return f"/articles/{self.slug}"
        return reverse('articles:detail', kwargs={'slug':self.slug})

    #Left in for example purposes 
    def save(self, *args, **kwargs):
         super().save(*args, **kwargs) 

def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance)

pre_save.connect(article_pre_save, sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True) 

post_save.connect(article_post_save, sender=Article)
from django.test import TestCase
from .models import Article
from django.utils.text import slugify
from .utils import slugify_instance_title

class ArticleTest(TestCase):
    def setUp(self):
        self.num_of_articles = 5
        self.slug_title = 'hello'
        for i in range(0, self.num_of_articles):
            Article.objects.create(title=self.slug_title, content='Something')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())
 
    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.num_of_articles)    

    def test_slug_equals(self):
        obj = Article.objects.all().order_by('id').first()
        title = obj.title
        slug = obj.slug
        slugified_title = slugify(title)
        self.assertEquals(slug, slugified_title)

    #Tests that the automatic number generation is working so titles won't be the same
    def test_unique_slug(self):
        qs = Article.objects.exclude(slug__iexact=self.slug_title)
        for obj in qs:
            title = obj.title
            slug = obj.slug
            slugified_title = slugify(title)
            self.assertNotEquals(slug, slugified_title)    

    def test_slugify_instance_title(self):
        obj = Article.objects.all().last()
        new_slugs = []
        for i in  range(0,5):
            instance = slugify_instance_title(obj, save=False)
            new_slugs.append(instance.slug)
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_article_search_manager(self):
        qs = Article.objects.search(query=self.slug_title)    
        self.assertEqual(qs.count(), self.num_of_articles)



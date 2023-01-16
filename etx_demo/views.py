
from django.http import HttpResponse
from articles.models import Article
from django.template.loader import render_to_string



def home_view(request, *args, **kwargs):
    # Takes a request and returns a webpage
    print(args, kwargs) 
    
    article_obj = Article.objects.get(id=2)

    article_queryset = Article.objects.all()

    context = {
        "object_list": article_queryset,
        "title": article_obj.title,
        "id": article_obj.id,
        "content": article_obj.content
    }

    htmlString = render_to_string("home_view.html", context=context)

    return HttpResponse(htmlString)
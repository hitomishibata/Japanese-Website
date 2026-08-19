from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import Blog
from django.http import Http404

# Create your views here.

def index(request):
    latest_blogs =Blog.objects.order_by('-pub_date')[:10]
    return render(request, 'blogs/index.html', {'latest_10_blogs': latest_blogs})

def content(request, blog_id: int):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blogs/content.html', {'blog': blog})

def category(request, tag: str):
    valid_tags = dict(Blog.TAG_CHOICES).keys()
    if tag not in valid_tags:
        raise Http404("Category does not exist")
    filtered_blogs = Blog.objects.filter(tags__contains=[tag]).order_by('-pub_date')
    return render(request, "blogs/category.html", {'tag_filt_blogs': filtered_blogs, 'input_tag': tag, 'tag_img': f'blogs/{tag}.jpg'})

def grammer(request, grammars: list):
    valid_grammars = Blog.GRAMMAR_CHOICES.keys()
    for grammer in grammars:
        if grammer not in valid_grammars:
            raise Http404("Grammer does not exist.")
    filtered_blogs = Blog.objects.filter(grammars__contains=grammars)
    return render(request, 'blogs/grammar.html', {'gra_filt_blogs': filtered_blogs, 'input_grammars': grammars})

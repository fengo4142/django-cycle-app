from django.shortcuts import render, get_object_or_404
from blog.models import Blog, Category
# Create your views here.

def index(request):
  template_name = "index.html"
  blogs = Blog.objects.all()
  context = {
      "blogs": blogs
  }
  return render(request, template_name, context)

def contact(request):
  template_name = "contact.html"
  return render(request, template_name)

def detail(request, id=None):
  blog = get_object_or_404(Blog, id=id)
  from difflib import SequenceMatcher
  
  vec = [ [b.id, SequenceMatcher(None, blog.title, b.title).ratio(), b.title] for b in Blog.objects.all() if blog.id != b.id ]
  related_blogs = sorted(vec, key=lambda x: x[0])[-3:]
  print(related_blogs)
  context= {
    'blog': blog,
    'related_blogs': related_blogs
  }
  return render(request, 'detail.html', context)

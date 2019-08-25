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
  context= {
    'blog': blog,
  }
  return render(request, 'detail.html', context)

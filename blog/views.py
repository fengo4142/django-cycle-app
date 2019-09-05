from django.shortcuts import render, get_object_or_404
from blog.models import Blog, Category
from django.http import HttpResponse, JsonResponse
# Create your views here.


def index(request):
    template_name = "index.html"
    blogs = Blog.objects.all()
    latest_blogs = Blog.objects.order_by('-timestamp')[:5]
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'blogs': blogs,
        'latest_blogs': latest_blogs
    }
    return render(request, template_name, context)


def contact(request):
    template_name = "contact.html"
    return render(request, template_name)


def detail(request, id=None):
    if request.is_ajax():
        is_liked = request.POST.get('like')
        id = request.POST.get('id')
        X = Blog.objects.get(id=id)
        if is_liked == 'true':
            X.favorite += 1
        else:
            X.favorite -= 1
        X.save()
        return JsonResponse({'message': 'success'})

    blog = get_object_or_404(Blog, id=id)
    from difflib import SequenceMatcher

    vec = [[b.id, SequenceMatcher(None, blog.title, b.title).ratio(
    ), b.title] for b in Blog.objects.all() if blog.id != b.id]
    related_blogs = sorted(vec, key=lambda x: x[0])[-3:]
    latest_blogs = Blog.objects.order_by('-timestamp')[:5]
    categories = Category.objects.all()

    context = {
        'blog': blog,
        'categories': categories,
        'related_blogs': related_blogs,
        'latest_blogs': latest_blogs
    }
    return render(request, 'detail.html', context)


def blogs(request, id=None):
    blogs = Blog.objects.all()[:5]
    if id != None:
        blogs = Blog.objects.filter(category=id)
    if request.method == "POST":
        search_key = request.POST.get('searchKey')
        blogs = Blog.objects.filter(title__icontains=search_key)
    latest_blogs = Blog.objects.order_by('-timestamp')[:5]
    categories = Category.objects.all()
    context = {
        'blogs': blogs,
        'categories': categories,
        'latest_blogs': latest_blogs
    }
    return render(request, "blogs.html", context)

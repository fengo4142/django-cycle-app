from django.contrib import admin
from blog.models import Category, Blog
from blog.forms import BlogAdminForm
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)

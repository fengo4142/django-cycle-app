from django.db import models

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField()
  is_active = models.BooleanField()
  
  def __str__(self):
    	return str(self.name)

class Blog(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField(null=True)
	timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
	author = models.CharField(max_length=255)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	is_active = models.BooleanField()
  
	def __str__(self):
	  return str(self.title)
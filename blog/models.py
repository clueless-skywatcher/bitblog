from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class BlogPost(models.Model):
	title = models.CharField(max_length = 50)
	content = models.TextField()
	post_date = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	votes = models.IntegerField(default = 0)

	def __str__(self):
		return f"{self.title}"

	def get_absolute_url(self):
		return reverse('post', kwargs = {
			'pk' : self.pk
		})

class BlogComment(models.Model):
	comment = models.TextField()
	comment_date = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	votes = models.IntegerField(default = 0)
	parent_post = models.ForeignKey(BlogPost, on_delete = models.CASCADE)
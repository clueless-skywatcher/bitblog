from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class BlogUser(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	desc = models.TextField(max_length = 250, default = "No description")
	hometown = models.CharField(max_length = 200, default = "Not specified")
	birth_date = models.DateField(null = True, blank = True)

class Following(models.Model):
	followed = models.ForeignKey(User, related_name = 'followers', on_delete = models.DO_NOTHING)
	follower = models.ForeignKey(User, related_name = 'following', on_delete = models.DO_NOTHING)

@receiver(post_save, sender = User)
def make_profile(sender, instance, created, **kwargs):
	if created:
		BlogUser.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
	instance.bloguser.save()
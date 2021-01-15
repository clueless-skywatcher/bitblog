from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField

User._meta.get_field('email')._unique = True

class BlogPost(models.Model):
	title = models.CharField(max_length = 50)
	content = RichTextField()
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

class Sigil(models.Model):
	name = models.CharField(unique=True, max_length=50)
	img = models.ImageField(upload_to='sigils')

	def __str__(self):
		return f"{self.name}"

class ProfileCard(models.Model):
	name = models.CharField(unique = True, max_length = 50)
	img = models.ImageField(upload_to = 'profile_cards')
	img_small = models.ImageField(upload_to = 'profile_cards_small')
	
	def __str__(self):
		return f"{self.name}"

class BlogUser(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	desc = models.TextField(max_length = 250, default = "No description")
	hometown = models.CharField(max_length = 200, default = "Not specified")
	birth_date = models.DateField(null = True, blank = True)
	current_profile_card = models.ForeignKey(ProfileCard, on_delete = models.DO_NOTHING, default = 1)
	current_sigil = models.ForeignKey(Sigil, on_delete = models.DO_NOTHING, default = 1)

	def __str__(self):
		return self.user.username

class Following(models.Model):
	followed = models.ForeignKey(User, related_name = 'followers', on_delete = models.DO_NOTHING)
	follower = models.ForeignKey(User, related_name = 'following', on_delete = models.DO_NOTHING)

class ProfileCardGallery(models.Model):
	user = models.ForeignKey(BlogUser, related_name = 'profile_cards', on_delete = models.DO_NOTHING)
	profile_card = models.ForeignKey(ProfileCard, on_delete = models.DO_NOTHING)

	class Meta:
		unique_together = ('user', 'profile_card')

	def __str__(self):
		return f"{self.profile_card.name}-{self.user.user.username}"

class SigilGallery(models.Model):
	user = models.ForeignKey(BlogUser, related_name = 'sigils', on_delete = models.DO_NOTHING)
	sigil = models.ForeignKey(Sigil, on_delete = models.DO_NOTHING)

	class Meta:
		unique_together = ('user', 'sigil')

	def __str__(self):
		return f"{self.sigil.name}-{self.user.user.username}"

@receiver(post_save, sender = User)
def make_profile(sender, instance, created, **kwargs):
	if created:
		BlogUser.objects.create(user = instance)

@receiver(post_save, sender = User)
def add_default_profile_card(sender, instance, created, **kwargs):
	if created:
		profile_card = ProfileCard.objects.filter(name = 'Welcome').first()
		sigil = Sigil.objects.filter(name = 'Radioactive').first()
		profcard_gallery_obj = ProfileCardGallery(user = instance.bloguser, profile_card = profile_card)
		sigil_gallery_obj = SigilGallery(user = instance.bloguser, sigil = sigil)
		instance.bloguser.current_profile_card = profile_card
		instance.bloguser.current_sigil = sigil
		instance.bloguser.save()
		profcard_gallery_obj.save()
		sigil_gallery_obj.save()

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
	instance.bloguser.save()

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(BlogComment)
admin.site.register(BlogUser)
admin.site.register(Following)
admin.site.register(ProfileCard)
admin.site.register(ProfileCardGallery)
admin.site.register(Sigil)
admin.site.register(SigilGallery)

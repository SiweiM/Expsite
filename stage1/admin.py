from django.contrib import admin

# Register your models here.
from .models import Item,Reviewer,ReviewSentence,Aspect,Answer,Review,UserItem

admin.site.register(Item)
admin.site.register(Reviewer)
admin.site.register(ReviewSentence)
admin.site.register(Aspect)
admin.site.register(Answer)
admin.site.register(Review)
admin.site.register(UserItem)
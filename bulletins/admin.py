from django.contrib import admin

from .models import Tag,Category,Bulletin,TeamMember,Partner,Action,Subscribers
from django_summernote.models import Attachment

admin.site.unregister(Attachment)

class TagAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Tag, TagAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    list_display = ('name', )
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

class BulletinAdmin(admin.ModelAdmin):
    fields = ['name', 'image','description','category','tags','bulletin_url','created_at']
    list_display = ('name','category','created_at','views')
    list_filter = ['tags','category']
    search_fields = ['name']

admin.site.register(Bulletin, BulletinAdmin)

class TeamMemberAdmin(admin.ModelAdmin):
    fields = ['name', 'function','link','image']
    list_display = ['name']
    search_fields = ['name']

admin.site.register(TeamMember, TeamMemberAdmin)

class PartnerAdmin(admin.ModelAdmin):
    fields = ['name', 'image']
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Partner, PartnerAdmin)

class ActionAdmin(admin.ModelAdmin):
    fields = ['name','image']
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Action, ActionAdmin)

class SubscribersAdmin(admin.ModelAdmin):
    fields = ['name','email']
    list_display = ['name', 'email','subscription_token']
    search_fields = ['name']

admin.site.register(Subscribers, SubscribersAdmin)
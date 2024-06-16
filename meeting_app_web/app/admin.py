
from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'gender', 'date_of_birth', 'place_of_birth')

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'accepted', 'updated', 'created')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'date_envoi')

@admin.register(CentresDInteret)
class CentresDInteretAdmin(admin.ModelAdmin):
    list_display = ('user', 'sport', 'musique', 'lecture', 'voyage', 'cinema', 'technologie')

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'common_percentage')

@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    list_display = ('connection', 'created_at')


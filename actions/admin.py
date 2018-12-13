from django.contrib import admin
from actions.models import Action

@admin.register(Action)
class ActionManager(admin.ModelAdmin):
	list_display = ('user', 'verb', 'target', 'created')

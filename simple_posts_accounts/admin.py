from django.contrib import admin
from simple_posts_accounts.models import Profile, Contact

@admin.register(Profile)
class ProfileAdmmin(admin.ModelAdmin):
	list_display = ('user', 'date_of_birth', 'occupation', 'business_name', 'school', 'address')

@admin.register(Contact)
class ContactAdmmin(admin.ModelAdmin):
	list_display = ('user_from', 'user_to')

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    OCCUPATION_CHOICES = (
        ('student', 'Student'),
        ('business man', 'Business man'),
        ('trader', 'Trader'),
        ('employee', 'Employee'),
        ('technician', 'Technician'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    occupation = models.CharField(
        max_length=25, choices=OCCUPATION_CHOICES, blank=True)
    photo = models.ImageField(upload_to='Users_Photos', blank=True)
    address = models.CharField(max_length=50, blank=True)
    school = models.CharField(max_length=50, blank=True)
    business_name = models.CharField(max_length=50, blank=True)
    business_address = models.CharField(max_length=50, blank=True)
    school_address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return 'profile for {}'.format(self.user.username)

class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

#following = models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False)

# Add following field to User dynamically
User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))
from django.contrib import admin

# Register your models here.
from users.models import UserProxy as User

admin.site.register(User)

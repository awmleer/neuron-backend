from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # (_('Info'), {'fields': (
        #     'nickname',
        #     # 'avatar',
        #     'phone',
        # )}),
        # (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        # (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
        #                                'groups', 'user_permissions')}),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # list_display = ('nickname', 'phone', 'date_joined', 'last_login', 'is_staff')
    # list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    # search_fields = ('username', 'nickname', 'phone')
    # ordering = ('date_joined',)
    # filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)

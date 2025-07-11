from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'email_verified', 'is_staff')
    list_filter = ('user_type', 'email_verified', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_updated')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'user_type', 'bio', 'profile_picture')}),
        (_('Verification'), {'fields': ('email_verified',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'last_updated')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    
    actions = ['mark_email_verified']
    
    def mark_email_verified(self, request, queryset):
        updated = queryset.update(email_verified=True)
        self.message_user(request, f"{updated} users marked as email verified.")
    mark_email_verified.short_description = "Mark selected users as email verified"

admin.site.register(CustomUser, CustomUserAdmin)

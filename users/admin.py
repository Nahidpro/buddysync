from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

@admin.register(Account)
class AccountAdmin(UserAdmin):
    model = Account

   
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio',)}), 
    )

   
    readonly_fields = ('password',)
  

    # Customize list view
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'bio')
    search_fields = ('username', 'email')
    ordering = ('id',)
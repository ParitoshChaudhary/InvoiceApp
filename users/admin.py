from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import UserAccount


class AccountAdmin(UserAdmin):
    list_display = ['username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff']
    search_fields = ['email', 'username']
    readonly_fields = ['id', 'last_login', 'date_joined']

    filter_horizontal = ()
    fieldsets = ()
    list_filter = ()


admin.site.register(UserAccount, AccountAdmin)

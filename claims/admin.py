# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# from claims.models import Claims, Queue, Priority, ClaimState, Workers
# from claims.models import User
# # from claims.forms import UserChangeForm, UserCreationForm
#
#
# class UserAdmin(AuthUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password', 'receive_newsletter', 'claims_per_page', 'comments_per_page', 'logs_per_page', 'queue', 'avatar')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {'fields': ('username', 'password1', 'password2', 'receive_newsletter')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#     )
#     form = UserChangeForm
#     add_form = UserCreationForm
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'receive_newsletter')
#     list_editable = ('is_active','receive_newsletter')
#     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'receive_newsletter')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     ordering = ('last_name','first_name',)
#
#
# class ClaimsAdmin(admin.ModelAdmin):
#
#     list_display = ('address', 'uid', 'login', 'email', 'queue', 'owner', 'problem', 'priority', 'created', 'worker', 'issued', 'closed')
#     #list_editable = ('is_active','receive_newsletter')
#     list_filter = ('queue', 'state', 'worker')
#     search_fields = ('uid', 'address')
#     ordering = ('-priority', 'created',)
#
#
#
# admin.site.register(User, UserAdmin)
# admin.site.register(Claims, ClaimsAdmin)
# admin.site.register(Workers)
# admin.site.register(Queue)
# admin.site.register(Priority)
# admin.site.register(ClaimState)

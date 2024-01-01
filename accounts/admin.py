from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'name', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'position', 'department', 'robu_end')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'date_of_birth', 'student_id', 'secondary_email',
                                      'phone_number', 'position', 'department', 'avatar',
                                      'rs_status', 'facebook_profile', 'linkedin_link',
                                      'robu_start', 'robu_end', 'bracu_start')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'date_of_birth', 'student_id', 'secondary_email',
                       'phone_number', 'position', 'department', 'avatar',
                       'rs_status', 'facebook_profile', 'linkedin_link',
                       'robu_start', 'robu_end', 'bracu_start', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email', 'id')
    filter_horizontal = ()

# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)

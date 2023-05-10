from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Therapist


# Register your models here.

class TherapistAdminConfig(BaseUserAdmin):

    model = Therapist

    filter_horizontal = ()

    search_fields = ('id', 'first_name', )

    readonly_fields = ('id', 'registration_date', 'last_login',)

    list_filter = ('is_active', 'is_staff', 'registration_date',)

    ordering = ('registration_date', )

    list_display = ('id', 'first_name', 'last_name', 'is_active', 'is_staff', 'last_login', 'registration_date',)

    fieldsets = (
        ('Personal Information', {'fields': ('id', 'email','first_name', 'last_name', 'phone', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        ('Dates', {'fields': ('last_login', 'registration_date',)}),
        #('Groups', {'fields': ('groups', )}), 
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('id', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )



admin.site.register(Therapist, TherapistAdminConfig)

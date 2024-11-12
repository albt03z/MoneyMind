from django.contrib import admin
from .models import *

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'doc_number', 'phone_number')
    search_fields = ('name', 'surname', 'doc_number')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'person')
    search_fields = ('user__username', 'person__name', 'person__surname')

# También registra los demás modelos
admin.site.register(GenderIdentity)
admin.site.register(MaritalStatus)
admin.site.register(Typesdocs)
admin.site.register(Country)
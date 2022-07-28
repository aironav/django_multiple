from django.contrib import admin
from .models import Plan, Member, Policy, ICDAdd
# Register your models here.

admin.site.register(Plan)
admin.site.register(Policy)
# admin.site.register(Member)


class addICD(admin.StackedInline):
    model = ICDAdd
    extra = 4

class memberadmin(admin.ModelAdmin):
    inlines = [addICD]



admin.site.register(Member,memberadmin)
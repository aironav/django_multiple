from django.contrib import admin
from .models import ICD, Exclusion, Plan, Member, Policy, Inclusion
# Register your models here.

admin.site.register(Plan)
admin.site.register(Policy)
admin.site.register(ICD)


class addInclusion(admin.StackedInline):
    model = Inclusion
    extra = 1

class addExclusion(admin.StackedInline):
    model = Exclusion
    extra = 1

class memberadmin(admin.ModelAdmin):
    inlines = [addInclusion, addExclusion]
    filter_horizontal = ('code',)



admin.site.register(Member,memberadmin)
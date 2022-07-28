from django.contrib import admin
from .models import ICD, Exclusion, Plan, Member, Policy, Inclusion
# Register your models here.


admin.site.register(ICD)


class addInclusion(admin.StackedInline):
    model = Inclusion
    filter_horizontal = ('code',)
    extra = 1

class addExclusion(admin.StackedInline):
    model = Exclusion
    filter_horizontal = ('code',)
    extra = 1

class memberadmin(admin.ModelAdmin):
    inlines = [addInclusion, addExclusion]
   

admin.site.register(Plan,memberadmin)
admin.site.register(Policy,memberadmin)
admin.site.register(Member,memberadmin)
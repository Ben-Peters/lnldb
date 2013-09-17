from events.models import *
from django.contrib import admin

#actions
def enable_show_in_wo_form(modeladmin, request, queryset):
    queryset.update(show_in_wo_form=True)
enable_show_in_wo_form.short_description = "Make locations show up in workorder form"

def disable_show_in_wo_form(modeladmin, request, queryset):
    queryset.update(show_in_wo_form=False)
disable_show_in_wo_form.short_description = "Make locations NOT show up in Workorder form"    

class EventAdmin(admin.ModelAdmin):
    filter_horizontal = ('crew','crew_chief','org')
    
class OrgAdmin(admin.ModelAdmin):
    filter_horizontal = ('user_in_charge','assoicated_users','associated_orgs')

class LocAdmin(admin.ModelAdmin):
    list_filter = ('show_in_wo_form',)
    actions = [enable_show_in_wo_form,disable_show_in_wo_form]
admin.site.register(Location,LocAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(CCReport)
admin.site.register(Organization)
admin.site.register(Extra)
admin.site.register(ExtraInstance)

admin.site.register(Lighting)
admin.site.register(Sound)
admin.site.register(Projection)

admin.site.register(Category)

admin.site.register(Service)
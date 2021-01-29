from django.contrib import admin
from . import models as mdl
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models

admin.site.site_header = 'Mis 2020'


class PartnerAdmin(admin.ModelAdmin):
    search_fields = ['afm', 'eponymia']
    list_display = ['afm', 'eponymia']
    # list_filter = ['']


class AccountAdmin(admin.ModelAdmin):
    model = mdl.Account
    search_fields = ['code', 'per']
    list_display = ['code', 'per', 'type']


class TrandLine(admin.TabularInline):
    model = mdl.Trand
    extra = 2
    autocomplete_fields = ['account']
    search_fields = ['account__code', 'account__per']
    # raw_id_fields = ("account",)
    # formfield_overrides = {
    #     models.ForeignKey: {'widget': AutocompleteSelect(model.account, admin.site, attrs={'data-dropdown-auto-width': 'true'})},
    # }


class TranAdmin(admin.ModelAdmin):
    inlines = [TrandLine]
    list_display = ['date', 'parastatiko', 'perigrafi', 'partner']
    list_filter = ['date', 'partner']
    autocomplete_fields = ['partner']
    date_hierarchy = 'date'


admin.site.register(mdl.Account, AccountAdmin)
admin.site.register(mdl.Tran, TranAdmin)
admin.site.register(mdl.Partner, PartnerAdmin)

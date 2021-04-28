from django.contrib import admin
from django import forms
# from django.conf.locale.he import formats as el_formats
from . import models as mdl
# el_formats.DATE_FORMAT = "d/M/Y"

admin.site.site_header = 'Mis 2020'


# admin.site.register(mdl.ApasxolisiEidos)
# admin.site.register(mdl.ApasxolisiType)
# admin.site.register(mdl.ApdDetails)


class ApdDetailsLine(admin.TabularInline):
    model = mdl.ApdDetails
    extra = 1


class ApdAdmin(admin.ModelAdmin):
    inlines = [ApdDetailsLine]
    list_display = ['minas', 'etos', 'apdtype', 'ekdosi', 'misthodosies']
    list_filter = ['minas', 'etos', 'apdtype', 'ekdosi']


admin.site.register(mdl.Apd, ApdAdmin)
# admin.site.register(mdl.ApdDilosiType)


class ApodoxesTypeEfkaAdmin(admin.ModelAdmin):
    list_display = ['apodtypeefka', 'per', 'plirotees']


admin.site.register(mdl.ApodoxesTypeEfka, ApodoxesTypeEfkaAdmin)


class apoxorisiAdmin(admin.ModelAdmin):
    list_display = ['apoxorisidate', 'proslipsi', 'aptyp']
    list_filter = ['apoxorisidate', 'aptyp']


admin.site.register(mdl.Apoxorisi, apoxorisiAdmin)
# admin.site.register(mdl.ApoxorisiType)
# admin.site.register(mdl.CompanyParartima)


class CompanyParartimaInLine(admin.TabularInline):
    model = mdl.CompanyParartima
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyParartimaInLine]


admin.site.register(mdl.Company, CompanyAdmin)
# admin.site.register(mdl.CompanyType)

admin.site.register(mdl.EfkaYpok)


class EidikotitaKekInLine(admin.TabularInline):
    model = mdl.EidikotitaKek
    extra = 1


class EidkotitaAdmin(admin.ModelAdmin):
    inlines = [EidikotitaKekInLine]


admin.site.register(mdl.Eidikotita, EidkotitaAdmin)


# class EidikotitaKekAdmin(admin.ModelAdmin):
#     list_display = ['eid', 'kad', 'eidefka', 'kpk']
#     list_filter = ['eid', 'kpk']


# admin.site.register(mdl.EidikotitaKek, EidikotitaKekAdmin)


class ErgOikKatAdmin(admin.ModelAdmin):
    list_display = ['ergazomenos', 'apoetos',
                    'apomina', 'oikkattype', 'paidia']
    search_fields = ('ergazomenos', )


# admin.site.register(mdl.ErgOikKat, ErgOikKatAdmin)


class ErgOikKatInLine(admin.TabularInline):
    model = mdl.ErgOikKat
    extra = 1


class ErgazomenosAdmin(admin.ModelAdmin):
    list_display = ['epo', 'ono', 'pat', 'afm', 'amka', 'ama']
    search_fields = ('epo', 'ono', 'afm')
    inlines = [ErgOikKatInLine, ]


admin.site.register(mdl.Ergazomenos, ErgazomenosAdmin)


class ErgazomenosTypeAdmin(admin.ModelAdmin):
    list_display = ['ergtype', 'evalmisthos',
                    'evalimeromisthio', 'evaloromisthio']


# admin.site.register(mdl.ErgazomenosType, ErgazomenosTypeAdmin)


class FormulaAdmin(admin.ModelAdmin):
    list_display = ['part', 'ergt', 'mist',
                    'apodt', 'evalu', 'meresefka', 'argiaefka']
    list_filter = ['part', 'ergt', 'mist']


admin.site.register(mdl.Formula, FormulaAdmin)


class FmyDetailsLine(admin.TabularInline):
    model = mdl.FmyDetails
    extra = 1


class FmyAdmin(admin.ModelAdmin):
    inlines = [FmyDetailsLine]
    list_display = ['minas', 'etos']
    list_filter = ['minas', 'etos']


# admin.site.register(mdl.FmyDetails)
admin.site.register(mdl.Fmy, FmyAdmin)


class kpkApoInline(admin.TabularInline):
    model = mdl.KpkApo
    extra = 1


class kpkAdmin(admin.ModelAdmin):
    inlines = [kpkApoInline]
    list_display = ['kpk', 'per']


admin.site.register(mdl.Kpk, kpkAdmin)
# admin.site.register(mdl.KpkApo)

# admin.site.register(mdl.Minas)


class MishodosiaAdmin(admin.ModelAdmin):
    list_display = ['title', 'mistype', 'apomina',
                    'eosmina', 'etos', 'ekdosidate', 'has_apd', 'has_fmy']
    list_filter = ['etos', 'mistype', 'ekdosidate']


admin.site.register(mdl.Misthodosia, MishodosiaAdmin)
admin.site.register(mdl.MisthodosiaType)

# admin.site.register(mdl.OikKatType)


class ParousiaDetailsLine(admin.TabularInline):
    model = mdl.ParousiaDetails
    autocomplete_fields = ['pro']
    extra = 1


class ParousiaAdmin(admin.ModelAdmin):
    list_display = ['minas', 'etos', ]
    list_filter = ['minas', 'etos']
    # inlines = [parousiaadmindetails(202002)]
    inlines = [ParousiaDetailsLine]


admin.site.register(mdl.Parousia, ParousiaAdmin)


class ParousiaDetailsAdmin(admin.ModelAdmin):
    list_display = ['parousia', 'pro', 'ptyp', 'value']
    list_filter = ['parousia__minas', 'parousia__etos', 'pro__erg', 'ptyp']
    # inlines = [parousiaadmindetails(202002)]


admin.site.register(mdl.ParousiaDetails, ParousiaDetailsAdmin)
# admin.site.register(mdl.ParousiaType)


class ProslipsiApodoxesline(admin.TabularInline):
    model = mdl.ProslipsiApodoxes
    extra = 1


class ProslipsiAdmin(admin.ModelAdmin):
    inlines = [ProslipsiApodoxesline]
    list_display = [
        'erg',
        'proslipsidate',
        'eid',
        'ergazomenostype',
        'last_apodoxes',
        'aptyp',
        'apeid',
        'is_active'
    ]
    list_filter = ['proslipsidate', 'eid', 'erg']
    autocomplete_fields = ['erg']
    search_fields = ['erg__epo', 'erg__ono', 'erg__afm', 'proslipsidate']


admin.site.register(mdl.Proslipsi, ProslipsiAdmin)
admin.site.register(mdl.ProslipsiApodoxes)

# admin.site.register(mdl.TaftotitaType)

admin.site.register(mdl.Xora)

# from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from . import models

# app_name = 'mis'


class HomePageView(generic.TemplateView):
    template_name = 'mis/home.html'


class AboutPageView(generic.TemplateView):
    template_name = 'mis/about.html'


class ErgListView(generic.ListView):
    model = models.Ergazomenos
    context_object_name = 'ergazomenoi_list'
    template_name = 'mis/ergazomenoi.html'


class ErgDetailView(generic.DetailView):
    model = models.Ergazomenos
    template_name = 'mis/erg_detail.html'
    context_object_name = 'ergazomenos'


class ErgCreateView(CreateView):
    model = models.Ergazomenos
    template_name = 'mis/erg_edit.html'
    fields = '__all__'

    def form_valid(self, form):
        erg = form.save()  # save form
        return redirect('erg')


class ErgUpdateView(UpdateView):
    model = models.Ergazomenos
    template_name = 'mis/erg_edit.html'
    fields = '__all__'

    def form_valid(self, form):
        erg = form.save()  # save form
        return redirect('erg')


class MisListView(generic.ListView):
    model = models.Misthodosia
    context_object_name = 'misthodosies_list'
    template_name = 'mis/mis.html'


class MisDetailView(generic.DetailView):
    model = models.Misthodosia
    template_name = 'mis/mis_detail.html'
    context_object_name = 'misthodosia'


class ApdListView(generic.ListView):
    model = models.Apd
    context_object_name = 'apd_list'
    template_name = 'mis/apd.html'


class ApdDetailView(generic.DetailView):
    model = models.Apd
    template_name = 'mis/apd_detail.html'
    context_object_name = 'apd'


class FmyListView(generic.ListView):
    model = models.Fmy
    context_object_name = 'fmy_list'
    template_name = 'mis/fmy.html'


def fmy2zip(request, fmy_id):
    """Δημιουργία αρχείου ΦΜΥ"""
    fmy_period = models.Fmy.objects.get(pk=fmy_id)
    mfi, fname = fmy_period.fmy2stream()
    if mfi is None:
        messages.warning(
            request, f'Δεν υπάρχει ΦΜΥ για την περίοδο: {fmy_period} (Μήπως λόγω κορωνοιού ?)')
        return redirect('/fmy/')
    response = HttpResponse(
        mfi.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={fname}'
    messages.info(request, f'Το αρχείο {fname} αποθηκεύτηκε ...')
    return response


def apd2zip(request, apd_id):
    """Δημιουργία αρχείου ΑΠΔ"""
    apd_period = models.Apd.objects.get(pk=apd_id)
    mfi, fname = apd_period.apd2stream()
    if mfi is None:
        messages.error(
            request, f'Δεν υπάρχει ΑΠΔ για την περίοδο: {apd_period}')
        return redirect('/apd/')
    response = HttpResponse(mfi.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={fname}'
    return response

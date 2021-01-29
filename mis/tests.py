from django.test import TestCase
from django.urls import reverse
from . import models as md


class MisTest(TestCase):
    def setUp(self):
        ctype = md.CompanyType.objects.create(
            companytype='Εταιρεία',
            fmytype=1
        )
        company = md.Company.objects.create(
            epon='Δοκιμή ΕΠΕ',
            afm='123123123',
            ame='1234512345',
            doy='Α Αθηνών',
            dra='Εστιατόριο',
            ctyp=ctype
        )
        efkayp = md.EfkaYpok.objects.create(
            ypno=1242,
            ypnam='ΑΦΚΑ Αθηνών'
        )
        kentriko = md.CompanyParartima.objects.create(
            company=company,
            efkayp=efkayp,
            parp='Κεντρικό',
            parno=1,
            adodo='ΑΓΑΘΗΜΕΡΟΥ',
            adnum='23B',
            adtk='33212',
            adpol='ΑΘΗΝΑ'
        )
        dat = md.TaftotitaType.objects.create(
            tat='ΔΕΛΤΙΟ ΑΣΤΥΝΟΜΙΚΗΣ ΤΑΥΤΟΤΗΤΑΣ'
        )
        ellas = md.Xora.objects.create(
            xora='ΕΛΛΑΔΑ'
        )
        ted = md.Ergazomenos.objects.create(
            epo='ΛΑΖΑΡΟΣ',
            ono='ΘΕΟΔΩΡΟΣ',
            pat='ΚΩΝΣΤΑΝΤΙΝΟΣ',
            mit='ΣΤΑΥΡΟΥΛΑ',
            afm='046949583',
            amka='15026305175',
            ama=1234567,
            sex=1,
            gen='1963-02-15',
            xor=ellas,
            taft=dat,
            taf='ΔΑ2322',
            adodo='ΣΙΣΜΑΝΟΓΛΕΙΟΥ',
            adnum='34',
            adpol='ΒΡΙΛΗΣΣΙΑ',
            adtk='15234',
            mobile='6984123456',
            telhome='2108660623'
        )
        tamias = md.Eidikotita.objects.create(
            eid='Ταμίας'
        )
        kpk101 = md.Kpk.objects.create(
            kpk='101',
            per='IKA MIKTA'
        )
        kpk101apo = md.KpkApo.objects.create(
            kpk=kpk101,
            apo=201906,
            perg=15.75,
            peti=24.81,
            ptot=40.56
        )
        eidkek = md.EidikotitaKek.objects.create(
            eid=tamias,
            kad='5540',
            eidefka='421110',
            kpk=kpk101
        )
        aoristoy = md.ApasxolisiType.objects.create(
            aptyp='Αορίστου χρόνου'
        )
        meriki_ek_peritropis = md.ApasxolisiEidos.objects.create(
            apeid='Μερική και εκ περιτροπής',
            plires_orario=False,
            oles_ergasimes=False
        )
        imeromisthios = md.ErgazomenosType.objects.create(
            ergtype='Ημερομίσθιος',
            evalmisthos='0',
            evalimeromisthio='self.apodoxes',
            evaloromisthio="self.apodoxes * Decimal('6') / Decimal('40')"
        )
        tedpro = md.Proslipsi.objects.create(
            proslipsidate='2020-01-03',
            parartima=kentriko,
            erg=ted,
            eid=tamias,
            aptyp=aoristoy,
            apeid=meriki_ek_peritropis,
            ergazomenostype=imeromisthios,
            apodoxes=38
        )
        ian2020 = md.Minas.objects.create(
            code='01',
            minas='Ιανουάριος'
        )
        parian2020 = md.Parousia.objects.create(
            etos=2020,
            minas=ian2020
        )
        ergasimes = md.ParousiaType.objects.create(
            parousiatype='Εργάσιμες'
        )
        pdian2020 = md.ParousiaDetails.objects.create(
            parousia=parian2020,
            pro=tedpro,
            ptyp=ergasimes,
            value=4,
        )

    def test_01(self):
        co = md.Company.objects.get(id=1)
        self.assertEqual(co.epon, 'Δοκιμή ΕΠΕ')
        self.assertEqual(co.afm, '123123123')
        self.assertEqual(co.ame, '1234512345')

    def test_02(self):
        resp = self.client.get(reverse('erg'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'mis/ergazomenoi.html')

    def test_03(self):
        pro = md.Proslipsi.objects.get(id=1)
        print(pro.erg.epo)

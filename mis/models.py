from decimal import Decimal
from django.db import models
from django.db.models import Sum, Max
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, int_list_validator
from django.urls import reverse
from utils.apd_functions import fill_spaces, fill_spaces_cut, decimal2flat, isodate2flat, leading_zeroes
from utils.validators import is_afm, is_amka
from utils.foros import calc_foros_eea_periodou
from utils.ziputil import create_zip, create_zip_stream
from mispdf.txt2pdf import txt2pdf


class ApdDilosiType(models.Model):
    """1=Κανονική, 2=Έκτακτη, 3=Επανυποβολή, 4=Συμπληρωματική"""
    apddiltyp = models.CharField('Τύπος Δήλωσης', max_length=50, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'ΑΠΔ ΤΥΠΟΣ ΔΗΛΩΣΗΣ'
        verbose_name_plural = 'ΑΠΔ ΤΥΠΟΙ ΔΗΛΩΣΗΣ'

    def code(self):
        return f'{self.id:02d}'
    code.short_description = "Κωδικός τύπου δήλωσης ΑΠΔ"

    def __str__(self):
        return f'{self.id:02d}-{self.apddiltyp}'


class ApasxolisiEidos(models.Model):
    """Πλήρης, Μερική, Εκ'περιτροπής, Μερική και εκ'περιτροπής"""
    apeid = models.CharField('Είδος απασχόλησης', max_length=50, unique=True)
    plires_orario = models.BooleanField('Πλήρες Ωράριο', default=False)
    oles_ergasimes = models.BooleanField('Όλες εργάσιμες', default=False)

    class Meta:
        ordering = ['id']
        verbose_name = 'ΑΠΑΣΧΟΛΗΣΗ ΕΙΔΟΣ'
        verbose_name_plural = 'ΠΡΟΣΛΗΨΕΙΣ-ΕΙΔΟΣ ΑΠΑΣΧΟΛΗΣΗΣ'

    def __str__(self):
        return f'{self.apeid}'

    def plires_orario_int(self):
        if self.plires_orario:
            return 1
        return 0

    def oles_ergasimes_int(self):
        if self.oles_ergasimes:
            return 1
        return 0


class ApasxolisiType(models.Model):
    """Αορίστου, ορισμένου, έργου"""
    aptyp = models.CharField('Τύπος απασχόλησης', max_length=50)

    class Meta:
        ordering = ['id']
        verbose_name = 'ΑΠΑΣΧΟΛΗΣΗ ΤΥΠΟΣ'
        verbose_name_plural = 'ΠΡΟΣΛΗΨΕΙΣ-ΤΥΠΟΣ ΑΠΑΣΧΟΛΗΣΗΣ'

    def __str__(self):
        return f'{self.aptyp}'


class Minas(models.Model):
    """Μήνας"""
    code = models.CharField(
        'Κωδικός Περιόδου', max_length=2, unique=True)
    minas = models.CharField('Όνομα', max_length=12, unique=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'ΜΗΝΑΣ'
        verbose_name_plural = 'ΜΗΝΕΣ'

    def __str__(self):
        return f'{self.minas}'


class EfkaYpok(models.Model):
    """Υποκατάστημα ΙΚΑ/ΕΦΚΑ"""
    ypno = models.IntegerField('Κωδικός Υποκαταστήματος ΕΦΚΑ', unique=True)
    ypnam = models.CharField(
        'Ονομασία Υποκαταστήματος ΕΦΚΑ', max_length=50, unique=True)

    class Meta:
        ordering = ['ypnam']
        verbose_name = 'ΕΦΚΑ ΥΠΟΚΑΤΑΣΤΗΜΑ'
        verbose_name_plural = 'ΕΦΚΑ ΥΠΟΚΑΤΑΣΤΗΜΑΤΑ'

    def __str__(self):
        return f'{self.ypno:3}-{self.ypnam}'


class CompanyType(models.Model):
    """Εταιρία, Φυσικό πρόσωπο"""
    companytype = models.CharField('Τύπος', max_length=15, unique=True)
    fmytype = models.IntegerField('Τύπος για ΦΜΥ', unique=True)

    class Meta:
        ordering = ['companytype']
        verbose_name = 'ΤΥΠΟΣ ΕΠΙΧΕΙΡΗΣΗΣ'
        verbose_name_plural = 'ΤΥΠΟΙ ΕΠΙΧΕΙΡΗΣΗΣ'

    def __str__(self):
        return f'{self.companytype}'


class Company(models.Model):
    """Εταιρεία"""
    ctyp = models.ForeignKey(
        CompanyType, verbose_name='Τύπος', default=1, on_delete=models.PROTECT)
    epon = models.CharField('Επωνυμία', max_length=80, unique=True)
    name = models.CharField('Όνομα (για φυσικά πρόσωπα)',
                            max_length=30, blank=True)
    patr = models.CharField('Όνομα πατέρα (για φυσικά πρόσωπα)',
                            max_length=30, blank=True)
    afm = models.CharField('ΑΦΜ', max_length=9, unique=True)
    ame = models.CharField('AME', max_length=10, unique=True)
    doy = models.CharField('ΔΟΥ', max_length=50)
    dra = models.CharField('Δραστηριότητα', max_length=50)

    @property
    def eponymia(self):
        if self.name:
            return f"{self.epon} {self.name}"
        return f'{self.epon}'

    @property
    def eponymia_afm(self):
        if self.name:
            return f"{self.epon} {self.name}, ΑΦΜ:{self.afm}"
        return f'{self.epon}, ΑΦΜ:{self.afm}'

    class Meta:
        verbose_name = 'ΕΠΙΧΕΙΡΗΣΗ'
        verbose_name_plural = 'ΕΠΙΧΕΙΡΗΣΕΙΣ'

    def __str__(self):
        return f'{self.epon} {self.name}'


class CompanyParartima(models.Model):
    """Παράρτημα εταιρείας"""
    company = models.ForeignKey(
        Company, verbose_name='Εταιρεία', on_delete=models.PROTECT
    )
    efkayp = models.ForeignKey(
        EfkaYpok, verbose_name='Υπ/μα ΕΦΚΑ', on_delete=models.PROTECT
    )
    parp = models.CharField('Ονομασία', max_length=50)
    parno = models.IntegerField('Αριθμός παραρτήματος')
    adodo = models.CharField('Διεύθυνση Οδός', max_length=50)
    adnum = models.CharField('Διεύθυνση Αριθμός', max_length=10)
    adtk = models.CharField('Διεύθυνση Τ.Κ.', max_length=5)
    adpol = models.CharField('Διεύθυνση Πόλη', max_length=30)

    class Meta:
        ordering = ['company', 'parno']
        unique_together = ('company', 'parno')
        verbose_name = 'ΕΠΙΧΕΙΡΗΣΗ-ΠΑΡΑΡΤΗΜΑ'
        verbose_name_plural = 'ΕΠΙΧΕΙΡΗΣΕΙΣ-ΠΑΡΑΡΤΗΜΑΤΑ'

    def __str__(self):
        return f'{self.company.epon} : {self.parp}'


class Kpk(models.Model):
    """Κωδικός Πακέτου Κάλυψης ΕΦΚΑ"""
    kpk = models.CharField('ΚΠΚ', max_length=4, unique=True)
    per = models.CharField('Περιγραφή', max_length=50, unique=True)

    class Meta:
        ordering = ['kpk']
        verbose_name = 'ΕΦΚΑ ΠΑΚΕΤΟ ΚΑΛΥΨΗΣ'
        verbose_name_plural = 'ΕΦΚΑ ΠΑΚΕΤΑ ΚΑΛΥΨΗΣ'

    def kpk_periodou(self, period):
        kpk_periods = self.kpkapo_set.all()
        kpk_max = None
        period_max = 190001  # Ελάχιστη περίοδος το 1900 01
        for kpk_period in kpk_periods:
            if kpk_period.apo <= period:
                if period_max < kpk_period.apo:
                    period_max = kpk_period.apo
                    kpk_max = kpk_period
        return kpk_max

    def kpk_per_test(self, period):
        try:
            return self.kpkapo_set.get(apo=self.kpkapo_set.filter(apo__lte=period).aggregate(Max('apo'))['apo__max'])
        except Exception:
            return None

    def __str__(self):
        return f'{self.kpk} {self.per}'


class KpkApo(models.Model):
    kpk = models.ForeignKey(
        Kpk, verbose_name='Πακέτο κάλυψης', on_delete=models.PROTECT
    )
    apo = models.IntegerField('Από περίοδο')
    perg = models.DecimalField(
        'Ποσοστό εργαζομένου', max_digits=4, decimal_places=2
    )
    peti = models.DecimalField(
        'Ποσοστό εργοδότη', max_digits=4, decimal_places=2
    )
    ptot = models.DecimalField(
        'Συνολικό ποσοστό', max_digits=4, decimal_places=2
    )

    def is_correct(self):
        return self.ptot == (self.perg + self.peti)
    is_correct.boolean = True
    is_correct.short_description = 'Συμφωνία'

    class Meta:
        ordering = ['kpk', 'apo']
        unique_together = ('kpk', 'apo')
        verbose_name = 'ΠΑΚΕΤΟ ΚΑΛΥΨΗΣ ΠΟΣΟΣΤΟ'
        verbose_name_plural = 'ΠΑΚΕΤΑ ΚΑΛΥΨΗΣ ΠΟΣΟΣΤΑ '

    def __str__(self):
        return f'{self.kpk} {self.apo} {self.perg}% {self.peti}% {self.ptot}%'


class Eidikotita(models.Model):
    """Ειδικότητα εργασίας"""
    eid = models.CharField('Ειδικότητα', max_length=70, unique=True)

    @ property
    def all_kpk(self):
        return ', '.join([str(i) for i in self.kpkkadeid.all()])

    @ property
    def kpk_obj(self):
        return self.kpkkadeid.all()

    def eid_keks(self):
        return self.eidikotitakek_set.all()

    class Meta:
        ordering = ['eid']
        verbose_name = 'ΕΙΔΙΚΟΤΗΤΑ'
        verbose_name_plural = 'ΠΡΟΣΛΗΨΕΙΣ-ΕΙΔΙΚΟΤΗΤΕΣ'

    def __str__(self):
        return f'{self.eid}'


class EidikotitaKek(models.Model):
    """Ειδικότητα-ΚΑΔ-ΕΙΔ-ΚΠΚ"""
    eid = models.ForeignKey(
        Eidikotita, verbose_name='Ειδικότητα', on_delete=models.PROTECT)
    kad = models.CharField('ΚΑΔ', max_length=4)
    eidefka = models.CharField('Κωδικός Ειδικότητας', max_length=6)
    kpk = models.ForeignKey(Kpk, verbose_name='ΚΠΚ',
                            on_delete=models.PROTECT)

    def kpk_periodou(self, period):
        return self.kpk.kpk_periodou(period)

    class Meta:
        ordering = ('kad', 'eid', 'kpk')
        unique_together = ('kad', 'eid', 'kpk')
        verbose_name = 'ΕΙΔΙΚΟΤΗΤΑ-ΚΠΚ'
        verbose_name_plural = 'ΠΡΟΣΛΗΨΕΙΣ-ΕΙΔΙΚΟΤΗΤΕΣ-ΚΠΚ'

    def __str__(self):
        return f'{self.eid} {self.kad} {self.eidefka} {self.kpk}'


class Xora(models.Model):
    xora = models.CharField('Χώρα', max_length=80, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'ΧΩΡΑ'
        verbose_name_plural = 'ΧΩΡΕΣ'

    def __str__(self):
        return f'{self.xora}'


class TaftotitaType(models.Model):
    tat = models.CharField('Τύπος ταυτότητας', max_length=60, unique=True)

    class Meta:
        ordering = ['tat']
        verbose_name = 'ΤΥΠΟΣ ΤΑΥΤΟΤΗΤΑΣ'
        verbose_name_plural = 'ΤΥΠΟΙ ΤΑΥΤΟΤΗΤΑΣ'

    def __str__(self):
        return f'{self.tat}'


class OikKatType(models.Model):
    """Οικογενειακή κατάσταση : άγαμος, έγγαμος, χωρισμένος κλπ"""
    oik = models.CharField('Οικογενειακή κατάσταση',
                           max_length=60, unique=True)

    class Meta:
        ordering = ['oik']
        verbose_name = 'ΤΥΠΟΣ ΟΙΚΟΓΕΝΕΙΑΚΗΣ ΚΑΤΑΣΤΑΣΗΣ'
        verbose_name_plural = 'ΤΥΠΟΙ ΟΙΚΟΓΕΝΕΙΑΚΗΣ ΚΑΤΑΣΤΑΣΗΣ'

    def __str__(self):
        return f'{self.oik}'


class Ergazomenos(models.Model):
    """Εργαζόμενοι"""
    SEX = (
        (1, 'Αντρας'),
        (2, 'Γυναίκα')
    )
    epo = models.CharField('Επώνυμο', max_length=30)
    ono = models.CharField('Όνομα', max_length=30)
    pat = models.CharField('Όνομα πατέρα', max_length=30)
    mit = models.CharField('Όνομα μητέρας', max_length=30)
    afm = models.CharField('ΑΦΜ', max_length=9,
                           unique=True, validators=[is_afm])
    amka = models.CharField('ΑMKA', max_length=11,
                            unique=True, validators=[is_amka])
    ama = models.IntegerField('Αρ.Μητρώου ΙΚΑ')
    sex = models.IntegerField('Φύλο', default=1, choices=SEX)
    gen = models.DateField('Ημ/νία γέννησης')
    xor = models.ForeignKey(
        Xora, verbose_name='Χώρα', default=1, on_delete=models.PROTECT
    )
    taft = models.ForeignKey(
        TaftotitaType, verbose_name='Τύπος ταυτότητας',
        default=1,
        on_delete=models.PROTECT
    )
    taf = models.CharField('Αριθμός ταυτότητας', max_length=20, unique=True)
    adodo = models.CharField('Διεύθυνση οδός', max_length=60)
    adnum = models.CharField('Διεύθυνση αριθμός', max_length=10)
    adpol = models.CharField('Διεύθυνση πόλη', max_length=60)
    adtk = models.CharField('Διεύθυνση T.K.', max_length=5)
    mobile = models.CharField('Κινητό τηλέφωνο', max_length=10)
    telhome = models.CharField('Tηλέφωνο οικίας', max_length=10, blank=True)

    @property
    def onomatep(self):
        return f"{self.epo} {self.ono}"

    @property
    def erglist(self):
        return f"{self.epo} {self.ono} {self.afm}"

    def active_for_period(self, period):
        proslipseis = self.proslipsi_set.all()
        for prs in proslipseis:
            if prs.active_for_period(period):
                return True
        return False

    def is_active(self):
        proslipseis = self.proslipsi_set.all()
        for prs in proslipseis:
            if prs.is_active():
                return True
        return False
    is_active.boolean = True

    def ama_txt(self):
        return f'{self.ama}'
    ama_txt.short_description = "AMA"

    def paidia(self, period):
        assert period >= 190001
        oikats = self.ergoikkat_set.all()
        oik_max = None
        period_max = 190001  # Ελάχιστη περίοδος το 1900 01
        paidia = 0
        for oikat in oikats:
            oikper = oikat.periodos()
            if oikper <= period:
                if period_max < oikper:
                    period_max = oikper
                    paidia = oikat.paidia
        return paidia

    class Meta:
        ordering = ['epo', 'ono', 'pat', 'mit']
        unique_together = ('epo', 'ono', 'pat', 'mit')
        verbose_name = 'ΕΡΓΑΖΟΜΕΝΟΣ'
        verbose_name_plural = 'ΕΡΓΑΖΟΜΕΝΟΙ'

    def __str__(self):
        return f'{self.epo} {self.ono}'

    def get_absolute_url(self):
        return reverse('erg_detail', args=[str(self.id)])


class ErgOikKat(models.Model):
    """Άν δεν υπάρχει εγραφή οικογενειακής κατάστασης εδώ,
       θεωρούμε ότι ο εργαζόμενος είναι άγαμος χωρίς παιδιά.
    """
    ergazomenos = models.ForeignKey(
        Ergazomenos, verbose_name='Εργαζόμενος', on_delete=models.PROTECT)
    apoetos = models.IntegerField('Από Έτος', default=2020)
    apomina = models.ForeignKey(
        Minas, verbose_name='Από Μήνα', on_delete=models.PROTECT)
    oikkattype = models.ForeignKey(
        OikKatType, verbose_name='Οικογενειακή κατάσταση', on_delete=models.PROTECT)
    paidia = models.IntegerField('Παιδιά', default=0)

    def periodos(self):
        """ReturnsYYYYMM as integer"""
        return int(str(self.apoetos) + self.apomina.code)

    class Meta:
        ordering = ['ergazomenos', 'apoetos', 'apomina']
        unique_together = ('apoetos', 'apomina', 'ergazomenos')
        verbose_name = 'ΑΛΛΑΓΗ ΟΙΚΟΓΕΝΕΙΑΚΗΣ ΚΑΤΑΣΤΑΣΗΣ'
        verbose_name_plural = 'ΑΛΛΑΓΕΣ ΟΙΚΟΓΕΝΕΙΑΚΗΣ ΚΑΤΑΣΤΑΣΗΣ'

    def __str__(self):
        return f'{self.ergazomenos} {self.apoetos} {self.apomina} {self.oikkattype} {self.paidia}'


class ApodoxesTypeEfka(models.Model):
    """Τύπος αποδοχών Εφκα (01=Τακτικες, 03=Δωρο Χριστ., 04=Δώρο Πάσχα κλπ)"""
    apodtypeefka = models.CharField('Κωδικός ΑΠΔ', max_length=3, unique=True)
    per = models.CharField('Περιγραφή', max_length=60, unique=True)
    plirotees = models.BooleanField('Αποδοχές πληρωτέες', default=True)

    class Meta:
        ordering = ['apodtypeefka']
        verbose_name = 'ΕΦΚΑ ΤΥΠΟΣ ΜΙΣΘΟΔΟΣΙΑΣ'
        verbose_name_plural = 'ΕΦΚΑ ΤΥΠΟΙ ΜΙΣΘΟΔΟΣΙΑΣ'

    def __str__(self):
        return f'{self.apodtypeefka}-{self.per}'


class ParousiaType(models.Model):
    """
    Τύπος παρουσίας
    """
    parousiatype = models.CharField('Περιγραφή', max_length=60, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'ΠΑΡΟΥΣΙΕΣ ΤΥΠΟΣ'
        verbose_name_plural = 'ΠΑΡΟΥΣΙΕΣ ΤΥΠΟΙ'

    def __str__(self):
        return f'{self.parousiatype}'


class ErgazomenosType(models.Model):
    """Μισθωτός / Ημερομίσθιος / Ωρομίσθιος"""
    ergtype = models.CharField('Τύπος εργαζομένου', max_length=12, unique=True)
    evalmisthos = models.CharField('Μισθός', max_length=100)
    evalimeromisthio = models.CharField('Ημερομίσθιο', max_length=100)
    evaloromisthio = models.CharField('Ωρομίσθιο', max_length=100)

    class Meta:
        ordering = ('id',)
        verbose_name = 'ΕΡΓΑΖΟΜΕΝΟΣ ΤΥΠΟΣ'
        verbose_name_plural = 'ΠΡΟΣΛΗΨΕΙΣ-ΤΥΠΟΣ ΕΡΓΑΖΟΜΕΝΟΥ'

    def __str__(self):
        return f'{self.ergtype}'


class Proslipsi(models.Model):
    """Πρόσληψη"""
    proslipsidate = models.DateField('Ημ/νία πρόσληψης')
    parartima = models.ForeignKey(
        CompanyParartima, verbose_name='Παράρτημα', on_delete=models.PROTECT)
    erg = models.ForeignKey(
        Ergazomenos, verbose_name='Εργαζόμενος', on_delete=models.PROTECT)
    eid = models.ForeignKey(
        Eidikotita, verbose_name='Ειδικότητα', on_delete=models.PROTECT)
    aptyp = models.ForeignKey(
        ApasxolisiType, verbose_name='Τύπος απασχόλησης', on_delete=models.PROTECT)
    apliksi = models.DateField('Ημερομηνία λήξης', blank=True, null=True)
    apeid = models.ForeignKey(
        ApasxolisiEidos, verbose_name='Είδος απασχόλησης', on_delete=models.PROTECT)
    ergazomenostype = models.ForeignKey(
        ErgazomenosType, verbose_name='Τύπος εργαζομένου', on_delete=models.PROTECT)
    apodoxes = models.DecimalField(
        'Αποδοχές', max_digits=8, decimal_places=2)

    def misthos(self):
        return round(eval(self.ergazomenostype.evalmisthos), 2)
    misthos.short_description = "Μισθός"

    def imeromisthio(self):
        return round(eval(self.ergazomenostype.evalimeromisthio), 2)
    imeromisthio.short_description = "Ημερομίσθιο"

    def imeromisthio_for_apd(self):
        if self.ergazomenostype.id == 2:
            return self.imeromisthio()
        return 0

    def oromisthio(self):
        return round(eval(self.ergazomenostype.evaloromisthio), 2)
    oromisthio.short_description = "Ωρομίσθιο"

    # @property
    # def typos_erg(self):
    #     ertypeobject = get_erg_type(self.ergtyp)
    #     return ertypeobject.typ

    # @property
    # def erg_obj(self):
    #     return get_erg_type(self.ergtyp)

    def energos_eos(self):
        try:
            return f'αποχώρησε στις {self.apoxorisi.apdate}'
        except ObjectDoesNotExist:
            return 'ενεργός'
    energos_eos.short_description = "Κατάσταση"

    def active_for_period(self, period):
        ap_date = None
        try:
            ap_date = self.apoxorisi.apoxorisidate
        except ObjectDoesNotExist:
            ap_date = None
        if ap_date:
            yyyy, mm, _ = ap_date.isoformat().split('-')
            return self.period_proslipsis <= period <= int(f'{yyyy}{mm}')
        else:
            return self.period_proslipsis <= period

    def is_active(self):
        try:
            self.apoxorisi.apoxorisidate
            return False
        except ObjectDoesNotExist:
            return True
    is_active.short_description = 'Ενεργός'
    is_active.boolean = True

    @property
    def is_activen(self):
        try:
            self.apoxorisi.apoxorisidate
            return False
        except ObjectDoesNotExist:
            return True

    @property
    def period_proslipsis(self):
        yyyy, mm, _ = self.proslipsidate.isoformat().split('-')
        return int(f'{yyyy}{mm}')

    @property
    def period_apoxorisis(self):
        try:
            yyyy, mm, _ = self.apoxorisi.apoxorisidate.isoformat().split('-')
            return int(f'{yyyy}{mm}')
        except ObjectDoesNotExist:
            return 999912

    def last_apodoxes(self):
        set_apodoxes = list(self.proslipsiapodoxes_set.all())
        if set_apodoxes:
            return set_apodoxes[-1].apodoxes
        else:
            return self.apodoxes
    last_apodoxes.short_description = 'Αποδοχές'

    class Meta:
        ordering = ['-proslipsidate', 'erg']
        unique_together = ('proslipsidate', 'erg')
        verbose_name = 'ΕΡΓΑΖΟΜΕΝΟΣ ΠΡΟΣΛΗΨΗ'
        verbose_name_plural = 'ΕΡΓΑΖΟΜΕΝΟΙ ΠΡΟΣΛΗΨΕΙΣ'

    def __str__(self):
        return f'{self.erg} {self.proslipsidate}'


class ProslipsiApodoxes(models.Model):
    """Για την παρακολούθηση αλλαγών σε αποδοχές και τύπο εργαζομένου"""
    proslipsi = models.ForeignKey(
        Proslipsi, verbose_name='Πρόσληψη', on_delete=models.PROTECT)
    apoetos = models.IntegerField('Από Έτος', default=2020)
    apomina = models.ForeignKey(
        Minas, verbose_name='Από Μήνα', on_delete=models.PROTECT)
    ergtyp = models.ForeignKey(
        ErgazomenosType, verbose_name='Τύπος', on_delete=models.PROTECT)
    apodoxes = models.DecimalField(
        'Αποδοχές', max_digits=8, decimal_places=2)

    class Meta:
        ordering = ['proslipsi', 'apoetos', 'apomina']
        unique_together = ('apoetos', 'apomina', 'proslipsi')
        verbose_name = 'ΑΛΛΑΓΗ ΑΠΟΔΟΧΩΝ'
        verbose_name_plural = 'ΑΛΛΑΓΕΣ ΑΠΟΔΟΧΩΝ'

    def __str__(self):
        return f'{self.apoetos} {self.apomina} {self.proslipsi} {self.ergtype} {self.apodoxes}'


class ApoxorisiType(models.Model):
    """Οικιοθελής, απόλυση, συνταξιοδότηση κλπ"""
    aptyp = models.CharField('Τύπος αποχώρησης', max_length=50, unique=True)

    class Meta:
        ordering = ['aptyp']
        verbose_name = 'ΤΥΠΟΣ ΑΠΟΧΩΡΗΣΗΣ'
        verbose_name_plural = 'ΤΥΠΟΙ ΑΠΟΧΩΡΗΣΗΣ'

    def __str__(self):
        return f'{self.aptyp}'


class Apoxorisi(models.Model):
    """Αποχώρηση εργαζομένου"""
    apoxorisidate = models.DateField('Ημερομηνία αποχώρησης')
    proslipsi = models.OneToOneField(
        Proslipsi, verbose_name='Πρόσληψη', on_delete=models.PROTECT)
    aptyp = models.ForeignKey(
        ApoxorisiType, verbose_name='Τύπος αποχώρησης', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-apoxorisidate', 'proslipsi']
        verbose_name = 'ΕΡΓΑΖΟΜΕΝΟΣ-ΠΡΟΣΛΗΨΗ-ΑΠΟΧΩΡΗΣΗ'
        verbose_name_plural = 'ΕΡΓΑΖΟΜΕΝΟΙ-ΠΡΟΣΛΗΨΕΙΣ-ΑΠΟΧΩΡΗΣΕΙΣ'

    def __str__(self):
        return f'{self.apoxorisidate} {self.proslipsi.erg} (πρόσληψη: {self.proslipsi.proslipsidate})'


class Parousia(models.Model):
    etos = models.IntegerField('Έτος', default=2020)
    minas = models.ForeignKey(
        Minas, verbose_name='Μήνας', on_delete=models.PROTECT)

    def periodos(self):
        """ReturnsYYYYMM as integer"""
        return int(str(self.etos) + self.minas.code)

    periodos.short_description = "Περίοδος"

    @property
    def number_of_lines(self):
        return len(self.parousiadetails_set.all())

    def number_of_ergazomenoi(self):
        ergset = set()
        for pard in self.parousiadetails_set.all():
            ergset.add(pard.pro.erg)
        return len(ergset)
    number_of_ergazomenoi.short_description = "Αριθμός εργαζομένων"

    def number_per_partype(self):
        found = {}
        for pard in self.parousiadetails_set.all():
            per = pard.ptyp.per
            found[per] = found.get(per, 0) + pard.value
        return found
    number_per_partype.short_description = "tots"

    class Meta:
        ordering = ['-etos', '-minas']
        verbose_name = 'ΠΑΡΟΥΣΙΑ'
        verbose_name_plural = 'ΠΑΡΟΥΣΙΕΣ'

    def __str__(self):
        return f'{self.etos} {self.minas}'


class ParousiaDetails(models.Model):
    parousia = models.ForeignKey(
        Parousia, verbose_name='Περίοδος', on_delete=models.PROTECT)
    pro = models.ForeignKey(
        Proslipsi,
        verbose_name='Εργαζόμενος',
        on_delete=models.PROTECT,
    )
    ptyp = models.ForeignKey(
        ParousiaType, verbose_name='Τύπος παρουσίας', on_delete=models.PROTECT)
    value = models.IntegerField('Ποσότητα', default=0)
    apo = models.DateField('Από', blank=True, null=True)
    eos = models.DateField('Εως', blank=True, null=True)

    def kratiseis_enos(self):
        perio = self.parousia.periodos()
        apodoxes = self.apod()
        eidikotita = self.pro.eid
        ergtype = self.pro.ergtyp
        kratiseis = 0
        for eid_kek in eidikotita.eid_keks():
            kpk = eid_kek.kpk_periodou(perio)
            kratiseis += round(kpk.perg * apodoxes / Decimal(100), 2)
        return kratiseis
    kratiseis_enos.short_description = "Κρατήσεις Εργαζομένου"

    def apod(self):
        val = Decimal(self.value)
        misthos = self.pro.misthos()
        imeromisthio = self.pro.imeromisthio()
        oromisthio = self.pro.oromisthio()
        return eval(self.ptyp.formula)
    apod.short_description = "Αποδ"

    def periodos(self):
        return self.parousia.periodos()
    periodos.short_description = "Περίοδος"

    class Meta:
        ordering = ['parousia', 'pro', 'ptyp']
        unique_together = ('parousia', 'pro', 'ptyp', 'apo')
        verbose_name = 'ΠΑΡΟΥΣΙΑ ΑΝΑΛΥΤΙΚΑ'
        verbose_name_plural = 'ΠΑΡΟΥΣΙΕΣ ΑΝΑΛΥΤΙΚΑ'

    def __str__(self):
        return f'{self.parousia.periodos()} {self.pro} {self.ptyp} {self.apo} {self.eos} {self.value}'


class MisthodosiaType(models.Model):
    """Τακτικές αποδοχές , Δ.Πάσχα, Επ.Αδείας κλπ"""
    mistype = models.CharField('Τύπος Μισθοδοσίας', max_length=50, unique=True)
    barytis = models.DecimalField(
        'Βαρύτητα', max_digits=5, decimal_places=1, default=14)

    class Meta:
        ordering = ['id']
        verbose_name = 'ΜΙΣΘΟΔΟΣΙΑ-ΤΥΠΟΣ'
        verbose_name_plural = 'ΜΙΣΘΟΔΟΣΙΑ-ΤΥΠΟΙ'

    def __str__(self):
        return f'{self.mistype}'


class Misthodosia(models.Model):
    etos = models.IntegerField('Έτος', default=2020)
    mistype = models.ForeignKey(
        MisthodosiaType,
        verbose_name='Τύπος μισθοδοσίας',
        on_delete=models.PROTECT)
    apomina = models.ForeignKey(
        Minas,
        verbose_name='Από Μήνα',
        related_name='MinasApo',
        on_delete=models.PROTECT)
    eosmina = models.ForeignKey(
        Minas,
        verbose_name='Έως Μήνα',
        related_name='MinasEos',
        on_delete=models.PROTECT)
    ekdosidate = models.DateField('Ημερομηνία έκδοσης')

    def clean(self):
        if (self.mistype.id == 1) and (self.apomina != self.eosmina):
            raise ValidationError(
                'Δεν επιτρέπεται για Τακτικές αποδοχές πάνω από μια περίοδος')

    def title(self):
        if self.apomina == self.eosmina:
            return f"{self.apomina} {self.etos} ({self.ekdosidate.strftime('%d/%m/%Y')})"
        else:
            return f"{self.mistype} {self.etos} ({self.ekdosidate.strftime('%d/%m/%Y')})"
        title.short_description = 'Μισθοδοσία'

    def periodos(self):
        """ReturnsYYYYMM as integer"""
        return int(str(self.etos) + self.eosmina.code)

    def has_fmy(self):
        try:
            self.fmydetails
            return True
        except Exception:
            return False
    has_fmy.short_description = 'ΦΜΥ'
    has_fmy.boolean = True

    def has_apd(self):
        try:
            self.apddetails
            return True
        except Exception:
            return False
    has_apd.short_description = 'ΑΠΔ'
    has_apd.boolean = True

    class Meta:
        ordering = ['-ekdosidate']
        unique_together = ('etos', 'mistype', 'apomina')
        verbose_name = 'ΜΙΣΘΟΔΟΣΙΑ'
        verbose_name_plural = 'ΜΙΣΘΟΔΟΣΙΕΣ'

    def __str__(self):
        return self.title()

    def calc_misthodosia(self):
        parousiesheads = Parousia.objects.filter(
            etos=self.etos, minas__gte=self.apomina, minas__lte=self.eosmina)
        pros = {}
        # 1o loop για άθροιση παρουσιών ανά πρόσληψη-τύπο παρουσίας
        # Για κάθε παρουσία που βρίσκουμε στο αρχείο
        #    Με βάση την πρόσληψη και τον τύπο παρουσίας
        #        αθροίζουμε τις τιμές της παρουσίας
        # Τα πεδία apo και eos έχουν νόημα μόνο για παρουσίες τύπου 1
        for parousiahead in parousiesheads:
            parousies = parousiahead.parousiadetails_set.all()
            for par in parousies:
                pros[par.pro] = pros.get(par.pro, {})
                pros[par.pro][par.ptyp] = pros[par.pro].get(
                    par.ptyp, {'val': 0, 'apo': '', 'eos': ''})
                if self.mistype.id == 1:
                    pros[par.pro][par.ptyp]['apo'] = par.apo or ''
                    pros[par.pro][par.ptyp]['eos'] = par.eos or ''
                pros[par.pro][par.ptyp]['val'] += par.value
        res = {}
        # 2ο loop για υπολογισμό αποδοχών και συγκέντρωση αθροιστικά ανά
        # ανά εργαζόμενο-τύπο μισθοδοσίας
        for pro, prod in pros.items():
            misthos = pro.misthos()
            imeromisthio = pro.imeromisthio()
            oromisthio = pro.oromisthio()
            # eidikotita = pro.eid
            for ptyp, ptypd in prod.items():
                try:
                    formula = Formula.objects.get(
                        part=ptyp,
                        ergt=pro.ergazomenostype,
                        mist=self.mistype
                    )
                except Exception:
                    print(
                        f"formula for {ptyp}, "
                        f"{pro.ergazomenostype} "
                        f"{self.mistype} does not exist"
                    )
                    continue
                val = ptypd['val']
                # Εδώ γίνεται ο υπολογισμός των αποδοχών
                apodoxes = round(eval(formula.evalu), 2)
                if apodoxes == 0:
                    continue
                apod_type = formula.apodt
                tmeres = val if formula.meresefka else 0
                targia = val if formula.argiaefka else 0
                res[pro] = res.get(pro, {})
                res[pro][apod_type] = res[pro].get(
                    apod_type,
                    {'apod': 0, 'meres': 0, 'argia': 0, 'apo': '', 'eos': ''}
                )
                res[pro][apod_type]['apod'] += apodoxes
                res[pro][apod_type]['meres'] += tmeres
                res[pro][apod_type]['argia'] += targia
                res[pro][apod_type]['apo'] = ptypd['apo']
                res[pro][apod_type]['eos'] = ptypd['eos']
                # {'enos': 0, 'etis': 0, 'total': 0}
        # 3ο loop για υπολογισμό κρατήσεων ανά εργαζόμενο - τύπο μισθοδοσίας
        # και ΚΑΔ-ΕΙΔ_ΚΠΚ. Καλύπουμε και την περίπτωση που ένας εργαζόμενος
        # έχει παραπάνω από ένα ΚΠΚ (π.χ. επικουρικό ταμείο έξτρα)
        for pro, apod in res.items():
            for aptype, vals in apod.items():
                vals['kratiseis'] = {}
                for eid_kek in pro.eid.eid_keks():
                    kpk = eid_kek.kpk_periodou(self.periodos())
                    kr_enos = round(kpk.perg * vals['apod'] / Decimal(100), 2)
                    kr_total = round(kpk.ptot * vals['apod'] / Decimal(100), 2)
                    kr_etis = kr_total - kr_enos
                    vals['kratiseis'][eid_kek] = {
                        'enos': kr_enos, 'etis': kr_etis, 'total': kr_total}
        # Το res έχει την δομή:
        # {
        #  {obj_proslipsi: {
        #     obj_apodoxestypeefka: {
        #         'apod': 0,
        #         'meres': 0,
        #         'argia': 0,
        #         'apo': '',
        #         'eos': '',
        #         'kratiseis': {
        #             obj_eidikotitakek: {
        #                 'enos': 0,
        #                 'etis': 0,
        #                 'total': 0
        #             }
        #         }
        #     }
        #  },
        # ...
        # }
        return res

    def calc_misthodosia_foroi(self):
        res = self.calc_misthodosia()
        head = {
            'onomatep': 'ΟΝΟΜΑΤΕΠΩΝΥΜΟ',
            'eid': 'ΕΙΔΙΚΟΤΗΤΑ',
            'imeromisthio': 'ΗΜ/ΣΘΙΟ',
            'meres': 'ΜΕΡΕΣ',
            'apodoxes': 'ΑΠΟΔΟΧΕΣ',
            'kr_enos': 'ΕΡΓ/ΝΟΣ',
            'kr_etis': 'ΕΡΓ/ΤΗΣ',
            'kr_total': 'ΣΥΝΟΛΟ',
            'foros': 'Φ.Μ.Υ.',
            'eea': 'ΕΕΑ',
            'pliroteo': 'ΠΛΗΡΩΤΕΟ'
        }
        lines = []
        totals = {
            'meres': 0, 'apodoxes': 0,
            'kr_enos': 0, 'kr_etis': 0, 'kr_total': 0,
            'foros': 0, 'eea': 0, 'pliroteo': 0}
        for pro, dapo in res.items():
            fl1 = {
                'pro': pro,
                'onomatep': pro.erg.onomatep,
                'eid': pro.eid.eid,
                'imeromisthio': pro.imeromisthio(),
                'meres': 0,
                'apodoxes': 0,
                'kr_enos': 0,
                'kr_etis': 0,
                'kr_total': 0,
                'forologiteo': 0,
                'foros': 0,
                'eea': 0,
                'pliroteo': 0
            }
            for typeapo, vals in dapo.items():
                # Αν ο τύπος αποδοχών δεν είναι για πληρωμή (πχ 18.Αναστολή )
                if not typeapo.plirotees:
                    continue
                fl1['meres'] += vals['meres']
                fl1['apodoxes'] += vals['apod']

                for eidkek, vls in vals['kratiseis'].items():
                    fl1['kr_enos'] += vls['enos']
                    fl1['kr_etis'] += vls['etis']
                    fl1['kr_total'] += vls['total']
            fl1['forologiteo'] = fl1['apodoxes'] - fl1['kr_enos']
            paidia = pro.erg.paidia(self.periodos()) or 0
            foros, eea = calc_foros_eea_periodou(
                self.etos, fl1['forologiteo'], paidia, self.mistype.barytis)
            # print("models:933>Edo Foros", fl1['forologiteo'], self.mistype.barytis, foros, eea)
            fl1['foros'] = foros
            fl1['eea'] = eea
            fl1['pliroteo'] = fl1['forologiteo'] - foros - eea
            # fl1['kostos'] = fl1['apodoxes'] + fl1['kr_etis']
            lines.append(fl1)
            totals['meres'] += fl1['meres']
            totals['apodoxes'] += fl1['apodoxes']
            totals['kr_enos'] += fl1['kr_enos']
            totals['kr_etis'] += fl1['kr_etis']
            totals['kr_total'] += fl1['kr_total']
            totals['foros'] += fl1['foros']
            totals['eea'] += fl1['eea']
            totals['pliroteo'] += fl1['pliroteo']
            # totals['kostos'] += fl1['kostos']
            lines.sort(key=lambda x: x['onomatep'])
        return head, lines, totals

    def calc_print(self):
        res = self.calc_misthodosia()
        for pro, dapo in res.items():
            print(f'{pro}')
            for typeapo, vals in dapo.items():
                print(
                    f"  {typeapo.__str__():60} {vals['meres']:>2} {vals['argia']:>2} {vals['apod']:>12}")
                for eidkek, vls in vals['kratiseis'].items():
                    print(
                        f"    {eidkek} {vls['enos']} {vls['etis']} {vls['total']}")


class Formula(models.Model):
    part = models.ForeignKey(
        ParousiaType,
        verbose_name='Τύπος Παρουσίας',
        on_delete=models.PROTECT
    )
    ergt = models.ForeignKey(
        ErgazomenosType, verbose_name='Τύπος Εργαζομένου', on_delete=models.PROTECT)
    mist = models.ForeignKey(
        MisthodosiaType, verbose_name='Τύπος Μισθοδοσίας', on_delete=models.PROTECT)
    apodt = models.ForeignKey(
        ApodoxesTypeEfka, verbose_name='Τύπος αποδοχών(ΕΦΚΑ)', on_delete=models.PROTECT)
    meresefka = models.BooleanField('Σε μέρες για ΕΦΚΑ', default=False)
    argiaefka = models.BooleanField('Σε Κυριακές για ΕΦΚΑ', default=False)
    evalu = models.TextField('Τύπος υπολογισμού')

    class Meta:
        verbose_name = 'ΤΥΠΟΣ ΥΠΟΛΟΓΙΣΜΟΥ'
        verbose_name_plural = 'ΤΥΠΟΙ ΥΠΟΛΟΓΙΣΜΟΥ'
        ordering = ['part', 'ergt', 'mist']
        unique_together = ('part', 'ergt', 'mist')

    def __str__(self):
        return f'{self.part} {self.ergt} {self.mist} {self.apodt} {self.evalu}'


class Apd(models.Model):
    etos = models.IntegerField('Έτος', default=2020)
    minas = models.ForeignKey(
        Minas, verbose_name='Περίοδος', on_delete=models.PROTECT)
    apdtype = models.ForeignKey(
        ApdDilosiType, verbose_name='Τύπος', on_delete=models.PROTECT)
    ekdosi = models.DateField('Ημερομηνία έκδοσης')

    def misthodosies(self):
        return ','.join(f'{i.mis}' for i in self.apddetails_set.all())
    misthodosies.short_description = 'Μισθοδοσίες'

    def join_mis(self):
        """
        Ενώνει τις μισθοδοσίες των περιόδων με κλειδί τον εργαζόμενο ...
        """
        fin = {}
        for fmydet in self.fmydetails_set.all():
            _, mis, totals = fmydet.mis.calc_misthodosia_foroi()
            if totals['pliroteo'] <= 0:
                continue
            for lin in mis:
                pass
        return fin

    class Meta:
        unique_together = ('etos', 'minas', 'apdtype')
        ordering = ['-etos', '-minas', '-apdtype']
        verbose_name = 'ΜΙΣΘΟΔΟΣΙΕΣ ΑΠΔ'
        verbose_name_plural = 'ΜΙΣΘΟΔΟΣΙΕΣ ΑΠΔ'

    def __str__(self):
        return f"{self.etos} {self.minas} {self.apdtype} ({self.misthodosies()})"

    def join_mis(self):
        """
        Ενώνει τις μισθοδοσίες των περιόδων με κλειδί τον εργαζόμενο ...
        """
        fin = {}
        for apddet in self.apddetails_set.all():
            for pro, prod in apddet.mis.calc_misthodosia().items():
                fin[pro] = fin.get(pro, {})
                for mtyp, mtypd in prod.items():
                    # Δεν επιτρέπεται να υπάρχει δύο φορές ο τύπος μισθοδοσίας
                    if mtyp in fin[pro]:
                        raise ValueError
                    fin[pro][mtyp] = mtypd
        return fin

    def calc_totals(self, result):
        tmeres = tapod = teisf = 0
        for pro, dapo in result.items():
            for typeapo, vals in dapo.items():
                tmeres += vals['meres']
                tapod += vals['apod']
                for eidkek, vls in vals['kratiseis'].items():
                    teisf += vls['total']
        return tmeres, tapod, teisf

    def apd2text(self):
        parartima = CompanyParartima.objects.get(pk=1)
        data = self.join_mis()
        tmeres, tapod, teisf = self.calc_totals(data)
        tx1 = []
        tx1.append('1')
        tx1.append('01')
        tx1.append('01')
        tx1.append('CSL01   ')
        tx1.append('01')
        tx1.append(f'{self.apdtype.id:02d}')
        tx1.append(f'{parartima.efkayp.ypno:03d}')
        tx1.append(fill_spaces(parartima.efkayp.ypnam, 50))
        tx1.append(fill_spaces(parartima.company.epon, 80))
        tx1.append(fill_spaces(parartima.company.name, 30))
        tx1.append(fill_spaces(parartima.company.patr, 30))
        tx1.append(fill_spaces(parartima.company.ame, 10))
        tx1.append(fill_spaces(parartima.company.afm, 9))
        tx1.append(fill_spaces(parartima.adodo, 50))
        tx1.append(fill_spaces(parartima.adnum, 10))
        tx1.append(fill_spaces(parartima.adtk, 5))
        tx1.append(fill_spaces(parartima.adpol, 30))
        tx1.append(fill_spaces(self.minas.code, 2))
        tx1.append(fill_spaces(f'{self.etos}', 4))
        tx1.append(fill_spaces(self.minas.code, 2))
        tx1.append(fill_spaces(f'{self.etos}', 4))
        # Σύνολα ΑΠΔ
        tx1.append(f'{tmeres:08d}')
        tx1.append(decimal2flat(tapod, 12))
        tx1.append(decimal2flat(teisf, 12))
        tx1.append(isodate2flat(f'{self.ekdosi}'))
        tx1.append(isodate2flat(''))  # Παύση εργασιών
        tx1.append(fill_spaces('', 30))
        header = ''.join(tx1)
        assert len(header) == 414
        apd_list = [header]
        for pro, dapo in data.items():
            tx2 = ['2']
            tx2.append(leading_zeroes(pro.erg.ama, 9))
            tx2.append(pro.erg.amka)
            tx2.append(fill_spaces(pro.erg.epo, 50))
            tx2.append(fill_spaces(pro.erg.ono, 30))
            tx2.append(fill_spaces(pro.erg.pat, 30))
            tx2.append(fill_spaces(pro.erg.mit, 30))
            tx2.append(isodate2flat(pro.erg.gen))
            tx2.append(pro.erg.afm)
            erg_line = ''.join(tx2)
            assert len(erg_line) == 178
            apd_list.append(erg_line)
            for typeapo, vals in dapo.items():
                eid_kek_set = pro.eid.eidikotitakek_set.all()[0]
                tx3 = ['3']
                tx3.append(leading_zeroes(pro.parartima.parno, 4))
                tx3.append(eid_kek_set.kad)
                tx3.append(str(pro.apeid.plires_orario_int()))
                tx3.append(str(pro.apeid.oles_ergasimes_int()))
                tx3.append(leading_zeroes(vals['argia'], 1))
                tx3.append(eid_kek_set.eidefka)
                tx3.append('00')
                tx3.append(leading_zeroes(eid_kek_set.kpk.kpk, 4))
                tx3.append(fill_spaces(self.minas.code, 2))
                tx3.append(fill_spaces(f'{self.etos}', 4))
                tx3.append(isodate2flat(vals['apo']))
                tx3.append(isodate2flat(vals['eos']))
                tx3.append(typeapo.apodtypeefka)
                tx3.append(leading_zeroes(vals['meres'], 3))
                tx3.append(decimal2flat(pro.imeromisthio_for_apd(), 10))
                tx3.append(decimal2flat(vals['apod'], 10))
                for eidkek, vls in vals['kratiseis'].items():
                    tx4 = []
                    tx4.append(decimal2flat(vls['enos'], 10))
                    tx4.append(decimal2flat(vls['etis'], 10))
                    tx4.append(decimal2flat(vls['total'], 11))
                    tx4.append(decimal2flat(0, 10))
                    tx4.append(decimal2flat(0, 5))
                    tx4.append(decimal2flat(0, 10))
                    tx4.append(decimal2flat(vls['total'], 11))
                    eisf_line = ''.join(tx3 + tx4)
                    assert len(eisf_line) == 139
                    apd_list.append(eisf_line)
        return '\n'.join(apd_list + ['EOF'])

    def apd2file(self, filename):
        with open(filename, 'w', encoding='WINDOWS-1253') as fil:
            fil.write(self.apd2text())
        print(f'File {filename} created !!!')

    def apd2stream(self):
        # from io import StringIO
        txt_data = self.apd2text()
        if txt_data is None:
            return None, None
        filename = f'apd-{self.etos}{self.minas.code}-{self.apdtype.code()}.zip'
        return create_zip_stream(txt_data, 'CSL01'), filename

    def calc_print(self):
        res = self.calc_apd()
        for pro, dapo in res.items():
            print(f'{pro}')
            for typeapo, vals in dapo.items():
                print(
                    f"  {typeapo.__str__():60} {vals['meres']:>2} {vals['argia']:>2} {vals['apod']:>12}")
                for eidkek, vls in vals['kratiseis'].items():
                    print(
                        f"    {eidkek} {vls['enos']} {vls['etis']} {vls['total']}")


class ApdDetails(models.Model):
    apd = models.ForeignKey(
        Apd, verbose_name='ΑΠΔ', on_delete=models.PROTECT)
    mis = models.OneToOneField(
        Misthodosia, verbose_name='Μισθοδοσία', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('apd', 'mis')
        verbose_name = 'ΑΠΔ ΑΝΑΛΥΤΙΚΑ'
        verbose_name_plural = 'ΑΠΔ ΑΝΑΛΥΤΙΚΑ'

    def __str__(self):
        return f"{self.apd}{self.mis}"


class Fmy(models.Model):
    etos = models.IntegerField('Έτος', default=2020)
    minas = models.ForeignKey(
        Minas, verbose_name='Περίοδος', on_delete=models.PROTECT)
    cdate = models.DateField('Ημερομηνία έκδοσης')

    def cdate_yyymmdd(self):
        return self.cdate.isoformat().replace('-', '')

    class Meta:
        unique_together = ('etos', 'minas')
        ordering = ['-etos', '-minas']
        verbose_name = 'ΜΙΣΘΟΔΟΣΙΕΣ ΦΜΥ'
        verbose_name_plural = 'ΜΙΣΘΟΔΟΣΙΕΣ ΦΜΥ'

    def __str__(self):
        return f"{self.etos}-{self.minas}"

    def periodos(self):
        """ReturnsYYYYMM as integer"""
        return int(str(self.etos) + self.minas.code)

    def join_mis(self):
        """
        Ενώνει τις μισθοδοσίες των περιόδων με κλειδί τον εργαζόμενο ...
        """
        fin = {}
        tot = {'apo': 0, 'kra': 0, 'kath': 0, 'foros': 0, 'eea': 0}
        for fmydet in self.fmydetails_set.all():
            _, mis, totals = fmydet.mis.calc_misthodosia_foroi()
            if totals['pliroteo'] <= 0:
                continue
            tot['apo'] += totals['apodoxes']
            tot['kra'] += totals['kr_enos']
            tot['foros'] += totals['foros']
            tot['eea'] += totals['eea']
            for lin in mis:
                afm = lin['pro'].erg.afm
                fin[afm] = fin.get(
                    afm,
                    {
                        'pro': lin['pro'],
                        'apo': 0,
                        'kra': 0,
                        'kath': 0,
                        'foros': 0,
                        'eea': 0
                    }
                )
                # epo = lin['pro'].erg.epo
                # ono = lin['pro'].erg.ono
                # pat = lin['pro'].erg.pat
                # amka = lin['pro'].erg.amka
                # paidia = lin['pro'].erg.paidia(self.periodos())
                fin[afm]['apo'] += lin['apodoxes']
                fin[afm]['kra'] += lin['kr_enos']
                fin[afm]['kath'] += lin['forologiteo']
                fin[afm]['foros'] += lin['foros']
                fin[afm]['eea'] += lin['eea']
        tot['kath'] = tot['apo'] - tot['kra']
        return fin, tot

    def fmy2text(self):
        fin, totals = self.join_mis()
        if totals['apo'] == 0:
            return None
        lines = []
        li0 = f"0JL10    {self.cdate_yyymmdd()}{self.etos}{' '*127}"
        assert len(li0) == 148
        lines.append(li0)
        li1 = f"1{self.etos}"
        company = Company.objects.get(pk=1)
        li1 += fill_spaces_cut(company.epon, 18)
        li1 += fill_spaces_cut(company.name, 9)
        li1 += fill_spaces_cut(company.patr, 3)
        li1 += f'{company.ctyp.fmytype}'
        li1 += fill_spaces_cut(company.afm, 9)
        li1 += fill_spaces_cut(company.dra, 16)
        parartima = company.companyparartima_set.get(pk=1)
        li1 += fill_spaces_cut(parartima.adpol, 10)
        li1 += fill_spaces_cut(parartima.adodo, 16)
        li1 += fill_spaces_cut(parartima.adnum, 5)
        li1 += fill_spaces_cut(parartima.adtk, 5)
        li1 += fill_spaces(self.minas.code, 2)
        li1 += fill_spaces('', 49)
        assert len(li1) == 148
        lines.append(li1)
        li2 = "2"
        li2 += decimal2flat(totals['apo'], 16)
        li2 += decimal2flat(totals['kra'], 16)
        li2 += decimal2flat(totals['kath'], 16)
        li2 += decimal2flat(0, 15)
        li2 += decimal2flat(totals['foros'], 15)
        li2 += decimal2flat(totals['eea'], 15)
        li2 += decimal2flat(0, 14)
        li2 += decimal2flat(0, 13)
        li2 += fill_spaces('', 27)
        assert len(li2) == 148
        lines.append(li2)
        for afm, vls in fin.items():
            erg = vls['pro'].erg
            li3 = f'3{afm} '
            li3 += fill_spaces_cut(erg.epo, 18)
            li3 += fill_spaces_cut(erg.ono, 9)
            li3 += fill_spaces_cut(erg.pat, 3)
            li3 += fill_spaces(erg.amka, 11)
            paidia = erg.paidia(self.periodos())
            li3 += leading_zeroes(paidia, 2)
            li3 += '01'
            li3 += decimal2flat(vls['apo'], 11)
            li3 += decimal2flat(vls['kra'], 10)
            li3 += decimal2flat(vls['kath'], 11)
            li3 += '0'
            li3 += fill_spaces('', 2)
            li3 += leading_zeroes(0, 2)
            li3 += leading_zeroes(0, 5)
            li3 += decimal2flat(vls['foros'], 10)
            li3 += decimal2flat(vls['eea'], 10)
            li3 += decimal2flat(0, 9)
            li3 += decimal2flat(0, 8)
            li3 += leading_zeroes(0, 4)
            li3 += fill_spaces('', 9)
            assert len(li3) == 148
            lines.append(li3)
        return '\n'.join(lines)

    # def fmy2file(self):
    #     txt_data = self.fmy2text()
    #     if txt_data is None:
    #         print("There are no misthodosia data. Exiting ...")
    #         return

    #     create_zip(txt_data, filename)
    #     print(f'file {filename} created !!!')

    def fmy2stream(self):
        # from io import StringIO
        txt_data = self.fmy2text()
        if txt_data is None:
            return None, None
        filename = f'fmy-{self.etos}{self.minas.code}.zip'
        return create_zip_stream(txt_data), filename


class FmyDetails(models.Model):
    fmy = models.ForeignKey(
        Fmy, verbose_name='ΦΜΥ', on_delete=models.PROTECT)
    mis = models.OneToOneField(
        Misthodosia, verbose_name='Μισθοδοσία', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('fmy', 'mis')
        verbose_name = 'ΦΟΡΟΣ ΜΙΣΘΩΤΩΝ ΥΠΗΡΕΣΙΩΝ ΑΝΑΛΥΤΙΚΑ'
        verbose_name_plural = 'ΦΟΡΟΣ ΜΙΣΘΩΤΩΝ ΥΠΗΡΕΣΙΩΝ ΑΝΑΛΥΤΙΚΑ'

    def __str__(self):
        return f"{self.fmy} {self.mis}"

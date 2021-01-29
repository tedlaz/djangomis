from django.db import models


class Partner(models.Model):
    afm = models.CharField(verbose_name='Κωδικός', max_length=9, unique=True)
    eponymia = models.CharField(
        verbose_name='Επωνυμία', max_length=70, unique=True)

    class Meta:
        verbose_name = 'ΣΥΝΑΛΛΑΣΣΟΜΕΝΟΣ'
        verbose_name_plural = 'ΣΥΝΑΛΛΑΣΣΟΜΕΝΟΙ'

    def __str__(self):
        return f"{self.afm} {self.eponymia}"


class Account(models.Model):
    code = models.CharField(verbose_name='Κωδικός', max_length=30, unique=True)
    per = models.CharField(verbose_name='Περιγραφή',
                           max_length=70, unique=True)

    class Meta:
        verbose_name = 'ΛΟΓΑΡΙΑΣΜΟΣ'
        verbose_name_plural = 'ΛΟΓΑΡΙΑΣΜΟΙ'

    def type(self):
        typ = {
            '0': 'ΤΑΞΕΩΣ',
            '1': 'ΠΑΓΙΑ',
            '2': 'ΑΠΟΘΕΜΑΤΑ',
            '3': 'ΑΠΑΙΤΗΣΕΙΣ',
            '4': 'ΚΕΦΑΛΑΙΟ',
            '5': 'ΥΠΟΧΡΕΩΣΕΙΣ',
            '6': 'ΕΞΟΔΑ',
            '7': 'ΕΣΟΔΑ',
            '8': 'ΤΑΞΕΩΣ',
            '9': 'ΑΝΑΛΥΤΙΚΗ ΛΟΓΙΣΤΙΚΗ'
        }
        first_digit = self.code[0]
        return typ.get(first_digit, 'ΑΓΝΩΣΤΟ')

    def __str__(self):
        return f"{self.code} {self.per}"


class Tran(models.Model):
    date = models.DateField('Ημερομηνία')
    parastatiko = models.CharField(verbose_name='Παραστατικό', max_length=30)
    perigrafi = models.CharField(verbose_name='Περιγραφή', max_length=70)
    partner = models.ForeignKey(
        Partner, verbose_name='Συναλλασσόμενος', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        unique_together = ('date', 'parastatiko')
        verbose_name = 'ΑΡΘΡΟ ΛΟΓΙΣΤΙΚΗΣ'
        verbose_name_plural = 'ΑΡΘΡΑ ΛΟΓΙΣΤΙΚΗΣ'

    def __str__(self):
        return f"{self.date} {self.parastatiko}"


class Trand(models.Model):
    tran = models.ForeignKey(Tran, on_delete=models.PROTECT)
    account = models.ForeignKey(
        Account, verbose_name='Λογαριασμός', on_delete=models.PROTECT)
    poso = models.DecimalField('Ποσό', max_digits=12, decimal_places=2)

    class Meta:
        # unique_together = ('tran', 'account')
        verbose_name = 'ΑΡΘΡΟ ΛΟΓΙΣΤΙΚΗΣ ΑΝΑΛΥΤΙΚΗ ΓΡΑΜΜΗ'
        verbose_name_plural = 'ΑΡΘΡΑ ΛΟΓΙΣΤΙΚΗΣ ΑΝΑΛΥΤΙΚΕΣ ΓΡΑΜΜΕΣ'

    def __str__(self):
        return f"{self.account} {self.poso}"

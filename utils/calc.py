# -*- coding: utf-8 -*-

from collections import OrderedDict as od
from decimal import Decimal


def mines_misthoton(xronia):
    '''
    Μήνες για αποζημίωση απόλυσης μισθωτών
    xronia : Χρόνια εργασίας στον εργοδότη
    '''
    # xronia must be integer
    xronia = int(xronia)
    mines = 0
    if xronia < 1:
        mines = 0
    elif xronia >= 1 and xronia < 4:
        mines = 2
    elif xronia >= 4 and xronia < 6:
        mines = 3
    elif xronia >= 6 and xronia < 8:
        mines = 4
    elif xronia >= 8 and xronia < 10:
        mines = 5
    elif xronia < 11:
        mines = 6
    elif xronia < 12:
        mines = 7
    elif xronia < 13:
        mines = 8
    elif xronia < 14:
        mines = 9
    elif xronia < 15:
        mines = 10
    elif xronia < 16:
        mines = 11
    elif xronia < 17:
        mines = 12
    elif xronia < 29:
        mines = 12 + (xronia % 17 + 1)
    else:
        mines = 24
    return mines


def meres_imeromisthion(xronia):
    '''
    Μέρες για αποζημίωση απόλυσης ημερομισθίων
    xronia : Χρόνια εργασίας στον εργοδότη
    '''
    meres = 0
    if xronia < 1:
        meres = 0
    elif xronia >= 1 and xronia < 2:
        meres = 7
    elif xronia >= 2 and xronia < 5:
        meres = 15
    elif xronia >= 5 and xronia < 10:
        meres = 30
    elif xronia >= 10 and xronia < 15:
        meres = 60
    elif xronia >= 15 and xronia < 20:
        meres = 100
    elif xronia >= 20 and xronia < 25:
        meres = 120
    elif xronia >= 25 and xronia < 30:
        meres = 145
    elif xronia >= 30:
        meres = 165
    return meres


def apoz_apol(xronia, apodoxes, misthotos=True, proeidopoiisi=False):
    '''
    Υπολογισμός αποζημίωσης απόλυσης
    '''
    if misthotos:
        apoz = apodoxes * 14.0 / 12.0 * mines_misthoton(xronia)
    else:
        apoz = apodoxes * 14.0 / 12.0 * meres_imeromisthion(xronia)
    if proeidopoiisi:
        apoz = apoz / 2
    return apoz


def doro_pasxa(meres, apodoxes, misthotos=True):
    '''
    meres για μισθωτούς οι ημερολογιακές μέρες εργασίας
          για ημερομίσθιους οι μέρες εργασίας.
    '''
    doro = 0
    if misthotos:
        if meres > 120:
            meres = 120
        doro = apodoxes * meres / 240.0 * 1.04166
    else:
        if meres > 97.5:
            meres = 97.5
        doro = Decimal(apodoxes * meres / 6.5 * 1.04166)
    return round(doro, 2)


def doro_xrist(meres, apodoxes, misthotos=True):
    '''
    meres για μισθωτούς οι ημερολογιακές μέρες εργασίας
          για ημερομίσθιους οι μέρες εργασίας.
    '''
    doro = 0
    if misthotos:
        if meres > 237.5:  # 25 * 19 / 2
            meres = 237.5
        doro = apodoxes * meres / 237.5 * 1.04166
    else:
        if meres > 200:
            meres = 200
        doro = apodoxes * meres / 8 * 1.04166
    return round(Decimal(doro), 2)


def epidoma_adeias(meres, apodoxes, misthotos=True):
    epid = 0
    mep = 0
    if misthotos:
        mep = meres / 25.0 * 2.0
        if mep > 12.5:
            mep = 12.5
        epid = apodoxes * mep / 25.0
    else:
        mep = meres / 25.0 * 2.0
        if mep > 13:
            mep = 13
        epid = apodoxes * mep
    return round(Decimal(epid), 2)


def prncalc(dic):
    '''
    Pretty print dictionary
    '''
    for key in dic:
        print("%20s : %12s" % (key, dic[key]))


def foros_eis(poso, paidia=0, misthotos=False):
    '''
    Φόρος Έισοδήματος
    '''
    foros = 0
    if poso <= 20000:
        foros = poso * 0.22
    elif poso <= 30000:
        fprin = 20000 * 0.22
        foros = fprin + (poso - 20000) * 0.29
    elif poso <= 40000:
        fprin = (20000 * 0.22) + (10000 * 0.29)
        foros = fprin + (poso - 30000) * 0.37
    elif poso > 40000:
        fprin = (20000 * 0.22) + (10000 * 0.29) + (10000 * 0.37)
        foros = fprin + (poso - 40000) * 0.45

    if paidia == 0:
        meiosi = 1900
    elif paidia == 1:
        meiosi = 1950
    elif paidia == 2:
        meiosi = 2000
    else:
        meiosi = 2100

    if poso > 20000:
        meiosi -= (poso - 20000) / 1000.0 * 10.0

    if meiosi < 0:
        meiosi = 0

    if not misthotos:  # Den dikaioytai meiosi ...
        meiosi = 0

    if meiosi >= foros:
        return Decimal(0)
    else:
        return round(Decimal(foros - meiosi), 2)


def foros_eispar(poso, paidia=0, misthotos=False, pekptosis=1.5):
    '''
    Φόρος εισοδήματος με έκπτωση παρακράτησης
    '''
    foros = foros_eis(poso, paidia, misthotos)
    ekptosi = Decimal(0)
    if misthotos:
        ekptosi = Decimal(foros * Decimal(pekptosis) / Decimal(100))
    return round(foros - ekptosi, 2)


def foros_ea(poso):
    '''
    Εισφορά Αλληλεγγύης
    '''
    foros = 0
    p20 = 8000 * 2.2 / 100.0
    p30 = p20 + 500  # (10000 * 5.0 / 100.0)
    p40 = p30 + 650  # (10000 * 6.5 / 100.0)
    p65 = p40 + 1875  # (25000 * 7.5 / 100.0)
    p22 = p65 + 13950  # (155000 * 9.0 / 100.0)
    if poso <= 12000:
        foros = 0
    elif poso <= 20000:
        foros = (poso - 12000) * 2.2 / 100.0
    elif poso <= 30000:
        foros = p20 + (poso - 20000) * 5.0 / 100.0
    elif poso <= 40000:
        foros = p30 + (poso - 30000) * 6.5 / 100.0
    elif poso <= 65000:
        foros = p40 + (poso - 40000) * 7.5 / 100.0
    elif poso <= 220000:
        foros = p65 + (poso - 65000) * 9.0 / 100.0
    else:
        foros = p22 + (poso - 220000) * 10.0 / 100.0
    return round(Decimal(foros), 2)


def printfor(apo, eos, bima=100, mis=False):
    '''
    Εκτύπωση πίνακα εισοδήματος και φόρων
    apo: Από εισόδημα
    eos: Έως εισόδημα
    bima: Βήμα ανάμεσα σε δύο γραμμές
    '''
    ast = "%12s %9s %9s %9s %9s %9s"
    j = ('Eisodima', 'foros 0', 'foros 1', 'foros 2', 'foros 3', 'Ep.All.')
    print(ast % j)
    if mis:
        fri = foros_eis  # par
    else:
        fri = foros_eis
    dea = foros_ea
    for i in range(apo, eos + bima, bima):
        print(ast % (i, fri(i, 0, mis),
                     fri(i, 1, mis),
                     fri(i, 2, mis),
                     fri(i, 3, mis), dea(i)))

from decimal import Decimal


def split_poso(poso, klimaka):
    ypoloipo = poso
    final = []
    for orio in klimaka:
        if ypoloipo <= orio:
            final.append(ypoloipo)
            ypoloipo = 0
        else:
            final.append(orio)
            ypoloipo = ypoloipo - orio
    final.append(ypoloipo)
    assert poso == sum(final)
    return final


def meiosi_paidia(paidia, etisio):
    # , 1120, 1340, 1560, 1780, 2000, 2220, 2440, 2660)
    # print('paidia-etisio', paidia, etisio)
    klimaka_meiosis = (777, 810, 900)
    # meiosi = 777
    if paidia <= 2:
        meiosi = klimaka_meiosis[paidia]
    else:
        meiosi = 900 + 220 * (paidia - 2)
    if paidia >= 5:
        return round(Decimal(meiosi), 2)
    meiosi_meiosis = 0
    if etisio > 12000:
        meiosi_meiosis = (etisio - 12000) // 1000 * 20
    final_meiosi = meiosi - meiosi_meiosis
    if final_meiosi <= 0:
        return 0
    return round(Decimal(final_meiosi), 2)


def calc_foros(etos, etisio, paidia):
    if etos < 2020:
        raise ValueError("Θα πρέπει το έτος να είναι πάνω από 2020")

    klimaka = (10000, 10000, 10000, 10000)
    pososta = (9, 22, 28, 36, 44)

    d100 = Decimal(100)
    dpos = [Decimal(i) for i in pososta]
    lpososta = len(pososta)
    assert len(klimaka) + 1 == lpososta

    kat = split_poso(etisio, klimaka)
    foros = round(
        Decimal(sum([dpos[i] * kat[i] / d100 for i in range(lpososta)])), 2)
    meiosi = meiosi_paidia(paidia, etisio)
    # print("foros:55>Foros-Meiosi", foros, meiosi)
    if meiosi >= foros:
        return 0
    return foros - meiosi


def calc_eea(poso):
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


def calc_foros_eea(etos, etisio, paidia):
    foros = calc_foros(etos, etisio, paidia)
    eea = calc_eea(etisio)
    return foros, eea, foros + eea


def calc_foros_eea_periodou(etos, forologiteo, paidia, barytis):
    etisio = forologiteo * barytis
    foros, eea, _ = calc_foros_eea(etos, etisio, paidia)
    foros_periodou = round(Decimal(foros / barytis), 2)
    eea_periodou = round(Decimal(eea / barytis), 2)
    return foros_periodou, eea_periodou

from decimal import Decimal as dec
from collections import namedtuple
MERES_BDOMADASd = dec(6)
ORES_BDOMADASd = dec(40)
MERES_MINA_MISTHOTOSd = dec(25)
MERES_MINA_IMSTHIOSd = dec(26)
NYXTA_PROSd = dec(.25)
ARGIA_PROSd = dec(.75)
DORO_PROSd = dec(0.04166)


def get_pososta_efka(period, kpk):
    return {'p_enos': 10, 'p_etis': 20, 'p_total': 30}


def kratiseis(poso, p_enos, p_total, orio=0):
    if orio:
        dposo = round(dec(orio), 2) if poso > orio else round(dec(poso), 2)
    else:
        dposo = round(dec(poso), 2)
    d100 = dec(100)
    k_enos = round(dposo * dec(p_enos) / d100, 2)
    k_total = round(dposo * dec(p_total) / d100, 2)
    k_etis = round(k_total - k_enos, 2)
    return {
        'poso_gia_kratisi': dposo,
        'orio': orio,
        'p_enos': p_enos,
        'p_total': p_total,
        'k_enos': k_enos,
        'k_etis': k_etis,
        'k_total': k_total
    }


class Erg:
    typos = 'Abstract'

    def taktikes_apodoxes(self, *, meres=0, ores=0, nyxta=0, argia=0, argia_ores=0):
        if self.typos == 'Oromisthios':
            assert argia == 0
            assert meres == 0
            apper = self.apodoxes_periodou(ores)
            aargiao = round(self.oromisthio * dec(argia_ores) * ARGIA_PROSd, 2)
            aargia = dec(0)
        else:
            apper = self.apodoxes_periodou(meres)
            aargiao = round(self.oromisthio * dec(argia_ores) * ARGIA_PROSd, 2)
            aargia = round(self.imeromisthio * dec(argia) * ARGIA_PROSd, 2)
        anyxta = round(self.oromisthio * dec(nyxta) * NYXTA_PROSd, 2)
        total = apper + aargia + aargiao + anyxta
        if self.typos == "Imeromisthios":
            imeromisthio_efka = self.imeromisthio
        else:
            imeromisthio_efka = 0
        dkr = kratiseis(total, 10, 30)
        return {
            'misthodosia': 'Taktikes Apodoxes',
            'typos': self.typos,
            'meres': meres,
            'meres_efka': meres,
            'argies_efka': argia,
            'imeromisthio_efka': imeromisthio_efka,
            'ores': ores,
            'nyxta': nyxta,
            'argia': argia,
            'argia_ores': argia_ores,
            'apodoxes_periodoy': apper,
            'prosafksisi_nyxeterinon_oron': anyxta,
            'prosafksisi_imeron_argias': aargia,
            'prosafksisi_oron_argias': aargiao,
            'synolo': total,
            'kratiseis': dkr
        }

    def astheneia(self, *, meres_le3=0, meres_more3=0, apozimiosi=0):
        """[summary]

        Args:
            meres_le3 (int, optional): [description]. Defaults to 0.
            meres_more3 (int, optional): [description]. Defaults to 0.
            apozimiosi (int, optional): [description]. Defaults to 0.

        Returns:
            [type]: [description]
        """
        aple3 = round(dec(meres_le3) * self.imeromisthio / dec(2), 2)
        apmore3 = round(dec(meres_more3) * self.imeromisthio, 2)
        tot = aple3 + apmore3
        return {
            'misthodosia': 'Astheneia',
            'typos': self.typos,
            'meres_le3': meres_le3,
            'meres_more3': meres_more3,
            'meres_efka': meres_le3 + meres_more3,
            'argies_efka': 0,
            'imeromisthio_efka': 0,
            'synolo': tot
        }

    def doro_xristoygennon(self, *, meres=0, ores=0):
        dc8 = dec(8)
        d25 = dec(25)
        if self.typos == 'Oromisthios':
            assert meres == 0
            doro = round(dec(ores) / dc8 * self.oromisthio, 2)
        elif self.typos == 'Imeromisthios':
            assert ores == 0
            meres = dec(200) if meres > 200 else dec(meres)
            doro = round(meres / dc8 * self.imeromisthio, 2)
        elif self.typos == 'Misthotos':
            assert ores == 0
            meres = dec(200) if meres > 200 else dec(meres)
            doro = round(meres / dc8 / d25 * self.misthos, 2)
        else:
            raise ValueError
        pros_ep_ad = round(doro * DORO_PROSd, 2)
        tot = round(doro + pros_ep_ad, 2)
        return {
            'misthodosia': 'Doro Xristougennon',
            'typos': self.typos,
            'meres': meres,
            'meres_efka': 0,
            'argies_efka': 0,
            'imeromisthio_efka': 0,
            'ores': ores,
            'doro': doro,
            'prosafksisi_ep_adeias': pros_ep_ad,
            'synolo': tot
        }

    def doro_pasxa(self, *, meres=0, ores=0):
        dc8 = dec(8)
        d25 = dec(25)
        if self.typos == 'Oromisthios':
            assert meres == 0
            doro = round(dec(ores) / dc8 * self.oromisthio, 2)
        elif self.typos == 'Imeromisthios':
            assert ores == 0
            meres = dec(100) if meres > 100 else dec(meres)
            doro = round(meres / dc8 * self.imeromisthio, 2)
        elif self.typos == 'Misthotos':
            assert ores == 0
            meres = dec(100) if meres > 100 else dec(meres)
            doro = round(meres / dc8 / d25 * self.misthos, 2)
        else:
            raise ValueError
        pros_ep_ad = round(doro * DORO_PROSd, 2)
        tot = round(doro + pros_ep_ad, 2)
        return {
            'misthodosia': 'Doro Pasxa',
            'typos': self.typos,
            'meres': meres,
            'meres_efka': 0,
            'argies_efka': 0,
            'imeromisthio_efka': 0,
            'ores': ores,
            'doro': doro,
            'prosafksisi_ep_adeias': pros_ep_ad,
            'synolo': tot
        }

    def __str__(self):
        return (
            f'typos  : {self.typos:15} '
            f'misthos: {self.misthos:8} '
            f'imer   : {self.imeromisthio:6} '
            f'orom   : {self.oromisthio:5}'
        )


class ErgMisthotos(Erg):
    typos = 'Misthotos'

    def __init__(self, misthos):
        self.misthos = round(dec(misthos), 2)

    @property
    def imeromisthio(self):
        return round(self.misthos / MERES_MINA_MISTHOTOSd, 2)

    @property
    def oromisthio(self):
        return round(self.imeromisthio * MERES_BDOMADASd / ORES_BDOMADASd, 2)

    def apodoxes_periodou(self, meres):
        return round(dec(meres) / MERES_MINA_MISTHOTOSd * self.misthos, 2)


class ErgImeromisthios(Erg):
    typos = 'Imeromisthios'

    def __init__(self, imeromisthio):
        self.imeromisthio = round(dec(imeromisthio), 2)

    @property
    def misthos(self):
        return round(self.imeromisthio * MERES_MINA_IMSTHIOSd, 2)

    @property
    def oromisthio(self):
        return round(self.imeromisthio * MERES_BDOMADASd / ORES_BDOMADASd, 2)

    def apodoxes_periodou(self, meres):
        return round(dec(meres) * self.imeromisthio)


class ErgOromisthios(Erg):
    typos = 'Oromisthios'

    def __init__(self, oromisthio):
        self.oromisthio = round(dec(oromisthio), 2)

    @property
    def misthos(self):
        return round(self.imeromisthio * MERES_MINA_IMSTHIOSd, 2)

    @property
    def imeromisthio(self):
        return round(self.oromisthio * ORES_BDOMADASd / MERES_BDOMADASd, 2)

    def apodoxes_periodou(self, ores):
        return round(dec(ores) * self.oromisthio, 2)


if __name__ == '__main__':
    ted = ErgMisthotos(750)
    ric = ErgMisthotos(840)
    pop = ErgImeromisthios(30)
    kos = ErgOromisthios(4.5)
    for erg in (ted, ric, pop, kos):
        print(erg)
    print(ted.taktikes_apodoxes(meres=25, argia=1))
    print(pop.taktikes_apodoxes(meres=25, argia=1))
    print(kos.taktikes_apodoxes(ores=167, argia_ores=6))
    print(ted.doro_xristoygennon(meres=200))
    print(pop.doro_xristoygennon(meres=200))
    print(ric.doro_xristoygennon(meres=200))
    print(kratiseis(100.10, 15, 40))

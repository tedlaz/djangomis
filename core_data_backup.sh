#!/bin/bash
python manage.py dumpdata \
mis.apasxolisieidos \
mis.apasxolisitype \
mis.apddilositype \
mis.apodoxestypeefka \
mis.apoxorisitype \
mis.companytype \
mis.formula \
mis.kpk \
mis.kpkapo \
mis.minas \
mis.misthodosiatype \
mis.oikkattype \
mis.parousiatype \
mis.taftotitatype \
mis.xora \
> miscore

python json_encode.py miscore
rm miscore

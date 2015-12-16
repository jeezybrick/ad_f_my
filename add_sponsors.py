# -*- coding: utf-8 -*-

import django
import csv
from sponsor.models import Sponsor

django.setup()
with open('Sponsors List (Can&US).csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(row)

from django.shortcuts import render
from django.views.generic import TemplateView
from . import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from poisenseapp.models import Hazardchemicals, Pictogramcode, Precautionstm
import cv2
import numpy as np
import requests
import io
import json
import re
import sys
import os
import time

# to check db if the elements detected are in the database and put them onto a new list called found_list
def check_db(text):
    found_list = []
    for each in text:
        try:
            if each == Hazardchemicals.objects.get(chemical_name__iexact=each).chemical_name:
                found_list.append(each)
        except:
                pass
    return found_list

# to extract the statements of prevention, response, storage
def value_extraction(x):
    try:
        return Precautionstm.objects.get(pictogramcode__iexact=x).statement
    except:
        return ""

# to clean the Pictogramcodes and extract their values using value_extraction function
def cleaning(value):
    value = [i for i in value if i]
    value = ', '.join(value)
    value = value.replace(u'\xa0', u'')
    value = value.split(', ')
    value = list(set(value))
    value = list(map(value_extraction, value))
    value = list(set(value))
    print(value)
    return value


def human_senses(id,statement):
    eye = []
    inhale = []
    skin = []
    ingestion = []
    other = []
    if id == 'hs':
        val1 = 'drows'
    else:
        val1 = 'breath'

    if id == 'hs':
        val2 = 'skin'
    else:
        val2 = 'skin'

    for hs in statement:
        hs = hs.lower()
        if "eye" in hs:
            eye.append(hs)
        elif "skin" in hs:
            skin.append(hs)
        elif val1 in hs:
            inhale.append(hs)
        elif 'swallow' in hs:
            ingestion.append(hs)
        else:
            other.append(hs)

    eye = '. '.join(eye)
    skin = '. '.join(skin)
    inhale = '. '.join(inhale)
    ingestion = '. '.join(ingestion)
    other = '. '.join(other)
    return eye, skin, inhale, ingestion, other

def retrieving(text):
    found_list = check_db(text)
    if len(found_list) == 1:
        element_names = found_list[0]
        element_names = element_names.capitalize()
    elif len(found_list)>1:
        element_names = [x.capitalize() for x in found_list]
        element_names = ', '.join(element_names)
        element_names = re.sub(r"(\b, \b)(?!.*\1)", r" and ", element_names)
    else:
        element_names = "NO ELEMENT FOUND"
        return element_names,'','','','','','','','','','','','',''




    HazardStatementCode = []
    ghs_code = []
    hazard_statement = []
    for each in found_list:
        HSC = (Hazardchemicals.objects.get(chemical_name__iexact=each).hazardstatementcode).split('; ')
        HSC = [x for x in HSC if not x.startswith('A')]
        HazardStatementCode = HazardStatementCode + HSC


        ghsc = (Hazardchemicals.objects.get(chemical_name__iexact=each).ghs_code).split('; ')
        while("" in ghsc) :
            ghsc.remove("")
        ghs_code = ghs_code + ghsc


        hazard_statement = hazard_statement + (Hazardchemicals.objects.get(chemical_name__iexact=each).hazard_statement).split('; ')
    HazardStatementCode = list(set(HazardStatementCode))
    ghs_code = list(set(ghs_code))

    ghs_code_names = []
    for val in ghs_code:
        if val=='GHS01':
            ghs_code_names.append('Explosive')
        elif val=='GHS02':
            ghs_code_names.append('Flammable')
        elif val=='GHS03':
            ghs_code_names.append('Oxidizer')
        elif val=='GHS05':
            ghs_code_names.append('Corrosive')
        elif val=='GHS06':
            ghs_code_names.append('Acute Toxic')
        elif val=='GHS07':
            ghs_code_names.append('Irritant')
        elif val=='GHS08':
            ghs_code_names.append('Health Hazard')
        elif val=='GHS09':
            ghs_code_names.append('Environment')
        elif val=='GHS04':
            ghs_code_names.append('Compressed Gas')

    ghs_code = ghs_code_names

    hazard_statement = list(set(hazard_statement))

    hs_eye, hs_skin, hs_inhale, hs_ingestion, hs_other = human_senses('hs',hazard_statement)

    prevention = []
    response = []
    storage = []
    for code in HazardStatementCode:
        try:
            prevention.append(Pictogramcode.objects.get(hazardstatementcode__iexact=code).prevention_code)
            response.append(Pictogramcode.objects.get(hazardstatementcode__iexact=code).response_code)
            storage.append(Pictogramcode.objects.get(hazardstatementcode__iexact=code).storage_code)
        except:
            pass

    prevention = cleaning(prevention)
    response = cleaning(response)
    storage = cleaning(storage)

    if len(prevention) > 5:
        prevention = prevention[:5]

    if len(storage) > 5:
        storage = storage[:5]
    rs_eye, rs_skin, rs_inhale, rs_ingestion, rs_other = human_senses('rs',response)


    return element_names,hs_eye, hs_skin, hs_inhale, hs_ingestion, hs_other,ghs_code,prevention,rs_eye, rs_skin, rs_inhale, rs_ingestion, rs_other,storage

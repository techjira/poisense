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
import pubchempy
# to check db if the elements detected are in the database and put them onto a new list called found_list
def check_db(text):
    found_list = []
    compound_names = []
    for each in text:
        ignore_list = ['aqua','water','glycol','glycerin','glycerine','fragrance','preservative','colour','soap','sodium salicylate','sodium chloride','sodium citrate','xanthan','sodium lauroyl sacrcosinate','cetyl acetate','cocamidopropyl betaine','cetearyl alcohol','cl 2-15 alkyl benzoate','triethanolamine','glyceryl stearate','steareth-2','propylparaben','methylparaben','dimethicone','caprylyl glycol','cetyl palmitate','tocopheryl acetate']
        if each in ignore_list:
            pass
        else:
            try:
                if (Hazardchemicals.objects.filter(chemical_name__iexact=each)).count()>=1:
                    found_list.append(each)
                    compound_names.append(each)
                else:
                    val = pubchempy.get_synonyms(each, 'name')[0]
                    val = val['Synonym']
                    # print("seaching in Synonym")
                    count = 0
                    for i in val:
                        count = count+1
                        i = i.lower()
                        if (Hazardchemicals.objects.filter(chemical_name__iexact=i)).count()>=1:
                            i = re.sub("'","\'",i)
                            found_list.append(i)
                            compound_names.append(each)
                            break
                        if count == 150:
                            break
                
            except:
                pass

    return found_list, compound_names

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
    # print(value)
    return value


def pull_ghs_info(ghs_code):
    ghs_code_explain = []
    for each in ghs_code:
        if each == 'GHS01':
            ghs_code_explain.append("Explosion, blast or projection hazard.")
        elif each == 'GHS02':
            ghs_code_explain.append("Flammable liquids, solids and gases; including self-heating and self-igniting substances.")
        elif each == 'GHS03':
            ghs_code_explain.append("Oxidising liquids, solids and gases, may cause or intensify fire.")
        elif each == 'GHS04':
            ghs_code_explain.append("Gases under pressure.")
        elif each == 'GHS05':
            ghs_code_explain.append("Fatal or toxic if swallowed, inhaled or in contact with skin.")
        elif each == 'GHS06':
            ghs_code_explain.append("Low level toxicity. This includes respiratory, skin, and eye irritation, skin sensitisers and chemicals harmful if swallowed, inhaled or in contact with skin.")
        elif each == 'GHS07':
            ghs_code_explain.append("Corrosive chemicals, may cause severe skin and eye damage and may be corrosive to metals.")
        elif each == 'GHS08':
            ghs_code_explain.append("Chronic health hazards; this includes aspiratory and respiratory hazards, carcinogenicity, mutagenicity and reproductive toxicity.")
        elif each == 'GHS09':
            ghs_code_explain.append("Hazardous to aquatic life and the environment.")
    return ghs_code_explain


# using the following function to get the details regarding eye, skin, inhalation, ingestion from hazard
# statement and precaution statements
def human_senses(id,statement):
    eye = []
    inhale = []
    skin = []
    ingestion = []
    other = []
    if id == 'hs':
        val1 = 'respiratory'
    else:
        val1 = 'breath'

    for hs in statement:
        hs = hs.lower()
        if "eye" in hs:
            eye.append(hs)
        elif "skin" in hs:
            skin.append(hs)
        elif 'swallow' in hs:
            ingestion.append(hs)
        elif "inhale" in hs:
            inhale.append(hs)
        elif "burns" in hs:
            skin.append(hs)
        elif "hair" in hs:
            skin.append(hs)
        elif "respiratory" in hs:
            inhale.append(hs)
        elif "breath" in hs:
            inhale.append(hs)
        elif "fire" in hs:
            other.append("In case of fire: extinguish appropriately")
        else:
            other.append(hs)

    # capitalizing the first letter of sentences
    eye = [x.capitalize() for x in eye]
    skin = [x.capitalize() for x in skin]
    ingestion = [x.capitalize() for x in ingestion]
    inhale = [x.capitalize() for x in inhale]
    other = [x.capitalize() for x in other]

    eye = ' '.join(eye)
    skin = ' '.join(skin)
    inhale = ' '.join(inhale)
    ingestion = ' '.join(ingestion)
    other = ' '.join(other)
    return eye, skin, inhale, ingestion, other

# This is the main function, where all the first level of data ectraction happens by extracting from
# the database.
def retrieving(text):
    # print(text)
    found_list, compound_names = check_db(text)
    # print(compound_names)
    if len(compound_names) == 1:
        element_names = compound_names[0]
        element_names = element_names.capitalize()
    elif len(compound_names)>1:
        element_names = [x.capitalize() for x in compound_names]
        element_names = ', '.join(element_names)
        element_names = re.sub(r"(\b, \b)(?!.*\1)", r" and ", element_names)
    else:
        element_names = "NO ELEMENT FOUND"
        return element_names,'','','','','','','','','','','','','',''




    HazardStatementCode = []
    ghs_code = []
    hazard_statement = []
    for each in found_list:
        # getting the hazard statement codes
        # print(each)
        HSC = (Hazardchemicals.objects.filter(chemical_name__iexact=each).first().hazardstatementcode).split('; ')
        HSC = [x for x in HSC if not x.startswith('A')]
        # HSC = [x for x in HSC if not len(x)==4]
        HazardStatementCode = HazardStatementCode + HSC
        # print(HazardStatementCode)
        # getting the GHS codes
        ghsc = (Hazardchemicals.objects.filter(chemical_name__iexact=each).first().ghs_code).split('; ')
        while("" in ghsc) :
            ghsc.remove("")
        ghs_code = ghs_code + ghsc

        # getting the hazard statements
        hazard_statement = hazard_statement + (Hazardchemicals.objects.filter(chemical_name__iexact=each).first().hazard_statement).split('; ')
    HazardStatementCode = list(set(HazardStatementCode))
    ghs_code = list(set(ghs_code))

    ghs_code_explain = pull_ghs_info(ghs_code)


    # extracting the GHS names
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
    ghs_dict = dict(zip(ghs_code, ghs_code_explain))
    # print(ghs_dict)

    # filtering hazard statements
    hazard_statement = list(set(hazard_statement))
    hazard_smt = hazard_statement
    hazard_statement = []
    for statement in hazard_smt:
        if "..." in statement:
            pass
        else:
            hazard_statement.append(statement)


    hs_eye, hs_skin, hs_inhale, hs_ingestion, hs_other = human_senses('hs',hazard_statement)

    # getting the details of prevention, response and storage
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


    return element_names,hs_eye, hs_skin, hs_inhale, hs_ingestion, hs_other,ghs_code,prevention,rs_eye, rs_skin, rs_inhale, rs_ingestion, rs_other,storage, ghs_dict

from django.shortcuts import render
from django.views.generic import TemplateView
from . import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from poisenseapp.models import Altername
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
def allergy_retrieving(text):
    try:
        text_detected = text.lower()
        text_detected = re.sub(r'\r\n', ' ',text_detected)
        text_detected = re.sub(r'[%\*\n]','',text_detected)
        # text_detected = re.sub(r'w/v','',text_detected)
        # print(text_detected)
        list_allergies = list(Altername.objects.values_list('alternativeingredient', flat=True))
        # print(list_allergies)
        all_values = Altername.objects.all()
        # for item in all_values:
        #     print(item.alternativeingredient)
        #     print(item.category)

        found_allergies = dict()
        for each in list_allergies:
            if each in text_detected:
                try:
                    print(each)
                    category = Altername.objects.filter(alternativeingredient__icontains=str(each)).first().category
                    print("category ", category)
                    # found_allergies[category] = each

                    if category in found_allergies:
                        print("appending",each)
                        found_allergies[category].append(each)
                    else:
                        print("creating with",each)
                        found_allergies[category] = [each,]
                except:
                    pass
        for key in found_allergies:
            combine = found_allergies[key]
            combine = [x.capitalize() for x in combine]
            combine = ', '.join(combine)
            combine = re.sub(r"(\b, \b)(?!.*\1)", r" and ", combine)
            found_allergies[key] = combine

        if "ngredients" in text_detected:
            return found_allergies
        elif "contains" in text_detected:
            return found_allergies
        else:
            found_allergies = "not detected"
            return found_allergies
    except:
        found_allergies = "not detected"
        return found_allergies
    return found_allergies

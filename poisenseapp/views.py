from django.shortcuts import render
from django.views.generic import TemplateView
from . import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, ChemForm, UploadAllergyFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from poisenseapp.database_extract import retrieving
from poisenseapp.allergy_database_extract import allergy_retrieving
from poisenseapp.image_detection import final_text
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
import random
import string
from pubchempy import get_compounds
import poisenseapp.allergy_image_detection as aid

# used to first call the password page
def password(request):
    return render(request,'password.html')

#Header
def header(request):
    return render(request,'header.html')

#Footer
def footer(request):
    return render(request,'footer.html')

# requests the home page
def home(request):
    return render(request, 'home.html')

def ssl(request):
    return render(request, '.well-known/acme-challenge/YWObyQs8K90gboL2UYaiKB6_k2emxhUuG-mZQ7yOg4c')

def ssl2(request):
    return render(request, '.well-known/acme-challenge/51_a9PO7gke53ZMZV0kbWLwiLIAn9xM2gsPFEaQS2j0')


# using the following function to generate random name for image files to avoid file name errors
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# complete functionality of the app is in this function
def allergy(request):

    fs = FileSystemStorage()
    if request.method == 'POST':
        Allergyuploadform = UploadAllergyFileForm(request.POST,request.FILES)
        if Allergyuploadform.is_valid():
            if request.method == 'POST' and request.FILES['Allergy_file']:
                file = request.FILES['Allergy_file']
                file_name = randomString(8)
                filename = fs.save(file_name, file)
                uploaded_file_url = fs.url(filename)
                text = aid.final_text(str(uploaded_file_url)[1:])
                fs.delete(filename)
                print(text)
                found_allergies = allergy_retrieving(text)
                if found_allergies == "not detected":
                    return render(request, 'allergy_not_detected.html')
                elif not bool(found_allergies):
                    return render(request, 'allergy_safe.html')
                return render(request, 'allergy-info.html', {'found_allergies': found_allergies})
    else:
        Allergyuploadform = UploadAllergyFileForm()
    return render(request, 'allergy-detection.html', {'Allergyuploadform': Allergyuploadform})


def sense(request):
    fs = FileSystemStorage()
    query_results = list(Hazardchemicals.objects.all().values_list("chemical_name", flat=True))
    if request.method == 'POST':
        # loading forms
        uploadform = UploadFileForm(request.POST,request.FILES)
        input_form = ChemForm(request.POST)
        if uploadform.is_valid():
            if request.method == 'POST' and request.FILES['file']:
                file = request.FILES['file']
                file_name = randomString(8)
                filename = fs.save(file_name, file)
                uploaded_file_url = fs.url(filename)
                text = final_text(str(uploaded_file_url)[1:])
                text = [x.strip() for x in text]
                fs.delete(filename)
                print(text)

                if text == ["not detected"]:
                    uploadform = UploadFileForm()
                    input_form = ChemForm()
                    return render(request, 'not_detected.html', {'uploadform': uploadform,'input_form':input_form})
        else:
            # text box, with dropdown list of elements
            text = []
            dropdown = request.POST.get('browser', None)
            text.append(dropdown)
            print(text)



        element_names,hs_eye, hs_skin, hs_inhale, hs_ingestion, hs_other,ghs_code,prevention,rs_eye, rs_skin, rs_inhale, rs_ingestion, rs_other,storage, ghs_dict = retrieving(text)

        # if no ingredients gets detected then safe.html is displayed
        if element_names == "NO ELEMENT FOUND":
            uploadform = UploadFileForm()
            input_form = ChemForm()
            return render(request, 'safe.html', {'uploadform': uploadform,'input_form':input_form})

        return render(request, 'info.html', {
            'element_names':element_names,'hs_eye':hs_eye,'hs_skin':hs_skin,'hs_inhale':hs_inhale,'hs_ingestion':hs_ingestion,'hs_other':hs_other,'ghs_code':ghs_code,'prevention':prevention,'rs_eye':rs_eye,'rs_skin':rs_skin,'rs_inhale':rs_inhale,'rs_ingestion':rs_ingestion,'rs_other':rs_other,'storage':storage,'ghs_dict':ghs_dict})
    else:
        uploadform = UploadFileForm()
        input_form = ChemForm()

    return render(request, 'sense.html', {'uploadform': uploadform,'input_form':input_form,'query_results':query_results})

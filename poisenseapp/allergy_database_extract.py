from django.shortcuts import render
from django.views.generic import TemplateView
from . import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from poisenseapp.models import Altername, User, UserAllergyinfo, Signandtreatment
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
# kid_no = list(UserAllergyinfo.objects.filter(userid=1).values_list("kid_id", flat=True))
# print(kid_no)
def personalised(text,userid,found_allergies):
    print("personalised")
    try:
        text_detected = text.lower()
        text_detected = re.sub(r'\r\n', ' ',text_detected)
        text_detected = re.sub(r'[%\*\n]','',text_detected)
        if bool(userid):
            print("user id",userid)
            kid_no = UserAllergyinfo.objects.filter(userid=userid).count()
            print("number of kids ", kid_no)
            allergy_dict = {}

            kid_no = list(UserAllergyinfo.objects.filter(userid=userid).values_list("kid_id", flat=True))
            print("kid ID's", kid_no)
            for each in kid_no:
                print(each)
                try:
                    kid_name = UserAllergyinfo.objects.get(userid=userid,kid_id=each).kid_name
                    print(kid_name)
                except:
                    pass

                try:
                    kid_allergy = [x.strip() for x in(UserAllergyinfo.objects.get(userid=userid,kid_id=each).kid_allergy).split(',')]
                    print(kid_allergy)
                    for val in kid_allergy:
                        if val in found_allergies:
                            if kid_name.capitalize() in allergy_dict:
                                print("appending",val)
                                allergy_dict[kid_name.capitalize()].append(val)
                            else:
                                print("creating with",val)
                                allergy_dict[kid_name.capitalize()] = [val,]
                except:
                    print("no common allergries for kids")


                try:
                    personalised_allergy = (UserAllergyinfo.objects.get(userid=userid,kid_id=each).personalised_allergy).split(',')
                    personalised_allergy = [x.lower() for x in personalised_allergy]
                    personalised_allergy = [x.strip() for x in personalised_allergy]
                    print(personalised_allergy)
                    for val in personalised_allergy:
                        print("personal item:",val)
                        # print(text_detected)
                        if val in text_detected:
                            print(val)
                            if kid_name.capitalize() in allergy_dict:
                                print("appending",val)
                                allergy_dict[kid_name.capitalize()].append(val)
                            else:
                                print("creating with",val)
                                allergy_dict[kid_name.capitalize()] = [val,]
                except:
                    print("no personalised allergies")

            return allergy_dict
        else:
            allergy_dict = ""
            return allergy_dict
    except:
        # print("no personalised allergies")
        allergy_dict = ""
        return allergy_dict

# The below fution is used to extractthe most common allergies that are found in the text extracted
def allergy_retrieving(text):
    try:
        # Cleaning the extracted text before checking for the elements
        text_detected = text.lower()
        text_detected = re.sub(r'\r\n', ' ',text_detected)
        text_detected = re.sub(r'[%\*\n]','',text_detected)
        # Making a list of allergies
        list_allergies = list(Altername.objects.values_list('alternativeingredient', flat=True))
        all_values = Altername.objects.all()
        found_allergies = dict()
        for each in list_allergies:
            if each in text_detected:
                # ignoring if it contains any words such as gluten free kind
                consider_free = each + " free"
                if consider_free not in text_detected:
                    try:
                        category = Altername.objects.filter(alternativeingredient__icontains=str(each)).first().category
                        # if allergy found append to dict
                        if category in found_allergies:

                            found_allergies[category].append(each)
                        else:

                            found_allergies[category] = [each,]
                    except:
                        pass
        found_allergies_list = found_allergies
        for key in found_allergies:
            combine = found_allergies[key]
            combine = [x.capitalize() for x in combine]
            combine = ', '.join(combine)
            combine = re.sub(r"(\b, \b)(?!.*\1)", r" and ", combine)
            found_allergies[key] = combine

        symptoms = {}
        for i in found_allergies_list:
            symptoms[i] = (Signandtreatment.objects.filter(categories__icontains=str(i)).first().symptoms).split('\n')
        # if ngrediets or contains is not found in the text extracted, then the user is asked to upload the image again
        if "ngredient" in text_detected:
            return found_allergies,found_allergies_list,symptoms
        elif "contain" in text_detected:
            return found_allergies,found_allergies_list,symptoms
        else:
            found_allergies = "not detected"
            return found_allergies,found_allergies_list,symptoms
    except:
        found_allergies = "not detected"
        found_allergies_list = {}
        symptoms = {}
        # if non works out, then blank entries are returned
        return found_allergies,found_allergies_list, symptoms
    return found_allergies,found_allergies_list, symptoms

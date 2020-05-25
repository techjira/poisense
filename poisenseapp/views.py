from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from . import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, ChemForm, UploadAllergyFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from poisenseapp.database_extract import retrieving
from poisenseapp.allergy_database_extract import allergy_retrieving, personalised
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
from . import models
from . import forms
import hashlib
import re
from poisenseapp.models import User, UserAllergyinfo

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

# using the following function to generate random name for image files to avoid file name errors
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# Requests the allergy related pages as well extracting text and allergy info from it
def allergy(request):
    # storing user_id
    userid = request.session.get('user_id')
    fs = FileSystemStorage()
    if request.method == 'POST':
        Allergyuploadform = UploadAllergyFileForm(request.POST,request.FILES)
        # On sumbitting form the following actions take place
        if Allergyuploadform.is_valid():
            if request.method == 'POST' and request.FILES['Allergy_file']:
                file = request.FILES['Allergy_file']
                # Image names could have symbols which will cause issues in reading files
                # Hence Randomizing the name
                file_name = randomString(8)
                filename = fs.save(file_name, file)
                uploaded_file_url = fs.url(filename)
                text = ""
                # Extracting the text from image using the following final_text function
                text = aid.final_text(str(uploaded_file_url)[1:])
                # deleting the image once the text has been extracted for the safety of user as well as to safe the memeory of the server
                fs.delete(filename)
                # retreiving the allergies found and their symptoms from the following 2 functions
                found_allergies,found_allergies_list,symptoms = allergy_retrieving(text)
                personal = personalised(text,userid,found_allergies_list)
                if found_allergies == "not detected":
                    if not bool(personal):
                        return render(request, 'allergy_not_detected.html')
                elif not bool(found_allergies):
                    if not bool(personal):
                        return render(request, 'allergy_safe.html')
                elif not bool(found_allergies_list):
                    if not bool(personal):
                        return render(request, 'allergy_safe.html')
                return render(request, 'allergy-info.html', {'found_allergies': found_allergies,'personal':personal,'symptoms':symptoms})
    else:
        Allergyuploadform = UploadAllergyFileForm()
    return render(request, 'allergy-detection.html', {'Allergyuploadform': Allergyuploadform})

# Sense is used to sense the chemical ingredients
def sense(request):
    fs = FileSystemStorage()
    #  storing all the chemical names in the query results to be used to populate in the text input form
    query_results = list(Hazardchemicals.objects.all().values_list("chemical_name", flat=True))
    #  If a form has been submitted then it enters the condition
    if request.method == 'POST':
        # loading forms
        uploadform = UploadFileForm(request.POST,request.FILES)
        input_form = ChemForm(request.POST)
        #  Depending on the form which is valid, enters that condition
        if uploadform.is_valid():
            if request.method == 'POST' and request.FILES['file']:
                file = request.FILES['file']
                # Image names could have symbols which will cause issues in reading files
                # Hence Randomizing the name
                file_name = randomString(8)
                filename = fs.save(file_name, file)
                uploaded_file_url = fs.url(filename)
                # Extracting the text from image using the following final_text function
                text = final_text(str(uploaded_file_url)[1:])
                text = [x.strip() for x in text]
                # deleting the image once the text has been extracted for the safety of user as well as to safe the memeory of the server
                fs.delete(filename)
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
        # extracting all the details that will be required to be displayed to the user for the details of chemicals
        element_names,hs_eye, hs_skin, hs_inhale, hs_ingestion, hs_other,ghs_code,prevention,rs_eye, rs_skin, rs_inhale, rs_ingestion, rs_other,storage, ghs_dict = retrieving(text)
        # if no ingredients gets detected then safe.html is displayed
        if element_names == "NO ELEMENT FOUND":
            count_text = len(text)
            return render(request, 'safe.html', {'count_text':count_text})
        return render(request, 'info.html', {
            'element_names':element_names,'hs_eye':hs_eye,'hs_skin':hs_skin,'hs_inhale':hs_inhale,'hs_ingestion':hs_ingestion,'hs_other':hs_other,'ghs_code':ghs_code,'prevention':prevention,'rs_eye':rs_eye,'rs_skin':rs_skin,'rs_inhale':rs_inhale,'rs_ingestion':rs_ingestion,'rs_other':rs_other,'storage':storage,'ghs_dict':ghs_dict})
    # if non of the conditions were satisfied, just displays the page with the forms for the user to enter
    else:
        uploadform = UploadFileForm()
        input_form = ChemForm()
    return render(request, 'sense.html', {'uploadform': uploadform,'input_form':input_form,'query_results':query_results})

# add your kid's allergic information
def addInfo(request,id=0):
    list1 = []
    list2 = []
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.method == 'POST':
        #id = 0 means creating the kids
        if id == 0:
            info_form = forms.AllergyInfoForm(request.POST)

        #update the kid's information
        else:
            #find and connect the kid instance using pk
            kid = models.UserAllergyinfo.objects.get(pk=id)
            info_form = forms.AllergyInfoForm(request.POST,instance=kid)
            if info_form.is_valid():
                kid_allergy = info_form.cleaned_data.get('kid_allergy')
                # clean the kid_allergy data
                if (kid_allergy):
                    for ele in kid_allergy:
                        list1.append(ele.allergycategory)
                        allergylist = ','.join(list1)

                    kid.kid_allergy = allergylist
                else:
                    kid.kid_allergy = "no allergy selected"

                info_form.save()
                return redirect('/index/')

        if info_form.is_valid():
            userid = request.session.get('user_id')
            # count the number of kids
            kid_no = models.UserAllergyinfo.objects.filter(userid=request.session.get('user_id')).count()
            if kid_no == None:
                kid_no = 1
            else:
                kid_no = kid_no + 1
            kid_id = kid_no
            kid_name = info_form.cleaned_data.get('kid_name')
            kid_allergy = info_form.cleaned_data.get('kid_allergy')
            personalised_allergy = info_form.cleaned_data.get('personalised_allergy')
            # create a new kid instance
            new_kid = models.UserAllergyinfo()
            new_kid.userid = userid
            new_kid.kid_id = kid_id
            new_kid.kid_name = kid_name
            # clean the kid_allergy data
            if (kid_allergy):
                for ele in kid_allergy:
                    list1.append(ele.allergycategory)
                    allergylist = ','.join(list1)

                new_kid.kid_allergy = allergylist
            else:
                new_kid.kid_allergy = "no allergy selected"

            new_kid.personalised_allergy = personalised_allergy
            new_kid.save()

    else:
        if id == 0:
            info_form = forms.AllergyInfoForm()
        else:
            kid = models.UserAllergyinfo.objects.get(pk=id)
            info_form = forms.AllergyInfoForm(instance=kid)
        return render(request, 'login/addinfo.html', {'form':info_form})

    return redirect('/index/')




# index page show all the kids' allergy information
def index(request):
    context = {'kidinfo_list':models.UserAllergyinfo.objects.filter(userid=request.session.get('user_id'))}
    return render(request, 'login/index.html',context)

# User login
def login(request):
    obj_num = models.UserAllergyinfo.objects.filter(userid=request.session.get('user_id')).count()
    # cannot login repeatly
    if request.session.get('is_login', None):
        if obj_num == 0:
            return redirect('/firstLogin/')
        else:
            return redirect('/index/')

    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = 'Please ensure the content is valid！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # validate if the user existed
            try:
                user = models.User.objects.get(username=username)
            except :
                message = 'The user does not exist！'
                return render(request, 'login/login.html', locals())

            if user.password_hash == hash_code(password):
                # use session to check user login status
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                kid_num = models.UserAllergyinfo.objects.filter(userid=user.id).count()
                # check whether the account has kids or not
                if kid_num == 0:
                    return redirect('/firstLogin/')
                else:
                    return redirect('/index/')
            else:
                message = 'Invalid password！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())

def register(request):
    # if user logged in, redirect to the index page
    if request.session.get('is_login', None):
        return redirect('/index/',locals())

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "Please ensure the content is valid！"

        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            # validate the username and password
            if password1 != password2:
                message = 'The passwords do not match！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                pattern = re.compile('[0-9]+')
                match = pattern.findall(password1)
                # 0521suqin
                pattern = re.compile('[a-zA-Z]')
                match1 = pattern.findall(password1)
                if same_name_user:
                    message = 'the username is already existed'
                    return render(request, 'login/register.html', locals())

                if  len(password1) < 8 or not match or not match1:
                    message = 'Make sure the password is at least 8 characters and contains at least one number.'
                    return render(request, 'login/register.html', locals())
                # save new user
                new_user = models.User()
                new_user.username = username
                new_user.password_hash = hash_code(password1)
                new_user.save()
                return redirect('/login/')

        else:
            return render(request, 'login/register.html', locals())

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

# User logout
def logout(request):
    if not request.session.get('is_login', None):
        # if not logged in, cannot log out
        return redirect("/login/")
    #delete the session
    request.session.flush()
    return redirect("/login/")

# delete the kid
def delete(reuqest,id):
    kid = models.UserAllergyinfo.objects.get(pk=id)
    kid.delete()
    return redirect('/index')

# hash the password
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    # add salt
    s += salt
    h.update(s.encode())
    return h.hexdigest()

# direct to firstLogin page if no kid in the account
def firstLogin(request):
    return render(request, "login/first account.html")

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

# the below function is used to ectract the text from an image
def read_text(img):
    # Ocr
    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)
    apikey = "66ecf22d2d88957"
    result = requests.post(url_api,
                 files = {"image.jpg": file_bytes},
                 data = {"apikey": apikey ,
                         "OCREngine":"2",
                         "detectOrientation":"True",
                         "scale":"True",
                         "language": "eng"})

    result = result.content.decode()
    result = json.loads(result)
    print(result)
    try:
        parsed_results = result.get("ParsedResults")[0]
        text_detected = parsed_results.get("ParsedText")
        print(1)
    except:
        scale_percent = 60 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
        file_bytes = io.BytesIO(compressedimage)
        apikey2 = "a8fce43d5888957"
        result = requests.post(url_api,
                     files = {"image.jpg": file_bytes},
                     data = {"apikey": apikey2 ,
                             "OCREngine":"1",
                             "detectOrientation":"True",
                             "scale":"True",
                             "language": "eng"})

        result = result.content.decode()
        result = json.loads(result)
        try:
            parsed_results = result.get("ParsedResults")[0]
            text_detected = parsed_results.get("ParsedText")
            print(2)
        except:
            text_detected =""
            print(3)
    print(text_detected)
    return text_detected

# the below code is used to process the image
def img_resize(img):
    if (os.path.getsize(img)/ (1024 * 1024)) > 1:
        img = cv2.imread(img)
        scale_percent = 60 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        return img
    else:
        return cv2.imread(img)

# the main function which calls the other functionalities
def final_text(img):
    img = img_resize(img)
    text = read_text(img)
    if text == "":
        text = ["not detected"]
    return text

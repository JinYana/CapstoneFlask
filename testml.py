import os
from io import BytesIO
import xml.etree.ElementTree as ET
import lxml
from lxml import objectify
from PIL import Image
from flask import Flask, request, flash, redirect
from deepface import DeepFace
from werkzeug.utils import secure_filename
import base64
import requests
import cv2
import matplotlib.pyplot as plt


def verify(img1_path,img2_path):
    
    output = DeepFace.verify(img1_path,img2_path)
    print(output)
    verification = output['verified']
    if verification:
       print('They are same')
    else:
       print('The are not same')

try: 
    result = verify(img1_path="img1.jpg", img2_path="img2.jpg")
except:
    print("Not the same person")
    
import pandas as pd
import re
import streamlit as st
import easyocr 
import numpy as np
from PIL import Image

st.title("Extracting Business Card Data with OCR")

# Load the EasyOCR reader
reader = easyocr.Reader(['en'])

#image uploader
uploaded_file = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])

if uploaded_file is not None:
    # Read the uploaded image file with EasyOCR
    image = uploaded_file.read()
    result = reader.readtext(image,detail=0,paragraph=True)

    with st.spinner("In progress"):        
         card_text = ' '.join([str(elem) for elem in result])
         card_text = card_text.replace(",", "")
         card_text = card_text.replace(";", "")
         name = result[0]
         Name1 = ' '.join([str(elem) for elem in name])
         Designation = re.findall(r"\s[D|M|T|G|C][A-Z]\w+\s?[&]?\s[A-Z]\w+", name)
         Designation1 = ''.join(str(elem) for elem in Designation)
         company_name = result[-2:]
         company_name1 = []
         for x in company_name:
             x = x.upper()
             company_name1.append(x)
         com_nam = ' '.join([str(elem) for elem in company_name1])
         Company_Name = re.findall(r"\s?[^W/./C][F|B|A-Z|]{3,}\s[A-Z]{8,}", com_nam)
         Company_name1 = ''.join(str(elem) for elem in Company_Name)
         phoneNums = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', card_text)
         Phone_Num = ''.join(str(elem) for elem in phoneNums)
         emails = re.findall(r"[A-Za-z]+@[A-Za-z0-9]+.[a-z]{3}", card_text)
         Email = ''.join(str(elem) for elem in emails)
         url_regex = r'(www|WWW|wWW)(\.)?\s?(?:\w+\.\w{2,3})?(?:\.\w{2})?'
         url = re.search(url_regex, card_text)
         if url:
            url = url.group(0)
         else:
            url = None
         address = re.findall(r"[123]{3}\s?[A-Za-z]{3,7}\s?[St]{2}", card_text)
         Address = ''.join(str(elem) for elem in address)
         state = re.findall(r"[T][a-z]{4}[N][a-z]{3}", card_text)
         State = ''.join(str(elem) for elem in state)
         pincode1 = re.findall(r"[1-9]{1}\d{2}\s?\d{3}", card_text)
         Pincode = ''.join(str(elem) for elem in pincode1)
         card_details = [Company_name1, Name1, Designation1, Phone_Num, Email, url, Address, State, Pincode]
         df = pd.DataFrame([card_details])
         df.columns = ['Company_Name', 'CardHolder_Name', 'Designation', 'Phone_Number', 'Email', 'URL', 'Address',
                   'State', 'pincode']

         st.write(df)

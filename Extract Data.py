import pandas as pd
import re
import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import sqlite3
import io

def delete_CARD(name):
    conn = sqlite3.connect("tutu.db")
    cursor = conn.cursor()  
    cursor.execute("DELETE FROM BizCard2 WHERE Cardholder_Name=?", (name,))
    conn.commit()
    conn.close()

def update_CARD(name,phone):
    conn = sqlite3.connect('tutu.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE BizCard2 SET Phone_Number = ?, URL = ? WHERE Cardholder_Name = ?", (phone, url, name))
    conn.commit()
    conn.close()

st.title("Extracting Business Card Data with OCR")
# Load the EasyOCR reader
reader = easyocr.Reader(['en'])
# image uploader
uploaded_file = st.file_uploader(label="Upload your image here", type=['png', 'jpg', 'jpeg'])

tab1, tab2= st.tabs(["EXTRACT TEXT", "DATABASE VIEW"])

with tab1:

  if uploaded_file is not None:
    # Read the uploaded image file with EasyOCR
     image = uploaded_file.read()
     st.image(image)

     with st.spinner(text="In progress..."):

        result1 = reader.readtext(image, detail=0, paragraph=True)
        card_text = ' '.join([str(elem) for elem in result1])
        card_text = card_text.replace(",", "")
        card_text = card_text.replace(";", "")
        name = result1[0].upper()
        Name = re.findall(r"^[A-Z]\w+", name)
        Name1 = ' '.join([str(elem) for elem in Name])
        Designation = re.findall(r"\s[D|M|T|G|C][A-Z]\w+\s?[&]?\s[A-Z]\w+", name)
        Designation1 = ''.join(str(elem) for elem in Designation)
        company_name = result1[-2:]
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
        df.columns = ['Company_Name', 'CardHolder_Name', 'Designation1', 'Phone_Number', 'Email', 'URL', 'Address',
                      'State', 'pincode']

        st.write(df)
     
        if st.button("upload"):

           with st.spinner(text="Uploading to Database..."):
    # Connect to the database
               conn = sqlite3.connect('tutu.db')

    # Create a cursor
               cursor = conn.cursor()

    # Create a table
               cursor.execute('''CREATE TABLE IF NOT EXISTS BizCard2
                         (Company_Name TEXT, CardHolder_Name TEXT, Designation TEXT,
                        Phone_Number INTEGER, Email TEXT, URL TEXT, Address TEXT  ,State TEXT, pincode  INTEGER
                        ,cardphoto BLOB NOT NULL)''')
    # card_photo=convertToBinaryData(image)
    # Insert data into the table
               sqlite_insert_with_param = """INSERT into Bizcard2 values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
               data_tuple = (Company_name1, Name1, Designation1, Phone_Num, Email, url, Address, State, Pincode, image)
               cursor.execute(sqlite_insert_with_param, data_tuple)
               conn.commit()

           st.success('Data has uploaded successfully!', icon="✅")


with tab2:
    conn = sqlite3.connect("tutu.db")
    cursor = conn.cursor()
    data=cursor.execute("SELECT * FROM BizCard2")
    for row in data:
        image_data = row[9]
        new_image = Image.open(io.BytesIO(image_data))

    def path_to_image_html(new_image):
        return '<img src="new_image" width="60" >'

    @st.cache_data
    def convert_df(input_df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
       return input_df.to_html(escape=False, formatters=dict(cardphoto=path_to_image_html))
   
   
    df1 = pd.read_sql_query("SELECT * FROM BizCard2", conn)
   
    html = convert_df(df1)

    st.markdown(
          html,unsafe_allow_html=True
     )
 
    option= st.selectbox('operations',('delete', 'update'))
    if option == 'delete':
       name = st.selectbox('Name',("  ","SELVA","AMIT","REVANTH","KARTHICK","SANTHOSH"))
       if name == "SELVA":
          delete_CARD(name)
       if name == "AMIT":
          delete_CARD(name)
       if name == "REVANTH":
          delete_CARD(name)
       if name == "KARTHICK":
          delete_CARD(name)
       if name == "SANTHOSH":
          delete_CARD(name)


    if option == 'update':
       name = st.selectbox('Name',("   ","SELVA","AMIT","REVANTH","KARTHICK","SANTHOSH"))
       if name ==  "SELVA":
          phone = st.text_input("Phone Number")
          url = st.text_input("URL")
          update_CARD(name,phone)
       if name ==  "AMIT":
          phone = st.text_input("Phone Number")
          url = st.text_input("URL")
          update_CARD(name,phone)
       if name ==  "REVANTH":
          phone = st.text_input("Phone Number")
          url = st.text_input("URL")
          update_CARD(name,phone)
       if name ==  "KARTHICK":
          phone = st.text_input("Phone Number")
          url = st.text_input("URL")
          update_CARD(name,phone)
       if name ==  "SANTHOSH":
          phone = st.text_input("Phone Number")
          url = st.text_input("URL")
          update_CARD(name,phone)
    # st.write(df1)
    # Commit the changes
    conn.commit()
    conn.close()

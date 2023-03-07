# Extracting-Data-from-image-using-OCR
  OCR is a technology that enables you to convert different types of documents, such as scanned paper documents, 
  PDF files, or images captured by a digital camera into editable and searchable data.
## Importing Libraries
      """import easyocr as ocr
         import streamlit as st
         import pandas as pd
         import sqlite3"""
### Streamlit
    Streamlit is an open-source app framework in python language.
    It helps us create beautiful web apps for data science and machine learning in a little time. 
    It is compatible with major python libraries such as scikit-learn, keras, PyTorch, latex, numpy, pandas, matplotlib, etc
        """st.title("Extracting Business Card Data with OCR")
           uploaded_file = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])
           st.button('upload')
           st.button('download')"""
       
       
       

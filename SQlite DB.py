import pandas as pd
import re
import streamlit as st
import easyocr 
import numpy as np
from PIL im
    import sqlite3

    # Connect to the database
    conn = sqlite3.connect('sim.db')

    # Create a cursor
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS BizCard 
                        (Company_Name TEXT, CardHolder_Name TEXT, Designation TEXT, 
                        Phone_Number INTEGER, Email TEXT, URL TEXT, Address TEXT  ,State TEXT, pincode  INTEGER)''')

    # Insert data into the table
    sqlite_insert_with_param = """INSERT into Bizcard values (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    data_tuple = (Company_name1, Name1, Designation1, Phone_Num, Email, url, Address, State, Pincode)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    df1 = pd.read_sql_query("SELECT * FROM Bizcard", conn)
    print(df1)
    st.write("success")
    # Commit the changes
    conn.commit()
    conn.close()
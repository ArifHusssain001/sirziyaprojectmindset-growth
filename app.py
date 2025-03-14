import streamlit as st
import pandas as pd
import os 
from io import BytasIO

st.set_page_config(page_title = "Data Sweeper", layout='wide' )

#custam css
st.markdown(
    """
    <style>
    .stApp{
       background-color: black;
       color: white;

       }
       </style>
       """,
       unsafe_allow_html=True
)
# title and description
st.title("Datasweeper Sterling Integerator By Arif Hussain")
st.write("Transform your files between CSV  and Excel format ")

#file uploader 
uploaded_files = st.file_uploader("upload your files (accepts CSV or Excel):", type=["cvs","xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
    
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsipported file type: {file_ext}"), 
            continue
    # file details
    st.write("preview the head of the dataframe")
    st.dataframe(df.head())
    # data Cleaning options
    st.subheader("Data Cleaning options")
    if st.checkbox(f"Clean data for {file.name}"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Remove duplicates from the file : {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Dublicates removed!")
        with col2:
            if st.button(f"fill mising Values for {file.name}"):
                numeric_cols = df.select_dtypes(includes=['number']).colums
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing value have been filles!")

    st.subheader("Select Columns to keep")
    colomns = st.multiselect(f"Choose colomns for {file.name}", df.colomns, default=df.colomns)
    df = df[colomns]

    #data visualization
    st.subheader("Data visualization")
    if st.checkbox(f"Show visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

    #Converstion Options
    st.subheader("Coversion Option")
    conversion_type = st.radio(f"Convert {file.name} to:", ["cvs", "Excel"], Key=file.name)
    if st.button(f"Convert{file.name}"):
        Buffer = BytasIO()
        if conversion_type == "csv":
            df.to.csv(Buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"

        elif conversion_type == "Excel":
            df.to.to_excel(Buffer, index=False)
            file_name = file.name.replace(file_ext, ".xlsx")
            mime_type = "application/Vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        Buffer.seek(0)   

        st.download_button(
            label=f"Download {file.name} as {conversion_type}",
            data=Buffer,
            file_name=file_name,
            mime=mime_type

        )     
st.success("All files Processed successfully!")    

#growth mindset challenge web app with streamlit | giaic quarter 3 project # mahak malik




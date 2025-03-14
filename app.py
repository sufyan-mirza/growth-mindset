import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up the page configuration
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Welcome to *Data Convert and Cleanify* 💿✨")
st.write("Convert your files between CSV and Excel formats 🔄, with powerful built-in data cleaning 🧹 and stunning visualizations 📈 to make your data truly stand out! 🌟")

# File uploader for CSV or Excel files
uploadedfile = st.file_uploader("Upload your files (CSV OR Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploadedfile:
    for file in uploadedfile:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the uploaded file based on its extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        # Display info about the uploaded file
        st.write(f"*File Name:* {file.name}")
        st.write(f"*File Size:* {file.size/1024:.2f} KB")

        # Preview the first few rows of the dataframe
        st.write("### Preview the Head of the Dataframe:")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates Removed! ✅")

            with col2:
                if st.button(f"Fill Missing Values from {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing Values Filled! ✅")

        # Choose specific columns to keep or convert
        st.subheader("🔲 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Visualization options
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.write("Here's a quick visual representation of your data:")
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File conversion (CSV <-> Excel)
        st.subheader("💾 Convert File")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download button for converted file
            st.download_button(
                label=f"Download {file.name} as {conversion_type} 🡆",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
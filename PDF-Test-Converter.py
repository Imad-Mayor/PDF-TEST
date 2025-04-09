# Import necessary libraries
import streamlit as st
import os
from pdf2docx import parse
from pdf2image import convert_from_path
import PyPDF2

# Set up the Streamlit app
st.title("📄 PDF Converter App")
st.write("Upload a PDF file and convert it to various formats")

# Create a file uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Define the output directory (we'll use a temporary one)
OUTPUT_DIR = "output_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to convert PDF to Word (DOCX)
def convert_to_docx(pdf_path, output_path):
    try:
        parse(pdf_path, output_path)
        return True
    except Exception as e:
        st.error(f"Error converting to DOCX: {e}")
        return False

# Function to convert PDF to images (one per page)
def convert_to_images(pdf_path, output_folder):
    try:
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image.save(f"{output_folder}/page_{i+1}.jpg", "JPEG")
        return True
    except Exception as e:
        st.error(f"Error converting to images: {e}")
        return False

# Function to extract text from PDF
def extract_text(pdf_path, output_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            with open(output_path, "w", encoding="utf-8") as text_file:
                text_file.write(text)
            return True
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return False

# If a file is uploaded
if uploaded_file is not None:
    # Display file info
    st.success("File uploaded successfully!")
    st.write(f"File name: {uploaded_file.name}")
    
    # Save the uploaded file temporarily
    temp_pdf_path = os.path.join(OUTPUT_DIR, uploaded_file.name)
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Create conversion options
    st.subheader("Conversion Options")
    col1, col2, col3 = st.columns(3)
    
    # DOCX conversion
    with col1:
        if st.button("Convert to Word (DOCX)"):
            output_docx = os.path.join(OUTPUT_DIR, f"{os.path.splitext(uploaded_file.name)[0]}.docx")
            if convert_to_docx(temp_pdf_path, output_docx):
                st.success("Conversion to DOCX successful!")
                with open(output_docx, "rb") as f:
                    st.download_button(
                        label="Download DOCX",
                        data=f,
                        file_name=os.path.basename(output_docx),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
    
    # Image conversion
    with col2:
        if st.button("Convert to Images (JPG)"):
            output_images_dir = os.path.join(OUTPUT_DIR, "images")
            os.makedirs(output_images_dir, exist_ok=True)
            if convert_to_images(temp_pdf_path, output_images_dir):
                st.success("Conversion to JPG images successful!")
                # Create a zip file of all images
                import zipfile
                zip_path = os.path.join(OUTPUT_DIR, "images.zip")
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for root, _, files in os.walk(output_images_dir):
                        for file in files:
                            zipf.write(os.path.join(root, file), file)
                
                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="Download Images (ZIP)",
                        data=f,
                        file_name="converted_images.zip",
                        mime="application/zip"
                    )
    
    # Text extraction
    with col3:
        if st.button("Extract Text (TXT)"):
            output_txt = os.path.join(OUTPUT_DIR, f"{os.path.splitext(uploaded_file.name)[0]}.txt")
            if extract_text(temp_pdf_path, output_txt):
                st.success("Text extraction successful!")
                with open(output_txt, "rb") as f:
                    st.download_button(
                        label="Download Text",
                        data=f,
                        file_name=os.path.basename(output_txt),
                        mime="text/plain"
                    )
    
    # Clean up temporary files (optional)
    # os.remove(temp_pdf_path)

# Add some instructions
st.markdown("""
### How to use this app:
1. Upload a PDF file using the file uploader
2. Click one of the conversion buttons
3. Download your converted file when it appears
4. Upload pdf file in lower sizes to save time            
""")

# Note about dependencies
st.info("""
Note: This app requires the following Python packages:
- streamlit
- pdf2docx
- pdf2image
- PyPDF2
- pillow (for image handling)
""")
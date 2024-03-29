import os
import fitz  # PyMuPDF

def convert_pdf_to_txt(pdf_path, output_folder):
    """
    Convert a PDF file to a text file.

    :param pdf_path: Path to the PDF file to be converted.
    :param output_folder: Folder where the text file will be saved.
    """
    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        text = ""
        # Iterate through each page and extract text
        for page in doc:
            text += page.get_text()

    # Generate the output text file path
    output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(pdf_path))[0] + ".txt")
    
    # Save the extracted text to a file
    with open(output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

def convert_folder_pdfs_to_txt(folder_path, output_folder):
    """
    Convert all PDF files in a folder to text files.

    :param folder_path: Path to the folder containing PDF files.
    :param output_folder: Folder where the text files will be saved.
    """
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Walk through the folder, and process each PDF file
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                print(f"Converting {pdf_path} to text...")
                convert_pdf_to_txt(pdf_path, output_folder)
                print(f"Finished converting {pdf_path}")

# Example usage
folder_path = "content/Surgery"  # Update this to your folder path
output_folder = "content/Surgery"   # Update this to your desired output path
convert_folder_pdfs_to_txt(folder_path, output_folder)
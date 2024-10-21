# [1] Import generic libraries
import io
import os
import csv
import datetime
import requests
import numpy as np
from pathlib import Path

# [2] Import image-processing libraries
import cv2
from PIL.ExifTags import TAGS
from PIL import Image, ImageFilter, ImageEnhance

# [3] Import OCR libraries
import easyocr
import pytesseract

# ================================================================================================================================================

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify the languages you want to use

# Set the tesseract_cmd to your Tesseract installation path
# pytesseract.pytesseract.tesseract_cmd = r'<path_to_tesseract.exe>'  # Adjust the path as needed

# ================================================================================================================================================

# *************************************************************
# ******* GENERIC FUNCTIONS ***********************************
# *************************************************************

def get_file_extension(file_name):
    _, ext = os.path.splitext(file_name) # Split the file name into the name and extension
    return ext

def get_filename_without_extension(file_path):
    path = Path(file_path) # Create a Path object from the file path
    return path.stem # Return the name without the extension

def get_filename_with_extension(filepath):
    return os.path.basename(filepath) # Use os.path.basename to extract the filename with extension

def get_valid_directory(): # Function to validate the user-provided directory path
    while True:
        directory_path = input(">> Enter the directory where you would like to save the OCR results: ")
        if os.path.isdir(directory_path):
            return directory_path
        else:
            print(f">> Invalid path: {directory_path}. Please enter a valid directory path.")

def get_valid_text_file_path():
    while True:
        text_file_path = input(">> Enter the path to the text file containing image file paths or URLs: ")
        # Check if the file exists and is a file
        if os.path.isfile(text_file_path):
            return text_file_path
        else:
            print(f">> Invalid file path. Please enter a valid text file path.")

def select_option():
    # Prompt user to select the source of images
    while True:
        print(">> Select desired option:")
        print("\t- Press 1 to process and OCR images stored in a local folder")
        print("\t- Press 2 to process and OCR images stored in image URLs")
        option = input("\tEnter your choice (1 or 2): ")

        if option in ['1', '2']:
            break
        else:
            print(">> Invalid choice. Please enter 1 or 2.\n")
    return option


def load_image_from_url(image_url):
    try:
        # Step 1: Download the image from the URL
        response = requests.get(image_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            image_data = response.content

            # Return the image data
            return image_data
        
        else:
            print(f">> Failed to download image from URL: {image_url}. Status Code: {response.status_code}")
    except Exception as e:
        print(f">> An error occurred while loading image from URL: {image_url}.  {e}")
        return None


# ************************************************************
# ******* ORIENTATION FUNCTION *******************************
# ************************************************************

def correct_image_orientation(image_data):
    try:
        # Open the image from byte data
        image = Image.open(io.BytesIO(image_data))

        # Get EXIF data (if it exists)
        exif_data = image._getexif()

        if exif_data:
            # Find the orientation tag in the EXIF data
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'Orientation':
                    orientation = value
                    
                    # If orientation is 6 (90° CCW), rotate it to orientation 3 (180°)
                    if orientation == 6:
                        oriented_image = image.rotate(-180, expand=True)
                        oriented_image_bytes_io = io.BytesIO()
                        oriented_image.save(oriented_image_bytes_io, format='JPEG')
                        oriented_image_bytes = oriented_image_bytes_io.getvalue()
                        return oriented_image_bytes

        # Return the original image if no orientation correction is needed or no EXIF data &
        # Convert back to image in bytes format (image_data)
        original_image_bytes_io = io.BytesIO()
        image.save(original_image_bytes_io, format='JPEG')
        original_image_bytes = original_image_bytes_io.getvalue()
        return original_image_bytes

    except Exception as e:
        print(f">> An error occurred while correcting image orientation: {e}")
        return None

# *************************************************************
# ******* PREPROCESSING FUNCTIONS *****************************
# *************************************************************

def preprocess_image(image_data, blur_radius, factor):
    # Step 1: Convert to grayscale
    gray_image = convert_image_to_grayscale(image_data)

    # Step 2: Apply gaussian blur
    blurred_image = apply_blur(gray_image, blur_radius)

    # Step 3: Enhance contrast
    enhanced_image = enhance_contrast(blurred_image, factor)

    # Step 4: Apply thresholding to create a binary image (OPTIONAL)
    # binary_image = apply_threshold(enhanced_image)

    return enhanced_image
    # return binary_image

# ---------------------------------------------------------------

def convert_image_to_grayscale(image_data):
    try:
        # Open the image from byte data
        image = Image.open(io.BytesIO(image_data))

        # Convert the image to RGB if it's not in RGB mode
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert the PIL Image to a NumPy array
        image_np = np.array(image)

        # Convert the image to grayscale using OpenCV
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

        # Convert the NumPy array back to a PIL Image
        gray_image_pil = Image.fromarray(gray_image)

        return gray_image_pil

    except Exception as e:
        print(f">> An error occurred while converting to grayscale: {e}")
        return None
    

def apply_blur(image, blur_radius):
    # Zero (0) - No blur is applied
    # Small Values (0.1 to 2.0) - Light blur
    # Medium Values (2.0 to 5.0)- Moderate blur
    # Large Values (5.0 and above)- Heavy blur

    try:
        if image is None:
            raise ValueError(">> Image data is None. Cannot apply blur.")
        
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        return blurred_image

    except Exception as e:
        print(f">> An error occurred while applying blur: {e}")
        return None


def enhance_contrast(image, factor):
    # factor < 1.0 - Decreases the contrast of the image
    # factor = 1.0 - Leaves the image unchanged. This is the default factor.
    # factor > 1.0 - Increases the contrast of the image

    try:
        # Create an ImageEnhance object for contrast
        enhancer = ImageEnhance.Contrast(image)
        
        # Apply the enhancement
        enhanced_image = enhancer.enhance(factor)

        return enhanced_image

    except Exception as e:
        print(f">> An error occurred while enhancing contrast with Pillow: {e}")
        return None
    

def apply_threshold(image):
    try:
        # Convert PIL Image to NumPy array
        image_np = np.array(image)

        # Apply binary thresholding
        _, binary_image_np = cv2.threshold(image_np, 128, 255, cv2.THRESH_BINARY)
        # _, binary_image_np = cv2.threshold(image_np, 120, 255, cv2.THRESH_BINARY, )

        # Convert back to PIL Image
        binary_image = Image.fromarray(binary_image_np)

        return binary_image

    except Exception as e:
        print(f">> An error occurred while applying threshold: {e}")
        return None
    

# ************************************************************
# ******* OCR FUNCTION ***************************************
# ************************************************************

# OCR Engine [1]: EasyOCR 
def ocr_using_easyocr(reader, image):
    try:
        image_np = np.array(image) # Convert PIL image to numpy array
        result = reader.readtext(image_np) # Perform OCR on the image
        recognized_text = ' '.join([entry[1] for entry in result]) # Extract the text from the result
        return recognized_text

    except Exception as e:
        print(f">> An error occurred while performing OCR: {e}")
        return None

# OCR Engine [2]: Tesseract
def ocr_using_pytesseract(image):
    try:
        # Use pytesseract to extract text from the image
        recognized_text = pytesseract.image_to_string(image)

        return recognized_text

    except Exception as e:
        print(f">> An error occurred while performing OCR: {e}")
        return None

# *************************************************************
# ******* CLEAN RAW TEXT FUNCTIONS *****************************
# *************************************************************

def clean_raw_text(image_text):
    lines = image_text.splitlines()  # or use image_text.split('\n')
    
    cleaned_lines = []

    for index, line in enumerate(lines, start=0):  # Start numbering from 0
        stripped_line = line.strip()

        # Filter out noisy lines
        if is_noise(stripped_line):
            continue

        # Remove pipe symbols from the line
        stripped_line = stripped_line.replace('|', '')

        # Add valid lines to cleaned_lines
        cleaned_lines.append(stripped_line)

    # Join the cleaned lines back together
    return " ".join(cleaned_lines)

# ---------------------------------------------------------------

def is_noise(line):
    # Strip leading/trailing spaces
    stripped_line = line.strip()

    # 1. If the line is empty after stripping, consider it noise
    if not stripped_line:
        return True

    # 2. Check if all segments are less than 4 characters long
    segments = stripped_line.split()
    all_short = all(len(segment) < 4 for segment in segments)
    if all_short:
        return True

    # 3. If the line contains only one character, consider it noise
    if len(stripped_line) == 1:
            return True
    
    return False # If none of the noise conditions are met, return False

# ================================================================================================================================================

def main():

    print(">> Starting data processing ...\n")

    option = select_option()

    # Get the path to the text file from the user
    text_file_path = get_valid_text_file_path()
    text_file_name = get_filename_with_extension(text_file_path)

    # Read image paths or URLs from the text file
    try:
        with open(text_file_path, 'r') as file:
            image_file_list = [line.strip() for line in file.readlines() if line.strip()]  # Remove empty lines
    except Exception as e:
        print(f">> An error occurred while reading the text file: {text_file_name}. {e}")
        return

    if not image_file_list:
        print(">> No valid images found in the specified text file. Exiting program.")
        return
    
    print(f">> Text file '{text_file_name}' was successfully loaded!")
    print(f">> There are {len(image_file_list)} images to be processed.")

    # Get valid directory path from the user
    output_directory_path = get_valid_directory()

    # CSV file with OCR results
    csv_filename = f"OCR_Results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csv_file_path = os.path.join(output_directory_path, csv_filename)

    # ------------------------------------------------------------------------------------------------

    # Write the extracted data to a CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["index_image", "timestamp", "image_path", "extracted_text"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='|')

        # Write the header
        writer.writeheader()

        # Loop to process each image
        for index, image_path in enumerate(image_file_list):
            print(f"\t[+] Processing and performing OCR on image ... {image_path}")

            # Step 1: Load image from URL or local file
            if option == '1':  # --- Local files
                try:
                    with open(image_path, 'rb') as file:
                        image_data = file.read()
                except Exception as e:
                    print(f">> An error occurred while loading the local file: {image_path}")
                    continue

            else: # --- Image URLs
                image_data = load_image_from_url(image_path)

            # If image data is not None, proceed with OCR
            if image_data:

                # Step 2: Correct image orientation
                oriented_image = correct_image_orientation(image_data)

                # Step 3: Preprocess the image
                enhanced_image = preprocess_image(oriented_image, 0.0 , 1.5)

                # Step 4: Perform OCR on the enhanced image
                recognized_text = ocr_using_easyocr(reader, enhanced_image) # Using EasyOCR
                # recognized_text = ocr_using_pytesseract(enhanced_image) # Using Tesseract

                # Step 5: Clean the raw OCR text
                clean_text = clean_raw_text(recognized_text)

                # Step 6: Get the current timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Step 7: Write the recognized text to CSV
                data = {
                    "index_image": index + 1,
                    "timestamp": timestamp,
                    "image_path": image_path,
                    "extracted_text": f'"{clean_text}"'
                }
                writer.writerow(data)



    print(f"\n>> Data has been successfully written to {csv_file_path}")
    print(">> Program execution completed.\n")
   
if __name__ == '__main__':
    main()
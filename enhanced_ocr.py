# [1] Import generic libraries
import io
import os
import numpy as np
from pathlib import Path

# [2] Import image-processing libraries
import cv2
from PIL import Image, ImageFilter, ImageEnhance

# [3] Import OCR libraries
# import easyocr
import pytesseract

# ================================================================================================================================================

# Set the tesseract_cmd to your Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\andres\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Adjust the path as needed

# ================================================================================================================================================

# *************************************************************
# ******* GENERIC FUNCTIONS ***********************************
# *************************************************************

def get_filename_without_extension(file_path):
    path = Path(file_path) # Create a Path object from the file path
    return path.stem # Return the name without the extension


# *************************************************************
# ******* PREPROCESSING FUNCTIONS *****************************
# *************************************************************

def preprocess_image(image_data, output_file_path, blur_radius, factor):
    # Step 1: Convert to grayscale
    gray_image = convert_image_to_grayscale(image_data)

    # Step 2: Apply gaussian blur
    blurred_image = apply_blur(gray_image, blur_radius)

    # Step 3: Enhance contrast
    enhanced_image = enhance_contrast(blurred_image, factor)

    # Step 4: Apply thresholding to create a binary image (OPTIONAL)
    # binary_image = apply_threshold(enhanced_image)

    # Step 5: Save to TIFF
    save_image_to_tiff(enhanced_image, output_file_path)


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
            raise ValueError("Image data is None. Cannot apply blur.")
        
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


def save_image_to_tiff(image, output_file_path):
    try:
        if image is None:
            raise ValueError(">> Image data is None. Cannot save.")
        
        image.save(output_file_path, format='TIFF')

    except Exception as e:
        print(f">> An error occurred while saving the image: {e}")


# *************************************************************
# ******* OCR FUNCTION ***************************************
# *************************************************************

def ocr_using_pytesseract(image_file_path):
    try:
        # Load the image from file
        image = Image.open(image_file_path)

        # Use pytesseract to extract text from the image
        recognized_text = pytesseract.image_to_string(image)

        return recognized_text

    except Exception as e:
        print(f">> An error occurred while performing OCR: {e}")
        return None


def ocr_using_easyocr(reader, image_file_path):
    try:
        # Perform OCR on the image
        result = reader.readtext(image_file_path)

        # Extract the text from the result
        recognized_text = '\n'.join([entry[1] for entry in result])

        return recognized_text

    except Exception as e:
        print(f">> An error occurred while performing OCR: {e}")
        return None


# ================================================================================================================================================

def main():

    # Initialize EasyOCR reader
    # reader = easyocr.Reader(['en'])

    directory = r"C:\Users\andres\Fiverr\01. Testing\26. Enhanced OCR Toolkit\images"
    out_directory = r"C:\Users\andres\Fiverr\01. Testing\26. Enhanced OCR Toolkit\tiff"

    for filename in os.listdir(directory):
        image_filepath = os.path.join(directory, filename)
        out_image_filepath = os.path.join(out_directory, get_filename_without_extension(filename) + '.tiff')

        with open(image_filepath, 'rb') as f:
            image_data = f.read()

        # Step 1: Preprocess image
        preprocess_image(image_data, out_image_filepath, 0.0 , 1.5)

        # Step 2: Perform OCR on the newly created TIFF image
        recognized_text = ocr_using_pytesseract(out_image_filepath)
        # recognized_text = ocr_using_easyocr(reader, out_image_filepath)

        # Step 3: Print or save the recognized text
        print(f">> Recognized text from {filename}:\n{recognized_text} \n======================================================================== \n")
   

if __name__ == '__main__':
    main()
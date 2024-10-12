# 🔍 Enhanced OCR Toolkit 📄✨

Welcome to the Enhanced OCR Toolkit! This Python-based tool enhances your ability to extract text from images by improving the image quality and performing OCR (Optical Character Recognition). It operates in two major phases: image preprocessing and image OCR. The tool integrates powerful libraries like Pillow, OpenCV, pytesseract, and optionally, EasyOCR, to deliver accurate results.


# 📜 Features

* 🖼️ **Image Preprocessing:** Clean up and enhance images to improve OCR accuracy.
* 💾 **TIFF Conversion:** Convert processed images to high-quality TIFF format for further processing.
* ⚙️ **Customizable Parameters:** Fine-tune blur radius, contrast, and other preprocessing parameters to get the best results.
* 🔍 **OCR Support:** Extract text from images using popular Python OCR libraries, including pytesseract and EasyOCR.


# 🚀 How It Works

This toolkit follows a two-step process:

1️⃣ Image Preprocessing

The preprocessing phase helps improve the quality of the input images to increase OCR accuracy. This phase consists of several sub-steps:

1. **Grayscale Conversion 🎨:** Images are converted to grayscale to simplify further processing.
2. **Gaussian Blur 🌫️:** Optional blur is applied to smooth the image and reduce noise.
3. **Contrast Enhancement ⚡:** The image contrast is boosted to make text stand out.
4. **Thresholding 🌓:** (Optional) Converts the image to a binary format (black & white) for easier OCR.

All preprocessing steps are done using **Pillow** and **OpenCV**.

2️⃣ Image OCR

Once the images are preprocessed, the toolkit applies OCR to extract text using one of the following libraries:

* **pytesseract 🖥️:** An open-source OCR engine for recognizing text in images.
* **EasyOCR 🤖:** A deep learning-based OCR library with multilingual support.


# 🔧 Installation

To use this toolkit, you need Python 3.x installed along with a few required libraries. Follow these steps to set up the environment:

- **Clone this repository**
  
    git clone https://github.com/dsprovider/enhanced_ocr_toolkit.git

- **Navigate to the project directory**

    cd enhanced_ocr_toolkit

- **Install the required dependencies**
  
    pip install -r requirements.txt


# 📦 Additional Setup

For pytesseract, ensure that you have Tesseract OCR installed on your machine (https://tesseract-ocr.github.io/tessdoc/Installation.html)

**Installed version: v5.4.0.20240606**

*pytesseract.pytesseract.tesseract_cmd = r'C:\path_to_tesseract\tesseract.exe'*


# 📂 Usage

1. Place the images you want to process in the input images folder.

2. Run the script to preprocess the images and perform OCR.

   python enhanced_ocr.py

3. The enhanced images will be saved in the output images directory in TIFF format.


# ⚙️ Customizing Preprocessing Parameters

**Customizable Parameters**

* *Function: def enhance_contrast(image, factor)*

    - factor < 1.0: Decreases the contrast of the image
 
    - factor = 1.0: Leaves the image unchanged (default setting)
 
    - factor > 1.0: Increases the contrast of the image

* *Function: def apply_blur(image, blur_radius)*

    - blur_radius = 0: No blur is applied
      
    - blur_radius (0.1 to 2.0): Light blur
      
    - blur_radius (2.0 to 5.0): Moderate blur
      
    - blur_radius > 5.0: Heavy blur

    factor < 1.0 - Decreases the contrast of the image
    factor = 1.0 - Leaves the image unchanged. This is the default factor.
    factor > 1.0 - Increases the contrast of the image

# 🔍 Future Improvements



# 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.



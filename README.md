# 🔍 Enhanced OCR Toolkit 📄✨

Welcome to the Enhanced OCR Toolkit! This Python-based tool enhances your ability to extract text from images by improving the image quality and performing OCR (Optical Character Recognition). It operates in two major phases: image preprocessing and image OCR. The tool integrates powerful libraries like Pillow, OpenCV, pytesseract, and EasyOCR, to deliver accurate results.


# 📜 Features

* 🖼️ **Image Preprocessing:** Clean up and enhance images to improve OCR accuracy.
* ⚙️ **Customizable Parameters:** Fine-tune blur radius, contrast, and other preprocessing parameters to get the best results.
* 🔍 **OCR Support:** Extract text from images using popular Python OCR libraries, including pytesseract and EasyOCR.


# 🚀 How It Works

This toolkit follows a two-step process:

1️⃣ Image Preprocessing

The preprocessing phase helps improve the quality of the input images to increase OCR accuracy. This phase consists of several sub-steps:

1. **Orientation Check 🔄:** The image is analyzed for its orientation, and if it is rotated, it is corrected to an upright position before further processing.
2. **Grayscale Conversion 🎨:** Images are converted to grayscale to simplify further processing.
3. **Gaussian Blur 🌫️:** Optional blur is applied to smooth the image and reduce noise.
4. **Contrast Enhancement ⚡:** The image contrast is boosted to make text stand out.
5. **Thresholding 🌓:** (Optional) Converts the image to a binary format (black & white) for easier OCR.

All preprocessing steps are done using **Pillow** and **OpenCV**.

2️⃣ Image OCR

Once the images are preprocessed, the toolkit applies OCR to extract text using one of the following libraries:

* **pytesseract 🖥️:** An open-source OCR engine for recognizing text in images.
* **EasyOCR 🤖:** A deep learning-based OCR library with multilingual support.

**3️⃣ Text Cleaning**

After extracting the raw text through OCR, a cleaning process is applied to enhance the accuracy and readability of the results. The following steps are executed in the text cleaning phase:

* **Line Splitting 📝**: The raw OCR text is split into individual lines for further processing.
* **Noise Filtering 🚫**: Each line is evaluated for potential noise. Lines are removed if they:
  - Are empty or contain only whitespace.
  - Consist entirely of short segments (less than 4 characters).
  - Contain only a single character.

* **Symbol Removal 🔧**: Unwanted symbols, such as pipe (|) characters, are removed from each line.
* **Reconstruction 🔄**: The cleaned lines are reassembled into a text block, with proper spacing.


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

This tool offers flexibility in providing input images for OCR processing and exporting the results. You can provide the input images in two different ways via the command prompt:

**Local Processing**

Supply a text file that contains the full file paths of the images stored on your local machine. Each image path should be listed on a new line. This method allows you to process images that are already available on your device.

*/path/to/image1.jpg*
*/path/to/image2.png*
*/path/to/image3.tiff*


**Remote Processing (Image URLs)**

Provide a text file that contains a list of URLs for images hosted on a server. Each URL should be on a new line. This option allows you to process images directly from their server location without downloading them manually.

*https://example.com/images/image1.jpg*
*https://example.com/images/image2.png*
*https://example.com/images/image3.tiff*

After specifying the images input file, you will be prompted to enter the folder path where the cleaned OCR results will be exported as a CSV file. This file will contain the extracted and cleaned text from the images. Once the process is complete, a CSV file with the extracted OCR text will be generated in the specified folder.


# ⚙️ Customizing Preprocessing Parameters

**Customizable Parameters**

* *def enhance_contrast(image, factor)*

    - factor < 1.0: Decreases the contrast of the image
 
    - factor = 1.0: Leaves the image unchanged (default setting)
 
    - factor > 1.0: Increases the contrast of the image

* *def apply_blur(image, blur_radius)*

    - blur_radius = 0: No blur is applied
      
    - blur_radius (0.1 to 2.0): Light blur
      
    - blur_radius (2.0 to 5.0): Moderate blur
      
    - blur_radius > 5.0: Heavy blur


# 🔍 Future Improvements

* **🛠️ Advanced Image Preprocessing Techniques:** Implement more sophisticated methods such as noise reduction and edge detection to further enhance image quality and OCR accuracy.

* **📊 Image Clustering:** Develop a more specialized approach for processing different types of images. This could include custom workflows for recognizing text from specific categories, such as: driving license plates, ID cards, billboards, receipts, etc


# 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.



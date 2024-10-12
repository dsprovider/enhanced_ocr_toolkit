# 🔍 Enhanced OCR Toolkit 📄✨

Welcome to the Enhanced OCR Toolkit! This Python-based tool enhances your ability to extract text from images by improving the image quality and performing OCR (Optical Character Recognition). It operates in two major phases: image preprocessing and image OCR. The tool integrates powerful libraries like Pillow, OpenCV, pytesseract, and optionally, EasyOCR, to deliver accurate results.


# 📜 Features

* 🖼️ Image Preprocessing: Clean up and enhance images to improve OCR accuracy.
* 🔍 OCR Support: Extract text from images using popular Python OCR libraries, including pytesseract and EasyOCR.
* 💾 TIFF Conversion: Convert processed images to high-quality TIFF format for further processing.
* ⚙️ Customizable Parameters: Fine-tune blur radius, contrast, and other preprocessing parameters to get the best results.


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


# Additional Setup

For pytesseract, ensure that you have Tesseract OCR installed on your machine.

*pytesseract.pytesseract.tesseract_cmd = r'C:\path_to_tesseract\tesseract.exe'*


# 📂 Usage


# Customizing Preprocessing Parameters



# 🔍 Future Improvements



# 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.



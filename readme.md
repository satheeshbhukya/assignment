# Text OCR – Streamlit App (Offline)

An **offline Optical Character Recognition (OCR)** application built using **Python, OpenCV, Tesseract OCR, and Streamlit**.
The app allows users to upload an image, extract text, visualize bounding boxes with confidence scores, and download results as **TXT** and **JSON** files.

---

## Project Structure

```
assignment/
│
├── scripts/
│   └── main.py          # Streamlit app
│
├── requirements.txt     # Project dependencies
└── README.md
```

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/satheeshbhukya/assignment.git
```

```bash
cd assignment/scripts
```

---

### Create and Activate Virtual Environment (Recommended)

```bash
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

---

### Install Dependencies

All dependencies are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

---

## Tesseract OCR Setup

Install **Tesseract OCR** locally.

**Default Windows path:**

```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

Ensure this path is correctly set in `main.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

If Tesseract is installed elsewhere, update the path accordingly.

---

## Run the Streamlit App

From the `scripts` directory:

```bash
streamlit run main.py
```

The app will open automatically in your browser.
If not, open:

```
http://localhost:8501
```

---

## How to Use

1. Upload an image (`.png`, `.jpg`, `.jpeg`)
2. Click **Run OCR**
3. View:

   * Preprocessed image
   * Annotated image with bounding boxes
   * Extracted text
   * JSON word-level data
4. Download:

   * Extracted text file
   * OCR results in JSON format

---

## Outputs

The application generates:

* Extracted text (`.txt`)
* OCR word data (`.json`)
* Annotated visualization (displayed in UI)

---

## Features

* Fully offline OCR
* Bounding box visualization
* Confidence scores
* Downloadable results
* Simple and clean Streamlit UI

---

## Notes

* Best results with **high-contrast images**
* Character whitelist optimized for **uppercase letters and digits**

---

## Future Improvements

* Image deskewing
* Confidence threshold slider
* Line-level OCR
* Batch image processing
* Webcam input support    

---

## Author

**Satheesh Bhukya**
**Project:** Assignment – OCR Streamlit App

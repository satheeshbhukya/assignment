import cv2
import json
import pytesseract
import numpy as np
from pathlib import Path
import streamlit as st
from PIL import Image

# Configuration
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

OUTPUT_DIR = "outputs"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    inverted = cv2.bitwise_not(gray)

    h, w = inverted.shape
    upscaled = cv2.resize(
        inverted, (w * 3, h * 3),
        interpolation=cv2.INTER_CUBIC
    )
    return upscaled


def perform_ocr(processed_image):
    config = "--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    text = pytesseract.image_to_string(
        processed_image, config=config
    )

    data = pytesseract.image_to_data(
        processed_image,
        config=config,
        output_type=pytesseract.Output.DICT
    )

    return text, data


def extract_text_data(ocr_data, scale=3):
    results = []

    for i in range(len(ocr_data["text"])):
        word = ocr_data["text"][i].strip()
        if not word:
            continue

        confidence = int(float(ocr_data["conf"][i]))
        if confidence > 0:
            x = ocr_data["left"][i] // scale
            y = ocr_data["top"][i] // scale
            w = ocr_data["width"][i] // scale
            h = ocr_data["height"][i] // scale

            results.append({
                "text": word,
                "confidence": confidence,
                "bounding_box": [x, y, w, h]
            })

    return results


def create_annotated_image(image, results):
    annotated = image.copy()

    for item in results:
        x, y, w, h = item["bounding_box"]
        label = f"{item['text']} ({item['confidence']}%)"

        cv2.rectangle(
            annotated, (x, y), (x + w, y + h),
            (0, 255, 0), 2
        )

        cv2.putText(
            annotated, label, (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (0, 255, 0), 2
        )

    return annotated


# ===================== Streamlit UI =====================

st.set_page_config(page_title="Text OCR", layout="wide")
st.title(" Text OCR (Offline)")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    st.subheader("Original Image")
    st.image(image, use_column_width=True)

    if st.button("Run OCR"):
        with st.spinner("Processing image..."):
            processed = preprocess_image(image_bgr)
            text, ocr_data = perform_ocr(processed)
            results = extract_text_data(ocr_data)
            annotated = create_annotated_image(image_bgr, results)

        st.subheader("Preprocessed Image")
        st.image(processed, clamp=True, use_column_width=True)

        st.subheader("Annotated Output")
        st.image(
            cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
            use_column_width=True
        )

        st.subheader("Extracted Text")
        st.text_area("OCR Result", text, height=200)

        st.subheader("Detected Words (JSON)")
        st.json(results)

        st.download_button(
            "Download Text",
            text,
            file_name="extracted_text.txt"
        )

        st.download_button(
            "Download JSON",
            json.dumps(results, indent=4),
            file_name="result.json"
        )

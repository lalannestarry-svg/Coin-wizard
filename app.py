
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import io

st.set_page_config(page_title="🪙 Coin Wizard", page_icon="🪙", layout="wide")

st.title("🪙 Coin Wizard — Identify & Appraise Coins")

st.sidebar.header("How to use")
st.sidebar.markdown("""
1. Upload a photo of your coin (or use the camera).  
2. Enter details (country, denomination, year, mint, grade).  
3. Press **Appraise** to get an estimated value.  
""")

# Image upload
src = st.radio("Choose image source", ["Upload", "Camera"], horizontal=True)

image = None
if src == "Upload":
    up = st.file_uploader("Upload a coin photo", type=["jpg","jpeg","png"])
    if up:
        image = Image.open(up).convert("RGB")
        image = ImageOps.exif_transpose(image)
elif src == "Camera":
    shot = st.camera_input("Take a photo of your coin")
    if shot:
        image = Image.open(shot).convert("RGB")
        image = ImageOps.exif_transpose(image)

if image:
    st.image(image, caption="Your coin", use_column_width=True)
    st.info("Demo grading: **XF** (Extra Fine).")

# Inputs
col1, col2 = st.columns(2)
with col1:
    country = st.text_input("Country", "united states")
    denom = st.text_input("Denomination", "quarter")
    year = st.text_input("Year", "1932")
with col2:
    mint = st.text_input("Mint (optional)", "d")
    grade = st.selectbox("Grade", ["G","VG","F","VF","XF","AU","MS"], index=4)
    conf = st.slider("Confidence", 0.0, 1.0, 0.7, 0.05)

if st.button("Appraise", use_container_width=True):
    # Demo price guide
    base_price = 120.0
    mult = {"G":0.25,"VG":0.4,"F":0.6,"VF":0.8,"XF":1.0,"AU":1.4,"MS":2.0}[grade]
    est = base_price * mult
    low, high = est*0.85, est*1.15
    st.success(f"Estimate: ${est:,.2f} (range ${low:,.2f}–${high:,.2f})")
    st.caption("Demo only. Upload your own price_guide.csv for real appraisals.")

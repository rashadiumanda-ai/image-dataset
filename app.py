import streamlit as st
import os
import random
import zipfile
import requests
from PIL import Image

st.set_page_config(page_title="Image Dataset Viewer", layout="wide", page_icon="🖼️")

st.title("🖼️ Image Dataset Explorer Dashboard")
st.write("Google Drive එකෙන් ගත්තු Image Dataset එක Streamlit මඟින් visualizes කිරීම.")

DATA_DIR = "MY_data"
ZIP_FILE = "MY_data.zip"
FILE_ID = "1GFmUWOjoSyEclPPnp3a2vl-4HvLl0SC9"

# --- AUTO DOWNLOAD & UNZIP SETUP (FIXED WITH REQUESTS) ---
if not os.path.exists(DATA_DIR):
    with st.spinner("📂 Dataset eka Google Drive eken download wenawa... Winadiyak wath yayi..."):
        try:
            # Google Drive Direct Download URL
            url = f"https://docs.google.com/uc?export=download&id={FILE_ID}&confirm=t"
            
            # Python requests වලින් file එක download කිරීම
            response = requests.get(url, stream=True)
            with open(ZIP_FILE, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Zip file eka extract කරනවා
            with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
                zip_ref.extractall(".")
                
            st.success("✅ Dataset download and unzip completed successfully!")
            
            # Storage ඉතුරු කරගන්න zip file එක delete කරනවා
            if os.path.exists(ZIP_FILE):
                os.remove(ZIP_FILE)
                
        except Exception as e:
            st.error(f"❌ Error downloading dataset: {e}")

# --- MAIN APP LOGIC ---
if os.path.exists(DATA_DIR):
    tabs = st.tabs(["📊 Dataset Summary", "🔍 Browse Images"])
    
    # --- TAB 1: DATASET SUMMARY ---
    with tabs[0]:
        st.subheader("Dataset Folder Structure & Image Counts")
        
        folder_stats = {}
        for folder in ["train", "test", "predict"]:
            path = os.path.join(DATA_DIR, folder)
            if os.path.exists(path):
                total_files = sum([len(files) for r, d, files in os.walk(path)])
                folder_stats[folder] = total_files
        
        if folder_stats:
            cols = st.columns(len(folder_stats))
            for i, (folder_name, count) in enumerate(folder_stats.items()):
                with cols[i]:
                    st.metric(label=f"Total Images in '{folder_name}'", value=count)
            st.bar_chart(folder_stats)
        else:
            st.warning("No splits (train/test/predict) found inside MY_data.")

    # --- TAB 2: IMAGE BROWSER ---
    with tabs[1]:
        st.subheader("Random Images from Dataset")
        selected_folder = st.selectbox("Select a split to view:", ["train", "test", "predict"])
        
        target_path = os.path.join(DATA_DIR, selected_folder)
        
        all_images = []
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    all_images.append(os.path.join(root, file))
                    
        if all_images:
            st.write(f"📸 Found {len(all_images)} images. Showing 6 random samples:")
            sample_images = random.sample(all_images, min(6, len(all_images)))
            
            img_cols = st.columns(3)
            for idx, img_path in enumerate(sample_images):
                col_idx = idx % 3
                with img_cols[col_idx]:
                    try:
                        img = Image.open(img_path)
                        caption_name = os.path.basename(os.path.dirname(img_path)) + " / " + os.path.basename(img_path)
                        st.image(img, caption=caption_name, use_column_width=True)
                    except Exception as e:
                        st.error(f"Error loading image: {e}")
        else:
            st.warning(f"No valid images found in '{selected_folder}' folder.")
else:
    st.error("Error: 'MY_data' folder eka hoyaganna bari una.")

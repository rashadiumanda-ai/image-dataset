import streamlit as st
import os
import random
from PIL import Image

st.set_page_config(page_title="Image Dataset Viewer", layout="wide", page_icon="🖼️")

st.title("🖼️ Image Dataset Explorer Dashboard")
st.write("Google Drive එකෙන් ගත්තු Image Dataset එක Streamlit මඟින් visualizes කිරීම.")

DATA_DIR = "MY_data"

# Folders තියෙනවද බලනවා
if os.path.exists(DATA_DIR):
    tabs = st.tabs(["📊 Dataset Summary", "🔍 Browse Images"])
    
    # --- TAB 1: DATASET SUMMARY ---
    with tabs[0]:
        st.subheader("Dataset Folder Structure & Image Counts")
        
        folder_stats = {}
        for folder in ["train", "test", "predict"]:
            path = os.path.join(DATA_DIR, folder)
            if os.path.exists(path):
                # ඇතුළේ තියෙන subdivisions (classes) හෝ image files ගණන් කරනවා
                total_files = sum([len(files) for r, d, files in os.walk(path)])
                folder_stats[folder] = total_files
        
        # Stats ටික ලස්සනට පෙන්නන්න Columns
        cols = st.columns(len(folder_stats))
        for i, (folder_name, count) in enumerate(folder_stats.items()):
            with cols[i]:
                st.metric(label=f"Total Images in '{folder_name}'", value=count)
                
        # Simple Bar Chart එකක්
        st.bar_chart(folder_stats)

    # --- TAB 2: IMAGE BROWSER ---
    with tabs[1]:
        st.subheader("Random Images from Dataset")
        selected_folder = st.selectbox("Select a split to view:", ["train", "test", "predict"])
        
        target_path = os.path.join(DATA_DIR, selected_folder)
        
        # සියලුම image paths ටික ලිස්ට් එකකට ගන්නවා
        all_images = []
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    all_images.append(os.path.join(root, file))
                    
        if all_images:
            st.write(f"📸 Found {len(all_images)} images. Showing 6 random samples:")
            
            # Random images 6ක් තෝරගන්නවා
            sample_images = random.sample(all_images, min(6, len(all_images)))
            
            # Grid එකක් විදිහට images 3 ගානේ පේළි දෙකකට පෙන්නනවා
            img_cols = st.columns(3)
            for idx, img_path in enumerate(sample_images):
                col_idx = idx % 3
                with img_cols[col_idx]:
                    try:
                        img = Image.open(img_path)
                        # Folder name එක caption එක විදිහට දානවා
                        caption_name = os.path.basename(os.path.dirname(img_path)) + " / " + os.path.basename(img_path)
                        st.image(img, caption=caption_name, use_column_width=True)
                    except Exception as e:
                        st.error(f"Error loading image: {e}")
        else:
            st.warning(f"No valid images found in '{selected_folder}' folder.")
else:
    st.error("Error: 'MY_data' folder එක සොයාගත නොහැකි විය. කරුණාකර පළමු පියවර නැවත බලන්න.")

import streamlit as st
from PIL import Image, ImageEnhance
from rembg import remove # हमारा नया AI दोस्त
import io

# पेज सेटअप
st.set_page_config(page_title="AI Magic Editor", page_icon="✨", layout="wide")

st.title("✨ Mera AI Magic Editor (Hepic Style)")
st.write("Asli AI ke saath Background Change aur Pro Editing!")

# --- साइडबार ---
st.sidebar.header("🎛️ Control Panel")

# 1. मुख्य फोटो अपलोड
main_image_file = st.sidebar.file_uploader("📂 1. अपनी Main फोटो यहाँ डालें (Subject):", type=['jpg', 'png', 'jpeg'], key="main")

# 2. नया बैकग्राउंड अपलोड (अगर बदलना हो तो)
bg_image_file = st.sidebar.file_uploader("🌆 2. नया Background फोटो यहाँ डालें (Optional):", type=['jpg', 'png', 'jpeg'], key="bg")


if main_image_file is not None:
    # ओरिजिनल इमेज को खोलना
    image = Image.open(main_image_file).convert("RGBA")
    
    # --- साइडबार में टूल्स चुनना ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("🚀 AI Mode चुनें:")
    ai_mode = st.sidebar.radio("क्या करना है?", ["Pro Editing (Brightness/Colors)", "🔥 AI Background Removal/Change"])

    final_image = image.copy()

    # ==============================
    # MODE 1: PRO EDITING (पुराना वाला)
    # ==============================
    if ai_mode == "Pro Editing (Brightness/Colors)":
        st.sidebar.subheader("🛠 Color & Details")
        brightness_val = st.sidebar.slider("☀️ Brightness", 0.5, 1.5, 1.0)
        contrast_val = st.sidebar.slider("🌗 Contrast", 0.5, 1.5, 1.0)
        saturation_val = st.sidebar.slider("🌈 Saturation", 0.0, 2.0, 1.0)
        sharpness_val = st.sidebar.slider("🔪 Sharpness", 0.0, 3.0, 1.0)
        
        # एडिटिंग अप्लाई करना (RGB मोड में)
        edit_img = final_image.convert("RGB")
        
        if saturation_val != 1.0:
            edit_img = ImageEnhance.Color(edit_img).enhance(saturation_val)
        if brightness_val != 1.0:
            edit_img = ImageEnhance.Brightness(edit_img).enhance(brightness_val)
        if contrast_val != 1.0:
            edit_img = ImageEnhance.Contrast(edit_img).enhance(contrast_val)
        if sharpness_val != 1.0:
            edit_img = ImageEnhance.Sharpness(edit_img).enhance(sharpness_val)
            
        final_image = edit_img

    # ==============================
    # MODE 2: AI BACKGROUND MAGIC (नया वाला!)
    # ==============================
    elif ai_mode == "🔥 AI Background Removal/Change":
        
        # 1. सबसे पहले बैकग्राउंड हटाओ (Cutout निकालो)
        # नोट: पहली बार इसमें थोड़ा समय लगेगा
        with st.spinner('AI बैकग्राउंड हटा रहा है... कृप्या इंतज़ार करें... 🤖'):
            # Rembg को बाइट्स चाहिए होते हैं
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            image_bytes = buf.getvalue()
            
            # जादू यहाँ होता है!
            output_bytes = remove(image_bytes)
            foreground_img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

        # 2. चेक करो कि क्या नया बैकग्राउंड लगाना है?
        if bg_image_file is not None:
            # नया बैकग्राउंड खोलो
            new_bg = Image.open(bg_image_file).convert("RGBA")
            # नए बैकग्राउंड को ओरिजिनल फोटो के साइज का बनाओ
            new_bg = new_bg.resize(image.size)
            # कटे हुए सब्जेक्ट को नए बैकग्राउंड पर चिपका दो (Overlay)
            new_bg.paste(foreground_img, (0, 0), foreground_img)
            final_image = new_bg
            st.success("बैकग्राउंड सफलतापूर्वक बदल गया! 🎉")
        else:
            # अगर नया बैकग्राउंड नहीं दिया, तो सिर्फ कटा हुआ (Transparent) दिखाओ
            final_image = foreground_img
            st.info("नया बैकग्राउंड अपलोड नहीं किया, इसलिए सिर्फ Cutout दिख रहा है।")


    # --- ✅ रिजल्ट दिखाना ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Subject")
        st.image(image, use_column_width=True)
        if bg_image_file:
             st.subheader("New Background Image")
             st.image(bg_image_file, use_column_width=True)

    with col2:
        st.subheader("Final AI Result ✨")
        # ट्रांसपेरेंट इमेज को सही से दिखाने के लिए
        st.image(final_image, use_column_width=True)

else:
    st.info("👈 शुरुआत करने के लिए साइडबार से अपनी Main फोटो अपलोड करें।")
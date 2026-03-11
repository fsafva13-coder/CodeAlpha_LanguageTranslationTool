import streamlit as st
from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException
from langdetect import detect as lang_detect
import time

st.set_page_config(page_title="LinguaAI — Translator", page_icon="🌐", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #f0f0f0; }
    .main-title { text-align: center; font-size: 2.8rem; font-weight: 600;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem; }
    .subtitle { text-align: center; color: #94a3b8; font-size: 1rem; margin-bottom: 2rem; }
    .result-box { background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.4);
        border-radius: 12px; padding: 1.2rem 1.5rem; font-size: 1.1rem; line-height: 1.7; color: #e2e8f0; margin-top: 1rem; }
    .detected-badge { display: inline-block; background: rgba(52,211,153,0.15);
        border: 1px solid rgba(52,211,153,0.4); color: #34d399; font-size: 0.8rem;
        padding: 0.2rem 0.8rem; border-radius: 20px; margin-bottom: 0.8rem; }
    .stForm [data-testid="stFormSubmitButton"] > button { width: 100%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important; font-weight: 600 !important; font-size: 1rem !important;
        border: none !important; border-radius: 10px !important; padding: 0.7rem 1.5rem !important; }
    .stForm { border: none !important; padding: 0 !important; background: transparent !important; }
    label { color: #c4b5fd !important; font-weight: 500 !important; }
    .footer { text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 3rem; }
</style>
""", unsafe_allow_html=True)

LANGUAGES = {
    "Auto Detect": "auto", "Afrikaans": "af", "Arabic": "ar", "Bengali": "bn",
    "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Dutch": "nl", "English": "en", "French": "fr", "German": "de",
    "Greek": "el", "Hebrew": "iw", "Hindi": "hi", "Indonesian": "id",
    "Italian": "it", "Japanese": "ja", "Korean": "ko", "Malay": "ms",
    "Malayalam": "ml", "Persian": "fa", "Filipino": "tl", "Polish": "pl",
    "Portuguese": "pt", "Russian": "ru", "Spanish": "es", "Swedish": "sv",
    "Tamil": "ta", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk",
    "Urdu": "ur", "Vietnamese": "vi",
}

CODE_TO_NAME = {v: k for k, v in LANGUAGES.items()}
TARGET_LANGUAGES = {k: v for k, v in LANGUAGES.items() if k != "Auto Detect"}

st.markdown('<div class="main-title">🌐 LinguaAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Instant AI-powered translation across 31 languages</div>', unsafe_allow_html=True)
st.markdown("---")

col1, col_arrow, col2 = st.columns([5, 1, 5])
with col1:
    source_lang_name = st.selectbox("🔤 Source Language", options=list(LANGUAGES.keys()), index=0)
with col_arrow:
    st.markdown("<br><br><div style='text-align:center; font-size:1.5rem;'>→</div>", unsafe_allow_html=True)
with col2:
    target_lang_name = st.selectbox("🎯 Target Language", options=list(TARGET_LANGUAGES.keys()),
        index=list(TARGET_LANGUAGES.keys()).index("Arabic"))

st.markdown("---")

with st.form(key="translate_form", clear_on_submit=False):
    input_text = st.text_area("✏️ Enter text to translate",
        placeholder="Type or paste your text here...", height=150, max_chars=5000)
    st.caption(f"{len(input_text) if input_text else 0}/5000 characters")
    translate_clicked = st.form_submit_button("🚀 Translate")

if translate_clicked:
    if not input_text or not input_text.strip():
        st.warning("⚠️ Please enter some text before translating!")
    else:
        source_code = LANGUAGES[source_lang_name]
        target_code = TARGET_LANGUAGES[target_lang_name]

        # Detect actual language of input
        try:
            detected_code = lang_detect(input_text)
            if detected_code == "zh-cn": detected_code = "zh-CN"
            if detected_code == "zh-tw": detected_code = "zh-TW"
            if detected_code == "he": detected_code = "iw"
        except:
            detected_code = None

        detected_name = CODE_TO_NAME.get(detected_code, detected_code) if detected_code else None

        if source_code != "auto" and detected_code and detected_code != source_code:
            st.warning(
                f"⚠️ You selected **{source_lang_name}** as source, but the text appears to be **{detected_name}**. "
                f"Please enter text in {source_lang_name}, or switch Source Language to **Auto Detect**."
            )
        elif source_code == target_code:
            st.warning("⚠️ Source and target languages are the same. Please select different languages.")
        else:
            try:
                with st.spinner("✨ Translating..."):
                    time.sleep(0.4)
                    translator = GoogleTranslator(source=source_code, target=target_code)
                    translated_text = translator.translate(input_text)
                st.success("✅ Translation complete!")
                if source_code == "auto" and detected_name:
                    st.markdown(
                        f'<div class="detected-badge">🔍 Detected language: {detected_name}</div>',
                        unsafe_allow_html=True
                    )
                st.markdown("**📄 Translated Text:**")
                st.markdown(f'<div class="result-box">{translated_text}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.text_area("📋 Copy translated text", value=translated_text, height=120, key="copy_area")
                from_label = f"{detected_name} (Auto Detected)" if source_code == "auto" and detected_name else source_lang_name
                st.caption(f"Translated from **{from_label}** → **{target_lang_name}**")
            except LanguageNotSupportedException:
                st.error("❌ Language not supported. Try another combination.")
            except Exception as e:
                st.error(f"❌ Translation failed. Check your internet connection.\n\nError: {str(e)}")

st.markdown("---")
st.markdown('<div class="footer">Built for CodeAlpha AI Internship — Task 1: Language Translation Tool 🌐</div>',
            unsafe_allow_html=True)

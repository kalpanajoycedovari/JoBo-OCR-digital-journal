import streamlit as st
import os
from PIL import Image

from jobo.preprocessor import load_image, preprocess
from jobo.ocr_engine import extract_with_confidence
from jobo.database import init_db, save_entry, get_all_entries, delete_entry
from jobo.models import JournalEntry
from jobo.search import search_entries
from jobo.sentiment import analyse_sentiment, get_sentiment_summary

st.set_page_config(page_title="JoBo Journal", page_icon="🌼", layout="wide")
init_db()

# --- Session state for page ---
if "page" not in st.session_state:
    st.session_state.page = "upload"

def go(p):
    st.session_state.page = p

# --- Styles ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Nunito:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    color: #3a5a40;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #e8f5e9 0%, #f1f8e9 40%, #e0f2e9 70%, #e8f5e9 100%);
    background-size: 300% 300%;
    animation: bgDrift 16s ease infinite;
}
@keyframes bgDrift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }

/* Floating daisies */
.daisy-field {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.daisy {
    position: absolute; opacity: 0;
    animation: floatDaisy linear infinite;
}
@keyframes floatDaisy {
    0%   { transform: translateY(110vh) rotate(0deg);   opacity: 0; }
    10%  { opacity: 0.5; }
    90%  { opacity: 0.5; }
    100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
}

/* Page content */
.page-wrap {
    position: relative; z-index: 1;
    max-width: 1100px; margin: 0 auto;
    padding: 24px 24px 80px;
    animation: fadeUp 0.6s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

h1 {
    font-family: 'Playfair Display', serif !important;
    color: #2e7d32 !important; font-size: 2.4rem !important;
}
h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #388e3c !important;
}

/* Nav buttons row */
.nav-row {
    position: sticky; top: 0; z-index: 999;
    background: rgba(232,245,233,0.90);
    backdrop-filter: blur(14px);
    border-bottom: 1.5px solid #b7ddb0;
    padding: 10px 24px;
    display: flex; align-items: center; gap: 8px;
    box-shadow: 0 2px 16px rgba(100,160,100,0.10);
    animation: slideDown 0.5s ease;
    margin-bottom: 8px;
}
@keyframes slideDown {
    from { transform: translateY(-50px); opacity: 0; }
    to   { transform: translateY(0);     opacity: 1; }
}
.nav-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem; color: #2e7d32;
    font-weight: 600; margin-right: 12px;
}

/* Entry cards */
.entry-card {
    background: rgba(255,255,255,0.78);
    border: 1.5px solid #c8e6c9; border-radius: 20px;
    padding: 18px 22px; margin-bottom: 14px;
    box-shadow: 0 4px 16px rgba(100,160,100,0.10);
    transition: transform 0.3s, box-shadow 0.3s;
    animation: fadeUp 0.5s ease;
}
.entry-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(100,160,100,0.18);
}

.pill {
    display: inline-block;
    background: #dcedc8; color: #33691e;
    padding: 4px 14px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 600;
    margin-right: 6px; margin-bottom: 4px;
}

[data-testid="stExpander"] {
    background: rgba(255,255,255,0.78) !important;
    border: 1.5px solid #c8e6c9 !important;
    border-radius: 18px !important; margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(100,160,100,0.09);
    transition: box-shadow 0.3s, transform 0.3s;
}
[data-testid="stExpander"]:hover {
    box-shadow: 0 8px 26px rgba(100,160,100,0.17);
    transform: translateY(-2px);
}

.stButton > button {
    background: linear-gradient(135deg, #66bb6a, #388e3c) !important;
    color: #fff !important; border: none !important;
    border-radius: 24px !important; padding: 10px 28px !important;
    font-family: 'Nunito', sans-serif !important; font-weight: 600 !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 4px 14px rgba(56,142,60,0.28) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 22px rgba(56,142,60,0.38) !important;
}

textarea {
    background: rgba(255,255,255,0.88) !important;
    border: 1.5px solid #c8e6c9 !important;
    border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important;
    color: #3a5a40 !important; font-size: 15px !important;
    line-height: 1.75 !important;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.78) !important;
    border: 2px dashed #a5d6a7 !important;
    border-radius: 18px !important;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.78) !important;
    border: 1.5px solid #c8e6c9 !important;
    border-radius: 18px !important; padding: 18px !important;
    box-shadow: 0 4px 14px rgba(100,160,100,0.09);
}
[data-testid="stMetricValue"] {
    color: #2e7d32 !important;
    font-family: 'Playfair Display', serif !important;
}

[data-testid="stAlert"] { border-radius: 14px !important; border: none !important; }

input[type="text"] {
    background: rgba(255,255,255,0.88) !important;
    border: 1.5px solid #c8e6c9 !important;
    border-radius: 12px !important; color: #3a5a40 !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #e8f5e9; }
::-webkit-scrollbar-thumb { background: #a5d6a7; border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: #66bb6a; }
html { scroll-behavior: smooth; }
</style>

<!-- Floating daisies -->
<div class="daisy-field" id="daisyField"></div>
<script>
(function() {
    const field = document.getElementById('daisyField');
    if (!field) return;
    for (let i = 0; i < 18; i++) {
        const d = document.createElement('div');
        d.className = 'daisy';
        const sz = 18 + Math.random() * 22;
        const left = Math.random() * 100;
        const dur  = 14 + Math.random() * 18;
        const delay = Math.random() * -20;
        d.style.cssText = `left:${left}%;width:${sz}px;height:${sz}px;
            animation-duration:${dur}s;animation-delay:${delay}s;`;
        d.innerHTML = `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(20,20)">
            ${Array.from({length:8},(_,k)=>`
                <ellipse transform="rotate(${k*45})" cx="0" cy="-11" rx="4" ry="7"
                    fill="white" stroke="#c8e6c9" stroke-width="0.8" opacity="0.92"/>`
            ).join('')}
            <circle cx="0" cy="0" r="6" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
            <circle cx="0" cy="0" r="3" fill="#f9a825" opacity="0.7"/>
            </g></svg>`;
        field.appendChild(d);
    }
})();
</script>
""", unsafe_allow_html=True)

# --- Top nav using Streamlit buttons ---
st.markdown('<div class="nav-row">', unsafe_allow_html=True)
st.markdown('<span class="nav-brand">🌼 JoBo Journal</span>', unsafe_allow_html=True)

col_a, col_b, col_c, col_d, col_e = st.columns([1.2, 1.1, 1.1, 0.8, 1.1])
with col_a:
    if st.button("✍️ Upload & Extract", use_container_width=True):
        go("upload")
with col_b:
    if st.button("📖 My Entries", use_container_width=True):
        go("entries")
with col_c:
    if st.button("🔍 Search", use_container_width=True):
        go("search")
with col_d:
    if st.button("🌸 Mood", use_container_width=True):
        go("mood")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

page = st.session_state.page

# -------------------------------------------------------
# PAGE 1 — Upload & Extract
# -------------------------------------------------------
if page == "upload":
    st.title("✍️ New Entry")
    st.markdown("<p style='color:#66bb6a;font-style:italic;margin-top:-10px;'>Upload a photo of your handwritten notes</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["png","jpg","jpeg","bmp","tiff"])

    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        save_path = os.path.join("uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("### 📷 Your Image")
            st.image(Image.open(save_path), use_container_width=True)
        with col2:
            st.markdown("### 🖊️ Extracted Text")
            with st.spinner("🌿 Reading your notes..."):
                img = load_image(save_path)
                processed = preprocess(img)
                result = extract_with_confidence(processed)

            text       = result["text"]
            confidence = result["avg_conf"]
            sentiment  = analyse_sentiment(text)

            if confidence >= 75:
                st.success(f"✨ Confidence: {confidence}%")
            elif confidence >= 50:
                st.warning(f"🌤 Confidence: {confidence}%")
            else:
                st.error(f"🌧 Confidence: {confidence}% — try a clearer image")

            st.info(f"Today's mood: {sentiment['emoji']} **{sentiment['label']}** (polarity: {sentiment['polarity']})")

            edited_text = st.text_area("Feel free to edit before saving:", value=text, height=240)
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🌼 Save to my Journal", use_container_width=True):
                if edited_text.strip():
                    entry = JournalEntry(image_path=save_path, extracted_text=edited_text, confidence=confidence)
                    saved = save_entry(entry)
                    st.success(f"🌿 Entry #{saved.id} saved!")
                    st.balloons()
                else:
                    st.error("Nothing to save — text is empty.")

# -------------------------------------------------------
# PAGE 2 — My Entries
# -------------------------------------------------------
elif page == "entries":
    st.title("📖 My Journal")
    st.markdown("<p style='color:#66bb6a;font-style:italic;margin-top:-10px;'>All your memories, in one place</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    entries = get_all_entries()
    if not entries:
        st.markdown("""
        <div style='text-align:center;padding:70px 0;color:#81c784;'>
            <div style='font-size:4rem;'>🌱</div>
            <div style='font-family:Playfair Display,serif;font-size:1.4rem;
                        margin-top:16px;color:#388e3c;'>No entries yet</div>
            <div style='margin-top:8px;font-size:0.95rem;'>Upload your first image to begin</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color:#81c784;'>{len(entries)} entries in your journal</p>", unsafe_allow_html=True)
        for entry in entries:
            sentiment = analyse_sentiment(entry.extracted_text)
            with st.expander(f"{sentiment['emoji']}  Entry #{entry.id} — {entry.created_at}  ·  {sentiment['label']}"):
                col1, col2 = st.columns([1, 2], gap="large")
                with col1:
                    if os.path.exists(entry.image_path):
                        st.image(Image.open(entry.image_path), use_container_width=True)
                    else:
                        st.warning("Image not found.")
                with col2:
                    st.markdown(f"""
                    <div style='margin-bottom:12px;'>
                        <span class='pill'>📊 {entry.confidence}% confidence</span>
                        <span class='pill'>{sentiment['emoji']} {sentiment['label']}</span>
                        <span class='pill'>🎯 polarity {sentiment['polarity']}</span>
                    </div>""", unsafe_allow_html=True)
                    st.text_area("Journal text", value=entry.extracted_text, height=200, key=f"text_{entry.id}")
                    if st.button(f"🗑️ Delete entry #{entry.id}", key=f"del_{entry.id}"):
                        delete_entry(entry.id)
                        st.success(f"Entry #{entry.id} deleted.")
                        st.rerun()

# -------------------------------------------------------
# PAGE 3 — Search
# -------------------------------------------------------
elif page == "search":
    st.title("🔍 Search")
    st.markdown("<p style='color:#66bb6a;font-style:italic;margin-top:-10px;'>Find any memory by keyword</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    keyword = st.text_input("", placeholder="🌿  Type a word to search your journal...")
    if keyword:
        results = search_entries(keyword)
        if not results:
            st.markdown(f"""
            <div style='text-align:center;padding:50px 0;color:#81c784;'>
                <div style='font-size:3rem;'>🍃</div>
                <div style='font-family:Playfair Display,serif;font-size:1.2rem;
                            margin-top:12px;color:#388e3c;'>
                    No entries found for "{keyword}"
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.success(f"🌿 Found {len(results)} result(s) for **{keyword}**")
            for entry in results:
                sentiment = analyse_sentiment(entry.extracted_text)
                with st.expander(f"{sentiment['emoji']}  Entry #{entry.id} — {entry.created_at}"):
                    col1, col2 = st.columns([1, 2], gap="large")
                    with col1:
                        if os.path.exists(entry.image_path):
                            st.image(Image.open(entry.image_path), use_container_width=True)
                        else:
                            st.warning("Image not found.")
                    with col2:
                        st.markdown(f"""
                        <div style='margin-bottom:12px;'>
                            <span class='pill'>{sentiment['emoji']} {sentiment['label']}</span>
                            <span class='pill'>🎯 polarity {sentiment['polarity']}</span>
                        </div>""", unsafe_allow_html=True)
                        st.text_area("Journal text", value=entry.extracted_text, height=200, key=f"s_{entry.id}")

# -------------------------------------------------------
# PAGE 4 — Mood Overview
# -------------------------------------------------------
elif page == "mood":
    st.title("🌸 Mood Overview")
    st.markdown("<p style='color:#66bb6a;font-style:italic;margin-top:-10px;'>How have you been feeling?</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    entries = get_all_entries()
    if not entries:
        st.markdown("""
        <div style='text-align:center;padding:70px 0;color:#81c784;'>
            <div style='font-size:4rem;'>🌼</div>
            <div style='font-family:Playfair Display,serif;font-size:1.4rem;
                        margin-top:16px;color:#388e3c;'>No entries yet</div>
        </div>""", unsafe_allow_html=True)
    else:
        summary = get_sentiment_summary(entries)
        counts  = summary["counts"]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📓 Total",    summary["total"])
        col2.metric("😊 Positive", counts["Positive"])
        col3.metric("😐 Neutral",  counts["Neutral"])
        col4.metric("😔 Negative", counts["Negative"])

        st.markdown("<br>", unsafe_allow_html=True)
        avg = summary["avg_polarity"]
        if avg > 0.1:
            st.success(f"✨ Overall mood: **Positive** (avg polarity: {avg}) — keep shining!")
        elif avg < -0.1:
            st.error(f"💙 Overall mood: **Negative** (avg polarity: {avg}) — it's okay, every day matters.")
        else:
            st.info(f"🌤 Overall mood: **Neutral** (avg polarity: {avg})")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Entry breakdown")
        for entry in entries:
            sentiment = analyse_sentiment(entry.extracted_text)
            bar_pct   = int((sentiment["polarity"] + 1) / 2 * 100)
            bar_color = "#81c784" if sentiment["label"] == "Positive" else "#a5d6a7" if sentiment["label"] == "Neutral" else "#ef9a9a"
            st.markdown(f"""
            <div class="entry-card">
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <span style='font-family:Playfair Display,serif;color:#2e7d32;
                                     font-weight:600;'>Entry #{entry.id}</span>
                        <span style='color:#81c784;font-size:0.85rem;margin-left:10px;'>
                            {entry.created_at}</span>
                    </div>
                    <div style='font-size:1.4rem;'>{sentiment['emoji']}</div>
                </div>
                <div style='margin-top:10px;background:#dcedc8;border-radius:10px;
                            height:7px;overflow:hidden;'>
                    <div style='width:{bar_pct}%;background:{bar_color};height:100%;
                                border-radius:10px;'></div>
                </div>
                <div style='font-size:0.82rem;color:#81c784;margin-top:5px;'>
                    {sentiment['label']} · polarity {sentiment['polarity']}
                </div>
            </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
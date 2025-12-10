# app.py - Theme Toggle Added
import streamlit as st
from textblob import TextBlob
import numpy as np 

# --- 0. Initialize Session State for Theme ---
# Check if the 'theme' key exists; if not, set default to 'light'
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# --- Function to Toggle Theme ---
def toggle_theme():
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

# --- Theme Variables ---
if st.session_state.theme == 'light':
    BG_COLOR = "#ffffff"
    TEXT_COLOR = "#1a1a1a"
    INPUT_BG = "#f8f9fa"
    FOOTER_BG = "#f8f9fa"
    BORDER_COLOR = "#ced4da"
    BUTTON_PRIMARY = "#007bff"
    BUTTON_SHADOW = "rgba(0, 123, 255, 0.3)"
else: # Dark Mode
    BG_COLOR = "#1e1e1e"
    TEXT_COLOR = "#ffffff"
    INPUT_BG = "#2a2a2a"
    FOOTER_BG = "#333333"
    BORDER_COLOR = "#444444"
    BUTTON_PRIMARY = "#3a8ee6" # Lighter blue for dark background
    BUTTON_SHADOW = "rgba(58, 142, 230, 0.5)"


# --- Configuration (Theme & Layout) ---
st.set_page_config(
    page_title="AI Mood-Tracker",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Theming ---
st.markdown(f"""
<style>
/* 1. Overall Page Style (Dynamically set background and text) */
body, .main, .stApp {{
    color: {TEXT_COLOR};
    background-color: {BG_COLOR};
}}

/* 2. Custom Styling for Input Area (Section 1) */
.stTextArea [data-testid='stEditables'] {{
    background-color: {INPUT_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    transition: all 0.3s;
    color: {TEXT_COLOR}; /* Ensure text color is readable */
}}
.stTextArea label {{
    font-size: 1.2em;
    font-weight: 600;
    color: {BUTTON_PRIMARY};
    margin-bottom: 10px;
}}

/* 3. Button Style */
div.stButton > button:first-child {{
    background-color: {BUTTON_PRIMARY};
    color: {TEXT_COLOR if st.session_state.theme == 'dark' else 'white'};
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    box-shadow: 0 4px 10px {BUTTON_SHADOW};
    transition: all 0.3s ease-in-out;
}}
div.stButton > button:first-child:hover {{
    background-color: #0056b3;
    box-shadow: 0 6px 12px {BUTTON_SHADOW};
}}

/* 4. Footer Style */
.footer {{
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: {FOOTER_BG};
    color: #6c757d; 
    text-align: center;
    padding: 10px 0;
    font-size: 0.85em;
    border-top: 1px solid {BORDER_COLOR};
}}
</style>
""", unsafe_allow_html=True)


# --- SECTION 1: Header & Instructions ---
# Use columns to put the logo/icon on the left of the title text and the toggle button on the right
col_logo, col_title, col_toggle = st.columns([0.1, 0.7, 0.2])

with col_logo:
    # Use the brain icon for better theming
    st.markdown(f"<h1 style='font-size: 2.5em; color: {BUTTON_PRIMARY};'>🧠</h1>", unsafe_allow_html=True) 

with col_title:
    st.title("AI Mood-Tracker & Journal Summarizer")

with col_toggle:
    # --- Theme Toggle Button ---
    if st.session_state.theme == 'light':
        toggle_label = "🌙 Dark Mode"
    else:
        toggle_label = "☀️ Light Mode"
        
    st.button(toggle_label, on_click=toggle_theme, key='theme_toggle_button')
    
st.markdown("---")

st.info("""
**Welcome to your Digital Journal!** Write about your day to receive an **Emotional Tone** analysis. The AI calculates a Polarity Score from -1.0 (Very Negative) to +1.0 (Very Positive).
""")

# --- SECTION 2: User Input Area ---
st.markdown(f"<h2 style='color:{TEXT_COLOR};'>🖋️ Journal Input Area</h2>", unsafe_allow_html=True)

journal_text = st.text_area(
    "✍️ Express yourself here:",
    height=250,
    placeholder="Example: I had a challenging meeting but felt proud of how I handled the difficult questions. Later, the rain made me feel a bit down. I feel motivated for tomorrow.",
    key="journal_input"
)

# --- Analysis Button ---
if st.button("✨ Analyze My Mood & Get Insights", type="primary"):
    
    if journal_text:
        # Core Logic
        try:
            blob = TextBlob(journal_text)
            sentiment_score = blob.sentiment.polarity
            
            # Determine Mood Category
            if sentiment_score > 0.3:
                mood, color = "Very Positive 😊", "success"
            elif sentiment_score > 0.05:
                mood, color = "Positive 🙂", "success"
            elif sentiment_score > -0.05:
                mood, color = "Neutral 😐", "info"
            elif sentiment_score > -0.3:
                mood, color = "Negative 🙁", "warning"
            else:
                mood, color = "Very Negative 😞", "error"

            # --- SECTION 3: Results Display ---
            st.markdown("---")
            st.markdown(f"<h2 style='color:{TEXT_COLOR};'>✅ Analysis Results</h2>", unsafe_allow_html=True)
            
            # Use columns for a cleaner layout of the core metric
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"<h3 style='color:{TEXT_COLOR};'>Overall Sentiment</h3>", unsafe_allow_html=True)
                st.metric(label="Polarity Score", value=f"{sentiment_score:.3f}", delta=mood)
            
            with col2:
                st.markdown(f"<h3 style='color:{TEXT_COLOR};'>Visual Meter</h3>", unsafe_allow_html=True)
                # Visual Polarity Meter
                st.slider(
                    'Mood Scale: Negative (-1.0) to Positive (+1.0)',
                    min_value=-1.0, 
                    max_value=1.0, 
                    value=sentiment_score, 
                    disabled=True,
                    label_visibility="collapsed"
                )

            st.markdown("### 💡 Summary Insight")
            
            # Display summary insights (Clear, boxed recommendations)
            if color == "success":
                st.success("Your journal shows a **strong positive focus**. Keep this momentum going! What steps can you take to build on this positive energy?")
            elif color == "error":
                st.error("It looks like you're going through a **challenging or difficult moment**. Prioritize a moment for self-care and reach out to a trusted person if you need support.")
            elif color == "warning":
                st.warning("You're experiencing some **negative feelings**. Identify the source of the stress and see if you can address it or talk to someone.")
            else: # Neutral/Info
                st.info("Your emotions are **balanced and reflective**. This is a great time to observe your thoughts without judgment or attachment.")

            # --- SECTION 4: Technical Details (Hidden by default) ---
            st.markdown("---")
            with st.expander("🛠️ Technical Breakdown (Polarity & Thresholds)"):
                st.code(f"Polarity (TextBlob): {sentiment_score:.3f}")
                st.caption("""
                Polarity is the measure of emotional tone ranging from -1.0 (very negative) to +1.0 (very positive).
                Thresholds used: 
                > Very Positive (> 0.3) | Positive (> 0.05) | Neutral (-0.05 to 0.05)
                """)
        
        except Exception as e:
            st.error(f"An error occurred: {e}. If the issue is related to TextBlob, try running `python -m textblob.download_corpora`.")

    else:
        st.error("⚠️ Please enter some text into the journal area before clicking Analyze. The box cannot be empty!")

# --- Beautiful Footer ---
st.markdown("""
<div class="footer">
    <p>© 2025 AI Mood-Tracker. Powered by TextBlob & Streamlit. | Privacy-Focused Analysis.</p>
</div>
""", unsafe_allow_html=True)
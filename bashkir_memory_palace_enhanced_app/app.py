"""
🏰 Bashkir Memory Palace: Secrets of Voyaging
==============================================
A language learning app integrating Ibn Arabi's mystical framework,
memory palace techniques, and anthropological pedagogy.

The Four Birds guide your journey:
🦅 Eagle (First Intellect) - Civic knowledge at Ufa
🐦⬛ Crow (Universal Body) - Ancestral memory at Shulgan-Tash
🔥🕊️ Anqa (Prime Matter) - Transformation at Yamantau
🕊️ Ringdove (Universal Soul) - Daily life at Beloretsk & Bizhbulyak

Enhanced with retry logic, audio export, and OCM cultural classifications.
"""

import streamlit as st
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import shared utilities
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.retry import RetryConfig

# --- Audio Setup with Retry Logic ---
try:
    from gtts import gTTS
    import hashlib
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# --- Translation Setup ---
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False

# --- Speech Recognition Setup (Whisper) ---
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# Create audio cache directory
AUDIO_CACHE_DIR = Path(__file__).parent / "audio_cache"
AUDIO_CACHE_DIR.mkdir(exist_ok=True)


def generate_audio_with_retry(text: str, slow: bool = True, language: str = 'ru') -> bytes:
    """
    Generate audio for Bashkir text with retry logic and caching.

    Uses exponential backoff: 2s, 4s, 8s, 16s delays between retries.
    Returns audio bytes or None if generation fails.
    """
    if not AUDIO_AVAILABLE:
        return None

    config = RetryConfig(
        max_retries=4,
        base_delay=2.0,
        exponential_base=2.0,
    )

    # Create a cached filename based on text hash
    text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    cache_file = AUDIO_CACHE_DIR / f"{text_hash}.mp3"

    # Return cached version if available
    if cache_file.exists():
        with open(cache_file, 'rb') as f:
            return f.read()

    # Generate with retry logic
    for attempt in range(config.max_retries + 1):
        try:
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(str(cache_file))

            with open(cache_file, 'rb') as f:
                return f.read()

        except Exception as e:
            if attempt >= config.max_retries:
                return None

            delay = config.base_delay * (config.exponential_base ** attempt)
            time.sleep(delay)

    return None


def play_audio(text: str, slow: bool = True, language: str = 'ru'):
    """Generate and play audio for Bashkir text with caching and retry logic."""
    if not AUDIO_AVAILABLE:
        st.warning("🔇 Audio unavailable. Install with: `pip install gTTS`")
        return

    audio_bytes = generate_audio_with_retry(text, slow, language)

    if audio_bytes:
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.error("🔇 Audio generation failed after multiple attempts.")


def translate_text(text: str, source: str = 'en', target: str = 'ru') -> str:
    """
    Translate text with retry logic.

    Uses exponential backoff: 2s, 4s, 8s, 16s delays between retries.
    """
    if not TRANSLATION_AVAILABLE:
        return text

    config = RetryConfig(
        max_retries=4,
        base_delay=2.0,
        exponential_base=2.0,
    )

    for attempt in range(config.max_retries + 1):
        try:
            translator = GoogleTranslator(source=source, target=target)
            return translator.translate(text)
        except Exception as e:
            if attempt >= config.max_retries:
                return text  # Return original on failure

            delay = config.base_delay * (config.exponential_base ** attempt)
            time.sleep(delay)

    return text


@st.cache_resource
def load_whisper_model():
    """Load Whisper model with caching for speech recognition."""
    if not WHISPER_AVAILABLE:
        return None

    config = RetryConfig(
        max_retries=4,
        base_delay=4.0,
        exponential_base=2.0,
    )

    for attempt in range(config.max_retries + 1):
        try:
            return whisper.load_model("base")
        except Exception as e:
            if attempt >= config.max_retries:
                return None

            delay = config.base_delay * (config.exponential_base ** attempt)
            time.sleep(delay)

    return None


def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file using Whisper."""
    if not WHISPER_AVAILABLE:
        return ""

    model = load_whisper_model()
    if model is None:
        return ""

    try:
        result = model.transcribe(audio_path)
        return result.get('text', '')
    except Exception as e:
        return ""

# Page configuration
st.set_page_config(
    page_title="Bashkir Memory Palace",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading ---
@st.cache_data
def load_words():
    """Load vocabulary data."""
    data_path = Path(__file__).parent / "data" / "words.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_loci():
    """Load memory palace locations."""
    data_path = Path(__file__).parent / "data" / "loci.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_patterns():
    """Load sentence patterns."""
    data_path = Path(__file__).parent / "data" / "patterns.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_ocm_mapping():
    """Load OCM mapping data."""
    data_path = Path(__file__).parent / "data" / "ocm_mapping.json"
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@st.cache_data
def load_ural_batyr_epic():
    """Load the Ural-Batyr epic data - the Golden Light."""
    data_path = Path(__file__).parent / "data" / "ural_batyr_epic.json"
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# --- Initialize Session State ---
def init_session_state():
    """Initialize session state variables."""
    if 'current_locus' not in st.session_state:
        st.session_state.current_locus = None
    if 'current_station' not in st.session_state:
        st.session_state.current_station = None
    if 'learned_words' not in st.session_state:
        st.session_state.learned_words = set()
    if 'review_queue' not in st.session_state:
        st.session_state.review_queue = []
    if 'saved_sentences' not in st.session_state:
        st.session_state.saved_sentences = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Palace"
    if 'truth_unveiled' not in st.session_state:
        st.session_state.truth_unveiled = False
    if 'srs_data' not in st.session_state:
        st.session_state.srs_data = {}
    if 'builder_sentence' not in st.session_state:
        st.session_state.builder_sentence = []
    if 'epic_chapter' not in st.session_state:
        st.session_state.epic_chapter = 0

init_session_state()

# --- CSS Styling v3 - Bashkortostan Flag Colors ---
# Flag: Blue (#0066B3), White (#FFFFFF), Green (#00AF66)
# Fixes: Light blue background, visible expanders, readable headers
st.markdown("""
<style>
    /* ===== MAIN BACKGROUND - Light Blue ===== */
    .stApp {
        background-color: #cce5ff !important;
        background: linear-gradient(180deg, #cce5ff 0%, #d9ecff 50%, #e6f2ff 100%) !important;
    }

    /* ===== SIDEBAR STYLING ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0066B3 0%, #004080 100%) !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }

    /* ===== ALL HEADERS - Green & Readable ===== */
    h1 {
        color: #00AF66 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    h2 {
        color: #00AF66 !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
    }
    h3 {
        color: #00AF66 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    h4 {
        color: #00AF66 !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }
    /* Markdown headers too */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #00AF66 !important;
    }

    /* ===== EXPANDERS - Always Visible ===== */
    .streamlit-expanderHeader {
        background-color: #e6f2ff !important;
        border: 2px solid #0066B3 !important;
        border-radius: 8px !important;
        color: #004d00 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: #d9ecff !important;
        border-color: #00AF66 !important;
    }
    .streamlit-expanderContent {
        background-color: #f0f8ff !important;
        border: 1px solid #0066B3 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    /* Expander icon always visible */
    .streamlit-expanderHeader svg {
        color: #0066B3 !important;
        opacity: 1 !important;
    }

    /* Alternative expander styling for newer Streamlit */
    [data-testid="stExpander"] {
        border: 2px solid #0066B3 !important;
        border-radius: 10px !important;
        background-color: #e6f2ff !important;
    }
    [data-testid="stExpander"]:hover {
        background-color: #d9ecff !important;
        border-color: #00AF66 !important;
    }
    [data-testid="stExpander"] summary {
        color: #004d00 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 12px !important;
    }
    [data-testid="stExpander"] summary:hover {
        background-color: #d9ecff !important;
    }
    [data-testid="stExpander"] svg {
        color: #0066B3 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* ===== POPOVER BUTTONS - Always Visible ===== */
    [data-testid="stPopover"] > button,
    .stPopover > button {
        background-color: #e6f2ff !important;
        border: 2px solid #0066B3 !important;
        color: #004d00 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    [data-testid="stPopover"] > button:hover,
    .stPopover > button:hover {
        background-color: #d9ecff !important;
        border-color: #00AF66 !important;
    }

    /* ===== BIRD CARDS ===== */
    .bird-card {
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 5px solid;
        color: #004d00;
    }
    .eagle-card { background: linear-gradient(135deg, #cce5ff 0%, #e6f2ff 100%); border-color: #0066B3; }
    .crow-card { background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%); border-color: #333333; }
    .anqa-card { background: linear-gradient(135deg, #ffe6e6 0%, #fff0f0 100%); border-color: #cc3333; }
    .ringdove-card { background: linear-gradient(135deg, #e6ffe6 0%, #f0fff0 100%); border-color: #00AF66; }

    /* ===== WORD CARDS ===== */
    .word-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 102, 179, 0.15);
        margin: 10px 0;
        border: 2px solid #0066B3;
    }

    /* Bashkir text - GREEN from flag */
    .bashkir-text {
        font-size: 1.8em;
        font-weight: bold;
        color: #00AF66 !important;
        display: block;
        margin-bottom: 8px;
    }

    /* IPA text - blue */
    .ipa-text {
        color: #0066B3;
        font-size: 1em;
        font-style: italic;
    }

    /* English translation - dark green */
    .english-text {
        color: #004d00;
        font-size: 1.2em;
        font-weight: bold;
        margin: 8px 0;
    }

    /* Russian - muted */
    .russian-text {
        color: #666666;
        font-size: 0.95em;
    }

    /* ===== MEDITATION BOXES ===== */
    .meditation-box {
        background: linear-gradient(135deg, #e6fff0 0%, #ccffe6 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #00AF66;
        font-style: italic;
        margin: 15px 0;
        color: #004d00;
    }

    /* ===== STATS BOXES ===== */
    .stat-box {
        background: linear-gradient(135deg, #e6f2ff 0%, #cce5ff 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #0066B3;
        color: #004d00;
    }

    /* ===== MNEMONIC BOXES ===== */
    .mnemonic-text {
        background: linear-gradient(135deg, #fffff5 0%, #ffffd0 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00AF66;
        color: #004d00;
        line-height: 1.6;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background-color: #00AF66 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background-color: #008f55 !important;
        color: white !important;
    }

    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background-color: #00AF66 !important;
    }

    /* ===== GENERAL TEXT ===== */
    .stMarkdown, .stMarkdown p, .stText {
        color: #004d00;
    }

    /* ===== SELECTBOX & DROPDOWNS - Dark Text ===== */
    .stSelectbox > div > div {
        background-color: white !important;
        border: 2px solid #0066B3 !important;
        border-radius: 8px !important;
    }
    .stSelectbox label {
        color: #004d00 !important;
        font-weight: 600 !important;
    }
    /* Dropdown text - DARK */
    .stSelectbox [data-baseweb="select"] > div {
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }
    .stSelectbox span {
        color: #1a1a1a !important;
    }
    /* Dropdown options */
    [data-baseweb="menu"] {
        background-color: white !important;
    }
    [data-baseweb="menu"] li {
        color: #1a1a1a !important;
    }
    [data-baseweb="menu"] li:hover {
        background-color: #e6f2ff !important;
    }
    /* Selected option text */
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] {
        color: #1a1a1a !important;
    }
    /* All input text dark */
    input, textarea, [contenteditable] {
        color: #1a1a1a !important;
    }
    /* Radio buttons */
    .stRadio label {
        color: #004d00 !important;
    }
    .stRadio label span {
        color: #1a1a1a !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e6f2ff !important;
        border-radius: 8px 8px 0 0 !important;
        color: #004d00 !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00AF66 !important;
        color: white !important;
    }

    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] {
        color: #00AF66 !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #004d00 !important;
    }

    /* ===== CAPTIONS ===== */
    .stCaption, small {
        color: #0066B3 !important;
    }

    /* ===== MOBILE RESPONSIVENESS ===== */
    @media (max-width: 768px) {
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.25rem !important; }
        .word-card { padding: 12px !important; }
        .bashkir-text { font-size: 1.5em !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("🏰 Memory Palace")

# Sidebar toggle hint for mobile users
st.sidebar.caption("📱 *Tap ✕ to collapse sidebar*")
st.sidebar.markdown("---")

# Navigation - Radio buttons for individual tabs
pages = [
    "🗺️ Palace",
    "📚 Four Birds",
    "⚔️ Ural-Batyr Epic",
    "✍️ Sentence Builder",
    "🔊 Audio Dictionary",
    "🔄 Review",
    "🕸️ BashkortNet Explorer",
    "📖 Cultural Context",
    "🌟 Truth Unveiled",
    "⚙️ Settings"
]

selected_page = st.sidebar.radio("Navigate", pages, label_visibility="collapsed")

# Progress indicator
words_data = load_words()
learned_count = len(st.session_state.learned_words)
total_count = len(words_data)
progress = learned_count / total_count if total_count > 0 else 0

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Progress")
st.sidebar.progress(progress)
st.sidebar.markdown(f"**{learned_count}** / {total_count} words learned")

# Quick stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Today")
st.sidebar.metric("Words to Review", len(st.session_state.review_queue))
st.sidebar.metric("Sentences Created", len(st.session_state.saved_sentences))

# === PAGE: PALACE ===
if "Palace" in selected_page:
    st.title("🏰 The Memory Palace of Bashkortostan")
    st.markdown("*Walk through the stations. Let the Four Birds guide your learning.*")

    loci_data = load_loci()

    # Locus selection
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Choose Your Destination")

        locus_options = list(loci_data.keys())
        locus_display = {
            "Ufa": "🦅 Өфө – Eagle's Perch (Civic)",
            "Shulgan-Tash": "🐦⬛ Шүлгәнташ – Crow's Archive (Ancestry)",
            "Yamantau": "🔥🕊️ Ямантау – Anqa's Ascent (Mystery)",
            "Beloretsk": "🕊️ Белорет – Ringdove's Forge (Labor)",
            "Bizhbulyak": "🕊️ Бижбуляк – Ringdove's Hearth (Home)"
        }

        selected_locus = st.selectbox(
            "Select Location",
            locus_options,
            format_func=lambda x: locus_display.get(x, x)
        )

    with col2:
        if selected_locus:
            locus = loci_data[selected_locus]
            bird_symbol = locus.get('symbol', '🐦')
            bird_name = locus.get('bird', 'Bird')
            # Handle nested description structure
            description = locus.get('description', {})
            if isinstance(description, dict):
                short_desc = description.get('short', '')
            else:
                short_desc = str(description)
            st.markdown(f"### {bird_symbol} {bird_name}")
            st.markdown(f"*{short_desc}*")

    st.markdown("---")

    # Display selected locus
    if selected_locus:
        locus = loci_data[selected_locus]

        # Handle nested description structure for Ibn Arabi connection
        description = locus.get('description', {})
        if isinstance(description, dict):
            ibn_arabi_connection = description.get('ibn_arabi_connection', '')
        else:
            ibn_arabi_connection = ''

        # Ibn Arabi connection
        if ibn_arabi_connection:
            with st.expander("🌟 Ibn Arabi's Teaching", expanded=False):
                st.markdown(f"""
                <div class="meditation-box">
                {ibn_arabi_connection}
                </div>
                """, unsafe_allow_html=True)

        # Station walkthrough
        st.markdown("### 🚶 Station Walkthrough")

        for station in locus.get('stations', []):
            station_name = station.get('display_name', station.get('name', 'Station'))
            station_words = station.get('words', [])

            with st.expander(f"📍 Station {station.get('number', '?')}: {station_name}", expanded=True):
                # Opening meditation
                opening_med = station.get('opening_meditation', '')
                if opening_med:
                    st.markdown(f"""
                    <div class="meditation-box">
                    <strong>🕯️ Opening Meditation:</strong><br>
                    {opening_med}
                    </div>
                    """, unsafe_allow_html=True)

                # Words in this station
                st.markdown("#### Words at this Station:")

                # Create word cards - FIXED: properly filter words by station
                words_at_station = [w for w in words_data if w['bashkir'] in station_words]

                if words_at_station:
                    cols = st.columns(min(3, len(words_at_station)))
                    for idx, word in enumerate(words_at_station):
                        with cols[idx % 3]:
                            is_learned = word['bashkir'] in st.session_state.learned_words

                            # Using proper HTML structure with CSS classes
                            card_html = f'''
                            <div class="word-card">
                                <span class="bashkir-text">{word['bashkir']} {"✅" if is_learned else ""}</span>
                                <span class="ipa-text">{word.get('ipa', '')}</span>
                                <div class="english-text">{word['english']}</div>
                                <span class="russian-text">🇷🇺 {word.get('russian', '')}</span>
                            </div>
                            '''
                            st.markdown(card_html, unsafe_allow_html=True)

                            # Audio and Mnemonic buttons in a row
                            btn_col1, btn_col2 = st.columns(2)
                            with btn_col1:
                                if st.button("🔊 Hear", key=f"audio_{station_name}_{word['bashkir']}_{idx}"):
                                    play_audio(word['bashkir'])

                            with btn_col2:
                                # Mnemonic
                                mnemonic = word.get('memory_palace', {}).get('mnemonic', '')
                                if mnemonic:
                                    with st.popover("💡 Hint"):
                                        st.markdown(f"""
                                        <div class="mnemonic-text">
                                        {mnemonic}
                                        </div>
                                        """, unsafe_allow_html=True)

                            # Learn button
                            if not is_learned:
                                if st.button(f"Learn '{word['bashkir']}'", key=f"learn_{station_name}_{word['bashkir']}_{idx}"):
                                    st.session_state.learned_words.add(word['bashkir'])
                                    st.session_state.review_queue.append(word['bashkir'])
                                    st.rerun()
                else:
                    st.info("No vocabulary words assigned to this station yet.")

                # Closing meditation
                closing_med = station.get('closing_meditation', '')
                if closing_med:
                    st.markdown(f"""
                    <div class="meditation-box">
                    <strong>🕯️ Closing Meditation:</strong><br>
                    {closing_med}
                    </div>
                    """, unsafe_allow_html=True)

# === PAGE: FOUR BIRDS ===
elif "Four Birds" in selected_page:
    st.title("📚 The Four Birds of Ibn Arabi")
    st.markdown("*Understanding the cosmological framework of your learning journey.*")

    birds = [
        {
            "name": "Eagle",
            "arabic": "العقل الأول",
            "english": "First Intellect",
            "symbol": "🦅",
            "color": "eagle",
            "locus": "Ufa",
            "domain": "Civic & Legal Knowledge",
            "description": """The Eagle represents the First Intellect (al-'Aql al-Awwal) —
            the primordial light of knowledge from which all understanding flows.
            At Ufa, we encounter constitutional knowledge, legal rights, and civic identity.
            The Eagle sees the whole landscape from above; it knows the law that governs.""",
            "vocabulary": ["Башҡортостан", "халыҡ", "иркенлек", "тел", "конституция"]
        },
        {
            "name": "Crow",
            "arabic": "الجسم الكلي",
            "english": "Universal Body",
            "symbol": "🐦⬛",
            "color": "crow",
            "locus": "Shulgan-Tash",
            "domain": "Ancestral Memory & Nature",
            "description": """The Crow represents Universal Body (al-Jism al-Kulli) —
            matter infused with spirit, darkness containing light. In the cave's depths,
            we find manifestation: the physical traces of spiritual vision painted on stone.
            The Crow guards what was; it remembers what others forget.""",
            "vocabulary": ["ҡояш", "ай", "таш", "һыу", "йылға", "Ағиҙел"]
        },
        {
            "name": "Anqa",
            "arabic": "الهيولى",
            "english": "Prime Matter",
            "symbol": "🔥🕊️",
            "color": "anqa",
            "locus": "Yamantau",
            "domain": "Potential & Transformation",
            "description": """The Anqa represents Prime Matter (al-Hayūlā) —
            pure potentiality, the 'name without a body.' Like the mythical phoenix,
            it exists in the realm of possibility. At Yamantau ('Bad Mountain'),
            danger and transformation intertwine. From difficulty comes growth.""",
            "vocabulary": ["тау", "ел", "урман", "ҡурҡыныс", "күл", "яман", "ҙур"]
        },
        {
            "name": "Ringdove",
            "arabic": "النفس الكلية",
            "english": "Universal Soul",
            "symbol": "🕊️",
            "color": "ringdove",
            "locus": "Beloretsk & Bizhbulyak",
            "domain": "Daily Life & Community",
            "description": """The Ringdove represents Universal Soul (al-Nafs al-Kulliyya) —
            the receptive, nurturing principle that brings potential into form.
            At Beloretsk, raw ore becomes steel through patient work.
            At Bizhbulyak, family, food, and music create the texture of daily life.""",
            "vocabulary": ["эш", "болат", "оҫта", "бал", "ата", "әсә", "өй", "ҡурай", "ат"]
        }
    ]

    for bird in birds:
        st.markdown(f"""
        <div class="bird-card {bird['color']}-card">
            <h3>{bird['symbol']} {bird['name']} — {bird['english']}</h3>
            <p><em>Arabic: {bird['arabic']}</em></p>
            <p><strong>Domain:</strong> {bird['domain']}</p>
            <p><strong>Location:</strong> {bird['locus']}</p>
            <p>{bird['description']}</p>
            <p><strong>Key Vocabulary:</strong> {', '.join(bird['vocabulary'])}</p>
        </div>
        """, unsafe_allow_html=True)

    # Quiz section
    st.markdown("---")
    st.markdown("### 🎯 Test Your Understanding")

    quiz_questions = [
        {
            "question": "Which bird represents civic knowledge and legal rights?",
            "options": ["Crow", "Eagle", "Anqa", "Ringdove"],
            "correct": "Eagle"
        },
        {
            "question": "At which location would you find the Crow?",
            "options": ["Ufa", "Shulgan-Tash", "Yamantau", "Beloretsk"],
            "correct": "Shulgan-Tash"
        },
        {
            "question": "Which bird represents transformation and potential?",
            "options": ["Eagle", "Crow", "Anqa", "Ringdove"],
            "correct": "Anqa"
        }
    ]

    for i, q in enumerate(quiz_questions):
        answer = st.radio(q["question"], q["options"], key=f"quiz_{i}")
        if st.button("Check", key=f"check_{i}"):
            if answer == q["correct"]:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ The correct answer is: {q['correct']}")

# === PAGE: URAL-BATYR EPIC ===
elif "Ural-Batyr" in selected_page:
    st.title("⚔️ Урал-Батыр / Ural-Batyr")
    st.markdown("*The foundational myth of the Bashkir people — 4,576 lines of heroic legend*")

    # Load epic data
    epic_data = load_ural_batyr_epic()
    chapters = epic_data.get('chapters', [])
    legacy_proverb = epic_data.get('legacy_proverb', {})

    # Legacy proverb banner
    st.markdown(f"""
    <div class="meditation-box" style="text-align: center; border-left: none; border: 3px solid #d4af37;">
        <p style="font-size: 1.3em; margin-bottom: 10px;">✨ <strong>{legacy_proverb.get('bashkir', '')}</strong></p>
        <p style="font-size: 1.1em; color: #004d00;">{legacy_proverb.get('english', '')}</p>
        <p style="font-size: 0.9em; color: #666;">[{legacy_proverb.get('phonetic', '')}]</p>
    </div>
    """, unsafe_allow_html=True)

    # Chapter navigation
    st.markdown("### 📖 The Ten Chapters")
    chapter_cols = st.columns(10)
    for idx, ch in enumerate(chapters):
        with chapter_cols[idx]:
            bird_colors = {'Eagle': '#0066B3', 'Crow': '#333333', 'Anqa': '#cc3333', 'Ringdove': '#00AF66'}
            color = bird_colors.get(ch.get('bird', 'Ringdove'), '#00AF66')
            if st.button(f"{ch.get('icon', '📖')}", key=f"ch_{idx}", help=ch.get('title', '')):
                st.session_state.epic_chapter = idx

    # Current chapter display
    if chapters:
        current_ch = chapters[st.session_state.epic_chapter]

        # Chapter header
        bird_colors = {'Eagle': 'eagle', 'Crow': 'crow', 'Anqa': 'anqa', 'Ringdove': 'ringdove'}
        card_class = bird_colors.get(current_ch.get('bird', 'Ringdove'), 'ringdove')

        st.markdown(f"""
        <div class="bird-card {card_class}-card">
            <h2>{current_ch.get('icon', '')} Chapter {current_ch.get('id', '')}: {current_ch.get('title', '')}</h2>
            <p style="font-size: 1.2em;"><em>{current_ch.get('bashkir', '')}</em></p>
            <p><strong>Bird Guide:</strong> {current_ch.get('bird', '')} | <strong>Theme:</strong> {current_ch.get('summary', '')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Create tabs for chapter content
        tab1, tab2, tab3, tab4 = st.tabs(["📜 Story", "🧠 Memory Palace", "📚 Vocabulary", "🌟 Unveiling"])

        with tab1:
            st.markdown("### The Tale")
            # Split text into paragraphs
            story_text = current_ch.get('text', '')
            paragraphs = story_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    st.markdown(f"_{para.strip()}_")
                    st.markdown("")

        with tab2:
            st.markdown("### 🧠 Method of Loci — Memory Palace Technique")
            memory = current_ch.get('memory_palace', {})

            st.markdown(f"""
            <div class="stat-box" style="text-align: left;">
                <h4>🔑 Memory Peg</h4>
                <p style="font-size: 1.3em; font-family: monospace; color: #0066B3;">{memory.get('peg', '')}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="mnemonic-text">
                <h4>🎨 Visualization</h4>
                <p>{memory.get('image', '')}</p>
            </div>
            """, unsafe_allow_html=True)

            st.info(f"**Technique:** {memory.get('technique', '')}")

        with tab3:
            st.markdown("### 📚 Chapter Vocabulary")
            vocab = current_ch.get('vocabulary', [])
            if vocab:
                vocab_cols = st.columns(len(vocab))
                for idx, word in enumerate(vocab):
                    with vocab_cols[idx]:
                        st.markdown(f"""
                        <div class="word-card" style="text-align: center;">
                            <span class="bashkir-text">{word.get('bashkir', '')}</span>
                            <span class="ipa-text">[{word.get('phonetic', '')}]</span>
                            <div class="english-text">{word.get('english', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"🔊 Hear", key=f"epic_audio_{current_ch['id']}_{idx}"):
                            play_audio(word.get('bashkir', ''), slow=True)

        with tab4:
            st.markdown("### 🌟 The Unveiling")
            unveiling = current_ch.get('unveiling', '')
            st.markdown(f"""
            <div class="meditation-box">
                <p style="font-size: 1.1em; line-height: 1.8;">{unveiling}</p>
            </div>
            """, unsafe_allow_html=True)

            # Connection to the user's twin mythology
            if current_ch.get('id') == 1:
                st.markdown("""
                **The Duality of Twins:** Like Ural and Shulgen, twins carry the potential for both paths.
                One may seek the light, another may guard the depths. Both are necessary—the hero who
                sacrifices and the guardian who preserves memory in darkness.
                """)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.epic_chapter > 0:
            if st.button("← Previous Chapter"):
                st.session_state.epic_chapter -= 1
                st.rerun()
    with col3:
        if st.session_state.epic_chapter < len(chapters) - 1:
            if st.button("Next Chapter →"):
                st.session_state.epic_chapter += 1
                st.rerun()

# === PAGE: SENTENCE BUILDER (Enhanced with Audio Export) ===
elif "Sentence Builder" in selected_page:
    st.title("✍️ Sentence Builder")
    st.markdown("*Create your own Bashkir sentences, hear them spoken, and export audio for poems or stories!*")

    patterns = load_patterns()

    # Pattern templates
    st.markdown("### 📝 Sentence Patterns")

    pattern_list = patterns.get('patterns', [])[:5]

    if pattern_list:
        cols = st.columns(len(pattern_list))
        for idx, pattern in enumerate(pattern_list):
            with cols[idx]:
                st.markdown(f"""
                **{pattern['name']}**
                `{pattern['template']}`
                *{pattern['english_pattern']}*
                """)
                example = pattern.get('examples', [{}])[0]
                if example:
                    st.caption(f"Ex: {example.get('bashkir', '')}")

    st.markdown("---")

    # Word bank
    st.markdown("### 🏦 Word Bank")
    st.markdown("Click words to add them to your sentence:")

    word_categories = patterns.get('word_bank_categories', {})

    if word_categories:
        tabs = st.tabs(list(word_categories.keys()))

        for tab, (category, word_list) in zip(tabs, word_categories.items()):
            with tab:
                cols = st.columns(6)
                for idx, word in enumerate(word_list):
                    with cols[idx % 6]:
                        word_data = next((w for w in words_data if w['bashkir'] == word), None)
                        english = word_data.get('english', '?') if word_data else '?'

                        if st.button(f"{word}\n({english})", key=f"word_{category}_{word}"):
                            st.session_state.builder_sentence.append({
                                'word': word,
                                'english': english
                            })
                            st.rerun()

    st.markdown("---")

    # Current sentence display
    st.markdown("### 📜 Your Sentence")

    if st.session_state.builder_sentence:
        sentence_text = ' '.join([w['word'] for w in st.session_state.builder_sentence])
        gloss_text = ' | '.join([w['english'] for w in st.session_state.builder_sentence])

        st.markdown(f"""
        <div class="word-card">
            <span class="bashkir-text">{sentence_text}</span>
            <br><br>
            <small style="color: #666;">Gloss: {gloss_text}</small>
        </div>
        """, unsafe_allow_html=True)

        # Audio controls
        st.markdown("### 🔊 Audio Controls")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🔊 Hear Sentence"):
                play_audio(sentence_text, slow=False)

        with col2:
            if st.button("🔊 Hear Slow"):
                play_audio(sentence_text, slow=True)

        with col3:
            if st.button("💾 Save Sentence"):
                st.session_state.saved_sentences.append({
                    'bashkir': sentence_text,
                    'gloss': gloss_text,
                    'created': datetime.now().isoformat()
                })
                st.success("Sentence saved to your phrasebook!")

        with col4:
            if st.button("🗑️ Clear"):
                st.session_state.builder_sentence = []
                st.rerun()

        # Audio export
        st.markdown("### 💾 Export Audio")
        audio_bytes = generate_audio_with_retry(sentence_text, slow=True)
        if audio_bytes:
            st.download_button(
                label="⬇️ Download Audio (MP3)",
                data=audio_bytes,
                file_name=f"bashkir_sentence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                mime="audio/mp3"
            )

        # Grammar notes
        st.markdown("### 📖 Grammar Helper")
        st.info("""
        **Bashkir Word Order: Subject - Object - Verb (SOV)**

        Unlike English (I *see* the mountain), Bashkir puts the verb at the END:
        - Мин тауҙы **күрәм** (I mountain **see**)

        **Case Suffixes:**
        - Nominative (subject): no suffix
        - Dative (to/for): -ға/-гә
        - Accusative (object): -ны/-не
        - Ablative (from): -дан/-дән
        """)
    else:
        st.markdown("*Click words from the Word Bank to build your sentence.*")

    # Saved sentences with audio export
    if st.session_state.saved_sentences:
        st.markdown("---")
        st.markdown("### 📒 Your Phrasebook")

        for idx, sentence in enumerate(st.session_state.saved_sentences[-5:]):
            with st.container():
                st.markdown(f"""
                <div class="word-card">
                    <strong>{sentence['bashkir']}</strong><br>
                    <small>{sentence.get('gloss', '')}</small>
                </div>
                """, unsafe_allow_html=True)

                sent_col1, sent_col2, sent_col3 = st.columns(3)
                with sent_col1:
                    if st.button(f"▶️ Play", key=f"play_saved_{idx}"):
                        play_audio(sentence['bashkir'], slow=True)
                with sent_col2:
                    audio_data = generate_audio_with_retry(sentence['bashkir'], slow=True)
                    if audio_data:
                        st.download_button(
                            label="⬇️ Download",
                            data=audio_data,
                            file_name=f"sentence_{idx+1}.mp3",
                            mime="audio/mp3",
                            key=f"download_saved_{idx}"
                        )
                with sent_col3:
                    if st.button(f"🗑️ Remove", key=f"remove_saved_{idx}"):
                        st.session_state.saved_sentences.pop(idx)
                        st.rerun()

# === PAGE: AUDIO DICTIONARY ===
elif "Audio Dictionary" in selected_page:
    st.title("🔊 Audio Dictionary")
    st.markdown("*Listen to Bashkir words with pronunciation guides.*")

    # Search
    search_term = st.text_input("Search words (Bashkir or English):", key="audio_search")

    # Filter words
    if search_term:
        filtered_words = [w for w in words_data if search_term.lower() in w['bashkir'].lower() or search_term.lower() in w['english'].lower()]
    else:
        filtered_words = words_data[:20]  # Show first 20 by default

    st.write(f"Showing {len(filtered_words)} words")

    for word in filtered_words:
        with st.expander(f"🔊 {word['bashkir']} ({word['english']})"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"""
                <div class="word-card">
                    <span class="bashkir-text">{word['bashkir']}</span>
                    <span class="ipa-text">{word.get('ipa', '')}</span>
                    <div class="english-text">{word['english']}</div>
                    <span class="russian-text">🇷🇺 {word.get('russian', '')}</span>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("**Audio Controls:**")
                if st.button("▶️ Normal", key=f"audio_normal_{word['bashkir']}"):
                    play_audio(word['bashkir'], slow=False)
                if st.button("🐢 Slow", key=f"audio_slow_{word['bashkir']}"):
                    play_audio(word['bashkir'], slow=True)

                # Download option
                audio_bytes = generate_audio_with_retry(word['bashkir'], slow=True)
                if audio_bytes:
                    st.download_button(
                        label="⬇️ Download",
                        data=audio_bytes,
                        file_name=f"{word['bashkir']}.mp3",
                        mime="audio/mp3",
                        key=f"download_{word['bashkir']}"
                    )

# === PAGE: REVIEW (Fixed ZeroDivisionError) ===
elif "Review" in selected_page:
    st.title("🔄 Spaced Repetition Review")
    st.markdown("*Review learned words using the SM-2 algorithm for optimal retention.*")

    # Stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="stat-box">
            <h3>📚</h3>
            <h2>{}</h2>
            <p>Total Learned</p>
        </div>
        """.format(len(st.session_state.learned_words)), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-box">
            <h3>📋</h3>
            <h2>{}</h2>
            <p>Due Today</p>
        </div>
        """.format(len(st.session_state.review_queue)), unsafe_allow_html=True)

    with col3:
        mastered = len([w for w in st.session_state.learned_words
                       if st.session_state.srs_data.get(w, {}).get('interval', 0) >= 21])
        st.markdown(f"""
        <div class="stat-box">
            <h3>🏆</h3>
            <h2>{mastered}</h2>
            <p>Mastered</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        accuracy = 85  # Placeholder
        st.markdown(f"""
        <div class="stat-box">
            <h3>🎯</h3>
            <h2>{accuracy}%</h2>
            <p>Accuracy</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Review session
    if st.session_state.review_queue:
        st.markdown("### 📝 Review Session")

        # Get current word
        if 'review_index' not in st.session_state:
            st.session_state.review_index = 0

        if st.session_state.review_index < len(st.session_state.review_queue):
            current_word = st.session_state.review_queue[st.session_state.review_index]
            word_data = next((w for w in words_data if w['bashkir'] == current_word), None)

            if word_data:
                # Flashcard
                if 'show_answer' not in st.session_state:
                    st.session_state.show_answer = False

                st.markdown(f"""
                <div class="word-card" style="text-align: center; padding: 40px;">
                    <span class="bashkir-text" style="font-size: 2.5em;">{word_data['bashkir']}</span>
                    <br><br>
                    <small>{word_data.get('ipa', '')}</small>
                </div>
                """, unsafe_allow_html=True)

                if not st.session_state.show_answer:
                    if st.button("👁️ Show Answer", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()
                else:
                    st.markdown(f"""
                    <div class="word-card" style="text-align: center; background: #e8f5e9;">
                        <h2>{word_data['english']}</h2>
                        <p><em>{word_data.get('russian', '')}</em></p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Show mnemonic
                    mnemonic = word_data.get('memory_palace', {}).get('mnemonic', '')
                    if mnemonic:
                        st.markdown(f"""
                        <div class="mnemonic-text">
                        {mnemonic}
                        </div>
                        """, unsafe_allow_html=True)

                    # Rating buttons
                    st.markdown("**How well did you remember?**")

                    col1, col2, col3, col4 = st.columns(4)

                    ratings = [
                        ("😞 Forgot", 1, col1),
                        ("😕 Hard", 3, col2),
                        ("🙂 Good", 4, col3),
                        ("😄 Easy", 5, col4)
                    ]

                    for label, rating, col in ratings:
                        with col:
                            if st.button(label, key=f"rate_{rating}", use_container_width=True):
                                # Update SRS data
                                if current_word not in st.session_state.srs_data:
                                    st.session_state.srs_data[current_word] = {
                                        'ease': 2.5, 'interval': 0, 'reps': 0
                                    }

                                srs = st.session_state.srs_data[current_word]

                                if rating >= 3:
                                    if srs['reps'] == 0:
                                        srs['interval'] = 1
                                    elif srs['reps'] == 1:
                                        srs['interval'] = 6
                                    else:
                                        srs['interval'] = int(srs['interval'] * srs['ease'])
                                    srs['reps'] += 1
                                else:
                                    srs['interval'] = 1
                                    srs['reps'] = 0

                                srs['ease'] = max(1.3, srs['ease'] + (0.1 - (5 - rating) * 0.08))

                                # Move to next word
                                st.session_state.review_index += 1
                                st.session_state.show_answer = False
                                st.rerun()

                # Progress - FIXED: proper parentheses to avoid ZeroDivisionError
                total_reviews = len(st.session_state.review_queue)
                if total_reviews > 0:
                    progress = (st.session_state.review_index + 1) / total_reviews
                else:
                    progress = 0.0
                st.progress(min(progress, 1.0))
                st.caption(f"Card {st.session_state.review_index + 1} of {total_reviews}")
        else:
            st.success("🎉 Review session complete!")
            if st.button("Start New Session"):
                st.session_state.review_index = 0
                st.session_state.show_answer = False
                st.rerun()
    else:
        st.info("No words to review! Visit the Palace to learn new words.")
        if st.button("Go to Palace"):
            st.rerun()

# === PAGE: BASHKORTNET EXPLORER (Enhanced with OCM) ===
elif "BashkortNet" in selected_page:
    st.title("🕸️ BashkortNet Explorer (Semantic Network)")
    st.markdown("*Explore the semantic network connecting Bashkir words with OCM cultural classifications.*")

    # Load OCM data
    ocm_data = load_ocm_mapping()
    ocm_labels = ocm_data.get('ocm_labels', {})
    bashkir_to_ocm = ocm_data.get('bashkir_to_ocm', {})

    # Word search with Bashkir and English
    search_word = st.selectbox(
        "Select a word to explore (Bashkir / English):",
        [w['bashkir'] for w in words_data],
        format_func=lambda x: f"{x} ({next((w['english'] for w in words_data if w['bashkir'] == x), '?')})"
    )

    if search_word:
        word_data = next((w for w in words_data if w['bashkir'] == search_word), None)

        if word_data:
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown(f"""
                <div class="word-card">
                    <span class="bashkir-text">{word_data['bashkir']} (Башҡорт теле)</span>
                    <br>
                    <small>{word_data.get('ipa', '')}</small>
                    <br><br>
                    <strong>{word_data['english']} (English)</strong>
                    <br>
                    <em>{word_data.get('russian', '')}</em>
                    <br><br>
                    <small>POS: {word_data.get('pos', 'noun')}</small>
                </div>
                """, unsafe_allow_html=True)

                # Audio button
                if st.button("🔊 Play Pronunciation", key="bashkortnet_audio"):
                    play_audio(word_data['bashkir'], slow=True)

            with col2:
                # Create tabs for different aspects
                tab1, tab2, tab3 = st.tabs(["🕸️ Semantic Network", "📚 OCM Codes", "🔗 Etymology"])

                with tab1:
                    st.markdown("### Semantic Relations")

                    bashkortnet = word_data.get('bashkortnet', {})
                    relations = bashkortnet.get('relations', {})

                    if relations:
                        for rel_type, targets in relations.items():
                            if targets:
                                rel_labels = {
                                    'SYN': '🔄 Synonyms',
                                    'ANT': '↔️ Antonyms',
                                    'ISA': '⬆️ Is a type of',
                                    'HAS_TYPE': '⬇️ Types',
                                    'PART_OF': '🧩 Part of',
                                    'HAS_PART': '🔧 Has parts',
                                    'CULT_ASSOC': '🏛️ Cultural',
                                    'MYTH_LINK': '📜 Mythological'
                                }

                                st.markdown(f"**{rel_labels.get(rel_type, rel_type)}:**")

                                for target in targets:
                                    if isinstance(target, dict):
                                        target_word = target.get('target', target.get('gloss', str(target)))
                                        gloss = target.get('gloss', '')
                                        note = target.get('note', '')
                                        display = f"- {target_word}"
                                        if gloss:
                                            display += f" ({gloss})"
                                        if note:
                                            display += f" *({note})*"
                                        st.markdown(display)
                                    else:
                                        st.markdown(f"- {target}")
                    else:
                        st.info("No relations defined for this word yet.")

                with tab2:
                    st.markdown("### OCM Cultural Classification (eHRAF 2021)")

                    # Get OCM codes from multiple sources
                    word_ocm_codes = bashkir_to_ocm.get(word_data['bashkir'], [])
                    cultural_context = word_data.get('cultural_context', {})
                    embedded_ocm_codes = cultural_context.get('ocm_codes', [])

                    all_codes = list(set([str(c) for c in word_ocm_codes + embedded_ocm_codes]))

                    if all_codes:
                        for code in all_codes:
                            label = ocm_labels.get(str(code), f"Category {code}")
                            st.markdown(f"- **OCM {code}**: {label}")
                    else:
                        st.info("No OCM codes assigned to this word yet.")

                    # Cultural significance
                    if cultural_context.get('significance'):
                        st.markdown("### Cultural Significance")
                        st.markdown(f"_{cultural_context['significance']}_")

                with tab3:
                    st.markdown("### Etymology")

                    bashkortnet = word_data.get('bashkortnet', {})
                    etymology = bashkortnet.get('etymology', {})

                    if etymology:
                        proto = etymology.get('proto_form', '')
                        note = etymology.get('note', '')
                        if proto:
                            st.markdown(f"**Proto-form:** {proto}")
                        if note:
                            st.markdown(f"**Note:** {note}")
                    else:
                        st.info("No etymology information available.")

                    # Memory palace info
                    memory_palace = word_data.get('memory_palace', {})
                    if memory_palace:
                        st.markdown("### Memory Palace")
                        st.write(f"🐦 Bird: {memory_palace.get('bird', 'N/A')}")
                        st.write(f"📍 Locus: {memory_palace.get('locus', 'N/A')}")

# === PAGE: CULTURAL CONTEXT (Enhanced with OCM) ===
elif "Cultural Context" in selected_page:
    st.title("📖 Cultural Context")
    st.markdown("*Understand the anthropological depth behind each word with eHRAF 2021 OCM classifications.*")

    # Load OCM data
    ocm_data = load_ocm_mapping()
    ocm_labels = ocm_data.get('ocm_labels', {})
    bashkir_to_ocm = ocm_data.get('bashkir_to_ocm', {})
    thematic_groups = ocm_data.get('thematic_groups', {})

    # Truth Unveiled toggle
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔓 Truth Unveiled")
    st.session_state.truth_unveiled = st.sidebar.toggle(
        "Show sensitive sources",
        value=st.session_state.truth_unveiled,
        help="Enable to see academic sources that may be politically sensitive"
    )

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["🔍 Browse by Word", "📊 Browse by OCM", "🎨 Thematic Groups"])

    with tab1:
        # Word selection
        search_word = st.selectbox(
            "Select a word:",
            [w['bashkir'] for w in words_data],
            format_func=lambda x: f"{x} ({next((w['english'] for w in words_data if w['bashkir'] == x), '?')})"
        )

        if search_word:
            word_data = next((w for w in words_data if w['bashkir'] == search_word), None)

            if word_data:
                st.markdown(f"## {word_data['bashkir']} — {word_data['english']}")

                cultural = word_data.get('cultural_context', {})

                # OCM codes
                word_ocm_codes = bashkir_to_ocm.get(word_data['bashkir'], [])
                embedded_ocm_codes = cultural.get('ocm_codes', [])
                all_codes = list(set([str(c) for c in word_ocm_codes + embedded_ocm_codes]))

                if all_codes:
                    st.markdown("### 🏷️ OCM Categories (eHRAF 2021)")
                    for code in all_codes:
                        label = ocm_labels.get(str(code), f"Category {code}")
                        st.markdown(f"- **{code}**: {label}")

                # Significance
                significance = cultural.get('significance', '')
                if significance:
                    st.markdown("### 📜 Cultural Significance")
                    st.markdown(f"""
                    <div class="meditation-box">
                    {significance}
                    </div>
                    """, unsafe_allow_html=True)

                # Sources
                sources = cultural.get('sources', [])
                if sources:
                    st.markdown("### 📚 Sources")
                    for source in sources:
                        if isinstance(source, dict):
                            st.markdown(f"- {source.get('author', '')} ({source.get('year', '')}). *{source.get('title', '')}*")
                        else:
                            st.markdown(f"- {source}")

                # Sensitivity warning
                sensitivity = cultural.get('sensitivity', {})
                if sensitivity.get('has_sensitive_context') and st.session_state.truth_unveiled:
                    st.markdown("### ⚠️ Sensitivity Context")
                    st.warning(sensitivity.get('note', 'This topic has sensitive political context.'))

    with tab2:
        st.markdown("### Browse by OCM Category")
        st.markdown("*Explore words organized by anthropological classification*")

        # Get unique OCM codes from all words
        all_ocm_codes_list = []
        for word in words_data:
            cultural = word.get('cultural_context', {})
            codes = cultural.get('ocm_codes', [])
            all_ocm_codes_list.extend([str(c) for c in codes])

        unique_codes = sorted(set(all_ocm_codes_list))

        if unique_codes:
            selected_code = st.selectbox(
                "Select OCM Category:",
                unique_codes,
                format_func=lambda x: f"{x}: {ocm_labels.get(x, 'Unknown')}"
            )

            if selected_code:
                st.markdown(f"### {ocm_labels.get(selected_code, f'Category {selected_code}')}")

                # Find words with this OCM code
                matching_words = [
                    w for w in words_data
                    if selected_code in [str(c) for c in w.get('cultural_context', {}).get('ocm_codes', [])]
                ]

                if matching_words:
                    for word in matching_words:
                        st.markdown(f"- **{word['bashkir']}** ({word['english']})")
                else:
                    st.info("No words found with this OCM code.")
        else:
            st.info("No OCM codes found in vocabulary data.")

    with tab3:
        st.markdown("### Thematic Groups")
        st.markdown("*Words organized by cultural and linguistic themes*")

        if thematic_groups:
            for theme_name, theme_data in thematic_groups.items():
                display_name = theme_name.replace('_', ' ').title()
                theme_ocm_codes = theme_data.get('ocm_codes', [])
                theme_words = theme_data.get('words', [])

                with st.expander(f"🎨 {display_name}"):
                    if theme_ocm_codes:
                        st.markdown("**OCM Codes:**")
                        code_labels = [f"{c}: {ocm_labels.get(c, 'Unknown')}" for c in theme_ocm_codes]
                        st.write(", ".join(code_labels))

                    if theme_words:
                        st.markdown("**Words:**")
                        word_displays = []
                        for bword in theme_words:
                            word_info = next((w for w in words_data if w['bashkir'] == bword), None)
                            if word_info:
                                word_displays.append(f"**{bword}** ({word_info['english']})")
                            else:
                                word_displays.append(f"**{bword}**")
                        st.markdown(" | ".join(word_displays))
        else:
            st.info("No thematic groups defined yet.")

# === PAGE: TRUTH UNVEILED ===
elif "Truth Unveiled" in selected_page:
    st.title("🌟 Truth Unveiled — Алтын Яҡты")
    st.markdown("*The Golden Light: Proverbs, Timeline, and the Deeper Knowledge*")

    # Load epic data for proverbs and timeline
    epic_data = load_ural_batyr_epic()
    proverbs = epic_data.get('proverbs', [])
    timeline = epic_data.get('timeline', [])
    cultural_facts = epic_data.get('cultural_facts', [])
    legacy_proverb = epic_data.get('legacy_proverb', {})

    # The Golden Light Introduction
    st.markdown(f"""
    <div class="meditation-box" style="border: 3px solid #d4af37; border-left: 5px solid #d4af37;">
        <h3 style="color: #d4af37; text-align: center;">✨ Алтын Яҡты — Golden Light ✨</h3>
        <p style="text-align: center; font-size: 1.2em; margin: 15px 0;">
            <strong>"{legacy_proverb.get('bashkir', '')}"</strong>
        </p>
        <p style="text-align: center; font-style: italic;">
            "{legacy_proverb.get('english', '')}"
        </p>
        <p style="text-align: center; color: #666; font-size: 0.9em;">
            [{legacy_proverb.get('phonetic', '')}]
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    *This is the anchoring proverb of Golden Light—the Ural-Batyr legacy. It reflects the hero's
    ultimate sacrifice and the enduring Bashkir spirit. When Ural poured the waters of life for
    all rather than drinking them himself, he demonstrated this truth: we live on through what we give.*
    """)

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📜 Proverbs", "⏳ Timeline", "🏔️ Cultural Facts", "🔥 The Duality"])

    with tab1:
        st.markdown("### 📜 Bashkir Proverbs — Мәҡәлдәр")
        st.markdown("*Wisdom passed down through generations*")

        # Filter by category
        categories = list(set([p.get('category', 'General') for p in proverbs]))
        selected_category = st.selectbox("Filter by theme:", ['All'] + categories)

        filtered_proverbs = proverbs if selected_category == 'All' else [p for p in proverbs if p.get('category') == selected_category]

        for proverb in filtered_proverbs:
            st.markdown(f"""
            <div class="word-card" style="border-left: 5px solid #d4af37;">
                <span style="background: #d4af37; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em;">
                    {proverb.get('category', 'General')}
                </span>
                <p class="bashkir-text" style="margin-top: 10px;">{proverb.get('bashkir', '')}</p>
                <p class="russian-text">🇷🇺 {proverb.get('russian', '')}</p>
                <p class="english-text">🇬🇧 {proverb.get('english', '')}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### ⏳ Historical Timeline — Тарих юлы")
        st.markdown("*Key moments in Bashkir history*")

        # Timeline visualization
        for idx, event in enumerate(timeline):
            year = event.get('year', '')
            desc = event.get('event', '')

            st.markdown(f"""
            <div style="display: flex; margin: 10px 0;">
                <div style="min-width: 80px; padding: 8px; background: #0066B3; color: white; border-radius: 8px; text-align: center; font-weight: bold;">
                    {year}
                </div>
                <div style="flex: 1; padding: 8px 15px; background: #e6f2ff; border-radius: 8px; margin-left: 10px; border-left: 3px solid #00AF66;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🏔️ Cultural Facts — Мәҙәниәт")
        st.markdown("*Deep knowledge of Bashkir heritage*")

        # Filter by category
        fact_categories = list(set([f.get('category', 'general') for f in cultural_facts]))
        selected_fact_category = st.selectbox("Filter facts by:", ['All'] + fact_categories, key="fact_filter")

        filtered_facts = cultural_facts if selected_fact_category == 'All' else [f for f in cultural_facts if f.get('category') == selected_fact_category]

        for fact in filtered_facts:
            cat_colors = {'history': '#0066B3', 'culture': '#00AF66', 'geography': '#d4af37', 'language': '#cc3333'}
            color = cat_colors.get(fact.get('category', ''), '#666')

            st.markdown(f"""
            <div class="word-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="background: {color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em;">
                        {fact.get('category', 'general').upper()}
                    </span>
                    <span style="color: #666; font-size: 0.9em;">{fact.get('year', '')}</span>
                </div>
                <h4 style="color: #00AF66; margin: 5px 0;">{fact.get('title', '')}</h4>
                <p style="color: #004d00;">{fact.get('content', '')}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("### 🔥 The Duality: Ural and Shulgen")
        st.markdown("*Understanding the twin paths of the Bashkir soul*")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="bird-card eagle-card" style="min-height: 350px;">
                <h3>🏔️ URAL</h3>
                <p><strong>The Path of Light</strong></p>
                <hr>
                <p><strong>Choice:</strong> Sacrifice for all</p>
                <p><strong>Symbol:</strong> The Mountains</p>
                <p><strong>Legacy:</strong> Eternal protection</p>
                <hr>
                <p style="font-style: italic;">
                "I am not dying—I am becoming something greater. These mountains will be my body,
                and I will protect our people forever."
                </p>
                <hr>
                <p><strong>Lesson:</strong> True immortality comes through selfless action.
                The hero who gives everything gains everything.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="bird-card crow-card" style="min-height: 350px;">
                <h3>🌊 SHULGEN</h3>
                <p><strong>The Path of Depth</strong></p>
                <hr>
                <p><strong>Choice:</strong> Power over love</p>
                <p><strong>Symbol:</strong> The Cave</p>
                <p><strong>Legacy:</strong> Guardian of memory</p>
                <hr>
                <p style="font-style: italic;">
                "Brother... I see now what I became. Forgive me..."
                — Shulgen's final words
                </p>
                <hr>
                <p><strong>Redemption:</strong> Shulgan-Tash cave holds 16,000-year-old paintings.
                The one who fell guards the ancient memory in darkness.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        ---
        ### The Unity of Opposites

        In Bashkir philosophy, Ural and Shulgen are not simply good and evil—they are
        complementary forces. The mountains rise into light; the caves descend into memory.
        Both are necessary.

        **For twins:** You carry both paths within you. One may be called to shine in the world;
        another may be called to preserve and protect from the depths. Neither path is lesser.
        Together, you form something complete—like the mountains and the caves of Bashkortostan.

        *"Батыр үлмәй, аты ҡала"* — The hero doesn't die, his name remains.
        """)

        st.markdown(f"""
        <div class="meditation-box" style="text-align: center; margin-top: 20px;">
            <p style="font-size: 1.1em;">
                🏔️ The Ural Mountains are Ural-Batyr's body.<br>
                🌊 Shulgan-Tash Cave holds Shulgen's memory.<br>
                🌟 Together, they are Bashkortostan.
            </p>
        </div>
        """, unsafe_allow_html=True)

# === PAGE: SETTINGS ===
elif "Settings" in selected_page:
    st.title("⚙️ Settings")

    st.markdown("### 🎨 Display Settings")

    st.markdown("### 🔊 Audio Settings")
    st.checkbox("Enable audio playback", value=True)
    st.slider("Audio speed", 0.5, 1.5, 1.0)

    st.markdown("### 📊 Learning Settings")
    st.number_input("New words per session", 1, 20, 5)
    st.number_input("Review words per session", 5, 50, 20)

    st.markdown("### 🔄 Data Management")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export Progress"):
            progress_data = {
                'learned_words': list(st.session_state.learned_words),
                'saved_sentences': st.session_state.saved_sentences,
                'srs_data': st.session_state.srs_data
            }
            st.download_button(
                "Download JSON",
                json.dumps(progress_data, ensure_ascii=False, indent=2),
                "bashkir_progress.json",
                "application/json"
            )

    with col2:
        if st.button("Reset All Progress"):
            st.session_state.learned_words = set()
            st.session_state.review_queue = []
            st.session_state.saved_sentences = []
            st.session_state.srs_data = {}
            st.success("Progress reset!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 📖 About")
    st.markdown("""
    **Bashkir Memory Palace** v2.0 Enhanced

    A language learning application integrating:
    - Ibn Arabi's mystical framework (Four Birds)
    - Memory Palace technique (Method of Loci)
    - Anthropological pedagogy (OCM/eHRAF 2021 methodology)
    - Spaced Repetition (SM-2 algorithm)
    - BashkortNet semantic network
    - Audio export for sentences and poems

    *"The journey made within yourself leads to yourself."*
    — Ibn Arabi, Secrets of Voyaging
    """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p>🏰 Bashkir Memory Palace — <em>Secrets of Voyaging</em></p>
    <p>🦅 Eagle · 🐦⬛ Crow · 🔥🕊️ Anqa · 🕊️ Ringdove</p>
    <p><em>"Voyaging has no end, for therein is the joy of the Real."</em></p>
</div>
""", unsafe_allow_html=True)

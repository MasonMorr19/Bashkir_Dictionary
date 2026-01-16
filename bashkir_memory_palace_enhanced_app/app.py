#!/usr/bin/env python3
"""
🏰 Bashkir Memory Palace: Enhanced Edition
==========================================
A language learning app integrating Ibn Arabi's mystical framework,
memory palace techniques, and anthropological pedagogy with advanced
audio dictionary features.

The Four Birds guide your journey:
🦅 Eagle (First Intellect) - Civic knowledge at Ufa
🐦⬛ Crow (Universal Body) - Ancestral memory at Shulgan-Tash
🔥🕊️ Anqa (Prime Matter) - Transformation at Yamantau
🕊️ Ringdove (Universal Soul) - Daily life at Beloretsk & Bizhbulyak

Enhanced with:
- Advanced audio dictionary features
- SM-2 Spaced Repetition
- Semantic Networks (BashkortNet)
- Mnemonic Generation
- Sentence Building
- Translation services
- Speech recognition (Whisper)
- Audio analysis
"""

import streamlit as st
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
import logging

# Add parent directory to path to import shared utilities
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.retry import RetryConfig

# --- Module Imports ---
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

# --- Additional Libraries for Enhanced Features ---
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# --- Enhanced Modules ---
from modules.audio_service import AudioService, get_audio_service
from modules.spaced_repetition import SpacedRepetitionSystem, ReviewSession
from modules.sentence_builder import SentenceBuilder, BashkirGrammar
from modules.mnemonic_generator import MnemonicGenerator, StoryChainGenerator
from modules.bashkortnet import BashkortNet

# Create audio cache directory
AUDIO_CACHE_DIR = Path(__file__).parent / "audio_cache"
AUDIO_CACHE_DIR.mkdir(exist_ok=True)

# --- Enhanced Audio Generation with Retry Logic ---
def generate_audio_with_retry(text: str, language: str = 'ru', slow: bool = True) -> bytes:
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


def play_audio(text: str, language: str = 'ru', slow: bool = True):
    """Generate and play audio for Bashkir text with caching and retry logic."""
    if not AUDIO_AVAILABLE:
        st.warning("🔇 Audio unavailable. Install with: `pip install gTTS`")
        return

    audio_bytes = generate_audio_with_retry(text, language, slow)

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


def analyze_audio_properties(audio_path: str) -> dict:
    """Analyze audio file properties using librosa."""
    if not LIBROSA_AVAILABLE:
        return {}

    try:
        # Load audio file
        y, sr = librosa.load(audio_path)

        # Calculate various audio properties
        duration = librosa.get_duration(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

        analysis = {
            "duration": duration,
            "sample_rate": sr,
            "tempo": float(tempo),
            "mfcc_mean": mfccs.mean(axis=1).tolist(),
            "total_frames": len(y)
        }

        return analysis
    except Exception as e:
        return {}


def tokenize_text(text: str) -> list:
    """Tokenize text using transformer tokenizer."""
    if not TRANSFORMERS_AVAILABLE:
        # Simple fallback tokenization
        return text.split()

    try:
        # Use a general-purpose tokenizer
        tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
        tokens = tokenizer.tokenize(text)
        return tokens
    except Exception as e:
        # Simple fallback tokenization
        return text.split()


# Page configuration
st.set_page_config(
    page_title="Bashkir Memory Palace - Enhanced",
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
    if 'sentence_builder' not in st.session_state:
        # Initialize the sentence builder
        words_data = load_words()
        patterns_data = load_patterns()
        st.session_state.sentence_builder = SentenceBuilder(words_data, patterns_data)
    if 'bashkortnet' not in st.session_state:
        # Initialize the semantic network
        words_data = load_words()
        st.session_state.bashkortnet = BashkortNet(words_data)
    if 'srs_system' not in st.session_state:
        # Initialize the spaced repetition system
        st.session_state.srs_system = SpacedRepetitionSystem()
    if 'audio_service' not in st.session_state:
        # Initialize the audio service
        st.session_state.audio_service = get_audio_service()

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

# Navigation - Individual radio buttons for all tabs (Audio Dictionary under Sentence Builder)
pages = [
    "🗺️ Palace",
    "📚 Four Birds",
    "✍️ Sentence Builder",
    "🔊 Audio Dictionary",  # Moved under Sentence Builder
    "🔄 Review",
    "🕸️ BashkortNet Explorer",
    "📖 Cultural Context",
    "⚙️ Settings"
]

# Use radio buttons instead of dropdown for visible individual tabs
st.sidebar.markdown("### Navigate")
selected_page = st.sidebar.radio(
    "Select a section:",
    pages,
    index=pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0,
    key="nav_radio",
    label_visibility="collapsed"
)

# Update session state when selection changes
if selected_page != st.session_state.current_page:
    st.session_state.current_page = selected_page
    st.rerun()

# --- Main Content Area ---
def render_palace_view():
    """Render the main palace navigation view."""
    st.title("🏰 Bashkir Memory Palace")
    st.subheader("Secrets of Voyaging")
    
    # Introduction
    st.markdown("""
    <div class="meditation-box">
    The Four Birds guide your journey through the Bashkir language:
    <br><br>
    <strong>🦅 Eagle (First Intellect)</strong> - Civic knowledge at Ufa<br>
    <strong>🐦⬛ Crow (Universal Body)</strong> - Ancestral memory at Shulgan-Tash<br>
    <strong>🔥🕊️ Anqa (Prime Matter)</strong> - Transformation at Yamantau<br>
    <strong>🕊️ Ringdove (Universal Soul)</strong> - Daily life at Beloretsk & Bizhbulyak
    </div>
    """, unsafe_allow_html=True)
    
    # Loci selection
    loci = load_loci()
    
    # Create columns for loci
    cols = st.columns(len(loci))
    
    for i, (locus_id, locus_info) in enumerate(loci.items()):
        with cols[i]:
            # Bird emoji based on the bird
            bird_emoji = {
                'Eagle': '🦅',
                'Crow': '🐦⬛',
                'Anqa': '🔥🕊️',
                'Ringdove': '🕊️'
            }.get(locus_info.get('bird', 'Ringdove'), '🕊️')
            
            # Create card for each locus - handle nested description structure
            description = locus_info.get('description', {})
            if isinstance(description, dict):
                short_desc = description.get('short', '')
                ibn_arabi = description.get('ibn_arabi_connection', '')
            else:
                short_desc = str(description)
                ibn_arabi = ''

            display_name = locus_info.get('display_name', locus_info.get('name', locus_id))

            st.markdown(f"""
            <div class="word-card bird-card {locus_info.get('bird', 'Ringdove').lower()}-card">
                <h4>{bird_emoji} {display_name}</h4>
                <p><strong>{locus_info.get('name', locus_id)}</strong></p>
                <p>{short_desc}</p>
                <p><em>{ibn_arabi}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Button to select this locus
            if st.button(f"Enter {locus_info['name']}", key=f"enter_{locus_id}"):
                st.session_state.current_locus = locus_id
                st.session_state.current_station = 0
                st.rerun()

def render_four_birds_view():
    """Render the Four Birds explanation view."""
    st.title("📚 The Four Birds Framework")
    
    birds_info = {
        'Eagle': {
            'name': 'Eagle (First Intellect)',
            'location': 'Ufa',
            'theme': 'Civic Knowledge',
            'description': 'The Eagle represents the First Intellect, the source of all laws and civic order. At Ufa, you learn formal language, legal terms, and governmental vocabulary.',
            'color': '#0066B3',
            'emoji': '🦅'
        },
        'Crow': {
            'name': 'Crow (Universal Body)',
            'location': 'Shulgan-Tash',
            'theme': 'Ancestral Memory',
            'description': 'The Crow embodies Universal Body, representing ancestral memory and cultural heritage. At Shulgan-Tash, you explore traditional vocabulary, historical terms, and cultural expressions.',
            'color': '#333333',
            'emoji': '🐦⬛'
        },
        'Anqa': {
            'name': 'Anqa (Prime Matter)',
            'location': 'Yamantau',
            'theme': 'Transformation',
            'description': 'The Anqa symbolizes Prime Matter, the transformative potential. At Yamantau, you encounter vocabulary related to change, growth, and personal transformation.',
            'color': '#cc3333',
            'emoji': '🔥鸽️'
        },
        'Ringdove': {
            'name': 'Ringdove (Universal Soul)',
            'location': 'Beloretsk & Bizhbulyak',
            'theme': 'Daily Life',
            'description': 'The Ringdove represents Universal Soul, the nurturing force of daily life. At Beloretsk and Bizhbulyak, you learn everyday vocabulary, family terms, and social expressions.',
            'color': '#00AF66',
            'emoji': '鸽️'
        }
    }
    
    for bird_id, bird_info in birds_info.items():
        st.markdown(f"""
        <div class="word-card bird-card {bird_id.lower()}-card">
            <h3>{bird_info['emoji']} {bird_info['name']}</h3>
            <p><strong>Location:</strong> {bird_info['location']}</p>
            <p><strong>Theme:</strong> {bird_info['theme']}</p>
            <p>{bird_info['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def render_sentence_builder_view():
    """Render the sentence builder view with audio export functionality."""
    st.title("✍️ Bashkir Sentence Builder")
    st.markdown("*Build sentences and export audio for poems, stories, or learning!*")

    # Initialize sentence builder if not exists
    if 'sentence_builder' not in st.session_state:
        words_data = load_words()
        patterns_data = load_patterns()
        st.session_state.sentence_builder = SentenceBuilder(words_data, patterns_data)

    sb = st.session_state.sentence_builder

    # Show current sentence
    st.subheader("Current Sentence")
    current_sentence = sb.get_sentence_text()
    if current_sentence:
        st.markdown(f"<div class='word-card'><span class='bashkir-text'>{current_sentence}</span></div>", unsafe_allow_html=True)

        # Show gloss
        gloss = sb.get_sentence_gloss()
        if gloss:
            st.markdown(f"<div class='word-card'><span class='english-text'>Gloss: {gloss}</span></div>", unsafe_allow_html=True)

        # Audio controls for current sentence
        st.subheader("🔊 Audio Controls")
        audio_col1, audio_col2, audio_col3 = st.columns(3)

        with audio_col1:
            if st.button("▶️ Play Sentence", key="play_sentence"):
                play_audio(current_sentence, language='ru', slow=True)

        with audio_col2:
            if st.button("▶️ Play Slow", key="play_slow"):
                play_audio(current_sentence, language='ru', slow=True)

        with audio_col3:
            # Export audio as downloadable file
            if st.button("💾 Generate Audio File", key="export_audio"):
                audio_bytes = generate_audio_with_retry(current_sentence, language='ru', slow=True)
                if audio_bytes:
                    st.download_button(
                        label="⬇️ Download Audio (MP3)",
                        data=audio_bytes,
                        file_name=f"bashkir_sentence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                        mime="audio/mp3",
                        key="download_sentence_audio"
                    )
                    st.success("Audio generated! Click to download.")
                else:
                    st.error("Failed to generate audio. Please try again.")
    else:
        st.info("Build a sentence by adding words below...")

    # Word bank
    st.subheader("Word Bank")
    col1, col2 = st.columns(2)

    with col1:
        # Show available parts of speech
        pos_options = ['noun', 'verb', 'adjective', 'pronoun', 'other']
        selected_pos = st.selectbox("Filter by Part of Speech", pos_options)

    with col2:
        # Show available cases
        case_options = ['nominative', 'genitive', 'dative', 'accusative', 'locative', 'ablative']
        selected_case = st.selectbox("Case Ending", case_options)

    # Get words based on filter
    all_words = sb.get_word_bank()
    filtered_words = [w for w in all_words if w.get('pos', 'other') == selected_pos] if selected_pos != 'other' else all_words

    # Display word selection
    word_options = [f"{w['bashkir']} ({w['english']})" for w in filtered_words]
    if word_options:
        selected_word_option = st.selectbox("Select Word", word_options)

        if selected_word_option:
            selected_word = selected_word_option.split(' (')[0]  # Extract bashkir word

            # Preview word audio
            word_col1, word_col2 = st.columns(2)
            with word_col1:
                if st.button(f"Add '{selected_word}' to Sentence"):
                    sb.add_word(selected_word, selected_case)
                    st.rerun()
            with word_col2:
                if st.button(f"🔊 Preview '{selected_word}'", key="preview_word"):
                    play_audio(selected_word, language='ru', slow=True)

    # Sentence actions
    st.subheader("Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗑️ Clear Sentence"):
            sb.clear_sentence()
            st.rerun()

    with col2:
        if current_sentence and st.button("📊 Analyze Sentence"):
            analysis = sb.get_sentence_analysis()
            st.json(analysis)

    with col3:
        if current_sentence:
            english_input = st.text_input("English Translation:", key="english_trans")
            if st.button("💾 Save Sentence") and english_input:
                saved = sb.save_sentence(english_input)
                st.success(f"Saved: {saved['bashkir']} - {english_input}")
                st.session_state.saved_sentences.append(saved)

    # Show saved sentences with audio export
    if st.session_state.saved_sentences:
        st.subheader("📝 Saved Sentences")
        st.markdown("*Your sentences with audio export options*")

        for i, sent in enumerate(st.session_state.saved_sentences):
            with st.container():
                st.markdown(f"""
                <div class='word-card'>
                    <span class='bashkir-text'>{sent['bashkir']}</span><br>
                    <span class='english-text'>{sent.get('english', '')}</span>
                </div>
                """, unsafe_allow_html=True)

                sent_col1, sent_col2, sent_col3 = st.columns(3)
                with sent_col1:
                    if st.button(f"▶️ Play", key=f"play_saved_{i}"):
                        play_audio(sent['bashkir'], language='ru', slow=True)
                with sent_col2:
                    audio_bytes = generate_audio_with_retry(sent['bashkir'], language='ru', slow=True)
                    if audio_bytes:
                        st.download_button(
                            label="⬇️ Download",
                            data=audio_bytes,
                            file_name=f"bashkir_sentence_{i+1}.mp3",
                            mime="audio/mp3",
                            key=f"download_saved_{i}"
                        )
                with sent_col3:
                    if st.button(f"🗑️ Remove", key=f"remove_saved_{i}"):
                        st.session_state.saved_sentences.pop(i)
                        st.rerun()

        # Batch export all sentences
        st.markdown("---")
        st.subheader("📦 Batch Export")
        if st.button("🎵 Generate All Audio Files"):
            st.write("Generating audio for all saved sentences...")
            progress_bar = st.progress(0)

            all_audio_data = []
            for idx, sent in enumerate(st.session_state.saved_sentences):
                audio_bytes = generate_audio_with_retry(sent['bashkir'], language='ru', slow=True)
                if audio_bytes:
                    all_audio_data.append({
                        'filename': f"sentence_{idx+1}_{sent['bashkir'][:20]}.mp3",
                        'data': audio_bytes,
                        'text': sent['bashkir'],
                        'english': sent.get('english', '')
                    })
                progress_bar.progress((idx + 1) / len(st.session_state.saved_sentences))

            st.success(f"Generated {len(all_audio_data)} audio files!")

            # Display download links for each
            for audio_item in all_audio_data:
                st.download_button(
                    label=f"⬇️ {audio_item['text'][:30]}...",
                    data=audio_item['data'],
                    file_name=audio_item['filename'],
                    mime="audio/mp3",
                    key=f"batch_download_{audio_item['filename']}"
                )

def render_review_view():
    """Render the review system view."""
    st.title("🔄 Spaced Repetition Review")
    
    # Initialize SRS if not exists
    if 'srs_system' not in st.session_state:
        st.session_state.srs_system = SpacedRepetitionSystem()
    
    srs = st.session_state.srs_system
    
    # Show statistics
    stats = srs.get_statistics()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Words", stats['total_words'])
    col2.metric("Learning", stats['learning'])
    col3.metric("Mastered", stats['mastered'])
    col4.metric("Due Today", stats['due_today'])
    
    # Start review session
    if st.button("Start Review Session"):
        words_data = load_words()
        session = ReviewSession(srs, words_data)
        if session.start_session(new_words=5, review_words=10):
            st.session_state.review_session = session
            st.rerun()
    
    # Show review session if active
    if 'review_session' in st.session_state and st.session_state.review_session:
        session = st.session_state.review_session
        
        item_data = session.get_current_item()
        if item_data:
            item, word_data = item_data
            
            st.subheader(f"Review: {word_data['bashkir']}")
            st.markdown(f"<div class='word-card'><span class='bashkir-text'>{word_data['bashkir']}</span><br><span class='english-text'>{word_data['english']}</span></div>", unsafe_allow_html=True)
            
            # Play audio
            if st.button("Play Audio"):
                play_audio(word_data['bashkir'])
            
            # Quality rating
            st.write("How well did you know this word?")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                if st.button("0 - Forgot"):
                    result = session.submit_answer(0)
                    st.rerun()
            with col2:
                if st.button("1 - Hard"):
                    result = session.submit_answer(1)
                    st.rerun()
            with col3:
                if st.button("2 - Medium"):
                    result = session.submit_answer(2)
                    st.rerun()
            with col4:
                if st.button("3 - Good"):
                    result = session.submit_answer(3)
                    st.rerun()
            with col5:
                if st.button("4 - Easy"):
                    result = session.submit_answer(4)
                    st.rerun()
            with col6:
                if st.button("5 - Perfect"):
                    result = session.submit_answer(5)
                    st.rerun()
            
            # Show session summary
            summary = session.get_session_summary()
            total_items = summary['completed'] + summary['remaining']
            progress_value = summary['completed'] / total_items if total_items > 0 else 0.0
            st.progress(min(progress_value, 1.0))
            st.write(f"Progress: {summary['completed']}/{total_items} | Accuracy: {summary['accuracy']}%")
        else:
            st.success("Session completed!")
            del st.session_state.review_session

@st.cache_data
def load_ocm_mapping():
    """Load OCM mapping data."""
    data_path = Path(__file__).parent / "data" / "ocm_mapping.json"
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def render_bashkortnet_view():
    """Render the BashkortNet Explorer (Semantic Network) view with OCM features."""
    st.title("🕸️ BashkortNet Explorer (Semantic Network)")
    st.markdown("*Explore semantic relationships between Bashkir words with cultural and anthropological context*")

    # Initialize BashkortNet if not exists
    if 'bashkortnet' not in st.session_state:
        words_data = load_words()
        st.session_state.bashkortnet = BashkortNet(words_data)

    net = st.session_state.bashkortnet

    # Load OCM mapping
    ocm_data = load_ocm_mapping()
    ocm_labels = ocm_data.get('ocm_labels', {})
    bashkir_to_ocm = ocm_data.get('bashkir_to_ocm', {})

    # Word search with both Bashkir and English display
    words_data = load_words()
    word_list = [f"{w['bashkir']} ({w['english']})" for w in words_data]
    selected_word_option = st.selectbox("Select a word to explore (Bashkir / English):", word_list)

    if selected_word_option:
        # Extract Bashkir word from selection
        selected_word = selected_word_option.split(' (')[0]

        # Show word information
        word_info = next((w for w in words_data if w['bashkir'] == selected_word), None)
        if word_info:
            # Main word card with Bashkir and English
            st.markdown(f"""
            <div class='word-card'>
                <span class='bashkir-text'>{word_info['bashkir']} (Башҡорт теле)</span>
                <span class='english-text'>{word_info['english']} (English)</span>
                {f"<span class='ipa-text'>{word_info.get('ipa', '')}</span>" if word_info.get('ipa') else ''}
                {f"<span class='russian-text'>Russian: {word_info.get('russian', '')}</span>" if word_info.get('russian') else ''}
            </div>
            """, unsafe_allow_html=True)

            # Audio playback
            if st.button("🔊 Play Pronunciation", key="bashkortnet_audio"):
                play_audio(word_info['bashkir'], language='ru', slow=True)

            # Create tabs for different aspects
            tab1, tab2, tab3 = st.tabs(["🕸️ Semantic Network", "📚 OCM Cultural Codes", "🔗 Etymology & Context"])

            with tab1:
                st.subheader("Semantic Network (Семантик сеть)")
                # Show relations with Bashkir and English labels
                relations = net.get_relations(selected_word)
                if relations:
                    for rel_type, targets in relations.items():
                        rel_label = net.RELATION_TYPES.get(rel_type, rel_type)
                        st.markdown(f"**{rel_label}**")
                        for target in targets:
                            if isinstance(target, dict):
                                target_word = target.get('target', '')
                                gloss = target.get('gloss', '')
                                relation = target.get('relation', '')
                                if gloss:
                                    st.write(f"  • {target_word} ({gloss})")
                                else:
                                    st.write(f"  • {target_word}")
                                if relation:
                                    st.caption(f"    ↳ {relation}")
                            else:
                                st.write(f"  • {target}")
                else:
                    st.info("No semantic relations found for this word.")

                # Show word family
                family = net.get_word_family(selected_word)
                if family:
                    st.subheader("Word Family (Һүҙ ғаиләһе)")
                    for category, words in family.items():
                        if words:
                            st.write(f"**{category.replace('_', ' ').title()}:** {', '.join(words)}")

            with tab2:
                st.subheader("OCM Cultural Classification (eHRAF 2021 Standards)")
                st.markdown("*Outline of Cultural Materials codes for anthropological analysis*")

                # Get OCM codes for this word
                word_ocm_codes = bashkir_to_ocm.get(word_info['bashkir'], [])

                # Also check cultural_context in word data
                cultural_context = word_info.get('cultural_context', {})
                embedded_ocm_codes = cultural_context.get('ocm_codes', [])

                # Combine all OCM codes
                all_ocm_codes = list(set(word_ocm_codes + embedded_ocm_codes))

                if all_ocm_codes:
                    st.markdown("**Associated OCM Categories:**")
                    for code in all_ocm_codes:
                        label = ocm_labels.get(str(code), f"Code {code}")
                        st.markdown(f"""
                        <div class='stat-box' style='margin: 5px 0; text-align: left;'>
                            <strong>OCM {code}</strong>: {label}
                        </div>
                        """, unsafe_allow_html=True)

                    # Show thematic groups
                    thematic_groups = ocm_data.get('thematic_groups', {})
                    related_themes = []
                    for theme_name, theme_data in thematic_groups.items():
                        if word_info['bashkir'] in theme_data.get('words', []):
                            related_themes.append(theme_name)

                    if related_themes:
                        st.markdown("**Thematic Groups:**")
                        for theme in related_themes:
                            st.write(f"  • {theme.replace('_', ' ').title()}")
                else:
                    st.info("No OCM codes assigned to this word yet.")

                # Show cultural significance
                if cultural_context.get('significance'):
                    st.markdown("**Cultural Significance:**")
                    st.markdown(f"_{cultural_context['significance']}_")

                if cultural_context.get('sources'):
                    st.markdown("**Sources:**")
                    for source in cultural_context['sources']:
                        st.write(f"  • {source}")

            with tab3:
                st.subheader("Etymology & Additional Context")

                # Show etymology from bashkortnet data
                bashkortnet_data = word_info.get('bashkortnet', {})
                etymology = bashkortnet_data.get('etymology', {})

                if etymology:
                    st.markdown("**Etymology (Этимология):**")
                    if etymology.get('proto_form'):
                        st.write(f"  Proto-form: {etymology['proto_form']}")
                    if etymology.get('note'):
                        st.write(f"  Note: {etymology['note']}")

                # Memory palace info
                memory_palace = word_info.get('memory_palace', {})
                if memory_palace:
                    st.markdown("**Memory Palace Location:**")
                    bird = memory_palace.get('bird', '')
                    locus = memory_palace.get('locus', '')
                    st.write(f"  🐦 Bird: {bird}")
                    st.write(f"  📍 Locus: {locus}")
                    if memory_palace.get('mnemonic'):
                        st.markdown("**Mnemonic:**")
                        st.markdown(f"_{memory_palace['mnemonic']}_")

                # Grammar information
                grammar = word_info.get('grammar', {})
                if grammar and grammar.get('case_forms'):
                    st.markdown("**Case Forms (Килеш формалары):**")
                    case_forms = grammar['case_forms']
                    case_names = {
                        'nominative': 'Nominative (Баш килеш)',
                        'genitive': 'Genitive (Эйәлек килеш)',
                        'dative': 'Dative (Төбәү килеш)',
                        'accusative': 'Accusative (Төшөм килеш)',
                        'locative': 'Locative (Урын-ваҡыт килеш)',
                        'ablative': 'Ablative (Сығанаҡ килеш)'
                    }
                    for case_key, case_value in case_forms.items():
                        case_label = case_names.get(case_key, case_key)
                        st.write(f"  • {case_label}: **{case_value}**")

def render_cultural_context_view():
    """Render the cultural context view with full OCM integration."""
    st.title("📖 Cultural Context")
    st.markdown("*Anthropological depth and eHRAF 2021 OCM classifications*")

    st.markdown("""
    <div class="meditation-box">
    Bashkir culture is deeply rooted in the traditions of the Ural Mountains region.
    The language reflects centuries of nomadic heritage, Islamic influence, and close connection to nature.
    <br><br>
    This section uses the <strong>Outline of Cultural Materials (OCM)</strong> classification system
    from the <strong>eHRAF World Cultures</strong> database (2021 standards) for anthropological analysis.
    </div>
    """, unsafe_allow_html=True)

    # Load data
    words_data = load_words()
    ocm_data = load_ocm_mapping()
    ocm_labels = ocm_data.get('ocm_labels', {})
    ocm_categories = ocm_data.get('ocm_categories', {})
    bashkir_to_ocm = ocm_data.get('bashkir_to_ocm', {})
    thematic_groups = ocm_data.get('thematic_groups', {})

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["🔍 Browse by Word", "📊 Browse by OCM Category", "🎨 Thematic Groups"])

    with tab1:
        st.subheader("Browse Cultural Context by Word")

        # Search/filter
        search_term = st.text_input("Search words (Bashkir or English):", key="cultural_search")

        # Filter words
        if search_term:
            filtered_words = [w for w in words_data if search_term.lower() in w['bashkir'].lower() or search_term.lower() in w['english'].lower()]
        else:
            filtered_words = words_data[:20]  # Show first 20 by default

        st.write(f"Showing {len(filtered_words)} words")

        for word in filtered_words:
            cultural = word.get('cultural_context', {})

            with st.expander(f"📖 {word['bashkir']} ({word['english']})"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    # Basic info
                    st.markdown(f"**Bashkir:** {word['bashkir']}")
                    st.markdown(f"**English:** {word['english']}")
                    if word.get('ipa'):
                        st.markdown(f"**IPA:** {word['ipa']}")
                    if word.get('russian'):
                        st.markdown(f"**Russian:** {word['russian']}")

                    # Cultural significance
                    if cultural.get('significance'):
                        st.markdown("---")
                        st.markdown("**Cultural Significance:**")
                        st.markdown(f"_{cultural['significance']}_")

                    if cultural.get('usage_context'):
                        st.markdown("**Usage Context:**")
                        st.markdown(f"_{cultural['usage_context']}_")

                    if cultural.get('sources'):
                        st.markdown("**Sources:**")
                        for source in cultural['sources']:
                            st.write(f"  • {source}")

                with col2:
                    # OCM codes
                    st.markdown("**OCM Classifications:**")

                    # Get OCM codes from multiple sources
                    word_ocm_codes = bashkir_to_ocm.get(word['bashkir'], [])
                    embedded_ocm_codes = cultural.get('ocm_codes', [])
                    all_codes = list(set([str(c) for c in word_ocm_codes + embedded_ocm_codes]))

                    if all_codes:
                        for code in all_codes:
                            label = ocm_labels.get(str(code), f"Code {code}")
                            st.markdown(f"• **{code}**: {label}")
                    else:
                        st.info("No OCM codes assigned")

                    # Memory palace info
                    mp = word.get('memory_palace', {})
                    if mp:
                        st.markdown("---")
                        st.markdown("**Memory Palace:**")
                        st.write(f"🐦 {mp.get('bird', 'N/A')}")
                        st.write(f"📍 {mp.get('locus', 'N/A')}")

                # Audio button
                if st.button(f"🔊 Listen", key=f"cultural_audio_{word['bashkir']}"):
                    play_audio(word['bashkir'], language='ru', slow=True)

    with tab2:
        st.subheader("Browse by OCM Category")
        st.markdown("*Explore words organized by anthropological classification*")

        # Create a list of main categories
        category_options = [(code, f"{code}: {data['name']}") for code, data in ocm_categories.items()]
        selected_category = st.selectbox("Select OCM Category:", [opt[1] for opt in category_options])

        if selected_category:
            # Extract category code
            cat_code = selected_category.split(':')[0].strip()
            cat_data = ocm_categories.get(cat_code, {})

            st.markdown(f"### {cat_data.get('name', cat_code)}")

            # Show subcategories
            subcategories = cat_data.get('subcategories', {})
            if subcategories:
                for sub_code, sub_data in subcategories.items():
                    sub_name = sub_data.get('name', sub_code)
                    bashkir_words = sub_data.get('bashkir_words', [])

                    if bashkir_words:
                        st.markdown(f"**{sub_code}: {sub_name}**")
                        word_displays = []
                        for bword in bashkir_words:
                            # Find English translation
                            word_info = next((w for w in words_data if w['bashkir'] == bword), None)
                            if word_info:
                                word_displays.append(f"{bword} ({word_info['english']})")
                            else:
                                word_displays.append(bword)
                        st.write("  • " + ", ".join(word_displays))

    with tab3:
        st.subheader("Thematic Groups")
        st.markdown("*Words organized by cultural and linguistic themes*")

        for theme_name, theme_data in thematic_groups.items():
            display_name = theme_name.replace('_', ' ').title()
            ocm_codes = theme_data.get('ocm_codes', [])
            theme_words = theme_data.get('words', [])

            with st.expander(f"🎨 {display_name}"):
                st.markdown("**OCM Codes:**")
                code_labels = [f"{c}: {ocm_labels.get(c, 'Unknown')}" for c in ocm_codes]
                st.write(", ".join(code_labels))

                st.markdown("**Words:**")
                word_displays = []
                for bword in theme_words:
                    word_info = next((w for w in words_data if w['bashkir'] == bword), None)
                    if word_info:
                        word_displays.append(f"**{bword}** ({word_info['english']})")
                    else:
                        word_displays.append(f"**{bword}**")

                st.markdown(" | ".join(word_displays))

def render_settings_view():
    """Render the settings view."""
    st.title("⚙️ Settings")
    
    st.subheader("Audio Settings")
    audio_slow = st.checkbox("Slow Audio Playback", value=True)
    audio_language = st.selectbox("Audio Language", ["ru", "en"], format_func=lambda x: {"ru": "Russian (Bashkir Approximation)", "en": "English"}[x])
    
    st.subheader("Display Settings")
    show_ipa = st.checkbox("Show IPA Transcriptions", value=True)
    show_russian = st.checkbox("Show Russian Translations", value=True)
    
    st.subheader("Learning Settings")
    srs_enabled = st.checkbox("Enable Spaced Repetition", value=True)
    show_mnemonics = st.checkbox("Show Mnemonics", value=True)

def render_audio_dictionary_view():
    """Render the audio dictionary view with enhanced features."""
    st.title("🔊 Enhanced Audio Dictionary")
    
    # Initialize audio service if not exists
    if 'audio_service' not in st.session_state:
        st.session_state.audio_service = get_audio_service()
    
    audio_service = st.session_state.audio_service
    
    # Word lookup
    words_data = load_words()
    word_list = [w['bashkir'] for w in words_data]
    
    # Search functionality
    search_term = st.text_input("Search for a word:", "")
    
    # Filter words based on search
    if search_term:
        filtered_words = [w for w in words_data if search_term.lower() in w['bashkir'].lower() or search_term.lower() in w['english'].lower()]
    else:
        filtered_words = words_data
    
    # Display results
    if filtered_words:
        selected_word = st.selectbox("Select a word:", [w['bashkir'] for w in filtered_words])
        
        # Find the selected word data
        word_info = next((w for w in words_data if w['bashkir'] == selected_word), None)
        
        if word_info:
            st.markdown(f"""
            <div class="word-card">
                <span class="bashkir-text">{word_info['bashkir']}</span>
                <span class="english-text">{word_info['english']}</span>
                {f'<span class="ipa-text">{word_info.get("ipa", "")}</span>' if word_info.get('ipa') else ''}
                {f'<span class="russian-text">{word_info.get("russian", "")}</span>' if word_info.get('russian') else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # Audio generation and playback
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔊 Play Word Audio"):
                    play_audio(word_info['bashkir'], language='ru', slow=True)
            
            with col2:
                if st.button("🔊 Play Slow Audio"):
                    play_audio(word_info['bashkir'], language='ru', slow=True)
            
            with col3:
                if st.button("🔊 Regenerate Audio"):
                    audio_service.generate_word_audio(word_info['bashkir'], slow=True)
                    play_audio(word_info['bashkir'], language='ru', slow=True)
            
            # Show additional info
            if 'definitions' in word_info:
                st.subheader("Definitions")
                for i, definition in enumerate(word_info['definitions']):
                    st.write(f"{i+1}. {definition.get('en', definition.get('english', ''))}")
            
            if 'examples' in word_info:
                st.subheader("Examples")
                for example in word_info['examples']:
                    st.write(f"**EN:** {example.get('en', '')}")
                    st.write(f"**BA:** {example.get('ba', example.get('bashkir', ''))}")
                    st.write("")
            
            # Translation functionality
            st.subheader("Translation")
            source_text = st.text_area("Enter text to translate:", value=word_info['bashkir'])
            
            if st.button("Translate"):
                translated = translate_text(source_text, source='auto', target='en')
                st.write(f"**Translated:** {translated}")
            
            # Advanced features
            st.subheader("Advanced Features")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Tokenize Text"):
                    tokens = tokenize_text(source_text)
                    st.write(f"**Tokens:** {tokens}")
            
            with col2:
                if st.button("Show Audio Cache Stats"):
                    stats = audio_service.get_cache_stats()
                    st.json(stats)
    
    # Add new word functionality
    st.subheader("Add New Word")
    with st.form("add_word_form"):
        new_bashkir = st.text_input("Bashkir Word")
        new_english = st.text_input("English Translation")
        new_russian = st.text_input("Russian Translation (optional)")
        new_ipa = st.text_input("IPA Transcription (optional)")
        
        submitted = st.form_submit_button("Add Word")
        if submitted and new_bashkir and new_english:
            # Create new word entry
            new_word_entry = {
                'bashkir': new_bashkir,
                'english': new_english,
                'russian': new_russian if new_russian else '',
                'ipa': new_ipa if new_ipa else '',
                'id': f"custom_{len(words_data)+1}",
                'pos': 'noun',  # Default part of speech
                'memory_palace': {
                    'bird': 'Ringdove',
                    'locus': 'Bizhbulyak'
                },
                'definitions': [{'en': new_english}],
                'examples': []
            }
            
            # Add to words data (in memory for this session)
            words_data.append(new_word_entry)
            st.success(f"Added new word: {new_bashkir}")

# --- Page Routing ---
if st.session_state.current_page == "🗺️ Palace":
    render_palace_view()
elif st.session_state.current_page == "📚 Four Birds":
    render_four_birds_view()
elif st.session_state.current_page == "✍️ Sentence Builder":
    render_sentence_builder_view()
elif st.session_state.current_page == "🔊 Audio Dictionary":
    render_audio_dictionary_view()
elif st.session_state.current_page == "🔄 Review":
    render_review_view()
elif st.session_state.current_page == "🕸️ BashkortNet Explorer":
    render_bashkortnet_view()
elif st.session_state.current_page == "📖 Cultural Context":
    render_cultural_context_view()
elif st.session_state.current_page == "⚙️ Settings":
    render_settings_view()

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #0066B3;'>🏰 Bashkir Memory Palace - Enhanced Edition 🏰</p>", unsafe_allow_html=True)
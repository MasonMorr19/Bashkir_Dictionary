#!/usr/bin/env python3
"""
Bilingual Audio Dictionary Application
English-Bashkir Dictionary with Text-to-Speech and Translation Features
"""

import os
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Callable, Any
import asyncio
from pathlib import Path
import sys

# Add parent directory to path to import shared utilities
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.retry import RetryConfig
    RETRY_AVAILABLE = True
except ImportError:
    RETRY_AVAILABLE = False
    # Fallback RetryConfig
    class RetryConfig:
        def __init__(self, max_retries=4, base_delay=2.0, exponential_base=2.0):
            self.max_retries = max_retries
            self.base_delay = base_delay
            self.exponential_base = exponential_base

# Import required libraries for audio processing (with graceful fallback)
libraries_loaded = {}

try:
    from gtts import gTTS
    libraries_loaded['gtts'] = True
except ImportError:
    libraries_loaded['gtts'] = False
    print("Warning: gTTS not available")

try:
    from pydub import AudioSegment
    libraries_loaded['pydub'] = True
except ImportError:
    libraries_loaded['pydub'] = False
    print("Warning: pydub not available")

try:
    import librosa
    libraries_loaded['librosa'] = True
except ImportError:
    libraries_loaded['librosa'] = False
    print("Warning: librosa not available")

try:
    import soundfile as sf
    libraries_loaded['soundfile'] = True
except ImportError:
    libraries_loaded['soundfile'] = False
    print("Warning: soundfile not available")

try:
    import whisper
    libraries_loaded['whisper'] = True
except ImportError:
    libraries_loaded['whisper'] = False
    print("Warning: whisper not available")

try:
    from deep_translator import GoogleTranslator
    libraries_loaded['deep_translator'] = True
except ImportError:
    libraries_loaded['deep_translator'] = False
    print("Warning: deep_translator not available")

try:
    import torch
    libraries_loaded['torch'] = True
except ImportError:
    libraries_loaded['torch'] = False
    print("Warning: torch not available")

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    libraries_loaded['transformers'] = True
except ImportError:
    libraries_loaded['transformers'] = False
    print("Warning: transformers not available")

# Check if essential libraries are available
essential_libs = ['gtts', 'deep_translator']
missing_essentials = [lib for lib in essential_libs if not libraries_loaded[lib]]
if missing_essentials:
    print(f"Error: Missing essential libraries: {missing_essentials}")
    print("Please install required packages: pip install flask flask-cors gTTS pydub deep-translator torch transformers librosa openai-whisper soundfile")
    exit(1)


class BilingualAudioDictionary:
    """
    A bilingual dictionary system supporting English-Bashkir with audio generation,
    translation, and text-to-speech capabilities.
    """
    
    def __init__(self, data_file: Optional[str] = None):
        """
        Initialize the dictionary with optional data file.
        
        Args:
            data_file: Path to dictionary data file (JSON format)
        """
        self.logger = self._setup_logging()
        self.dictionary_data: Dict[str, Dict] = {}
        self.audio_cache: Dict[str, str] = {}  # Cache for generated audio files
        
        # Supported languages
        self.supported_languages = {
            'en': 'english',
            'ba': 'bashkir',  # Using 'ba' as code for Bashkir
            'ru': 'russian'
        }
        
        # Load sample data if no file provided
        if data_file and os.path.exists(data_file):
            self.load_dictionary(data_file)
        else:
            self._load_sample_data()
        
        # Initialize transformer models for advanced NLP tasks
        self.translation_pipeline = None
        self.summarization_pipeline = None
        self.qa_pipeline = None
        
        # Initialize Whisper model for speech recognition
        self.whisper_model = None
        
        self.logger.info("Bilingual Audio Dictionary initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the application."""
        logger = logging.getLogger('BilingualAudioDictionary')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _load_sample_data(self):
        """Load sample dictionary data."""
        self.logger.info("Loading sample dictionary data...")
        
        # Sample English-Bashkir dictionary entries
        sample_data = {
            "hello": {
                "bashkir": "һәләй",
                "transcription": "[hæˈlæj]",
                "pos": "interjection",
                "definitions": [
                    {"en": "Used as a greeting", "ba": "Иҫәнлек итеү өсөн ҡулланыла"},
                    {"en": "To attract attention", "ba": "Иғтибар йүнәлтеү өсөн"}
                ],
                "examples": [
                    {"en": "Hello, how are you?", "ba": "Сәләм, ни хәлдәһеҙ?"},
                    {"en": "He said hello to everyone", "ba": "Ул бөтәнге донъяға һәләй телендә иҫәнлек һаҡлай"}
                ]
            },
            "water": {
                "bashkir": "һыу",
                "transcription": "[hɪˈuː]",
                "pos": "noun",
                "definitions": [
                    {"en": "A clear liquid substance", "ba": "Аныҡ шыр һыулыҡ"},
                    {"en": "Essential for life", "ba": "Тере ҡалыу өсөн кәрәк"}
                ],
                "examples": [
                    {"en": "I need some water", "ba": "Миңә бер аҙ һыу кәрәк"},
                    {"en": "Water is important", "ba": "Һыу мөһим"}
                ]
            },
            "book": {
                "bashkir": "китап",
                "transcription": "[kɪtˈap]",
                "pos": "noun",
                "definitions": [
                    {"en": "A written or printed work", "ba": "Яҙылған йәки бастырылған эш"},
                    {"en": "Pages bound together", "ba": "Берләтеп бәйләнгән биттәр"}
                ],
                "examples": [
                    {"en": "I am reading a book", "ba": "Мин китап уҡыйым"},
                    {"en": "This book is interesting", "ba": "Был китап ҡыҙыҡ"}
                ]
            },
            "house": {
                "bashkir": "йорт",
                "transcription": "[jurt]",
                "pos": "noun",
                "definitions": [
                    {"en": "A building for living", "ba": "Ял итеү өсөн йорт"},
                    {"en": "Family dwelling", "ba": "Ғаилә ялыу урыны"}
                ],
                "examples": [
                    {"en": "My house is big", "ba": "Минең йортом бейек"},
                    {"en": "Welcome to my house", "ba": "Минең йортума рәхим итегеҙ"}
                ]
            },
            "friend": {
                "bashkir": "дуст",
                "transcription": "[dust]",
                "pos": "noun",
                "definitions": [
                    {"en": "A person whom one knows", "ba": "Бер кеше, кемде беләһең"},
                    {"en": "Close companion", "ba": "Яҡын ялдаш"}
                ],
                "examples": [
                    {"en": "She is my friend", "ba": "Ул минең достом"},
                    {"en": "Good friends last forever", "ba": "Яҡшы достар даими ҡала"}
                ]
            }
        }
        
        self.dictionary_data = sample_data
        self.logger.info(f"Loaded {len(sample_data)} sample entries")
    
    def load_dictionary(self, file_path: str):
        """
        Load dictionary data from a JSON file.
        
        Args:
            file_path: Path to the JSON dictionary file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.dictionary_data = json.load(f)
            self.logger.info(f"Loaded dictionary from {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading dictionary: {e}")
            self._load_sample_data()  # Fallback to sample data
    
    def save_dictionary(self, file_path: str):
        """
        Save dictionary data to a JSON file.
        
        Args:
            file_path: Path to save the dictionary file
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.dictionary_data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Dictionary saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving dictionary: {e}")
    
    def get_word_info(self, word: str, target_lang: str = 'ba') -> Optional[Dict]:
        """
        Get information about a word.
        
        Args:
            word: The word to look up
            target_lang: Target language ('ba' for Bashkir, 'en' for English)
            
        Returns:
            Dictionary entry or None if not found
        """
        word_lower = word.lower()
        
        # Check if exact match exists
        if word_lower in self.dictionary_data:
            return self.dictionary_data[word_lower]
        
        # Try to find case-insensitive match
        for key, value in self.dictionary_data.items():
            if key.lower() == word_lower:
                return value
        
        # If not found, return None
        return None
    
    def search_words(self, query: str) -> List[str]:
        """
        Search for words containing the query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching words
        """
        query_lower = query.lower()
        matches = []
        
        for word in self.dictionary_data.keys():
            if query_lower in word.lower():
                matches.append(word)
        
        return matches
    
    def generate_audio(self, text: str, language: str = 'en', filename: Optional[str] = None) -> str:
        """
        Generate audio file from text using gTTS with retry logic.

        Uses exponential backoff: 2s, 4s, 8s, 16s delays between retries.

        Args:
            text: Text to convert to speech
            language: Language code ('en', 'ba', 'ru')
            filename: Optional filename for the output audio file

        Returns:
            Path to the generated audio file
        """
        # Check if gTTS is available
        if not libraries_loaded.get('gtts', False):
            self.logger.warning("gTTS library not available, returning empty string")
            return ""

        # Validate language
        lang_code = language.lower()
        if lang_code not in self.supported_languages:
            lang_code = 'en'  # Default to English

        # Create audio directory if it doesn't exist
        audio_dir = Path("audio")
        audio_dir.mkdir(exist_ok=True)

        # Generate filename if not provided
        if not filename:
            # Create safe filename from text
            safe_text = "".join(c for c in text if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_text[:30]}_{lang_code}.mp3".replace(' ', '_')
            filename = str(audio_dir / filename)
        elif not filename.endswith('.mp3'):
            filename += '.mp3'

        # Check cache first
        cache_key = f"{text}_{lang_code}"
        if cache_key in self.audio_cache:
            self.logger.info(f"Using cached audio for: {text}")
            return self.audio_cache[cache_key]

        # Use retry logic for network call
        result = self._generate_audio_with_retry(text, lang_code, filename)
        if result:
            self.audio_cache[cache_key] = result
        return result

    def _generate_audio_with_retry(self, text: str, lang_code: str, filename: str) -> str:
        """
        Internal method to generate audio with retry logic.

        Uses exponential backoff: 2s, 4s, 8s, 16s delays between retries.
        """
        config = RetryConfig(
            max_retries=4,
            base_delay=2.0,
            exponential_base=2.0,
        )

        for attempt in range(config.max_retries + 1):
            try:
                tts = gTTS(text=text, lang=lang_code, slow=False)
                tts.save(filename)
                self.logger.info(f"Generated audio file: {filename}")
                return filename

            except Exception as e:
                if attempt >= config.max_retries:
                    self.logger.error(
                        f"Failed to generate audio after {config.max_retries + 1} attempts: {e}"
                    )
                    return ""

                delay = config.base_delay * (config.exponential_base ** attempt)
                self.logger.warning(
                    f"Audio generation attempt {attempt + 1}/{config.max_retries + 1} failed for "
                    f"'{text[:20]}...': {e}. Retrying in {delay:.1f}s..."
                )
                time.sleep(delay)

        return ""
    
    def generate_bashkir_audio(self, text: str, filename: Optional[str] = None) -> str:
        """
        Generate audio specifically for Bashkir text.
        
        Args:
            text: Bashkir text to convert to speech
            filename: Optional filename for the output audio file
            
        Returns:
            Path to the generated audio file
        """
        # Since gTTS doesn't support Bashkir natively, we'll use Russian voice as approximation
        # In a real implementation, you'd need a native Bashkir TTS system
        return self.generate_audio(text, language='ru', filename=filename)
    
    def translate_text(self, text: str, source_lang: str = 'en', target_lang: str = 'ba') -> str:
        """
        Translate text between languages using Google Translator with retry logic.

        Uses exponential backoff: 2s, 4s, 8s, 16s delays between retries.

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translated text
        """
        # Check if deep_translator is available
        if not libraries_loaded.get('deep_translator', False):
            self.logger.warning("deep_translator library not available, returning original text")
            return text

        if source_lang == target_lang:
            return text

        # Determine effective target language
        # For Bashkir, we'll use Russian as intermediate since Google Translate
        # might not directly support English-Bashkir translation
        effective_target = 'ru' if target_lang == 'ba' else target_lang

        return self._translate_with_retry(text, source_lang, effective_target)

    def _translate_with_retry(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Internal method to translate with retry logic.

        Uses exponential backoff: 2s, 4s, 8s, 16s delays between retries.
        """
        config = RetryConfig(
            max_retries=4,
            base_delay=2.0,
            exponential_base=2.0,
        )

        for attempt in range(config.max_retries + 1):
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                translated = translator.translate(text)
                return translated

            except Exception as e:
                if attempt >= config.max_retries:
                    self.logger.error(
                        f"Translation failed after {config.max_retries + 1} attempts: {e}"
                    )
                    return text  # Return original text if translation fails

                delay = config.base_delay * (config.exponential_base ** attempt)
                self.logger.warning(
                    f"Translation attempt {attempt + 1}/{config.max_retries + 1} failed: {e}. "
                    f"Retrying in {delay:.1f}s..."
                )
                time.sleep(delay)

        return text
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text using transformer tokenizer.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        try:
            # Check if transformers is available
            if not libraries_loaded.get('transformers', False):
                self.logger.warning("Transformers library not available, using simple split")
                # Simple fallback tokenization
                return text.split()
            
            # Use a general-purpose tokenizer
            if not hasattr(self, 'tokenizer'):
                self.tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
            
            tokens = self.tokenizer.tokenize(text)
            return tokens
        except Exception as e:
            self.logger.error(f"Tokenization error: {e}")
            # Simple fallback tokenization
            return text.split()
    
    def analyze_audio(self, audio_path: str) -> Dict:
        """
        Analyze audio file properties.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with audio analysis results
        """
        try:
            # Check if librosa is available
            if not libraries_loaded.get('librosa', False):
                self.logger.warning("Librosa library not available, returning empty analysis")
                return {}
            
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
            self.logger.error(f"Audio analysis error: {e}")
            return {}
    
    def transcribe_speech(self, audio_path: str) -> str:
        """
        Transcribe speech from audio file using Whisper.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            # Check if whisper is available
            if not libraries_loaded.get('whisper', False):
                self.logger.warning("Whisper library not available, returning empty string")
                return ""
            
            # Initialize Whisper model if not already loaded
            if self.whisper_model is None:
                self.logger.info("Loading Whisper model...")
                self.whisper_model = whisper.load_model("base")
            
            # Transcribe audio
            result = self.whisper_model.transcribe(audio_path)
            return result['text']
        except Exception as e:
            self.logger.error(f"Speech transcription error: {e}")
            return ""
    
    def get_all_words(self) -> List[str]:
        """
        Get list of all words in the dictionary.
        
        Returns:
            List of all words
        """
        return list(self.dictionary_data.keys())
    
    def add_word(self, word: str, definition: Dict) -> bool:
        """
        Add a new word to the dictionary.
        
        Args:
            word: The word to add
            definition: Dictionary containing the definition details
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.dictionary_data[word.lower()] = definition
            self.logger.info(f"Added word: {word}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding word: {e}")
            return False
    
    def update_word(self, word: str, definition: Dict) -> bool:
        """
        Update an existing word in the dictionary.
        
        Args:
            word: The word to update
            definition: Updated dictionary definition
            
        Returns:
            True if successful, False otherwise
        """
        if word.lower() in self.dictionary_data:
            try:
                self.dictionary_data[word.lower()] = definition
                self.logger.info(f"Updated word: {word}")
                return True
            except Exception as e:
                self.logger.error(f"Error updating word: {e}")
                return False
        else:
            self.logger.warning(f"Word not found: {word}")
            return False
    
    def delete_word(self, word: str) -> bool:
        """
        Delete a word from the dictionary.
        
        Args:
            word: The word to delete
            
        Returns:
            True if successful, False otherwise
        """
        if word.lower() in self.dictionary_data:
            try:
                del self.dictionary_data[word.lower()]
                self.logger.info(f"Deleted word: {word}")
                return True
            except Exception as e:
                self.logger.error(f"Error deleting word: {e}")
                return False
        else:
            self.logger.warning(f"Word not found: {word}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the dictionary.
        
        Returns:
            Dictionary with statistics
        """
        total_entries = len(self.dictionary_data)
        pos_counts = {}
        
        for word, info in self.dictionary_data.items():
            pos = info.get('pos', 'unknown')
            pos_counts[pos] = pos_counts.get(pos, 0) + 1
        
        stats = {
            "total_entries": total_entries,
            "parts_of_speech": pos_counts,
            "languages_supported": list(self.supported_languages.keys()),
            "audio_cache_size": len(self.audio_cache)
        }

        return stats

    # ===== SM-2 SPACED REPETITION ALGORITHM =====
    # Ported from Bashkir Memory Palace

    def init_srs_data(self) -> None:
        """Initialize spaced repetition data structure."""
        if not hasattr(self, 'srs_data'):
            self.srs_data = {}

    def get_srs_status(self, word: str) -> Dict:
        """
        Get the spaced repetition status for a word.

        Returns:
            Dict with ease, interval, reps, and next_review
        """
        self.init_srs_data()
        return self.srs_data.get(word, {
            'ease': 2.5,
            'interval': 0,
            'reps': 0,
            'next_review': None
        })

    def update_srs(self, word: str, quality: int) -> Dict:
        """
        Update spaced repetition data for a word using SM-2 algorithm.

        Args:
            word: The word being reviewed
            quality: Rating from 0-5 (0=complete blackout, 5=perfect response)

        Returns:
            Updated SRS data for the word
        """
        self.init_srs_data()

        if word not in self.srs_data:
            self.srs_data[word] = {
                'ease': 2.5,
                'interval': 0,
                'reps': 0,
                'next_review': None
            }

        srs = self.srs_data[word]

        # SM-2 algorithm
        if quality >= 3:
            # Correct response
            if srs['reps'] == 0:
                srs['interval'] = 1
            elif srs['reps'] == 1:
                srs['interval'] = 6
            else:
                srs['interval'] = int(srs['interval'] * srs['ease'])
            srs['reps'] += 1
        else:
            # Incorrect response - reset
            srs['interval'] = 1
            srs['reps'] = 0

        # Update ease factor
        srs['ease'] = max(1.3, srs['ease'] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        # Calculate next review date
        from datetime import timedelta
        srs['next_review'] = (datetime.now() + timedelta(days=srs['interval'])).isoformat()

        self.logger.info(f"Updated SRS for '{word}': interval={srs['interval']}, ease={srs['ease']:.2f}")
        return srs

    def get_words_due_for_review(self) -> List[str]:
        """
        Get list of words due for review today.

        Returns:
            List of word strings due for review
        """
        self.init_srs_data()
        now = datetime.now()
        due_words = []

        for word, data in self.srs_data.items():
            next_review = data.get('next_review')
            if next_review:
                review_date = datetime.fromisoformat(next_review)
                if review_date <= now:
                    due_words.append(word)
            else:
                # Never reviewed - due immediately
                due_words.append(word)

        return due_words

    def get_learning_stats(self) -> Dict:
        """
        Get learning statistics from SRS data.

        Returns:
            Dict with learning statistics
        """
        self.init_srs_data()

        total_learned = len(self.srs_data)
        mastered = len([w for w, d in self.srs_data.items() if d.get('interval', 0) >= 21])
        due_today = len(self.get_words_due_for_review())

        return {
            'total_learned': total_learned,
            'mastered': mastered,
            'due_today': due_today,
            'in_progress': total_learned - mastered
        }

    # ===== BASHKORTNET SEMANTIC NETWORK =====
    # Ported from Bashkir Memory Palace

    def add_semantic_relation(self, word: str, relation_type: str, target: str, note: str = "") -> bool:
        """
        Add a semantic relation to a word.

        Args:
            word: The source word
            relation_type: Type of relation (SYN, ANT, ISA, HAS_TYPE, PART_OF, etc.)
            target: The target word or concept
            note: Optional note about the relation

        Returns:
            True if successful
        """
        word_lower = word.lower()
        if word_lower not in self.dictionary_data:
            self.logger.warning(f"Word not found: {word}")
            return False

        if 'bashkortnet' not in self.dictionary_data[word_lower]:
            self.dictionary_data[word_lower]['bashkortnet'] = {'relations': {}, 'etymology': {}}

        relations = self.dictionary_data[word_lower]['bashkortnet']['relations']
        if relation_type not in relations:
            relations[relation_type] = []

        relation_entry = {'target': target}
        if note:
            relation_entry['note'] = note

        relations[relation_type].append(relation_entry)
        self.logger.info(f"Added {relation_type} relation: {word} -> {target}")
        return True

    def get_semantic_relations(self, word: str) -> Dict[str, List]:
        """
        Get all semantic relations for a word.

        Args:
            word: The word to look up

        Returns:
            Dict mapping relation types to lists of targets
        """
        word_lower = word.lower()
        word_data = self.dictionary_data.get(word_lower)
        if not word_data:
            return {}

        bashkortnet = word_data.get('bashkortnet', {})
        return bashkortnet.get('relations', {})

    def find_related_words(self, word: str, relation_types: Optional[List[str]] = None) -> List[str]:
        """
        Find all words related to a given word.

        Args:
            word: The source word
            relation_types: Optional list of relation types to filter by

        Returns:
            List of related words
        """
        relations = self.get_semantic_relations(word)
        related = []

        for rel_type, targets in relations.items():
            if relation_types and rel_type not in relation_types:
                continue

            for target in targets:
                if isinstance(target, dict):
                    related.append(target.get('target', ''))
                else:
                    related.append(target)

        return [r for r in related if r]

    def get_synonyms(self, word: str) -> List[str]:
        """Get synonyms for a word."""
        return self.find_related_words(word, ['SYN'])

    def get_antonyms(self, word: str) -> List[str]:
        """Get antonyms for a word."""
        return self.find_related_words(word, ['ANT'])

    # ===== SENTENCE BUILDER =====
    # Ported from Bashkir Memory Palace

    def build_sentence(self, words: List[str], pattern: str = "SOV") -> Dict:
        """
        Build a sentence from a list of words following Bashkir grammar.

        Args:
            words: List of words (Bashkir or English)
            pattern: Sentence pattern (SOV = Subject-Object-Verb, default for Bashkir)

        Returns:
            Dict with bashkir sentence, gloss, and grammar notes
        """
        sentence_parts = []
        gloss_parts = []

        for word in words:
            word_data = self.get_word_info(word)
            if word_data:
                sentence_parts.append(word_data.get('bashkir', word))
                gloss_parts.append(word_data.get('definitions', [{}])[0].get('en', word))
            else:
                # Word not found - use as-is
                sentence_parts.append(word)
                gloss_parts.append(word)

        return {
            'bashkir': ' '.join(sentence_parts),
            'gloss': ' | '.join(gloss_parts),
            'pattern': pattern,
            'word_count': len(words),
            'grammar_note': self._get_grammar_note(pattern)
        }

    def _get_grammar_note(self, pattern: str) -> str:
        """Get grammar note for a sentence pattern."""
        notes = {
            'SOV': "Bashkir follows Subject-Object-Verb order. The verb comes at the end.",
            'SV': "Simple Subject-Verb pattern. No object.",
            'OV': "Object-Verb pattern (subject implied).",
            'question': "Questions typically add interrogative particles or use rising intonation."
        }
        return notes.get(pattern, "")

    def get_word_with_case(self, word: str, case: str) -> str:
        """
        Apply a grammatical case suffix to a Bashkir word.

        Args:
            word: The Bashkir word
            case: Case name (nominative, dative, accusative, ablative, locative, genitive)

        Returns:
            Word with case suffix applied
        """
        # Bashkir case suffixes (simplified - actual suffixes depend on vowel harmony)
        case_suffixes = {
            'nominative': '',
            'dative': 'ға',      # -ga/-ge (to/for)
            'accusative': 'ны',  # -ny/-ne (direct object)
            'ablative': 'дан',   # -dan/-den (from)
            'locative': 'да',    # -da/-de (at/in)
            'genitive': 'ның',   # -nyng/-neng (of/possessive)
        }

        suffix = case_suffixes.get(case.lower(), '')
        return word + suffix

    def generate_example_sentences(self, word: str, count: int = 3) -> List[Dict]:
        """
        Generate example sentences using a word.

        Args:
            word: The word to use in sentences
            count: Number of sentences to generate

        Returns:
            List of sentence dicts with bashkir, gloss, and english
        """
        word_data = self.get_word_info(word)
        if not word_data:
            return []

        examples = word_data.get('examples', [])[:count]
        result = []

        for ex in examples:
            result.append({
                'bashkir': ex.get('ba', ''),
                'english': ex.get('en', ''),
                'word_highlighted': word
            })

        return result


def main():
    """Main function to demonstrate the dictionary functionality."""
    print("Initializing Bilingual Audio Dictionary...")
    
    # Create dictionary instance
    dictionary = BilingualAudioDictionary()
    
    # Display statistics
    stats = dictionary.get_statistics()
    print(f"\nDictionary Statistics:")
    print(f"- Total entries: {stats['total_entries']}")
    print(f"- Parts of speech: {stats['parts_of_speech']}")
    
    # Demonstrate search functionality
    print(f"\nAll words in dictionary: {dictionary.get_all_words()}")
    
    # Look up a word
    word_to_lookup = "water"
    word_info = dictionary.get_word_info(word_to_lookup)
    
    if word_info:
        print(f"\nDefinition of '{word_to_lookup}':")
        print(f"Bashkir: {word_info['bashkir']}")
        print(f"Transcription: {word_info['transcription']}")
        print(f"Part of speech: {word_info['pos']}")
        
        print("\nDefinitions:")
        for i, def_item in enumerate(word_info['definitions'], 1):
            print(f"  {i}. EN: {def_item['en']}")
            print(f"     BA: {def_item['ba']}")
        
        print("\nExamples:")
        for i, example in enumerate(word_info['examples'], 1):
            print(f"  {i}. EN: {example['en']}")
            print(f"     BA: {example['ba']}")
    
    # Generate audio for the word
    print(f"\nGenerating audio for '{word_to_lookup}'...")
    audio_file = dictionary.generate_audio(word_to_lookup, language='en')
    print(f"Audio file created: {audio_file}")
    
    # Generate audio for Bashkir translation
    ba_translation = word_info['bashkir'] if word_info else "һыу"
    print(f"\nGenerating audio for Bashkir: '{ba_translation}'...")
    ba_audio_file = dictionary.generate_bashkir_audio(ba_translation)
    print(f"Bashkir audio file created: {ba_audio_file}")
    
    # Demonstrate translation
    english_text = "Hello, how are you?"
    translated = dictionary.translate_text(english_text, source_lang='en', target_lang='ru')
    print(f"\nTranslation of '{english_text}': {translated}")
    
    # Demonstrate tokenization
    tokens = dictionary.tokenize_text(english_text)
    print(f"\nTokens for '{english_text}': {tokens}")
    
    print("\nBilingual Audio Dictionary is ready for use!")


if __name__ == "__main__":
    main()
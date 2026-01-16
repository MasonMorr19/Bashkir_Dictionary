# 🛠️ Code Snippets Guide: Customizing Your Bashkir Memory Palace

This guide shows you exactly how to modify the app for your needs.

---

## 🎨 FIX #1: Bashkortostan Flag Colors (Green Text on Blue Background)

**File to edit:** `app.py`  
**Location:** Lines 72-122 (the CSS section)

### Replace the entire CSS block with this:

```python
# --- CSS Styling with Bashkortostan Flag Colors ---
# Flag colors: Blue (#0066B3), White (#FFFFFF), Green (#00AF66)

st.markdown("""
<style>
    /* Main app background - light blue tint */
    .stApp {
        background: linear-gradient(180deg, #e6f2ff 0%, #ffffff 50%, #e6fff0 100%);
    }
    
    /* Bird cards with flag-inspired colors */
    .bird-card {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
        color: #004d00;  /* Dark green text */
    }
    .eagle-card { 
        background: linear-gradient(135deg, #cce5ff 0%, #e6f2ff 100%); 
        border-color: #0066B3; 
    }
    .crow-card { 
        background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%); 
        border-color: #333333; 
    }
    .anqa-card { 
        background: linear-gradient(135deg, #ffe6e6 0%, #fff0f0 100%); 
        border-color: #cc0000; 
    }
    .ringdove-card { 
        background: linear-gradient(135deg, #e6ffe6 0%, #f0fff0 100%); 
        border-color: #00AF66; 
    }
    
    /* Word cards - white background, green text */
    .word-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 102, 179, 0.2);
        margin: 10px 0;
        border: 2px solid #0066B3;
    }
    
    /* MAIN FIX: Bashkir text in GREEN */
    .bashkir-text {
        font-size: 1.8em;
        font-weight: bold;
        color: #00AF66 !important;  /* Bashkortostan green */
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* IPA and translations */
    .word-card small {
        color: #0066B3 !important;  /* Bashkortostan blue */
        font-size: 1em;
    }
    
    .word-card strong {
        color: #004d00;  /* Dark green for English */
        font-size: 1.2em;
    }
    
    /* Meditation boxes */
    .meditation-box {
        background: linear-gradient(135deg, #e6fff0 0%, #ccffe6 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00AF66;
        font-style: italic;
        margin: 15px 0;
        color: #004d00;
    }
    
    /* Stats boxes */
    .stat-box {
        background: linear-gradient(135deg, #e6f2ff 0%, #cce5ff 100%);
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #0066B3;
        color: #004d00;
    }
    
    /* Mnemonic text boxes */
    .mnemonic-text {
        background: linear-gradient(135deg, #fffff0 0%, #ffffd0 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #00AF66;
        color: #004d00;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0066B3 0%, #004080 100%);
    }
    
    /* Headers in green */
    h1, h2, h3 {
        color: #00AF66 !important;
    }
    
    /* Links in blue */
    a {
        color: #0066B3 !important;
    }
</style>
""", unsafe_allow_html=True)
```

---

## 🔧 FIX #2: HTML Not Rendering Properly

The issue is that raw HTML might not display correctly in some Streamlit versions. 
Here's a **hybrid approach** using both native Streamlit AND HTML:

### Replace the word card rendering (around line 223-238) with:

```python
# Create word cards - HYBRID APPROACH
words_at_station = [w for w in words_data if w['bashkir'] in station_words]

cols = st.columns(min(3, len(words_at_station) if words_at_station else 1))
for idx, word in enumerate(words_at_station):
    with cols[idx % 3]:
        is_learned = word['bashkir'] in st.session_state.learned_words
        
        # Use a container with native Streamlit elements
        with st.container():
            # Bashkir word (large, green)
            st.markdown(f"### :green[{word['bashkir']}] {'✅' if is_learned else ''}")
            
            # IPA
            st.caption(f"🔊 {word.get('ipa', '')}")
            
            # English translation
            st.markdown(f"**{word['english']}**")
            
            # Russian
            st.caption(f"🇷🇺 {word.get('russian', '')}")
            
            # Divider
            st.markdown("---")
        
        # Mnemonic in expander
        mnemonic = word.get('memory_palace', {}).get('mnemonic', '')
        if mnemonic:
            with st.expander("💡 Mnemonic"):
                st.info(mnemonic)
        
        # Learn button
        if not is_learned:
            if st.button(f"📖 Learn", key=f"learn_{word['bashkir']}"):
                st.session_state.learned_words.add(word['bashkir'])
                st.session_state.review_queue.append(word['bashkir'])
                st.rerun()
```

### Or keep HTML but ensure rendering with this wrapper function:

```python
def render_word_card(word: dict, is_learned: bool = False) -> None:
    """Render a word card with proper HTML."""
    html = f"""
    <div style="
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #0066B3;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,102,179,0.2);
    ">
        <div style="font-size: 1.8em; font-weight: bold; color: #00AF66;">
            {word['bashkir']} {'✅' if is_learned else ''}
        </div>
        <div style="color: #0066B3; font-size: 0.9em; margin: 5px 0;">
            {word.get('ipa', '')}
        </div>
        <div style="color: #004d00; font-size: 1.2em; font-weight: bold; margin: 5px 0;">
            {word['english']}
        </div>
        <div style="color: #666; font-size: 0.9em;">
            {word.get('russian', '')}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
```

---

## 🔊 FIX #3: gTTS Audio Not Working

The audio service needs to be properly integrated. Here's how to add working audio:

### Add this to the top of `app.py` (after imports):

```python
# Audio imports
import base64
from pathlib import Path

# Try to import gTTS
try:
    from gtts import gTTS
    import tempfile
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    st.sidebar.warning("⚠️ Install gTTS for audio: `pip install gTTS`")

def get_audio_player(text: str) -> None:
    """Generate and display audio player for text."""
    if not AUDIO_AVAILABLE:
        st.caption("🔇 Audio unavailable (install gTTS)")
        return
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts = gTTS(text=text, lang='ru', slow=True)
            tts.save(fp.name)
            
            # Read and display
            with open(fp.name, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            
            st.audio(audio_bytes, format='audio/mp3')
            
            # Clean up
            Path(fp.name).unlink()
    except Exception as e:
        st.caption(f"🔇 Audio error: {e}")
```

### Then use it in word cards:

```python
# In the word card section:
if st.button("🔊 Hear", key=f"audio_{word['bashkir']}"):
    get_audio_player(word['bashkir'])
```

---

## 🏘️ FIX #4: Change Bizhbulyak to Bizhbulyak

**File to edit:** `data/loci.json`

### Find the "Bizhbulyak" section and replace with:

```json
"Bizhbulyak": {
    "id": "locus_bizhbulyak",
    "name": "Bizhbulyak",
    "display_name": "Бижбуляк – Ringdove's Hearth",
    "bird": "Ringdove",
    "symbol": "🕊️",
    "coordinates": [54.5833, 55.4167],
    "description": {
      "short": "Traditional aul preserving language, song, and hospitality.",
      "long": "Bizhbulyak (Бижбуляк) represents the heart of Bashkir village life — where language lives in daily speech, where honey is shared with guests, where the kuray plays at sunset. The Ringdove makes its true home here, among family and tradition. This is where the soul finds rest.",
      "ibn_arabi_connection": "The Ringdove at the hearth embodies the Universal Soul in its most nurturing aspect — the warmth of community, the bonds of family, the preservation of tradition through love. Here, language is not learned but lived."
    },
    "stations": [
      {
        "id": "station_bizhbulyak_1",
        "number": 5,
        "name": "The Village Hearth",
        "display_name": "Village Hearth – Where Language Lives",
        "words": ["бал", "ата", "әсә", "өй", "ҡурай", "ат", "сабантуй", "яҡшы", "бәләкәй", "матур"],
        "opening_meditation": "You enter Bizhbulyak as the sun sets golden over the fields. The Ringdove waits on the windowsill of a wooden house, smoke rising from the chimney. 'Voyager,' it coos, 'I am the soul of home. Every word you learn here tastes of honey and sounds like family.' The door opens. You are welcomed. What will you share?",
        "closing_meditation": "You leave the Village Hearth with honey on your lips and warmth in your heart. Ten words now nestle within you — honey, father, mother, house, kuray, horse, festival, good, small, beautiful. The Ringdove accompanies you to the gate. 'You are no longer a stranger. You carry our words; you are part of our story.' The journey has transformed you.",
        "mnemonic_theme": "family, food, music, hospitality, daily life"
      }
    ],
    "themes": ["family", "honey", "daily life", "hospitality"],
    "ocm_codes": ["593", "594", "222", "342"]
  }
```

### Also update `data/words.json` - change all words with `"locus": "Bizhbulyak"` to `"locus": "Bizhbulyak"`:

```python
# Quick Python script to update words.json:
import json

with open('data/words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

for word in words:
    if word.get('memory_palace', {}).get('locus') == 'Bizhbulyak':
        word['memory_palace']['locus'] = 'Bizhbulyak'

with open('data/words.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)

print("Updated all Bizhbulyak references to Bizhbulyak!")
```

### Update `app.py` - find the locus_display dictionary (around line 165) and change:

```python
locus_display = {
    "Ufa": "🦅 Өфө – Eagle's Perch (Civic)",
    "Shulgan-Tash": "🐦⬛ Шүлгәнташ – Crow's Archive (Ancestry)",
    "Yamantau": "🔥🕊️ Ямантау – Anqa's Ascent (Mystery)",
    "Beloretsk": "🕊️ Белорет – Ringdove's Forge (Labor)",
    "Bizhbulyak": "🕊️ Бижбуляк – Ringdove's Hearth (Home)"  # CHANGED!
}
```

---

## ➕ HOW TO ADD NEW WORDS

This is the most important skill! Here's the template and process:

### Step 1: The Word Entry Template

```json
{
  "id": "word_041",
  "bashkir": "YOUR_BASHKIR_WORD",
  "ipa": "[phonetic_transcription]",
  "pos": "noun|verb|adjective|pronoun|adverb",
  "english": "English translation",
  "russian": "Russian translation",
  "frequency_rank": 100,
  
  "memory_palace": {
    "locus": "Ufa|Shulgan-Tash|Yamantau|Beloretsk|Bizhbulyak",
    "bird": "Eagle|Crow|Anqa|Ringdove",
    "station": 1,
    "mnemonic": "🦅 Your vivid mnemonic story here!"
  },
  
  "bashkortnet": {
    "relations": {
      "SYN": ["synonym1", "synonym2"],
      "ANT": ["antonym1"],
      "ISA": ["category it belongs to"],
      "HAS_TYPE": ["specific types"],
      "PART_OF": ["what it's part of"],
      "HAS_PART": ["its components"],
      "CULT_ASSOC": [
        {"target": "related_concept", "relation": "type_of_relation", "note": "explanation"}
      ],
      "MYTH_LINK": [
        {"target": "mythological_entity", "relation": "connection_type", "note": "from which epic/story"}
      ]
    },
    "etymology": {
      "proto_form": "*proto_word",
      "proto_language": "Proto-Turkic",
      "cognates": [
        {"language": "Turkish", "form": "turkish_word"},
        {"language": "Kazakh", "form": "kazakh_word"}
      ]
    }
  },
  
  "cultural_context": {
    "ocm_codes": ["code1", "code2"],
    "significance": "Why this word matters culturally...",
    "sources": ["Source 1", "Source 2"]
  },
  
  "grammar": {
    "case_forms": {
      "nominative": "base_form",
      "genitive": "base_form + ның/нең",
      "dative": "base_form + ға/гә",
      "accusative": "base_form + ны/не",
      "locative": "base_form + да/дә",
      "ablative": "base_form + дан/дән"
    }
  }
}
```

### Step 2: Choosing the Right Bird/Locus

| If the word is about... | Bird | Locus |
|------------------------|------|-------|
| Government, law, rights, constitution | 🦅 Eagle | Ufa |
| Nature, rivers, ancient things, cosmos | 🐦⬛ Crow | Shulgan-Tash |
| Mountains, danger, transformation, mystery | 🔥🕊️ Anqa | Yamantau |
| Work, craft, industry, tools | 🕊️ Ringdove | Beloretsk |
| Family, food, home, daily life, festivals | 🕊️ Ringdove | Bizhbulyak |

### Step 3: Creating Effective Mnemonics

**Formula:** `SYMBOL + PHONETIC_HOOK + SENSORY_DETAIL + EMOTION + CULTURAL_CONNECTION`

**Example for "ҡымыҙ" (kumys/fermented mare's milk):**

```
"🕊️ 'Koo-MUZZ!' The Ringdove lands on the leather bag! 
Feel the fizz of ҠЫМЫҘ on your tongue — sour, alive, ancient! 
Your grandmother offers you the sacred drink at Сабантуй. 
This is what heroes drink!"
```

**Tips:**
- Use the bird's emoji at the start
- Include a phonetic hook (how it SOUNDS like English)
- Add sensory details (taste, touch, smell, sound, sight)
- Connect to emotion (joy, wonder, fear, warmth)
- Link to cultural context (festivals, stories, places)

### Step 4: Adding to the Station

In `loci.json`, add the word to the station's word list:

```json
"words": ["бал", "ата", "әсә", "өй", "ҡурай", "ат", "сабантуй", "яҡшы", "бәләкәй", "матур", "ҡымыҙ"]
```

---

## 📚 EXAMPLE: Adding 5 New Words

Here are 5 new words ready to paste into `words.json`:

```json
{
  "id": "word_041",
  "bashkir": "ҡымыҙ",
  "ipa": "[qɯmɯð]",
  "pos": "noun",
  "english": "kumys (fermented mare's milk)",
  "russian": "кумыс",
  "frequency_rank": 345,
  "memory_palace": {
    "locus": "Bizhbulyak",
    "bird": "Ringdove",
    "station": 5,
    "mnemonic": "🕊️ 'Koo-MUZZ!' The Ringdove lands on the leather bag! Feel the fizz of ҠЫМЫҘ on your tongue — sour, alive, ancient! Your grandmother offers you the sacred drink at Сабантуй!"
  },
  "bashkortnet": {
    "relations": {
      "ISA": ["эсемлек (drink)", "ашамлыҡ (food)"],
      "MADE_FROM": ["бейә һөтө (mare's milk)"],
      "CULT_ASSOC": [
        {"target": "сабантуй", "relation": "served_at"},
        {"target": "ҡунаҡлыҡ", "gloss": "hospitality", "relation": "symbol_of"}
      ]
    }
  },
  "cultural_context": {
    "ocm_codes": ["222", "273"],
    "significance": "Sacred drink of the nomads; offered to honored guests",
    "sources": ["Rudenko (1955)"]
  },
  "grammar": {
    "case_forms": {
      "nominative": "ҡымыҙ",
      "genitive": "ҡымыҙҙың",
      "dative": "ҡымыҙға",
      "accusative": "ҡымыҙҙы",
      "locative": "ҡымыҙҙа",
      "ablative": "ҡымыҙҙан"
    }
  }
},
{
  "id": "word_042",
  "bashkir": "күк",
  "ipa": "[kyk]",
  "pos": "noun",
  "english": "sky/blue",
  "russian": "небо/синий",
  "frequency_rank": 189,
  "memory_palace": {
    "locus": "Shulgan-Tash",
    "bird": "Crow",
    "station": 2,
    "mnemonic": "🐦⬛ 'KOOK!' The Crow caws at the КҮК above! Blue sky stretches eternal over the cave mouth — the same sky the ancient painters saw 14,000 years ago!"
  },
  "bashkortnet": {
    "relations": {
      "ISA": ["төҫ (color)", "табиғәт (nature)"],
      "ANT": ["ер (earth)"],
      "CULT_ASSOC": [
        {"target": "Тәңре", "gloss": "Tengri", "relation": "dwelling_of", "note": "Sky god of Turkic peoples"}
      ]
    }
  },
  "cultural_context": {
    "ocm_codes": ["821", "773"],
    "significance": "Blue is the color of Tengri (sky god); appears on Bashkortostan flag",
    "sources": ["Turkic mythology"]
  },
  "grammar": {
    "case_forms": {
      "nominative": "күк",
      "genitive": "күктөң",
      "dative": "күккә",
      "accusative": "күктө",
      "locative": "күктә",
      "ablative": "күктән"
    }
  }
},
{
  "id": "word_043",
  "bashkir": "йәшел",
  "ipa": "[jæʃɛl]",
  "pos": "adjective",
  "english": "green",
  "russian": "зелёный",
  "frequency_rank": 234,
  "memory_palace": {
    "locus": "Yamantau",
    "bird": "Anqa",
    "station": 3,
    "mnemonic": "🔥🕊️ 'Ya-SHELL!' The Anqa spreads wings over ЙӘШЕЛ forest! Green covers the mountain slopes — life bursting from every branch, every leaf a prayer!"
  },
  "bashkortnet": {
    "relations": {
      "ISA": ["төҫ (color)"],
      "CULT_ASSOC": [
        {"target": "урман", "relation": "color_of"},
        {"target": "яҙ", "gloss": "spring", "relation": "associated_with"}
      ]
    }
  },
  "cultural_context": {
    "ocm_codes": ["137", "784"],
    "significance": "Green is the color of Islam and appears on Bashkortostan flag",
    "sources": ["Flag symbolism"]
  },
  "grammar": {
    "case_forms": {
      "nominative": "йәшел",
      "genitive": "йәшелдең",
      "dative": "йәшелгә",
      "accusative": "йәшелде",
      "locative": "йәшелдә",
      "ablative": "йәшелдән"
    }
  }
},
{
  "id": "word_044",
  "bashkir": "йондоҙ",
  "ipa": "[jondoð]",
  "pos": "noun",
  "english": "star",
  "russian": "звезда",
  "frequency_rank": 278,
  "memory_palace": {
    "locus": "Shulgan-Tash",
    "bird": "Crow",
    "station": 2,
    "mnemonic": "🐦⬛ 'Yon-DOZ!' The Crow points its wing at the ЙОНДОҘ! Stars pierce the night above the cave — the same constellations that guided nomads across the steppe!"
  },
  "bashkortnet": {
    "relations": {
      "ISA": ["күк йәшмеге (celestial body)"],
      "PART_OF": ["күк (sky)"],
      "CULT_ASSOC": [
        {"target": "Өмөт", "gloss": "hope", "relation": "symbol_of"}
      ]
    }
  },
  "cultural_context": {
    "ocm_codes": ["821"],
    "significance": "Stars used for navigation and appear in Bashkir folk astronomy",
    "sources": ["Folk traditions"]
  },
  "grammar": {
    "case_forms": {
      "nominative": "йондоҙ",
      "genitive": "йондоҙҙоң",
      "dative": "йондоҙға",
      "accusative": "йондоҙҙо",
      "locative": "йондоҙҙа",
      "ablative": "йондоҙҙан"
    }
  }
},
{
  "id": "word_045",
  "bashkir": "дуҫ",
  "ipa": "[dus]",
  "pos": "noun",
  "english": "friend",
  "russian": "друг",
  "frequency_rank": 123,
  "memory_palace": {
    "locus": "Bizhbulyak",
    "bird": "Ringdove",
    "station": 5,
    "mnemonic": "🕊️ 'DOOSE!' The Ringdove brings a ДУҪ to the hearth! Your friend arrives with honey and stories — together you share warmth against the winter cold!"
  },
  "bashkortnet": {
    "relations": {
      "ISA": ["кеше (person)"],
      "ANT": ["дошман (enemy)"],
      "CULT_ASSOC": [
        {"target": "ҡунаҡлыҡ", "relation": "object_of"},
        {"target": "ярҙам", "gloss": "help", "relation": "provides"}
      ]
    }
  },
  "cultural_context": {
    "ocm_codes": ["571"],
    "significance": "Friendship highly valued in Bashkir culture; guests treated as friends",
    "sources": ["Social customs"]
  },
  "grammar": {
    "case_forms": {
      "nominative": "дуҫ",
      "genitive": "дуҫтың",
      "dative": "дуҫҡа",
      "accusative": "дуҫты",
      "locative": "дуҫта",
      "ablative": "дуҫтан"
    }
  }
}
```

---

## 🗺️ GROWING YOUR VOCABULARY: A Roadmap

### Phase 1: Core 100 Words (Current + 60 more)
Focus on:
- Basic nouns (body parts, nature, food)
- Common verbs (come, go, eat, drink, see, hear, speak)
- Numbers 1-10
- Family terms
- Colors
- Time words (today, tomorrow, yesterday)

### Phase 2: Thematic Expansion (200 words)
Add clusters around:
- Epic of Ural-Batyr vocabulary
- Sabantuy festival words
- Traditional crafts
- Animal names (especially horse-related!)
- Weather and seasons

### Phase 3: Conversational (500 words)
- Question words (who, what, where, when, why, how)
- Conjunctions and connectors
- Emotional vocabulary
- More verbs and their conjugations

### Phase 4: Literary/Advanced (1000+ words)
- Abstract concepts
- Poetic vocabulary
- Technical terms
- Regional dialects

---

## 🔧 Quick Reference: File Locations

| What to Edit | File | Purpose |
|--------------|------|---------|
| App appearance, colors | `app.py` (CSS section) | Visual styling |
| Word data | `data/words.json` | Vocabulary entries |
| Locations | `data/loci.json` | Memory palace structure |
| Sentence patterns | `data/patterns.json` | Grammar templates |
| Cultural categories | `data/ocm_mapping.json` | OCM codes |
| Semantic network logic | `modules/bashkortnet.py` | Relationship queries |
| Story generation | `modules/mnemonic_generator.py` | Mnemonic creation |
| Review algorithm | `modules/spaced_repetition.py` | SM-2 scheduling |

---

*Happy voyaging! 🦅🐦⬛🔥🕊️🕊️*

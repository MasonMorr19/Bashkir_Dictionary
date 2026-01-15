# 🏰 Bashkir Memory Palace: Secrets of Voyaging

A language learning application integrating Ibn Arabi's mystical framework, memory palace techniques, and anthropological pedagogy for learning the Bashkir language.

## 🌟 Features

### 🗺️ Memory Palace Navigation
Walk through 5 geographic loci in Bashkortostan, each guided by one of the Four Birds:
- **🦅 Ufa (Eagle)** - Civic knowledge, constitution, rights
- **🐦⬛ Shulgan-Tash (Crow)** - Ancestral memory, nature, cosmos
- **🔥🕊️ Yamantau (Anqa)** - Transformation, danger, potential
- **🕊️ Beloretsk (Ringdove)** - Labor, craft, industry
- **🕊️ Bizhbulyak (Ringdove)** - Family, hospitality, daily life

### 📚 The Four Birds Framework
Based on Ibn Arabi's cosmology from "Secrets of Voyaging":
- **Eagle (al-'Aql al-Awwal)** - First Intellect
- **Crow (al-Jism al-Kulli)** - Universal Body
- **Anqa (al-Hayūlā)** - Prime Matter
- **Ringdove (al-Nafs al-Kulliyya)** - Universal Soul

### ✍️ Sentence Builder
- Construct grammatically correct Bashkir sentences
- Learn SOV word order
- Case suffix guidance
- Save sentences to personal phrasebook

### 🔄 Spaced Repetition (SM-2)
- Optimal review scheduling
- Quality-based interval adjustment
- Progress tracking and statistics

### 🕸️ BashkortNet
Semantic network connecting words through:
- Synonyms & Antonyms
- Taxonomic relations (is-a, has-type)
- Part-whole relationships
- **Cultural associations**
- **Mythological links**

### 📖 Cultural Context
- OCM (Outline of Cultural Materials) coding
- Ethnographic significance
- Academic sources
- "Truth Unveiled" toggle for sensitive contexts

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone or download the project
cd bashkir_memory_palace

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Access
Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
bashkir_memory_palace/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── data/
│   ├── words.json           # Vocabulary with BashkortNet structure
│   ├── loci.json            # Memory palace locations
│   ├── patterns.json        # Sentence patterns & grammar
│   └── ocm_mapping.json     # Cultural category mappings
├── modules/
│   ├── __init__.py
│   ├── bashkortnet.py       # Semantic network
│   ├── mnemonic_generator.py # Story generation
│   ├── spaced_repetition.py # SM-2 algorithm
│   ├── sentence_builder.py  # Grammar & construction
│   └── audio_service.py     # TTS integration
└── audio_cache/             # Generated audio files
```

## 📊 Data Models

### Word Entry Structure
```json
{
  "id": "word_001",
  "bashkir": "бал",
  "ipa": "[bal]",
  "english": "honey",
  "memory_palace": {
    "locus": "Bizhbulyak",
    "bird": "Ringdove",
    "station": 5,
    "mnemonic": "🕊️ 'BAL!' Golden sweetness..."
  },
  "bashkortnet": {
    "relations": {
      "ISA": ["аҙыҡ (food)"],
      "CULT_ASSOC": [{"target": "Бурзян", "relation": "famous_from"}]
    }
  },
  "cultural_context": {
    "ocm_codes": ["222", "225", "231"],
    "significance": "UNESCO-recognized tradition..."
  },
  "grammar": {
    "case_forms": {...}
  }
}
```

## 🎓 Pedagogical Foundations

This application is built on research from:

- **Memory Palace / Method of Loci** - Ancient mnemonic technique
- **Spaced Repetition (SM-2)** - Piotr Wozniak's algorithm
- **Dual Coding Theory** - Allan Paivio
- **Zone of Proximal Development** - Lev Vygotsky
- **Thick Description** - Clifford Geertz
- **Ibn Arabi's Mysticism** - "Secrets of Voyaging"

## 🌍 Cultural Sources

- Rudenko, S.I. (1955). *Bashkiry*
- Kuzeev, R.G. (1974). *Proiskhozhdenie bashkirskogo naroda*
- Baklykov, S. (2023). *Real Russia* documentaries
- Epic of Ural-Batyr
- Constitution of the Republic of Bashkortostan

## 📜 Ibn Arabi's Teaching

> *"The heart heading toward the Real is called the voyager... 
> The journey made within yourself leads to yourself."*
>
> — Ibn Arabi, Secrets of Voyaging

The Four Birds represent aspects of the soul's journey:
- Recognition → Recall → Production → Automaticity
- Separation → Liminality → Incorporation (Van Gennep)

## 🔮 Future Development

- [ ] Native Bashkir TTS voices
- [ ] Neo4j graph database for BashkortNet
- [ ] Mobile application
- [ ] Community contributions
- [ ] Advanced NLP tokenization
- [ ] Anki export

## 📄 License

Educational use. Cultural content respects Bashkir heritage.

## 🙏 Acknowledgments

- Bashkir language activists and educators
- Ibn Arabi and the Sufi tradition
- Memory palace practitioners throughout history
- The people of Bashkortostan

---

*"Voyaging has no end, for therein is the joy of the Real."*

🦅 Eagle · 🐦⬛ Crow · 🔥🕊️ Anqa · 🕊️ Ringdove

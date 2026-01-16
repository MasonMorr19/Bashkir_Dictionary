#!/usr/bin/env python3
"""
Bashkir Memory Palace - Word Addition Tool
==========================================

This tool streamlines the process of adding new words to the Memory Palace.
It ensures all words have consistent structure with:
- IPA transcription (auto-generated)
- Part of speech
- Memory Palace assignment
- Cultural context (OCM codes)
- Evocative mnemonics

Usage:
    python add_word.py                  # Interactive mode
    python add_word.py --batch file.csv # Batch import from CSV

CSV format for batch import:
    bashkir,english,russian,pos,locus,mnemonic_hint
    ҡала,city,город,noun,Ufa,The KALA (castle) rises in the city!
"""

import json
import os
import sys
from pathlib import Path

# Bashkir IPA phoneme mapping
IPA_MAP = {
    'а': 'ɑ', 'ә': 'æ', 'б': 'b', 'в': 'v', 'г': 'g', 'ғ': 'ʁ',
    'д': 'd', 'е': 'e', 'ё': 'jo', 'ж': 'ʒ', 'з': 'z', 'и': 'i',
    'й': 'j', 'к': 'k', 'ҡ': 'q', 'л': 'l', 'м': 'm', 'н': 'n',
    'ң': 'ŋ', 'о': 'o', 'ө': 'ø', 'п': 'p', 'р': 'r', 'с': 's',
    'ҫ': 'θ', 'т': 't', 'у': 'u', 'ү': 'y', 'ф': 'f', 'х': 'x',
    'һ': 'h', 'ц': 'ts', 'ч': 'tʃ', 'ш': 'ʃ', 'щ': 'ʃtʃ', 'ъ': '',
    'ы': 'ɤ', 'ь': '', 'э': 'ɛ', 'ю': 'ju', 'я': 'jɑ'
}

# Locus configurations with their birds and themes
LOCI = {
    'Ufa': {
        'bird': 'Eagle',
        'symbol': '🦅',
        'station': 1,
        'themes': ['civic', 'rights', 'identity', 'law', 'language', 'education']
    },
    'Shulgan-Tash': {
        'bird': 'Crow',
        'symbol': '🐦⬛',
        'station': 2,
        'themes': ['ancestors', 'rivers', 'myth', 'cosmos', 'nature', 'belief']
    },
    'Yamantau': {
        'bird': 'Anqa',
        'symbol': '🔥🕊️',
        'station': 3,
        'themes': ['ecology', 'mountains', 'resilience', 'danger', 'animals', 'weather']
    },
    'Beloretsk': {
        'bird': 'Ringdove',
        'symbol': '🕊️',
        'station': 4,
        'themes': ['craft', 'industry', 'labor', 'transformation', 'metal', 'tools']
    },
    'Bizhbulyak': {
        'bird': 'Ringdove',
        'symbol': '🕊️',
        'station': 5,
        'themes': ['family', 'honey', 'daily life', 'hospitality', 'music', 'food', 'kinship']
    }
}

# OCM code categories for cultural context
OCM_CATEGORIES = {
    'geography': ['131', '132', '133', '134', '135', '136', '137'],
    'language': ['191', '192', '193', '195', '197'],
    'food': ['222', '231', '234', '251', '252', '262', '271', '272', '273'],
    'crafts': ['322', '325', '326', '341', '342', '348'],
    'family': ['591', '592', '593', '594', '601', '602', '618', '619'],
    'arts': ['526', '527', '531', '533', '534', '535', '536', '541'],
    'religion': ['771', '772', '773', '776', '778', '784', '788'],
    'politics': ['619', '641', '642', '648', '668', '669', '671'],
    'education': ['867', '868', '869', '871', '875']
}


def generate_ipa(word: str) -> str:
    """Generate IPA transcription for a Bashkir word."""
    ipa = ''
    for char in word.lower():
        if char in IPA_MAP:
            ipa += IPA_MAP[char]
        elif char == ' ':
            ipa += ' '
        elif char.isalpha():
            ipa += char
    return f'[{ipa}]'


def suggest_locus(pos: str, themes: list = None) -> str:
    """Suggest a locus based on word type and themes."""
    if themes:
        for locus, config in LOCI.items():
            if any(theme in config['themes'] for theme in themes):
                return locus

    # Default suggestions by POS
    defaults = {
        'noun': 'Bizhbulyak',
        'verb': 'Beloretsk',
        'adjective': 'Yamantau',
        'pronoun': 'Ufa'
    }
    return defaults.get(pos, 'Bizhbulyak')


def create_mnemonic_template(bashkir: str, english: str, locus: str) -> str:
    """Create a mnemonic template for the word."""
    config = LOCI[locus]
    return f"{config['symbol']} '{bashkir.upper()}!' [Add evocative imagery connecting {english} to {locus}...]"


def get_next_word_id(words: list) -> str:
    """Get the next available word ID."""
    max_id = 0
    for w in words:
        if w.get('id', '').startswith('word_'):
            try:
                num = int(w['id'].replace('word_', ''))
                max_id = max(max_id, num)
            except ValueError:
                pass
    return f'word_{max_id + 1:03d}'


def load_words():
    """Load the words database."""
    data_path = Path(__file__).parent.parent / 'data' / 'words.json'
    if data_path.exists():
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_words(words: list):
    """Save the words database."""
    data_path = Path(__file__).parent.parent / 'data' / 'words.json'
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)


def update_loci(bashkir: str, locus: str):
    """Add word to the appropriate locus station."""
    loci_path = Path(__file__).parent.parent / 'data' / 'loci.json'
    with open(loci_path, 'r', encoding='utf-8') as f:
        loci = json.load(f)

    if locus in loci and loci[locus].get('stations'):
        station_words = loci[locus]['stations'][0].get('words', [])
        if bashkir not in station_words:
            station_words.append(bashkir)
            loci[locus]['stations'][0]['words'] = station_words

            with open(loci_path, 'w', encoding='utf-8') as f:
                json.dump(loci, f, ensure_ascii=False, indent=2)


def add_word_interactive():
    """Interactive mode for adding a single word."""
    print("\n" + "="*60)
    print("  BASHKIR MEMORY PALACE - Add New Word")
    print("="*60 + "\n")

    words = load_words()
    existing = {w['bashkir'] for w in words}

    # Get basic info
    bashkir = input("Bashkir word (in Cyrillic): ").strip()
    if bashkir in existing:
        print(f"⚠️  '{bashkir}' already exists in the database!")
        return None

    english = input("English meaning: ").strip()
    russian = input("Russian meaning: ").strip()

    # Part of speech
    print("\nPart of speech:")
    print("  1. noun")
    print("  2. verb")
    print("  3. adjective")
    print("  4. pronoun")
    print("  5. other")
    pos_choice = input("Choose (1-5): ").strip()
    pos_map = {'1': 'noun', '2': 'verb', '3': 'adjective', '4': 'pronoun', '5': 'other'}
    pos = pos_map.get(pos_choice, 'noun')

    # Generate IPA
    ipa = generate_ipa(bashkir)
    print(f"\nGenerated IPA: {ipa}")
    custom_ipa = input("Press Enter to accept or type custom IPA: ").strip()
    if custom_ipa:
        ipa = custom_ipa if custom_ipa.startswith('[') else f'[{custom_ipa}]'

    # Suggest and choose locus
    print("\nMemory Palace Locus:")
    for i, (locus, config) in enumerate(LOCI.items(), 1):
        print(f"  {i}. {config['symbol']} {locus} ({config['bird']}) - {', '.join(config['themes'][:3])}")

    suggested = suggest_locus(pos)
    locus_choice = input(f"Choose (1-5) [suggested: {suggested}]: ").strip()
    locus_map = {str(i): name for i, name in enumerate(LOCI.keys(), 1)}
    locus = locus_map.get(locus_choice, suggested)

    # Mnemonic
    print(f"\nCreate a mnemonic for {locus} ({LOCI[locus]['bird']}):")
    print("Tips: Use vivid imagery, puns, sound-alikes, cultural connections")
    mnemonic_template = create_mnemonic_template(bashkir, english, locus)
    print(f"Template: {mnemonic_template}")
    mnemonic = input("Your mnemonic: ").strip()
    if not mnemonic:
        mnemonic = mnemonic_template

    # OCM codes
    print("\nCultural context (OCM codes):")
    for cat, codes in OCM_CATEGORIES.items():
        print(f"  {cat}: {', '.join(codes[:3])}...")
    ocm_input = input("Enter OCM codes (comma-separated) or leave blank: ").strip()
    ocm_codes = [c.strip() for c in ocm_input.split(',')] if ocm_input else []

    # Create word entry
    word_entry = {
        'id': get_next_word_id(words),
        'bashkir': bashkir,
        'ipa': ipa,
        'pos': pos,
        'english': english,
        'russian': russian,
        'memory_palace': {
            'locus': locus,
            'bird': LOCI[locus]['bird'],
            'station': LOCI[locus]['station'],
            'mnemonic': f"{LOCI[locus]['symbol']} {mnemonic}"
        },
        'cultural_context': {
            'ocm_codes': ocm_codes
        }
    }

    # Confirm and save
    print("\n" + "-"*40)
    print("Word entry to add:")
    print(json.dumps(word_entry, ensure_ascii=False, indent=2))
    print("-"*40)

    confirm = input("\nAdd this word? (y/n): ").strip().lower()
    if confirm == 'y':
        words.append(word_entry)
        save_words(words)
        update_loci(bashkir, locus)
        print(f"\n✅ '{bashkir}' added successfully!")
        return word_entry
    else:
        print("❌ Cancelled.")
        return None


def add_words_batch(csv_path: str):
    """Batch import words from CSV file."""
    import csv

    words = load_words()
    existing = {w['bashkir'] for w in words}
    added = 0
    skipped = 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bashkir = row.get('bashkir', '').strip()
            if not bashkir or bashkir in existing:
                skipped += 1
                continue

            locus = row.get('locus', 'Bizhbulyak')
            if locus not in LOCI:
                locus = 'Bizhbulyak'

            word_entry = {
                'id': get_next_word_id(words),
                'bashkir': bashkir,
                'ipa': generate_ipa(bashkir),
                'pos': row.get('pos', 'noun'),
                'english': row.get('english', ''),
                'russian': row.get('russian', ''),
                'memory_palace': {
                    'locus': locus,
                    'bird': LOCI[locus]['bird'],
                    'station': LOCI[locus]['station'],
                    'mnemonic': f"{LOCI[locus]['symbol']} {row.get('mnemonic_hint', '')}"
                },
                'cultural_context': {
                    'ocm_codes': row.get('ocm_codes', '').split(';') if row.get('ocm_codes') else []
                }
            }

            words.append(word_entry)
            existing.add(bashkir)
            update_loci(bashkir, locus)
            added += 1

    save_words(words)
    print(f"\n✅ Batch import complete!")
    print(f"   Added: {added} words")
    print(f"   Skipped: {skipped} (duplicates or invalid)")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--batch' and len(sys.argv) > 2:
            add_words_batch(sys.argv[2])
        elif sys.argv[1] == '--help':
            print(__doc__)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        while True:
            add_word_interactive()
            again = input("\nAdd another word? (y/n): ").strip().lower()
            if again != 'y':
                break
        print("\n👋 Goodbye! Your words await in the Memory Palace.")


if __name__ == '__main__':
    main()

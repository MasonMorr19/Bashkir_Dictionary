#!/usr/bin/env python3
"""
Flask API Server for Bilingual Audio Dictionary
Provides REST API endpoints for the English-Bashkir dictionary application
"""

from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os
from pathlib import Path
import json

# Import our dictionary class
from app import BilingualAudioDictionary

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize the dictionary
dictionary = BilingualAudioDictionary()

@app.route('/')
def index():
    """Serve the main HTML page."""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return "Index file not found", 404

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files like CSS, JS, images."""
    return send_from_directory('static', filename)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dictionary statistics."""
    stats = dictionary.get_statistics()
    return jsonify(stats)

@app.route('/api/search/<query>', methods=['GET'])
def search_words(query):
    """Search for words containing the query string."""
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    results = dictionary.search_words(query)
    return jsonify(results)

@app.route('/api/word/<word>', methods=['GET'])
def get_word(word):
    """Get information about a specific word."""
    if not word:
        return jsonify({"error": "Word parameter is required"}), 400
    
    word_info = dictionary.get_word_info(word)
    if word_info:
        # Add the word itself to the response
        word_info['word'] = word
        return jsonify(word_info)
    else:
        return jsonify({"error": "Word not found"}), 404

@app.route('/api/word', methods=['POST'])
def add_word():
    """Add a new word to the dictionary."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must contain JSON data"}), 400
        
        word = data.get('word')
        if not word:
            return jsonify({"error": "Word field is required"}), 400
        
        # Prepare the definition in the expected format
        definition = {
            'bashkir': data.get('ba', ''),
            'transcription': data.get('transcription', ''),
            'pos': data.get('pos', 'noun'),
            'definitions': [{'en': data.get('definition', ''), 'ba': data.get('ba', '')}],
            'examples': data.get('examples', [])
        }
        
        success = dictionary.add_word(word, definition)
        if success:
            return jsonify({"message": "Word added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add word"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/word/<word>', methods=['PUT'])
def update_word(word):
    """Update an existing word in the dictionary."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must contain JSON data"}), 400
        
        success = dictionary.update_word(word, data)
        if success:
            return jsonify({"message": "Word updated successfully"})
        else:
            return jsonify({"error": "Failed to update word"}), 404
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/word/<word>', methods=['DELETE'])
def delete_word(word):
    """Delete a word from the dictionary."""
    try:
        success = dictionary.delete_word(word)
        if success:
            return jsonify({"message": "Word deleted successfully"})
        else:
            return jsonify({"error": "Failed to delete word"}), 404
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    """Generate audio for the given text."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must contain JSON data"}), 400
        
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({"error": "Text parameter is required"}), 400
        
        # Generate audio file
        if language == 'ba':  # Bashkir
            audio_path = dictionary.generate_bashkir_audio(text)
        else:
            audio_path = dictionary.generate_audio(text, language=language)
        
        if audio_path and os.path.exists(audio_path):
            return send_from_directory(os.path.dirname(audio_path), 
                                     os.path.basename(audio_path), 
                                     as_attachment=True)
        else:
            return jsonify({"error": "Failed to generate audio"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/tokenize', methods=['POST'])
def tokenize_text():
    """Tokenize the provided text."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must contain JSON data"}), 400
        
        text = data.get('text', '')
        if not text:
            return jsonify({"error": "Text parameter is required"}), 400
        
        tokens = dictionary.tokenize_text(text)
        return jsonify({"tokens": tokens})
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text between languages."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must contain JSON data"}), 400
        
        text = data.get('text', '')
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'ba')
        
        if not text:
            return jsonify({"error": "Text parameter is required"}), 400
        
        translated = dictionary.translate_text(text, source_lang, target_lang)
        return jsonify({"original": text, "translated": translated, 
                       "source_lang": source_lang, "target_lang": target_lang})
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/words', methods=['GET'])
def get_all_words():
    """Get list of all words in the dictionary."""
    words = dictionary.get_all_words()
    return jsonify(words)

if __name__ == '__main__':
    print("Starting Bilingual Audio Dictionary API Server...")
    print("Loading dictionary data...")
    
    # Print initial stats
    stats = dictionary.get_statistics()
    print(f"Dictionary loaded with {stats['total_entries']} entries")
    print("Server starting on http://localhost:5000")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
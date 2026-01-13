# Bilingual Audio Dictionary - English & Bashkir

A comprehensive bilingual dictionary application that supports English-Bashkir translations with audio generation, text-to-speech, and advanced NLP features.

## Features

- **Bilingual Dictionary**: English-Bashkir word translations with definitions and examples
- **Audio Generation**: Text-to-speech functionality for both English and Bashkir text
- **Translation**: Cross-language translation capabilities
- **Tokenization**: Advanced text tokenization using transformer models
- **Audio Analysis**: Comprehensive audio file analysis and processing
- **Speech Recognition**: Speech-to-text conversion using Whisper
- **Web Interface**: Modern, responsive web application with search and browse capabilities
- **API Endpoints**: RESTful API for programmatic access to dictionary functions

## Technologies Used

- **Python**: Backend logic and NLP processing
- **JavaScript**: Frontend interactivity and API communication
- **Flask**: Web framework for API endpoints
- **gTTS**: Text-to-speech generation
- **PyDub**: Audio manipulation
- **Librosa**: Audio analysis
- **Transformers**: Natural language processing
- **Whisper**: Speech recognition
- **Deep Translator**: Cross-language translation
- **HTML/CSS**: User interface design

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. Start the API server:
   ```bash
   python api_server.py
   ```

2. Access the web interface at `http://localhost:5000`

### API Endpoints

- `GET /api/words` - Get all words in the dictionary
- `GET /api/word/{word}` - Get details for a specific word
- `GET /api/search/{query}` - Search for words containing the query
- `POST /api/word` - Add a new word to the dictionary
- `PUT /api/word/{word}` - Update an existing word
- `DELETE /api/word/{word}` - Delete a word from the dictionary
- `POST /api/generate-audio` - Generate audio for text
- `POST /api/translate` - Translate text between languages
- `POST /api/tokenize` - Tokenize text
- `GET /api/stats` - Get dictionary statistics

## Project Structure

```
bilingual_audio_dictionary/
├── app.py                 # Main dictionary application logic
├── api_server.py          # Flask API server
├── requirements.txt       # Python dependencies
├── index.html             # Main web interface
├── static/
│   └── dict_app.js       # JavaScript frontend application
└── README.md             # This file
```

## Key Components

### BilingualAudioDictionary Class
The core class that manages dictionary data and provides all functionality:

- Word lookup and management
- Audio generation and caching
- Translation services
- Text tokenization
- Audio analysis
- Speech recognition

### Web Interface
A responsive web application with:
- Search functionality
- Word detail views
- Audio playback controls
- Statistics dashboard
- Word addition form

### API Server
A Flask-based REST API that exposes all dictionary functionality to the web interface.

## Audio Features

The application includes comprehensive audio processing capabilities:

- **Text-to-Speech**: Convert text in both English and Bashkir to audio
- **Audio Analysis**: Extract duration, tempo, and MFCC features
- **Speech Recognition**: Convert spoken audio back to text

## NLP Capabilities

- **Translation**: Between supported languages using deep-translator
- **Tokenization**: Break text into meaningful units using transformer models
- **Cross-lingual Processing**: Handle text in multiple languages seamlessly

## Bashkir Language Support

While gTTS doesn't natively support Bashkir, the application uses Russian voices as a close approximation for Bashkir text, providing functional audio playback for Bashkir words and phrases.

## Development Notes

This application was developed to work with the Bashkir language corpus and dictionary resources, incorporating modern NLP techniques and audio processing to create a comprehensive linguistic tool.

The project demonstrates integration between Python and JavaScript, combining server-side processing with client-side interactivity to create a seamless user experience for exploring the English-Bashkir dictionary.

## Libraries Used

- **gTTS**: Google Text-to-Speech for audio generation
- **PyDub**: Audio manipulation and processing
- **Librosa**: Audio analysis and feature extraction
- **SoundFile**: Audio file handling
- **Whisper**: OpenAI's speech recognition model
- **Deep Translator**: Multi-service translation library
- **Torch/Transformers**: Deep learning and NLP models
- **Flask**: Web framework for API development
- **Flask-CORS**: Cross-origin resource sharing support
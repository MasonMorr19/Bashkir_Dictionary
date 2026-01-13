/**
 * Bilingual Audio Dictionary Web Application
 * JavaScript Frontend for English-Bashkir Dictionary
 */

class BilingualDictionaryApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.currentWord = null;
        this.audioContext = null;
        this.initializeEventListeners();
        this.loadInitialData();
    }

    initializeEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('search-input');
        const searchButton = document.getElementById('search-button');
        const searchForm = document.getElementById('search-form');

        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.searchWord();
            });
        }

        if (searchButton) {
            searchButton.addEventListener('click', () => this.searchWord());
        }

        // Audio playback controls
        const playEnBtn = document.getElementById('play-en-audio');
        const playBaBtn = document.getElementById('play-ba-audio');

        if (playEnBtn) {
            playEnBtn.addEventListener('click', () => this.playAudio('en'));
        }

        if (playBaBtn) {
            playBaBtn.addEventListener('click', () => this.playAudio('ba'));
        }

        // Add word form
        const addWordForm = document.getElementById('add-word-form');
        if (addWordForm) {
            addWordForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.addWord();
            });
        }
    }

    async loadInitialData() {
        try {
            // Load recent words or statistics
            await this.loadStatistics();
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    async searchWord() {
        const searchInput = document.getElementById('search-input');
        if (!searchInput) return;

        const query = searchInput.value.trim();
        if (!query) {
            this.showMessage('Please enter a word to search', 'warning');
            return;
        }

        try {
            this.showLoader(true);
            const response = await fetch(`${this.apiBaseUrl}/search/${encodeURIComponent(query)}`);
            
            if (!response.ok) {
                throw new Error(`Search failed: ${response.status} ${response.statusText}`);
            }
            
            const data = await response.json();
            this.displaySearchResults(data);
        } catch (error) {
            console.error('Search error:', error);
            this.showMessage(`Search error: ${error.message}`, 'error');
        } finally {
            this.showLoader(false);
        }
    }

    displaySearchResults(results) {
        const resultsContainer = document.getElementById('results-container');
        if (!resultsContainer) return;

        if (!results || results.length === 0) {
            resultsContainer.innerHTML = '<p class="no-results">No results found.</p>';
            return;
        }

        if (Array.isArray(results)) {
            // Multiple results
            let html = '<div class="search-results-grid">';
            results.forEach(word => {
                html += `
                    <div class="result-card" onclick="app.selectWord('${word}')">
                        <h3>${word}</h3>
                    </div>
                `;
            });
            html += '</div>';
            resultsContainer.innerHTML = html;
        } else if (typeof results === 'object') {
            // Single word result
            this.displayWordDetails(results);
        }
    }

    async selectWord(word) {
        try {
            this.showLoader(true);
            const response = await fetch(`${this.apiBaseUrl}/word/${encodeURIComponent(word)}`);
            
            if (!response.ok) {
                throw new Error(`Word lookup failed: ${response.status} ${response.statusText}`);
            }
            
            const data = await response.json();
            this.displayWordDetails(data);
        } catch (error) {
            console.error('Word selection error:', error);
            this.showMessage(`Error loading word: ${error.message}`, 'error');
        } finally {
            this.showLoader(false);
        }
    }

    displayWordDetails(wordData) {
        const detailsContainer = document.getElementById('word-details');
        if (!detailsContainer) return;

        if (!wordData) {
            detailsContainer.innerHTML = '<p>Word not found.</p>';
            return;
        }

        this.currentWord = wordData;

        let html = `
            <div class="word-card">
                <div class="word-header">
                    <h2>${wordData.word || wordData.en || 'Unknown'}</h2>
                    <div class="word-meta">
                        <span class="pos-tag">${wordData.pos || 'N/A'}</span>
                        <span class="transcription">${wordData.transcription || ''}</span>
                    </div>
                </div>

                <div class="translations">
                    <div class="translation-pair">
                        <h4>English</h4>
                        <p>${wordData.en || wordData.word || 'N/A'}</p>
                    </div>
                    <div class="translation-pair">
                        <h4>Bashkir</h4>
                        <p class="bashkir-text">${wordData.ba || wordData.bashkir || 'N/A'}</p>
                    </div>
                </div>

                <div class="definitions">
                    <h4>Definitions</h4>
                    <ul>
        `;

        if (wordData.definitions && Array.isArray(wordData.definitions)) {
            wordData.definitions.forEach(def => {
                html += `
                    <li>
                        <div class="def-en">${def.en || def.definition || 'N/A'}</div>
                        <div class="def-ba">${def.ba || def.bashkir || 'N/A'}</div>
                    </li>
                `;
            });
        } else if (wordData.definition) {
            html += `<li><div class="def-en">${wordData.definition}</div></li>`;
        }

        html += `
                    </ul>
                </div>

                <div class="examples">
                    <h4>Examples</h4>
                    <ul>
        `;

        if (wordData.examples && Array.isArray(wordData.examples)) {
            wordData.examples.forEach(example => {
                html += `
                    <li>
                        <div class="ex-en">${example.en || 'N/A'}</div>
                        <div class="ex-ba">${example.ba || example.bashkir || 'N/A'}</div>
                    </li>
                `;
            });
        }

        html += `
                    </ul>
                </div>

                <div class="audio-controls">
                    <button id="play-en-audio" class="audio-btn" data-lang="en">
                        <i class="icon-volume-up"></i> Play English
                    </button>
                    <button id="play-ba-audio" class="audio-btn" data-lang="ba">
                        <i class="icon-volume-up"></i> Play Bashkir
                    </button>
                </div>
            </div>
        `;

        detailsContainer.innerHTML = html;

        // Re-initialize event listeners for the new buttons
        document.getElementById('play-en-audio')?.addEventListener('click', () => this.playAudio('en'));
        document.getElementById('play-ba-audio')?.addEventListener('click', () => this.playAudio('ba'));
    }

    async playAudio(language) {
        if (!this.currentWord) {
            this.showMessage('No word selected', 'warning');
            return;
        }

        const text = language === 'en' ? 
            (this.currentWord.en || this.currentWord.word) : 
            (this.currentWord.ba || this.currentWord.bashkir);

        if (!text) {
            this.showMessage(`No ${language.toUpperCase()} text available`, 'warning');
            return;
        }

        try {
            // Generate audio via API
            const response = await fetch(`${this.apiBaseUrl}/generate-audio`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    language: language
                })
            });

            if (!response.ok) {
                throw new Error(`Audio generation failed: ${response.status}`);
            }

            const blob = await response.blob();
            const audioUrl = URL.createObjectURL(blob);
            
            // Play the audio
            const audio = new Audio(audioUrl);
            audio.play().catch(error => {
                console.error('Audio playback error:', error);
                this.showMessage('Could not play audio: ' + error.message, 'error');
            });
        } catch (error) {
            console.error('Audio play error:', error);
            this.showMessage(`Audio playback error: ${error.message}`, 'error');
        }
    }

    async addWord() {
        const word = document.getElementById('new-word').value.trim();
        const bashkir = document.getElementById('bashkir-translation').value.trim();
        const definition = document.getElementById('definition').value.trim();

        if (!word || !bashkir || !definition) {
            this.showMessage('Please fill in all fields', 'warning');
            return;
        }

        const newWordData = {
            word: word,
            ba: bashkir,
            en: word,
            definition: definition,
            pos: document.getElementById('pos').value || 'noun',
            examples: []
        };

        if (document.getElementById('example-en').value.trim()) {
            newWordData.examples.push({
                en: document.getElementById('example-en').value.trim(),
                ba: document.getElementById('example-ba').value.trim()
            });
        }

        try {
            this.showLoader(true);
            const response = await fetch(`${this.apiBaseUrl}/word`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newWordData)
            });

            if (!response.ok) {
                throw new Error(`Add word failed: ${response.status}`);
            }

            this.showMessage('Word added successfully!', 'success');
            
            // Reset form
            document.getElementById('add-word-form').reset();
            
            // Optionally reload the word
            setTimeout(() => {
                this.selectWord(word);
            }, 1000);
        } catch (error) {
            console.error('Add word error:', error);
            this.showMessage(`Error adding word: ${error.message}`, 'error');
        } finally {
            this.showLoader(false);
        }
    }

    async loadStatistics() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/stats`);
            if (!response.ok) {
                throw new Error(`Stats load failed: ${response.status}`);
            }
            
            const stats = await response.json();
            this.updateStatsDisplay(stats);
        } catch (error) {
            console.error('Stats load error:', error);
        }
    }

    updateStatsDisplay(stats) {
        const statsContainer = document.getElementById('stats-container');
        if (!statsContainer || !stats) return;

        const html = `
            <div class="stats-grid">
                <div class="stat-card">
                    <h4>Total Words</h4>
                    <p class="stat-number">${stats.total_entries || 0}</p>
                </div>
                <div class="stat-card">
                    <h4>Languages</h4>
                    <p class="stat-number">${stats.languages_supported?.length || 0}</p>
                </div>
                <div class="stat-card">
                    <h4>Audio Files</h4>
                    <p class="stat-number">${stats.audio_cache_size || 0}</p>
                </div>
            </div>
        `;

        statsContainer.innerHTML = html;
    }

    showMessage(message, type = 'info') {
        const messageEl = document.getElementById('message-display');
        if (!messageEl) return;

        messageEl.textContent = message;
        messageEl.className = `message ${type}`;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageEl.textContent = '';
            messageEl.className = 'message';
        }, 5000);
    }

    showLoader(show) {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.style.display = show ? 'block' : 'none';
        }
    }

    // Utility functions
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    sanitizeHTML(str) {
        const temp = document.createElement('div');
        temp.textContent = str;
        return temp.innerHTML;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new BilingualDictionaryApp();
});

// Export for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BilingualDictionaryApp;
}
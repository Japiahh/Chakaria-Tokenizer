# Chakaria-Tokenizer
Tokenizer for Indonesian Language Data Cleaning

Chakaria-Tokenizer is a lightweight text preprocessing tool specifically designed for Indonesian text normalization and tokenization. This tool breaks down words into their meaningful components while preserving semantic structure, making it useful for linguistic research, NLP applications, or data cleaning tasks involving Bahasa Indonesia.

---

## Features
* Base word checking with optional fallback handling
* Affix separation (prefixes and suffixes) based on regex patterns
* Punctuation handling and token isolation
* Reduplication processing (e.g., anak-anak → anak, anak)
* Particle splitting ("pergilah" → "pergi", "-lah")
* Clean output with no empty tokens

---
 
## Tokenization Pipeline Overview
```bash
Input Text
   │
   └─▶ Base Word Checker
            │
            └─▶ pre_handle_split (for unmatched tokens)
                       │
                       └─▶ Empty Token Filtering
```

### pre_handle_split Steps:
1. handle_punctuation – separates punctuation marks from words, handles hyphenated reduplications and compounds.
2. split_affixes – detects and isolates prefixes and suffixes using regex validation.
3. handle_repeats – normalizes reduplication (e.g., berjalan-jalan).
4. split_particles – separates sentence particles (e.g., -lah, -pun, -kah, -tah).

---

Built with pain and black coffee

Thanks Risa

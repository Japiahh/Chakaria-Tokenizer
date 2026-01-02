# Chakaria-Tokenizer
I built Tokenizer for Indonesian Language Data Cleaning

Chakaria-Tokenizer is a specialized text preprocessing tool designed to handle the linguistic complexity of Bahasa Indonesia. Unlike standard white space tokenizers, Chakaria employs a hybrid approach combining rule based morphological segmentation with dictionary based validation to break down words into their meaningful components (stems, affixes, particles) while preserving semantic structure.

This tool is optimized for NLP pipelines, linguistic analysis, and deep data cleaning tasks where understanding word structure is crucial.

---

## Latest Updates

We have significantly upgraded the core tokenization logic to handle complex agglutination cases:

* **Deep Recursive Validation:** The tokenizer now verifies the deep root of a word before splitting. This prevents over stemming (ensuring *'menang'* remains *'menang'*, not *'me-' + 'nang'* unless *'nang'* is a valid root).
* **Process-Oriented Splitting:** Removed Early Exit limitations. Words are now analyzed for morphological structure even if they exist in the dictionary (*'memakan'* is correctly split into `['me-', 'makan']` instead of remaining `['memakan']`).
* **Greedy Affix Matching:** Implemented length priority sorting to ensure the longest valid prefix/suffix is processed first (distinguishing *'meng-'* from *'me-'*).
* **Smart Clitic & Particle Handling:** Improved logic for separating enclitics (*-ku*, *-mu*, *-nya*) and particles (e.g., *-lah*, *-kah*) without breaking the root word.

---

## Key Features

* **Hybrid Tokenization:** Combines regex patterns for affix detection with a comprehensive base word dictionary (`kata_dasar`) for validation.
* **Morphological Segmentation:**
    * **Prefixes:** Separates active/passive markers (e.g., *'mem-*, *'ber-'*, *'di-'*).
    * **Suffixes:** Isolates transitive/benefactive markers (e.g., *'-kan'*, *'-i'*, *'-an'*).
* **Reduplication Normalization:** Handles Indonesian repetition patterns (e.g., *"anak-anak"* → `"anak"`, `"-"`, `"anak"`).
* **Particle & Clitic Isolation:** Cleanly splits sentence particles ("pergilah" → "pergi", "-lah").
* **Punctuation Handling:** Context aware separation of punctuation from words.
* **Clean Output:** Automatically filters empty tokens and noise.

---
 
## Tokenization Pipeline Overview
```bash
graph TD
    A[Input Text] --> B(Basic Split & Lowercase)
    B --> C{Base Word Check}
    C -- Matched --> D[Final Token]
    C -- Unmatched / Morphological Mode --> E[pre_handle_split]
    
    subgraph "Morphological Processing"
    E --> F[Handle Punctuation]
    F --> G[Handle Repeats / Reduplication]
    G --> H[Split Particles]
    H --> I[Split Affixes & Deep Root Check]
    end
    
    I --> J[Greedy Dictionary Re-Merge]
    J --> K[Final Token List]
```

### Processing Steps Detail:
1. Handle Punctuation: Separates non-alphanumeric characters while respecting hyphenated compound words.
2. Handle Repeats: Detects and standardizes reduplicated words (kata ulang).
3. Split Particles: Detaches particles (-lah, -kah, -tah, -pun) only if the remaining stem is valid.
4. Split Affixes: The core engine. It iteratively strips prefixes and suffixes, validating the remaining stem against the dictionary at every step to ensure linguistic validity.

---

## Example
### How to use
```bash
from chakaria import ChakariaTokenizer
tokenizer = ChakariaTokenizer()
```

```bash
for i, text in enumerate(texts):
    print(f"\n[Kalimat {i+1}]: {text}")
    tokens = tokenizer.tokenize(text)
    print("→ Token:", tokens)
```

### Texts
```bash
texts = [
    "Berjalan-jalanlah di taman itu.",
    "Anak-anak bermain bola di lapangan.",
    "Dia memakan makanannya dengan lahap.",
    "Pergilah sekarang juga!",
    "Kucingku sangat lucu dan manja.",
    "terima kasih atas makanannya.",
    "kenapa demikian?",
    "sama-sama",
]

```

### Result
```bash
[Kalimat 1]: Berjalan-jalanlah di taman itu.
Token: ['ber-', 'jalan', '-', 'jalan', '-lah', 'di', 'taman', 'itu', '.']

[Kalimat 2]: Anak-anak bermain bola di lapangan.
Token: ['anak', '-', 'anak', 'ber-', 'main', 'bola', 'di', 'lapang', '-an', '.']

[Kalimat 3]: Dia memakan makanannya dengan lahap.
Token: ['dia', 'me-', 'makan', 'makan', '-an', '-nya', 'dengan', 'lahap', '.']

[Kalimat 4]: Pergilah sekarang juga!
Token: ['pergi', '-lah', 'sekarang', 'juga', '!']

[Kalimat 5]: Kucingku sangat lucu dan manja.
Token: ['kucing', '-ku', 'sangat', 'lucu', 'dan', 'manja', '.']

[Kalimat 6]: terima kasih atas makanannya.
Token: ['terima', 'kasih', 'atas', 'makan', '-an', '-nya', '.']

[Kalimat 7]: kenapa demikian?
Token: ['kenapa', 'demikian', '?']

[Kalimat 8]: sama-sama
Token: ['sama', '-', 'sama']
```

---

Built with pain and black coffee.

Thanks Risa.

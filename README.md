# Chakaria-Tokenizer
I built Tokenizer for Indonesian Language Data Cleaning

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
3. handle_repeats – normalizes reduplication (e.g., "berjalan-jalan").
4. split_particles – separates sentence particles (e.g., "-lah", "-pun", "-kah", "-tah").

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
    "dimana",
    "Anak-anak bermain bola di lapangan.",
    "Dia memakan makanannya dengan lahap.",
    "Pergilah sekarang juga!",
    "Kucingku sangat lucu dan manja.",
    "terima kasih atas makanannya.",
    "kenapa demikian?",
    "sama-sama",
    "apakah kamu baik-baik saja?",
    "12.000 rupiah",
    "aku hanya punya 2rb",
    "sejuta akanku ambil",
    "kapanpun kamu siap, aku akan datang",
    "bersama dengannya", 
    "berjalan bersama-sama",
    "semoga kamu baik-baik saja",
]
```

### Result
```bash
[Kalimat 1]: Berjalan-jalanlah di taman itu.
→ Token: ['ber-', 'jalan', '-', 'jalan', '-lah', 'di', 'taman', 'itu', '.']

[Kalimat 2]: dimana
→ Token: ['dimana']

[Kalimat 3]: Anak-anak bermain bola di lapangan.
→ Token: ['anak', '-', 'anak', 'ber-', 'main', 'bola', 'di', 'lapang', '-an', '.']

[Kalimat 4]: Dia memakan makanannya dengan lahap.
→ Token: ['dia', 'mem-', 'akan', 'makan', '-annya', 'dengan', 'lahap', '.']

[Kalimat 5]: Pergilah sekarang juga!
→ Token: ['pergi', '-lah', 'sekarang', 'juga', '!']

[Kalimat 6]: Kucingku sangat lucu dan manja.
→ Token: ['kucing', '-ku', 'sangat', 'lucu', 'dan', 'manja', '.']

[Kalimat 7]: terima kasih atas makanannya.
→ Token: ['terima', 'kasih', 'atas', 'makan', '-annya', '.']

[Kalimat 8]: kenapa demikian?
→ Token: ['kenapa', 'demikian', '?']

[Kalimat 9]: sama-sama
→ Token: ['sama', '-', 'sama']

[Kalimat 10]: apakah kamu baik-baik saja?
→ Token: ['apa', '-kah', 'kamu', 'baik', '-', 'baik', 'saja', '?']

[Kalimat 11]: 12.000 rupiah
→ Token: ['12', '.', '000', 'rupiah']

[Kalimat 12]: aku hanya punya 2rb
→ Token: ['aku', 'hanya', 'punya', '2rb']

[Kalimat 13]: sejuta akanku ambil
→ Token: ['se-', 'juta', 'akan', '-ku', 'ambil']

[Kalimat 14]: kapanpun kamu siap, aku akan datang
→ Token: ['kapan', '-pun', 'kamu', 'siap', ',', 'aku', 'akan', 'datang']

[Kalimat 15]: bersama dengannya
→ Token: ['ber-', 'sama', 'dengan', '-nya']

[Kalimat 16]: berjalan bersama-sama
→ Token: ['ber-', 'jalan', 'ber-', 'sama', '-', 'sama']

[Kalimat 17]: semoga kamu baik-baik saja
→ Token: ['semoga', 'kamu', 'baik', '-', 'baik', 'saja']
```

---

Built with pain and black coffee

Thanks Risa

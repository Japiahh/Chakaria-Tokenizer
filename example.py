from chakaria import ChakariaTokenizer

tokenizer = ChakariaTokenizer()

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

for i, text in enumerate(texts):
    print(f"\n[Kalimat {i+1}]: {text}")
    tokens = tokenizer.tokenize(text)
    print("→ Token:", tokens)
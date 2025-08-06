import re
from typing import List

class ChakariaTokenizer:
    def __init__(
        self,
        enable_split_affixes=True,
        enable_handle_repeats=True,
        enable_split_particles=True,
        enable_handle_confixes=True,
        use_base_words=True,
        verbose=False,
    ):
        # Konfigurasi fitur
        self.enable_split_affixes = enable_split_affixes
        self.enable_handle_repeats = enable_handle_repeats
        self.enable_split_particles = enable_split_particles
        self.enable_handle_confixes = enable_handle_confixes
        self.use_base_words = use_base_words
        self.verbose = verbose

        # Prefix dan suffix (tanpa tanda '-')
        self.prefixes = ["meng", "meny", "mem", "men", "me", "ber", "ter", "se", "diper", "per", "pe", "di", "ke"]
        self.suffixes = ["annya", "kan", "annya", "nya", "ku", "mu", "an"]

        self.particles = ["-lah", "-kah", "-tah", "-pun", "-ku", "-mu"]

        self.kata_dasar = self.load_base_words()

    def load_base_words(self):
        """
        Memuat daftar kata dasar dari file eksternal untuk referensi pemrosesan morfologi.

        Fungsi ini secara otomatis mengimpor data dari file:
        `dataset.nlp.kata_dasar.kada_cleaned` dan mengakses atribut `kada["kata_dasar"]`.

        Data ini digunakan untuk:
        - Memvalidasi hasil pemisahan afiks (prefix, suffix, konfiks),
        - Mencegah over-splitting terhadap kata yang memang sudah utuh,
        - Menjadi dasar bagi logika linguistik yang lebih dalam (mis. POS tagging berbasis akar kata).

        Keluaran:
        - Sebuah set (tipe data `set`) yang berisi seluruh kata dasar unik,
        untuk mempercepat pencarian (lookup) saat proses tokenisasi.
        """
        from data import kadas
        return set(kadas["kata_dasar"])

    def tokenize(self, text):
        """
        Fungsi utama tokenisasi.
        Jalankan pipeline:
        1. Kata dasar checker
        2. pre_handle_split (untuk yang gak ada di kata dasar)
        3. Filtering token kosong
        """
        tokens = text.split()

        final_tokens = []
        for token in tokens:
            token_lc = token.lower()
            
            if token_lc in self.kata_dasar:
                final_tokens.append(token_lc)
                continue
            
            preprocessed = self.pre_handle_split([token_lc])
            final_tokens.extend(preprocessed)

        final_tokens = [t for t in final_tokens if t.strip() != ""]

        return final_tokens


    def pre_handle_split(self, tokens):
        """
        Menjalankan pipeline handle sesuai urutan:
        1. handle_punctuation
        2. split_affixes
        3. handle_repeats
        4. split_particles
        """

        # 1. Handle punctuation
        tokens = self.handle_punctuation(tokens)

        # 2. Split affixes
        if self.enable_split_affixes:
            new_tokens = []
            for token in tokens:
                new_tokens.extend(self.split_affixes([token]))
            tokens = new_tokens

        # 3. Handle reduplikasi
        if self.enable_handle_repeats:
            new_tokens = []
            for token in tokens:
                new_tokens.extend(self.handle_repeats([token]))
            tokens = new_tokens

        # 4. Split particles
        if self.enable_split_particles:
            tokens = self.split_particles(tokens)

        return tokens

    def is_base_word(self, token):
        """
        Cek apakah token adalah kata dasar.
        """
        return token in self.kata_dasar

    def handle_punctuation(self, tokens):
        """
        Memisahkan tanda baca dari kata.
        Mempertimbangkan tanda hubung pada kata ulang dan majemuk.
        """
        processed = []
        for token in tokens:
            split = re.findall(r"\w+|[.,!?;:\-\"'\(\)]", token)
            processed.extend(split)
        return processed

    def handle_repeats(self, tokens: List[str]) -> List[str]:
        """
        Menangani kata ulang seperti 'anak-anak', 'berjalan-jalan'.
        Token akan dipisah dan diurai menjadi bagian-bagian logis.
        """
        result = []

        for token in tokens:
            if '-' in token:
                parts = token.split('-')
                if len(parts) == 2 and parts[0] == parts[1]:
                    result.extend([parts[0], '-', parts[1]])
                    continue
                else:
                    result.append(token)
                    continue

            found = False

            for prefix in self.prefixes:
                if token.startswith(prefix):
                    sisa = token[len(prefix):]
                    if len(sisa) % 2 == 0:
                        half = len(sisa) // 2
                        first = sisa[:half]
                        second = sisa[half:]
                        if first == second and first in self.kata_dasar:
                            result.extend([prefix, first, second])
                            found = True
                            break

            if found:
                continue

            if len(token) % 2 == 0:
                half = len(token) // 2
                part1 = token[:half]
                part2 = token[half:]
                if part1 == part2 and part1 in self.kata_dasar:
                    result.extend([part1, part2])
                    continue

            result.append(token)

        return result

    def split_affixes(self, tokens):
        """
        Memanggil pemrosesan prefix dan suffix secara terpisah untuk setiap token.
        Fungsi ini akan memeriksa dan memisahkan awalan (prefix) serta akhiran (suffix)
        dari setiap token, dengan mempertimbangkan daftar kata dasar sebagai validasi.
        """
        result = []

        for token in tokens:
            original = token
            token_lower = token.lower()
            parts = []

            # Step 1
            prefix = ""
            for p in sorted(self.prefixes, key=lambda x: -len(x)):
                if token_lower.startswith(p):
                    candidate = token_lower[len(p):]
                    if candidate in self.kata_dasar or any(candidate.endswith(s) for s in self.suffixes):
                        prefix = p
                        token = token[len(p):] 
                        break
            if prefix:
                parts.append(prefix + '-')

            # Step 2
            suffix_parts = self.split_suffix(token)

            # Step 3
            if suffix_parts:
                base = suffix_parts[0]
                suffixes = suffix_parts[1:]

                parts.append(base)  
                parts.extend(suffixes)  

            else:
                parts.append(original)  

            result.extend(parts)

        return result

    def split_prefix(self, token):
        """
        Memisahkan awalan dari kata dasar jika cocok dengan pola regex.
        Mempertimbangkan daftar kata dasar agar pemisahan valid.

        Proses:
        - Mencocokkan token dengan daftar pola prefix menggunakan regex.
        - Jika ditemukan prefix:
            - Prefix dihapus dari token sementara.
            - Dicek apakah sisa token termasuk dalam base_words.
            - Jika ya, kembalikan prefix dan akar kata sebagai dua token.
            - Jika tidak, biarkan token tetap utuh (hindari over-splitting).
        
        Catatan:
        - Menggunakan urutan pola yang lebih panjang terlebih dahulu agar awalan kompleks dideteksi lebih dulu (mis. 'meny-' sebelum 'me-').
        """
        for prefix in self.prefixes:
            if token.lower().startswith(prefix):
                root_candidate = token[len(prefix):]
                if root_candidate.lower() in self.kata_dasar:
                    return [prefix + '-', root_candidate]
        return [token]

    def split_suffix(self, token):
        """
        Memisahkan akhiran dari kata jika sesuai.
        Bekerja sama dengan split_prefix untuk dekomposisi afiks penuh.

        Proses:
        - Mencocokkan token dengan pola suffix menggunakan regex dari akhir kata.
        - Jika ditemukan suffix:
            - Potong suffix dari token sementara.
            - Periksa apakah akar katanya ada dalam daftar base_words.
            - Jika ya, kembalikan akar kata dan suffix sebagai dua token.
            - Jika tidak, biarkan token tetap utuh (hindari over-splitting).

        Catatan:
        - Suffix harus diurutkan dari yang paling panjang untuk menghindari pemotongan tidak lengkap.
        """
        token_lc = token.lower()

        if token_lc in self.kata_dasar:
            return [token_lc]
        
        result = []

        for suffix in self.suffixes:
            if token_lc.endswith(suffix):
                base = token_lc[:-len(suffix)]
                if base in self.kata_dasar:
                    result = [base, f"-{suffix}"]
                    break
        if not result:
            result = [token_lc]

        return result

    def split_particles(self, tokens):
        """
        Menangani partikel seperti '-lah', '-pun', '-kah', '-tah'.
        Partikel tidak memengaruhi makna dasar, tetapi penting dalam struktur kalimat.

        Proses:
        - Iterasi setiap token dan periksa apakah mengandung partikel di akhir.
        - Gunakan regex untuk mencocokkan partikel.
        - Jika ditemukan:
            - Pisahkan partikel dari kata dasarnya.
            - Tambahkan keduanya sebagai token terpisah.
        - Jika tidak ditemukan:
            - Simpan token seperti semula.
        """
        processed = []

        for token in tokens:
            matched = False
            for particle in sorted(self.particles, key=len, reverse=True):
                particle_clean = particle.replace("-", "")
                if token.endswith(particle_clean):
                    root = token[:-len(particle_clean)]
                    if len(root) > 1:
                        processed.append(root)
                        processed.append(particle)  
                        matched = True
                        break
            if not matched:
                processed.append(token)

        return processed

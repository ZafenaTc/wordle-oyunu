input_file = "kelimeler_en.txt"
output_file = "kelimeler_en_clean.txt"

unique_words = set()

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        word = line.strip()
        if word:  # boş satırı at
            unique_words.add(word.lower())  # küçük harfe çevirerek tekrarları engelle

# Sıralı çıkış istersen:
sorted_words = sorted(unique_words)

with open(output_file, "w", encoding="utf-8") as f:
    for word in sorted_words:
        f.write(word + "\n")

print("Tamamlandı. Çıktı:", output_file)

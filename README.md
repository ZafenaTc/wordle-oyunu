# 🎮 Wordle Tarzı Kelime Oyunu

Python 3.10+ | Kivy | KivyMD ile geliştirilmiş mobil uyumlu kelime tahmin oyunu.

## 📋 Özellikler

### 🎯 Oyun Özellikleri
- ✅ 5, 6 veya 7 harfli kelime desteği
- ✅ Türkçe ve İngilizce kelime listeleri
- ✅ Kelime uzunluğu kadar tahmin hakkı
- ✅ Doğru/yanlış harf ve konum kontrolü
- ✅ Gerçek zamanlı geri bildirim

### 🎨 UI/UX Özellikleri
- ✅ Mobil uyumlu responsive tasarım
- ✅ Light ve Dark tema desteği
- ✅ QWERTY klavye düzeni
- ✅ Türkçe özel karakter desteği (İ, Ş, Ğ, Ü, Ö, Ç)
- ✅ Akıcı ve belirgin animasyonlar
  - Doğru harf + konum → Yeşil flip animasyonu
  - Doğru harf + yanlış konum → Sarı flip animasyonu
  - Yanlış harf → Gri flip + titreme animasyonu

### ⚙️ Ayarlar
- ✅ Tema değiştirme (Light/Dark)
- ✅ Dil seçimi (Türkçe/İngilizce)
- ✅ Kelime uzunluğu seçimi (5/6/7)
- ✅ Ayarlar otomatik kaydedilir
- ✅ Açılışta son ayarlar yüklenir

## 📁 Dosya Yapısı

```
kelime_oyunu/
├── main.py              # Ana uygulama, ekran yönetimi, animasyonlar
├── words.py             # Kelime yönetimi, önbellekleme
├── game_logic.py        # Oyun mantığı, tahmin kontrolü
├── settings.json        # Kullanıcı tercihleri
├── kelimeler_tr.txt     # Türkçe kelime listesi
├── kelimeler_en.txt     # İngilizce kelime listesi
└── README.md            # Dokümantasyon
```

## 🚀 Kurulum

### Gereksinimler
```bash
Python 3.10 veya üzeri
pip (Python paket yöneticisi)
```

### Bağımlılıkları Yükleme
```bash
# Kivy ve KivyMD kurulumu
pip install kivy kivymd

# veya requirements.txt ile
pip install -r requirements.txt
```

### requirements.txt İçeriği
```
kivy>=2.3.0
kivymd>=1.1.1
```

## 🎮 Oyunu Başlatma

```bash
# Terminal/Komut satırından
python main.py

# veya
python3 main.py
```

## 📖 Kullanım

### Ana Menü
1. **Dil Seçimi**: Türkçe veya İngilizce kelimeler
2. **Kelime Uzunluğu**: 5, 6 veya 7 harf
3. **Tema**: Light veya Dark mod
4. **OYUNA BAŞLA**: Oyunu başlatır

### Oyun Ekranı
1. Ekranda kelime uzunluğu kadar kutu görünür
2. Klavyeden harflere dokunarak tahmin yapın
3. **GİR** tuşu ile tahmini onaylayın
4. **SİL** tuşu ile son harfi silin
5. Renkli geri bildirimler:
   - 🟩 **Yeşil**: Doğru harf, doğru konum
   - 🟨 **Sarı**: Doğru harf, yanlış konum
   - ⬜ **Gri**: Yanlış harf

### Oyun Sonu
- **TEKRAR OYNA**: Aynı ayarlarla yeni oyun
- **ANA MENÜ**: Ayarları değiştirmek için menüye dön

## 🔧 Geliştirici Notları

### Modüler Yapı
Her dosya bağımsız çalışabilir ve test edilebilir:

```bash
# Kelime yöneticisini test et
python words.py

# Oyun mantığını test et
python game_logic.py
```

### Animasyon Ayarları
`main.py` içinde `LetterBox` sınıfında:
- `animate_flip()` → Flip süreleri (şu an 0.15s)
- `shake()` → Titreme süresi (şu an 0.05s)

### Kelime Listeleri
`kelimeler_tr.txt` ve `kelimeler_en.txt`:
- Her satırda bir kelime
- Büyük harfle yazılmalı
- Türkçe karakterler desteklenir
- Boş satırlar yok sayılır

### Ayarlar Dosyası
`settings.json` formatı:
```json
{
    "theme": "Light",      // "Light" veya "Dark"
    "language": "tr",      // "tr" veya "en"
    "word_length": 5       // 5, 6 veya 7
}
```

## 🐛 Hata Ayıklama

### DEBUG Modu
`game_logic.py` içinde gizli kelime konsola yazdırılır:
```python
print(f"[DEBUG] Gizli kelime: {self.secret_word}")
```

### Kelime Listesi Kontrol
```bash
python words.py
```
Yüklenen kelime sayılarını ve örnekleri gösterir.

### Oyun Mantığı Test
```bash
python game_logic.py
```
Tahmin algoritmasını ve sonuçları test eder.

## 📱 Mobil Derleme

### Android (Buildozer)
```bash
# Buildozer kurulumu
pip install buildozer

# buildozer.spec oluştur
buildozer init

# APK derle
buildozer android debug
```

### iOS (Kivy-iOS)
```bash
# Kivy-iOS kurulumu
pip install kivy-ios

# Toolchain oluştur
toolchain build python3 kivy

# Proje oluştur
toolchain create Wordle /path/to/project
```

## 🎨 Özelleştirme

### Renk Temaları
`main.py` içinde hex renk kodları:
- Yeşil (correct): `#6aaa64`
- Sarı (present): `#c9b458`
- Gri (absent): `#787c7e` (Light) / `#3a3a3c` (Dark)

### Klavye Düzeni
`create_keyboard()` fonksiyonunda `rows` listesi:
```python
# Türkçe Q klavye
rows = [
    ['E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Ğ', 'Ü'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ş', 'İ'],
    ['⏎', 'Z', 'C', 'V', 'B', 'N', 'M', 'Ö', 'Ç', '⌫']
]
```

### Animasyon Hızları
```python
# Flip animasyonu
anim1 = Animation(size=(dp(60), dp(10)), duration=0.15)  # Küçültme
anim2 = Animation(size=(dp(60), dp(60)), duration=0.15)  # Büyütme

# Titreme animasyonu
anim = Animation(x=x - dp(5), duration=0.05)  # Her adım
```

## 📝 TODO / Geliştirme Fikirleri

### Oyun Özellikleri
- [ ] İstatistik ekranı (kazanma oranı, ortalama tahmin sayısı)
- [ ] Günlük kelime modu (herkes aynı kelimeyi tahmin eder)
- [ ] Zor mod (tahminler geçerli kelime olmalı)
- [ ] İpucu sistemi
- [ ] Skor sistemi ve liderlik tablosu

### UI/UX Geliştirmeleri
- [ ] Nasıl oynanır ekranı
- [ ] Ses efektleri
- [ ] Haptic feedback (titreşim)
- [ ] Kazanma animasyonu
- [ ] Paylaşma özelliği (emoji grid)

### Teknik Geliştirmeler
- [ ] Online çok oyunculu mod
- [ ] Kelime sözlüğü entegrasyonu
- [ ] Oyun geçmişi kaydetme
- [ ] Bulut senkronizasyonu
- [ ] Farklı dillerde kelime listeleri

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing`)
5. Pull Request açın

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 🙏 Teşekkürler

- Wordle oyunu için Josh Wardle'a
- Kivy ve KivyMD geliştirici topluluğuna

## 📞 İletişim

Sorularınız veya önerileriniz için issue açabilirsiniz.

---

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!

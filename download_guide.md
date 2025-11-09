# 🎮 Wordle Oyunu - Nasıl Kullanılır?

## 📥 1. ADIM: Dosyaları İndirin

### Yöntem A: Artifact'lardan İndirme (Claude.ai)

1. Bu konuşmada oluşturulan **artifact'ları** bulun
2. Her bir artifact'ın sağ üst köşesindeki **⋮** (üç nokta) menüsüne tıklayın
3. **"Copy"** veya **"Download"** seçeneğini seçin
4. Dosyayı bilgisayarınıza kaydedin

### İndirilmesi Gereken Dosyalar

#### 🎮 Temel Oyun Dosyaları (Zorunlu)
- ✅ `main_v2.py` - Ana uygulama
- ✅ `game_screen.py` - Oyun ekranı
- ✅ `words.py` - Kelime yönetimi
- ✅ `game_logic.py` - Oyun mantığı

#### ✨ Özellik Dosyaları (Önerilen)
- ⭐ `statistics.py` - İstatistikler
- ⭐ `sounds.py` - Ses efektleri
- ⭐ `themes.py` - Temalar
- ⭐ `security.py` - Güvenlik
- ⭐ `accessibility.py` - Erişilebilirlik

#### 🧪 Test ve Dokümantasyon (Opsiyonel)
- 📝 `test_wordle.py` - Testler
- 📚 `README.md` - Dokümantasyon
- 📚 `TAM_REHBER.md` - Detaylı rehber
- 📚 `NASIL_KULLANILIR.md` - Bu dosya

#### 📝 Kelime Listeleri (Zorunlu)
- 📄 `kelimeler_tr.txt` - Türkçe kelimeler
- 📄 `kelimeler_en.txt` - İngilizce kelimeler

#### ⚙️ Diğer Dosyalar
- 🔧 `requirements.txt` - Python bağımlılıkları
- 🔧 `settings.json` - Ayarlar (otomatik oluşur)

---

## 📁 2. ADIM: Klasör Yapısını Oluşturun

### Windows

```cmd
# Klasör oluştur
mkdir C:\wordle_oyunu
cd C:\wordle_oyunu

# Tüm .py dosyalarını bu klasöre kopyalayın
```

### macOS / Linux

```bash
# Klasör oluştur
mkdir ~/wordle_oyunu
cd ~/wordle_oyunu

# Tüm .py dosyalarını bu klasöre kopyalayın
```

### Klasör Yapısı (En Az)

```
wordle_oyunu/
├── main_v2.py
├── game_screen.py
├── words.py
├── game_logic.py
├── statistics.py
├── sounds.py
├── themes.py
├── security.py
├── accessibility.py
├── kelimeler_tr.txt
└── kelimeler_en.txt
```

---

## 🔧 3. ADIM: Python Kurulumu

### Python Yüklü mü Kontrol Edin

```bash
python --version
# veya
python3 --version

# Çıktı: Python 3.10.x veya üzeri olmalı
```

### Python Yoksa İndirin

- **Windows**: https://www.python.org/downloads/
  - ⚠️ Kurulumda "Add Python to PATH" işaretleyin!
- **macOS**: `brew install python3` (Homebrew ile)
- **Linux**: `sudo apt install python3 python3-pip`

---

## 📦 4. ADIM: Bağımlılıkları Yükleyin

### Temel Bağımlılıklar (Zorunlu)

```bash
# Kivy ve KivyMD yükleyin
pip install kivy kivymd

# VEYA requirements.txt varsa:
pip install -r requirements.txt
```

### Ses Dosyaları İçin (Opsiyonel)

```bash
# Sadece ses dosyası oluşturacaksanız
pip install numpy scipy
```

---

## 🎵 5. ADIM: Ses Dosyalarını Hazırlayın (Opsiyonel)

### Yöntem A: Otomatik Oluşturma

```bash
# Ses dosyalarını otomatik oluştur
python sounds.py

# sounds/ klasörü otomatik oluşturulacak
```

### Yöntem B: Sessiz Kullanım

Ses dosyaları olmadan da oyun çalışır! Ana menüden sesi kapatabilirsiniz.

---

## 🚀 6. ADIM: Oyunu Başlatın!

```bash
# Oyunu çalıştırın
python main_v2.py

# VEYA
python3 main_v2.py
```

### İlk Başlatma Ekranı

```
╔════════════════════════════╗
║    WORDLE OYUNU v2.0       ║
╠════════════════════════════╣
║                            ║
║  Dil: Türkçe ▼             ║
║  Kelime Uzunluğu: 5 ▼      ║
║  Tema: Klasik ▼            ║
║  Ses: Açık ▼               ║
║                            ║
║  [  OYUNA BAŞLA  ]         ║
║  [ İSTATİSTİKLER ]         ║
║                            ║
╚════════════════════════════╝
```

---

## 🎮 7. ADIM: İlk Oyununuz

### Oyun Ekranı

```
┌─────┬─────┬─────┬─────┬─────┐
│     │     │     │     │     │  ← Tahmin kutular
├─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │
├─────┼─────┼─────┼─────┼─────┤
│     │     │     │     │     │
└─────┴─────┴─────┴─────┴─────┘

┌─ KLAVYE ──────────────────────┐
│ Q W E R T Y U I O P          │
│  A S D F G H J K L           │
│   GİR Z X C V B N M SİL      │
└───────────────────────────────┘
```

### Nasıl Oynanır?

1. **Kelime Tahmin Edin**
   - Klavyeden harflere tıklayın
   - Örnek: E-L-M-A

2. **GİR Tuşuna Basın**
   - Tahminizi onaylayın

3. **Renk Kodlarını İzleyin**
   - 🟩 **Yeşil**: Doğru harf, doğru yer
   - 🟨 **Sarı**: Doğru harf, yanlış yer
   - ⬜ **Gri**: Yanlış harf

4. **Kelimeyi Bulun**
   - 5 tahmin hakkınız var (5 harfli kelime için)
   - İpuçlarını kullanın
   - Kelimeyi tahmin edin!

---

## ❓ SORUN GİDERME

### "Python bulunamadı" Hatası

**Çözüm**:
- Python'u yükleyin: https://www.python.org/downloads/
- PATH'e eklendiğinden emin olun

### "ModuleNotFoundError: No module named 'kivy'"

**Çözüm**:
```bash
pip install kivy kivymd
```

### "Kelime listesi bulunamadı"

**Çözüm**:
1. `kelimeler_tr.txt` oluşturun
2. İçine kelime ekleyin (her satıra bir kelime, BÜYÜK HARFLE):
   ```
   ELMA
   ARMUT
   KARPUZ
   ```

### Oyun Açılmıyor

**Çözüm**:
1. Python versiyonunu kontrol edin: `python --version`
2. Bağımlılıkları tekrar yükleyin: `pip install kivy kivymd`
3. Grafik sürücülerini güncelleyin

### Ses Çalmıyor

**Çözüm**:
- Normal! Ses dosyaları opsiyonel
- Ana Menü → Ses: Kapalı yapın
- VEYA `python sounds.py` ile ses dosyaları oluşturun

---

## 🎯 HIZLI BAŞLANGİÇ KONTROL LİSTESİ

- [ ] Python 3.10+ yüklü
- [ ] Tüm .py dosyaları indirildi
- [ ] `kelimeler_tr.txt` ve `kelimeler_en.txt` hazır
- [ ] Kivy ve KivyMD yüklü (`pip install kivy kivymd`)
- [ ] Oyun başlatılıyor (`python main_v2.py`)
- [ ] Ana menü görünüyor
- [ ] Oyun oynandı ✅

---

## 📱 MOBİL KULLANIM (İleri Düzey)

### Android APK Oluşturma

```bash
# Buildozer yükle
pip install buildozer

# APK oluştur
buildozer init
buildozer android debug

# APK çıktı: bin/wordle-*.apk
```

### iOS (sadece macOS)

```bash
# Kivy-iOS yükle
pip install kivy-ios

# Proje oluştur
toolchain build python3 kivy
toolchain create Wordle .
```

---

## 🆘 YARDIM VE DESTEK

### Hata Alıyorsanız

1. **TAM_REHBER.md** dosyasını okuyun
2. **test_wordle.py** çalıştırın: `python test_wordle.py`
3. Log dosyalarını kontrol edin
4. Tüm dosyaların doğru klasörde olduğunu kontrol edin

### Test Komutları

```bash
# Her modülü test edebilirsiniz
python words.py          # Kelime sistemi
python game_logic.py     # Oyun mantığı
python statistics.py     # İstatistikler
python sounds.py         # Sesler
python themes.py         # Temalar
python test_wordle.py    # Tüm testler
```

### Başarılı Kurulum Kontrolü

```bash
# Tüm testleri çalıştır
python test_wordle.py

# Çıktı:
# Ran 50 tests in 0.234s
# OK ← Bu görünmeli!
```

---

## 🎉 BAŞARILI! Artık Oynayabilirsiniz!

```bash
python main_v2.py
```

### İlk Oyununuz İçin İpuçları

1. **Yaygın harflerle başlayın**: ARISE, AUDIO, ELMAS
2. **Sarı harfleri farklı pozisyonlara deneyin**
3. **Yeşil harfleri sabit tutun**
4. **İstatistiklerinizi takip edin**: Ana Menü → İSTATİSTİKLER

### Keyifli Oyunlar! 🎮✨

---

## 📞 İletişim

- **Dokümantasyon**: README.md, TAM_REHBER.md
- **Testler**: test_wordle.py
- **Örnek Oyun**: Ana menüden "OYUNA BAŞLA"

**Son Güncelleme**: 2024
**Versiyon**: 2.0.0

**Başarılar! 🚀**

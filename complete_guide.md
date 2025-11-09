# 📚 Wordle v2.0 - Tam Rehber

## 📋 İçindekiler
1. [Hızlı Başlangıç](#hızlı-başlangıç)
2. [Detaylı Kurulum](#detaylı-kurulum)
3. [Dosya Yapısı](#dosya-yapısı)
4. [Test Etme](#test-etme)
5. [Geliştirme Önerileri](#geliştirme-önerileri)
6. [Sorun Giderme](#sorun-giderme)
7. [API Referansı](#api-referansı)

---

## 🚀 Hızlı Başlangıç

### 1. İndirme ve Kurulum (5 Dakika)

```bash
# Proje klasörü oluştur
mkdir wordle_oyunu
cd wordle_oyunu

# Gerekli dosyaları indir (artifact'lardan)
# - main_v2.py (veya main.py)
# - game_screen.py
# - words.py
# - game_logic.py
# - statistics.py
# - sounds.py
# - themes.py
# - security.py
# - accessibility.py
# - test_wordle.py

# Bağımlılıkları yükle
pip install kivy kivymd

# Opsiyonel: Test sesleri için
pip install numpy scipy
```

### 2. Kelime Listeleri

**kelimeler_tr.txt** oluşturun:
```
ELMA
ARMUT
KARPUZ
PORTAKAL
MANGO
KAYISI
KIRAZ
ÜZÜM
İNCİR
AYVA
```

**kelimeler_en.txt** oluşturun:
```
APPLE
GRAPE
ORANGE
BANANA
MANGO
MELON
LEMON
PEACH
BERRY
FRUIT
```

### 3. Çalıştırma

```bash
# Oyunu başlat
python main_v2.py

# VEYA bileşenleri test et
python game_screen.py     # Oyun ekranı
python test_wordle.py     # Unit testler
python accessibility.py   # Erişilebilirlik
```

---

## 🔧 Detaylı Kurulum

### Sistem Gereksinimleri

| Bileşen | Minimum | Önerilen |
|---------|---------|----------|
| Python | 3.10 | 3.11+ |
| RAM | 2 GB | 4 GB |
| Disk | 500 MB | 1 GB |
| İşletim Sistemi | Windows 10, macOS 10.14, Ubuntu 20.04 | En son sürümler |

### Platform Bazlı Kurulum

#### Windows
```cmd
# Python kurulumu (python.org)
python --version

# Sanal ortam
python -m venv venv
venv\Scripts\activate

# Bağımlılıklar
pip install kivy kivymd

# Oyunu başlat
python main_v2.py
```

#### macOS
```bash
# Python kurulumu (Homebrew)
brew install python3

# Sanal ortam
python3 -m venv venv
source venv/bin/activate

# Bağımlılıklar
pip install kivy kivymd

# SDL kütüphaneleri
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer

# Oyunu başlat
python main_v2.py
```

#### Linux (Ubuntu/Debian)
```bash
# Sistem bağımlılıkları
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
    build-essential git python3-dev ffmpeg \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev \
    libsdl2-ttf-dev libportmidi-dev libswscale-dev \
    libavformat-dev libavcodec-dev zlib1g-dev

# Sanal ortam
python3 -m venv venv
source venv/bin/activate

# Bağımlılıklar
pip install kivy kivymd

# Oyunu başlat
python main_v2.py
```

### Ses Dosyaları Hazırlama

#### Yöntem 1: Otomatik Oluşturma
```bash
# Gerekli kütüphaneler
pip install numpy scipy

# Ses dosyaları oluştur
python sounds.py

# sounds/ klasörü otomatik oluşturulacak
```

#### Yöntem 2: Manuel Ekleme
```bash
# sounds/ klasörü oluştur
mkdir sounds

# .wav dosyalarını ekleyin:
sounds/
├── key.wav      # Tuş sesi
├── correct.wav  # Doğru sesi
├── present.wav  # Mevcut sesi
├── absent.wav   # Yanlış sesi
├── win.wav      # Kazanma
├── lose.wav     # Kaybetme
├── error.wav    # Hata
├── delete.wav   # Silme
└── enter.wav    # Enter
```

---

## 📁 Dosya Yapısı

```
wordle_oyunu/
│
├── 🎮 OYUN DosyaLARI
│   ├── main_v2.py              # Ana uygulama (v2.0)
│   ├── game_screen.py          # Oyun ekranı modülü
│   ├── words.py                # Kelime yönetimi
│   ├── game_logic.py           # Oyun mantığı
│   │
├── ✨ YENİ ÖZELLİKLER
│   ├── statistics.py           # İstatistik sistemi
│   ├── sounds.py               # Ses yönetimi
│   ├── themes.py               # Tema yönetimi (8 tema)
│   ├── security.py             # Şifreleme + önbellek
│   ├── accessibility.py        # Erişilebilirlik
│   │
├── 🧪 TEST VE DOKÜMANTASYON
│   ├── test_wordle.py          # Unit testler
│   ├── README.md               # Genel dokümantasyon
│   ├── KURULUM.md              # Kurulum rehberi
│   ├── HIZLI_BAŞLANGIÇ.md      # Hızlı başlangıç
│   ├── TAM_REHBER.md           # Bu dosya
│   │
├── ⚙️ AYARLAR VE VERİLER
│   ├── settings.json           # Kullanıcı ayarları
│   ├── statistics.json         # Oyun istatistikleri
│   ├── accessibility_settings.json  # Erişilebilirlik
│   ├── game_metrics.json       # Performans metrikleri
│   ├── tutorials.json          # Tutorial durumu
│   ├── achievements.json       # Başarılar
│   │
├── 📝 KELİME LİSTELERİ
│   ├── kelimeler_tr.txt        # Türkçe kelimeler
│   ├── kelimeler_en.txt        # İngilizce kelimeler
│   │
├── 🔊 SES DOSYALARI
│   └── sounds/
│       ├── key.wav
│       ├── correct.wav
│       ├── present.wav
│       ├── absent.wav
│       ├── win.wav
│       ├── lose.wav
│       ├── error.wav
│       ├── delete.wav
│       └── enter.wav
│
└── 📦 DİĞER
    ├── requirements.txt        # Python bağımlılıkları
    ├── .gitignore             # Git yoksay listesi
    └── buildozer.spec         # Mobil derleme (opsiyonel)
```

### Dosya Açıklamaları

#### Ana Modüller
- **main_v2.py**: Uygulama başlangıcı, ekran yönetimi
- **game_screen.py**: Oyun ekranı, animasyonlar, klavye
- **words.py**: Kelime listesi yönetimi
- **game_logic.py**: Wordle algoritması

#### Özellik Modülleri
- **statistics.py**: Performans takibi, grafikler
- **sounds.py**: Ses efektleri yönetimi
- **themes.py**: 8 farklı renk teması
- **security.py**: Şifreleme ve önbellek
- **accessibility.py**: Erişilebilirlik, metrikler

#### Test ve Dokümantasyon
- **test_wordle.py**: 50+ unit test
- **README.md**: Genel bakış
- **KURULUM.md**: Detaylı kurulum
- **TAM_REHBER.md**: Kapsamlı rehber

---

## 🧪 Test Etme

### Unit Testler Çalıştırma

```bash
# Tüm testleri çalıştır
python test_wordle.py

# Beklenen çıktı:
# test_initialization (TestGameLogic) ... ok
# test_evaluate_guess_all_correct (TestGameLogic) ... ok
# ...
# Ran 50 tests in 0.234s
# OK
```

### Tek Bir Test Sınıfı

```bash
# Sadece oyun mantığı testleri
python -m unittest test_wordle.TestGameLogic

# Sadece istatistik testleri
python -m unittest test_wordle.TestStatistics
```

### Test Coverage

```bash
# Coverage yükle
pip install coverage

# Testleri coverage ile çalıştır
coverage run -m unittest test_wordle

# Rapor oluştur
coverage report

# HTML rapor
coverage html
# htmlcov/index.html açın
```

### Manuel Test Senaryoları

#### Senaryo 1: İlk Oyun
```
1. Oyunu başlat: python main_v2.py
2. Ana Menü → OYUNA BAŞLA
3. İlk tahmin: ELMA
4. GİR tuşuna bas
5. Renk kodlarını kontrol et:
   - Yeşil kutu görünmeli
   - Animasyon akıcı olmalı
   - Ses çalmalı (açıksa)
```

#### Senaryo 2: İstatistikler
```
1. 3 oyun oyna (1 kazan, 2 kaybet)
2. Ana Menü → İSTATİSTİKLER
3. Kontrol et:
   - Oynanan: 3
   - Kazanma oranı: 33.3%
   - Grafik görünmeli
```

#### Senaryo 3: Tema Değiştirme
```
1. Ana Menü → Tema: Klasik
2. "Neon" seç
3. Oyuna gir
4. Kontrol et:
   - Renkler değişti mi?
   - Yeşil → Neon yeşil
   - Sarı → Neon sarı
```

---

## 🔨 Geliştirme Önerileri

### Seviye 1: Başlangıç İyileştirmeleri

#### 1. Daha Fazla Kelime Ekleyin
```python
# kelimeler_tr.txt dosyasını genişletin
# Hedef: En az 1000 kelime

# Otomatik kelime scraping (opsiyonel)
# TDK API veya kelime listesi kullanın
```

#### 2. Günlük Kelime Modu
```python
# daily_word.py oluşturun
import datetime
import random

def get_daily_word(word_length, language):
    # Tarihi seed olarak kullan
    today = datetime.date.today()
    seed = int(today.strftime('%Y%m%d'))
    random.seed(seed)
    
    # Kelime seç
    # ...
    return word
```

#### 3. Paylaşma Özelliği
```python
# share.py modülü
def generate_share_text(game_logic):
    """Emoji grid oluştur"""
    text = f"Wordle {game_logic.current_attempt}/{game_logic.max_attempts}\n\n"
    
    for result in game_logic.results:
        for status in result:
            if status == 'correct':
                text += '🟩'
            elif status == 'present':
                text += '🟨'
            else:
                text += '⬜'
        text += '\n'
    
    return text
```

### Seviye 2: Orta Düzey Özellikler

#### 4. Zor Mod
```python
# game_logic.py içine ekleyin
def validate_hard_mode(self, guess, previous_results):
    """
    Zor mod kuralları:
    - Yeşil harfler sabit olmalı
    - Sarı harfler kullanılmalı
    """
    if not previous_results:
        return True
    
    last_guess = self.guesses[-1]
    last_result = previous_results[-1]
    
    for i, (letter, status) in enumerate(zip(last_guess, last_result)):
        if status == 'correct':
            if guess[i] != letter:
                return False  # Yeşil harf değiştirilmiş
        elif status == 'present':
            if letter not in guess:
                return False  # Sarı harf kullanılmamış
    
    return True
```

#### 5. İpucu Sistemi
```python
# hints.py modülü
class HintSystem:
    def __init__(self, max_hints=2):
        self.max_hints = max_hints
        self.used_hints = 0
    
    def get_hint(self, secret_word, game_logic):
        if self.used_hints >= self.max_hints:
            return None
        
        # İpucu türleri
        hints = [
            f"İlk harf: {secret_word[0]}",
            f"Son harf: {secret_word[-1]}",
            f"Kelimede '{secret_word[2]}' harfi var",
            f"Kelime {len(secret_word)} harfli"
        ]
        
        self.used_hints += 1
        return random.choice(hints)
```

#### 6. Başarı Rozetleri
```python
# achievements.py genişletme
def check_achievements(self, game_logic, statistics):
    achievements = []
    
    # İlk zafer
    if statistics.games_won == 1:
        achievements.append('first_win')
    
    # 5 oyun serisi
    if statistics.current_streak == 5:
        achievements.append('win_streak_5')
    
    # Mükemmel oyun (2 tahminde)
    if game_logic.is_won() and game_logic.current_attempt == 2:
        achievements.append('perfect_game')
    
    # Hız canavarı (60 saniyeden kısa)
    # ...
    
    return achievements
```

### Seviye 3: İleri Düzey Özellikler

#### 7. Çevrimiçi Çok Oyunculu
```python
# multiplayer.py (Firebase veya WebSocket)
class MultiplayerManager:
    def __init__(self):
        self.firebase = firebase_admin.initialize_app()
    
    def create_room(self, player_name):
        """Oda oluştur"""
        room_id = generate_room_id()
        # Firebase'e kaydet
        return room_id
    
    def join_room(self, room_id, player_name):
        """Odaya katıl"""
        # ...
    
    def sync_guess(self, room_id, guess):
        """Tahmini senkronize et"""
        # ...
```

#### 8. Kelime Sözlüğü Entegrasyonu
```python
# dictionary.py
import requests

def get_word_definition(word, language='tr'):
    """TDK veya Dictionary API"""
    if language == 'tr':
        url = f"https://sozluk.gov.tr/gts?ara={word}"
        response = requests.get(url)
        # Parse JSON
        return response.json()
    else:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        return response.json()

def text_to_speech(text, language='tr'):
    """TTS ile kelimeyi oku"""
    from gtts import gTTS
    tts = gTTS(text=text, lang=language)
    tts.save('word.mp3')
    # Ses dosyasını çal
```

#### 9. Gelişmiş Analitik
```python
# advanced_analytics.py
import matplotlib.pyplot as plt

def create_performance_chart(statistics):
    """Performans grafiği oluştur"""
    plt.figure(figsize=(10, 6))
    
    # Tahmin dağılımı
    dist = statistics.get_guess_distribution()
    plt.bar(dist.keys(), dist.values())
    plt.xlabel('Tahmin Sayısı')
    plt.ylabel('Oyun Sayısı')
    plt.title('Tahmin Dağılımı')
    
    plt.savefig('performance.png')
    plt.close()

def export_statistics_csv(statistics):
    """İstatistikleri CSV'ye aktar"""
    import csv
    
    with open('statistics.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Metrik', 'Değer'])
        
        summary = statistics.get_summary()
        for key, value in summary.items():
            writer.writerow([key, value])
```

---

## 🐛 Sorun Giderme

### Yaygın Hatalar ve Çözümleri

#### 1. "ModuleNotFoundError: No module named 'kivy'"
**Neden**: Kivy yüklenmemiş

**Çözüm**:
```bash
pip install kivy kivymd
```

#### 2. "Kelime listesi bulunamadı"
**Neden**: kelimeler_*.txt dosyaları eksik

**Çözüm**:
```bash
# Dosyaları oluşturun
echo "ELMA\nARMUT\nKARPUZ" > kelimeler_tr.txt
echo "APPLE\nGRAPE\nORANGE" > kelimeler_en.txt
```

#### 3. Sesler Çalmıyor
**Neden**: Ses dosyaları yok veya yanlış format

**Çözüm**:
```bash
# Otomatik oluştur
python sounds.py

# VEYA sesleri kapat
# Ana Menü → Ses: Kapalı
```

#### 4. Pencere Açılmıyor
**Neden**: Grafik sürücü sorunu

**Çözüm**:
```bash
# Windows: DirectX güncelle
# macOS: Sistem güncellemesi
# Linux:
sudo apt install mesa-utils libgl1-mesa-glx
```

#### 5. Testler Başarısız
**Neden**: Eksik dosyalar veya bağımlılık

**Çözüm**:
```bash
# Tüm dosyaları kontrol edin
ls *.py

# Test bağımlılıklarını yükleyin
pip install unittest mock
```

### Debug Modu

```python
# main_v2.py başına ekleyin
import os
os.environ['KIVY_LOG_LEVEL'] = 'debug'

# Detaylı log göreceksiniz
```

### Log Dosyaları

```bash
# Kivy logları
~/.kivy/logs/  # Linux/macOS
%USERPROFILE%\.kivy\logs\  # Windows

# En son log
cat ~/.kivy/logs/kivy_*.txt
```

---

## 📖 API Referansı

### GameLogic Sınıfı

```python
from game_logic import GameLogic

# Başlatma
game = GameLogic(secret_word='ELMA', max_attempts=6)

# Tahmin yapma
result = game.make_guess('ARMA')
# Returns: ['absent', 'absent', 'correct', 'correct'] veya None

# Oyun durumu
is_over = game.is_game_over()  # bool
is_won = game.is_won()  # bool
remaining = game.get_remaining_attempts()  # int

# İstatistikler
stats = game.get_statistics()  # dict
keyboard = game.get_keyboard_state()  # dict
```

### Statistics Sınıfı

```python
from statistics import Statistics

# Başlatma
stats = Statistics(stats_file='statistics.json')

# Oyun kaydetme
stats.record_game(
    won=True,
    attempts=3,
    word_length=5,
    language='tr'
)

# İstatistik alma
summary = stats.get_summary()  # dict
win_rate = stats.get_win_rate()  # float
avg_guesses = stats.get_average_guesses()  # float
distribution = stats.get_guess_distribution()  # dict

# Sıfırlama
stats.reset_stats()
```

### ThemeManager Sınıfı

```python
from themes import ThemeManager

# Başlatma
theme_manager = ThemeManager()

# Tema değiştirme
theme_manager.set_current_theme('neon')  # bool

# Tema alma
theme = theme_manager.get_current_theme()  # Theme

# Renk alma
color = theme_manager.get_color('correct', dark_mode=False)  # RGBA tuple
hex_color = theme_manager.get_hex_color('correct', dark_mode=False)  # str

# Tüm temalar
themes = theme_manager.get_all_themes()  # List[Theme]
```

### SoundManager Sınıfı

```python
from sounds import SoundManager

# Başlatma
sound_manager = SoundManager(sounds_dir='sounds', enabled=True)

# Ses çalma
sound_manager.play_key_sound()
sound_manager.play_correct_sound()
sound_manager.play_win_sound()

# Ses kontrolü
sound_manager.enable()
sound_manager.disable()
enabled = sound_manager.toggle()  # bool

# Ses seviyesi
sound_manager.set_volume('key', 0.5)  # 0.0 - 1.0
sound_manager.set_master_volume(0.7)

# Durum
status = sound_manager.get_sound_status()  # dict
```

---

## 🚀 Üretim Hazırlığı

### Performans Optimizasyonu

```python
# 1. Kelime listelerini şifreleyin
from security import SecureWordManager

manager = SecureWordManager()
manager.convert_plaintext_to_encrypted(
    'kelimeler_tr.txt',
    'kelimeler_tr_encrypted.json'
)

# 2. Lazy loading kullanın
# words.py içinde zaten var

# 3. Animasyonları optimize edin
# Reduced motion modunu aktifleştirin
```

### Mobil Derleme

```bash
# Android
buildozer init
buildozer android debug

# iOS (macOS gerekli)
toolchain build python3 kivy
toolchain create Wordle .
```

### Dağıtım Checklist

- [ ] Tüm testler geçiyor
- [ ] Kelime listeleri hazır
- [ ] Ses dosyaları eklendi
- [ ] Performans testleri yapıldı
- [ ] Güvenlik kontrolleri yapıldı
- [ ] Dokümantasyon tamamlandı
- [ ] Lisans dosyası eklendi
- [ ] README güncel
- [ ] CHANGELOG oluşturuldu

---

## 📞 Destek ve Topluluk

### Yardım Kaynakları

- **Kivy Dokümantasyonu**: https://kivy.org/doc/stable/
- **KivyMD Dokümantasyonu**: https://kivymd.readthedocs.io/
- **Python Dokümantasyonu**: https://docs.python.org/3/

### Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun
3. Testler ekleyin
4. Pull request açın

### Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---

**Son Güncelleme**: 2024
**Versiyon**: 2.0.0
**Yazar**: Wordle Oyunu Geliştirme Ekibi

**İyi geliştirmeler! 🚀**

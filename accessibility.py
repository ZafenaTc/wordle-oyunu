"""
Erişilebilirlik ve Kullanıcı Deneyimi Modülü
Screen reader desteği, ses imlası, font ayarları, metrikler
"""

import time
from typing import Dict, List, Optional
from kivy.core.audio import SoundLoader
from kivy.logger import Logger
import json
import os


class AccessibilityManager:
    """Erişilebilirlik yöneticisi"""
    
    def __init__(self):
        """Erişilebilirlik ayarlarını başlat"""
        self.settings = self.load_accessibility_settings()
        self.screen_reader_enabled = self.settings.get('screen_reader', False)
        self.voice_guidance_enabled = self.settings.get('voice_guidance', False)
        self.high_contrast = self.settings.get('high_contrast', False)
        self.font_size_multiplier = self.settings.get('font_size_multiplier', 1.0)
        self.reduced_motion = self.settings.get('reduced_motion', False)
        
    def load_accessibility_settings(self) -> Dict:
        """Erişilebilirlik ayarlarını yükle"""
        default_settings = {
            'screen_reader': False,
            'voice_guidance': False,
            'high_contrast': False,
            'font_size_multiplier': 1.0,
            'reduced_motion': False,
            'color_blind_mode': False
        }
        
        try:
            if os.path.exists('accessibility_settings.json'):
                with open('accessibility_settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    for key, value in default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
        except Exception as e:
            Logger.error(f"Erişilebilirlik ayarları yüklenemedi: {e}")
            
        return default_settings
        
    def save_accessibility_settings(self):
        """Erişilebilirlik ayarlarını kaydet"""
        try:
            with open('accessibility_settings.json', 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            Logger.error(f"Erişilebilirlik ayarları kaydedilemedi: {e}")
            
    def announce(self, text: str):
        """
        Ekran okuyucu için duyuru
        
        Args:
            text: Duyurulacak metin
        """
        if self.screen_reader_enabled:
            Logger.info(f"[SCREEN READER] {text}")
            # Gerçek ekran okuyucu entegrasyonu için:
            # - iOS: UIAccessibility.post()
            # - Android: announceForAccessibility()
            
    def describe_game_state(self, game_logic) -> str:
        """
        Oyun durumunu açıkla
        
        Args:
            game_logic: GameLogic instance
            
        Returns:
            Açıklama metni
        """
        description = f"Tahmin {game_logic.current_attempt} / {game_logic.max_attempts}. "
        
        if game_logic.current_attempt > 0:
            last_guess = game_logic.guesses[-1]
            last_result = game_logic.results[-1]
            
            description += f"Son tahmin: {last_guess}. "
            
            correct_count = sum(1 for r in last_result if r == 'correct')
            present_count = sum(1 for r in last_result if r == 'present')
            
            description += f"{correct_count} harf doğru yerde, "
            description += f"{present_count} harf yanlış yerde. "
            
        return description
        
    def describe_letter_status(self, letter: str, status: str) -> str:
        """
        Harf durumunu sesli açıkla
        
        Args:
            letter: Harf
            status: Durum (correct, present, absent)
            
        Returns:
            Açıklama
        """
        descriptions = {
            'correct': f"{letter} harfi doğru yerde",
            'present': f"{letter} harfi kelimede var ama yanlış yerde",
            'absent': f"{letter} harfi kelimede yok"
        }
        return descriptions.get(status, "")
        
    def get_font_size(self, base_size: float) -> float:
        """
        Font boyutunu erişilebilirlik ayarına göre döndür
        
        Args:
            base_size: Temel font boyutu
            
        Returns:
            Ayarlanmış font boyutu
        """
        return base_size * self.font_size_multiplier
        
    def should_reduce_motion(self) -> bool:
        """Animasyonlar azaltılmalı mı?"""
        return self.reduced_motion
        
    def get_animation_duration(self, base_duration: float) -> float:
        """
        Animasyon süresini ayarla
        
        Args:
            base_duration: Temel süre
            
        Returns:
            Ayarlanmış süre
        """
        if self.reduced_motion:
            return base_duration * 0.5  # %50 daha hızlı
        return base_duration


class GameMetrics:
    """Oyun metrikleri ve analiz"""
    
    def __init__(self):
        """Metrik yöneticisini başlat"""
        self.metrics = self.load_metrics()
        self.current_session = {
            'start_time': time.time(),
            'games_played': 0,
            'total_playtime': 0,
            'abandonment_count': 0,
            'word_lengths': {},
            'languages': {},
            'themes_used': {},
            'fps_samples': [],
            'memory_samples': []
        }
        
    def load_metrics(self) -> Dict:
        """Metrikleri yükle"""
        default_metrics = {
            'total_sessions': 0,
            'total_playtime': 0,
            'average_game_duration': 0,
            'abandonment_rate': 0,
            'word_length_distribution': {'5': 0, '6': 0, '7': 0},
            'language_distribution': {'tr': 0, 'en': 0},
            'theme_usage': {},
            'average_fps': 0,
            'peak_memory_mb': 0,
            'app_size_mb': 0,
            'startup_time_sec': 0
        }
        
        try:
            if os.path.exists('game_metrics.json'):
                with open('game_metrics.json', 'r', encoding='utf-8') as f:
                    metrics = json.load(f)
                    for key, value in default_metrics.items():
                        if key not in metrics:
                            metrics[key] = value
                    return metrics
        except Exception as e:
            Logger.error(f"Metrikler yüklenemedi: {e}")
            
        return default_metrics
        
    def save_metrics(self):
        """Metrikleri kaydet"""
        try:
            with open('game_metrics.json', 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=4, ensure_ascii=False)
        except Exception as e:
            Logger.error(f"Metrikler kaydedilemedi: {e}")
            
    def record_game_start(self, word_length: int, language: str, theme: str):
        """Oyun başlangıcını kaydet"""
        self.current_session['games_played'] += 1
        self.current_session['game_start_time'] = time.time()
        
        # Kelime uzunluğu
        if word_length not in self.current_session['word_lengths']:
            self.current_session['word_lengths'][word_length] = 0
        self.current_session['word_lengths'][word_length] += 1
        
        # Dil
        if language not in self.current_session['languages']:
            self.current_session['languages'][language] = 0
        self.current_session['languages'][language] += 1
        
        # Tema
        if theme not in self.current_session['themes_used']:
            self.current_session['themes_used'][theme] = 0
        self.current_session['themes_used'][theme] += 1
        
    def record_game_end(self, completed: bool):
        """Oyun bitişini kaydet"""
        if 'game_start_time' in self.current_session:
            duration = time.time() - self.current_session['game_start_time']
            self.current_session['total_playtime'] += duration
            
            if not completed:
                self.current_session['abandonment_count'] += 1
                
    def record_fps(self, fps: float):
        """FPS kaydı"""
        self.current_session['fps_samples'].append(fps)
        
        # Son 100 örneği tut
        if len(self.current_session['fps_samples']) > 100:
            self.current_session['fps_samples'].pop(0)
            
    def record_memory(self, memory_mb: float):
        """Bellek kullanımı kaydı"""
        self.current_session['memory_samples'].append(memory_mb)
        
        # Son 50 örneği tut
        if len(self.current_session['memory_samples']) > 50:
            self.current_session['memory_samples'].pop(0)
            
    def get_session_summary(self) -> Dict:
        """Oturum özetini döndür"""
        session_duration = time.time() - self.current_session['start_time']
        
        avg_fps = 0
        if self.current_session['fps_samples']:
            avg_fps = sum(self.current_session['fps_samples']) / len(
                self.current_session['fps_samples']
            )
            
        peak_memory = 0
        if self.current_session['memory_samples']:
            peak_memory = max(self.current_session['memory_samples'])
            
        abandonment_rate = 0
        if self.current_session['games_played'] > 0:
            abandonment_rate = (
                self.current_session['abandonment_count'] / 
                self.current_session['games_played']
            ) * 100
            
        return {
            'session_duration_min': session_duration / 60,
            'games_played': self.current_session['games_played'],
            'total_playtime_min': self.current_session['total_playtime'] / 60,
            'abandonment_rate': abandonment_rate,
            'average_fps': avg_fps,
            'peak_memory_mb': peak_memory,
            'word_lengths': self.current_session['word_lengths'],
            'languages': self.current_session['languages'],
            'themes': self.current_session['themes_used']
        }
        
    def update_global_metrics(self):
        """Global metrikleri güncelle"""
        summary = self.get_session_summary()
        
        self.metrics['total_sessions'] += 1
        self.metrics['total_playtime'] += summary['total_playtime_min']
        
        # Ortalama oyun süresi
        if self.metrics['total_sessions'] > 0:
            self.metrics['average_game_duration'] = (
                self.metrics['total_playtime'] / self.metrics['total_sessions']
            )
            
        # Terk etme oranı
        self.metrics['abandonment_rate'] = summary['abandonment_rate']
        
        # Kelime uzunluğu dağılımı
        for length, count in summary['word_lengths'].items():
            length_str = str(length)
            if length_str not in self.metrics['word_length_distribution']:
                self.metrics['word_length_distribution'][length_str] = 0
            self.metrics['word_length_distribution'][length_str] += count
            
        # Dil dağılımı
        for lang, count in summary['languages'].items():
            if lang not in self.metrics['language_distribution']:
                self.metrics['language_distribution'][lang] = 0
            self.metrics['language_distribution'][lang] += count
            
        # FPS ortalaması
        if summary['average_fps'] > 0:
            self.metrics['average_fps'] = summary['average_fps']
            
        # Bellek
        if summary['peak_memory_mb'] > self.metrics['peak_memory_mb']:
            self.metrics['peak_memory_mb'] = summary['peak_memory_mb']
            
        self.save_metrics()
        
    def get_analytics_report(self) -> str:
        """Analitik raporu oluştur"""
        report = "=== OYUN ANALİTİK RAPORU ===\n\n"
        
        report += "GENEL İSTATİSTİKLER:\n"
        report += f"  Toplam Oturum: {self.metrics['total_sessions']}\n"
        report += f"  Toplam Oyun Süresi: {self.metrics['total_playtime']:.1f} dakika\n"
        report += f"  Ortalama Oyun: {self.metrics['average_game_duration']:.1f} dakika\n"
        report += f"  Terk Etme Oranı: {self.metrics['abandonment_rate']:.1f}%\n\n"
        
        report += "KELİME UZUNLUĞU TERCİHLERİ:\n"
        total_games = sum(self.metrics['word_length_distribution'].values())
        if total_games > 0:
            for length, count in sorted(
                self.metrics['word_length_distribution'].items()
            ):
                percentage = (count / total_games) * 100
                report += f"  {length} harf: {count} oyun ({percentage:.1f}%)\n"
        report += "\n"
        
        report += "DİL TERCİHLERİ:\n"
        total_lang = sum(self.metrics['language_distribution'].values())
        if total_lang > 0:
            for lang, count in sorted(
                self.metrics['language_distribution'].items()
            ):
                percentage = (count / total_lang) * 100
                lang_name = "Türkçe" if lang == 'tr' else "İngilizce"
                report += f"  {lang_name}: {count} oyun ({percentage:.1f}%)\n"
        report += "\n"
        
        report += "PERFORMANS METRİKLERİ:\n"
        report += f"  Ortalama FPS: {self.metrics['average_fps']:.1f}\n"
        report += f"  Peak Bellek: {self.metrics['peak_memory_mb']:.1f} MB\n"
        report += f"  Uygulama Boyutu: {self.metrics['app_size_mb']:.1f} MB\n"
        report += f"  Başlangıç Süresi: {self.metrics['startup_time_sec']:.2f} saniye\n"
        
        return report


class TutorialManager:
    """Tutorial ve rehberlik yöneticisi"""
    
    def __init__(self):
        """Tutorial yöneticisini başlat"""
        self.completed_tutorials = self.load_completed()
        self.achievements = self.load_achievements()
        
    def load_completed(self) -> List[str]:
        """Tamamlanan tutorial'ları yükle"""
        try:
            if os.path.exists('tutorials.json'):
                with open('tutorials.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('completed', [])
        except:
            pass
        return []
        
    def save_completed(self):
        """Tamamlanan tutorial'ları kaydet"""
        try:
            with open('tutorials.json', 'w', encoding='utf-8') as f:
                json.dump({'completed': self.completed_tutorials}, f, indent=4)
        except Exception as e:
            Logger.error(f"Tutorial kayıt hatası: {e}")
            
    def mark_completed(self, tutorial_id: str):
        """Tutorial'ı tamamlandı olarak işaretle"""
        if tutorial_id not in self.completed_tutorials:
            self.completed_tutorials.append(tutorial_id)
            self.save_completed()
            
    def is_completed(self, tutorial_id: str) -> bool:
        """Tutorial tamamlandı mı?"""
        return tutorial_id in self.completed_tutorials
        
    def get_tutorial_text(self, tutorial_id: str) -> str:
        """Tutorial metnini döndür"""
        tutorials = {
            'first_game': """
🎮 WORDLE'A HOŞ GELDİNİZ!

Nasıl Oynanır:
1️⃣ Gizli kelimeyi tahmin edin
2️⃣ Her tahmin sonrası renk ipuçları:
   🟩 Yeşil: Doğru harf, doğru yer
   🟨 Sarı: Doğru harf, yanlış yer
   ⬜ Gri: Yanlış harf
3️⃣ Sınırlı tahmin hakkınız var
4️⃣ Kelimeyi bulmaya çalışın!

İpuçları:
• Yaygın harflerle başlayın
• Sarı harfleri farklı yerlere deneyin
• Yeşil harfleri sabit tutun

İyi şanslar! 🍀
            """,
            
            'keyboard_colors': """
⌨️ KLAVYE RENK SİSTEMİ

Klavye tuşları da renklenir:
🟩 Yeşil tuş: Bu harf doğru kullanıldı
🟨 Sarı tuş: Bu harf başka yerde
⬜ Gri tuş: Bu harf yok, kullanmayın

Bu sayede hangi harfleri
kullandığınızı takip edebilirsiniz!
            """,
            
            'statistics': """
📊 İSTATİSTİKLER

Performansınızı takip edin:
• Kazanma oranı
• Ortalama tahmin sayısı
• En iyi oyun
• Seri rekoru

İstatistikler Ekranı:
Ana Menü → İSTATİSTİKLER
            """
        }
        
        return tutorials.get(tutorial_id, "")
        
    def load_achievements(self) -> Dict:
        """Başarıları yükle"""
        default_achievements = {
            'first_win': {'unlocked': False, 'title': 'İlk Zafer'},
            'win_streak_5': {'unlocked': False, 'title': '5 Oyun Serisi'},
            'win_streak_10': {'unlocked': False, 'title': '10 Oyun Serisi'},
            'perfect_game': {'unlocked': False, 'title': 'Mükemmel Oyun'},
            'speed_demon': {'unlocked': False, 'title': 'Hız Canavarı'},
            'word_master': {'unlocked': False, 'title': 'Kelime Ustası'},
        }
        
        try:
            if os.path.exists('achievements.json'):
                with open('achievements.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
            
        return default_achievements
        
    def unlock_achievement(self, achievement_id: str) -> bool:
        """
        Başarı kilidi aç
        
        Returns:
            Yeni açıldıysa True
        """
        if achievement_id in self.achievements:
            if not self.achievements[achievement_id]['unlocked']:
                self.achievements[achievement_id]['unlocked'] = True
                self.save_achievements()
                return True
        return False
        
    def save_achievements(self):
        """Başarıları kaydet"""
        try:
            with open('achievements.json', 'w', encoding='utf-8') as f:
                json.dump(self.achievements, f, indent=4)
        except Exception as e:
            Logger.error(f"Başarı kayıt hatası: {e}")


# Test
if __name__ == '__main__':
    print("=== Erişilebilirlik ve Metrik Testleri ===\n")
    
    # Erişilebilirlik
    print("1. Erişilebilirlik Testi")
    accessibility = AccessibilityManager()
    print(f"   Screen Reader: {accessibility.screen_reader_enabled}")
    print(f"   Font Çarpanı: {accessibility.font_size_multiplier}x")
    
    # Metrikler
    print("\n2. Metrik Testi")
    metrics = GameMetrics()
    metrics.record_game_start(5, 'tr', 'classic')
    metrics.record_fps(60.0)
    metrics.record_memory(45.5)
    metrics.record_game_end(completed=True)
    
    summary = metrics.get_session_summary()
    print(f"   Oynanan Oyun: {summary['games_played']}")
    print(f"   Ortalama FPS: {summary['average_fps']:.1f}")
    
    # Tutorial
    print("\n3. Tutorial Testi")
    tutorial = TutorialManager()
    tutorial.mark_completed('first_game')
    print(f"   İlk oyun tamamlandı: {tutorial.is_completed('first_game')}")
    
    print("\n✓ Testler tamamlandı!")

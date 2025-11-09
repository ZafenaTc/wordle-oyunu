"""
Ses Efektleri Yönetim Modülü
Oyun seslerini yükler ve çalar
"""

from kivy.core.audio import SoundLoader
from kivy.logger import Logger
import os
from typing import Dict, Optional


class SoundManager:
    """Ses efektlerini yöneten sınıf"""
    
    def __init__(self, sounds_dir: str = 'sounds', enabled: bool = True):
        """
        Ses yöneticisini başlat
        
        Args:
            sounds_dir: Ses dosyalarının klasörü
            enabled: Sesler aktif mi
        """
        self.sounds_dir = sounds_dir
        self.enabled = enabled
        self.sounds: Dict[str, Optional[object]] = {}
        self.volumes = {
            'key': 0.3,
            'correct': 0.5,
            'present': 0.4,
            'absent': 0.3,
            'win': 0.7,
            'lose': 0.5,
            'error': 0.4,
            'delete': 0.2,
            'enter': 0.3
        }
        
        # Ses dosyalarını yükle
        self.load_sounds()
        
    def load_sounds(self):
        """Tüm ses dosyalarını yükle"""
        sound_files = {
            'key': 'key.wav',
            'correct': 'correct.wav',
            'present': 'present.wav',
            'absent': 'absent.wav',
            'win': 'win.wav',
            'lose': 'lose.wav',
            'error': 'error.wav',
            'delete': 'delete.wav',
            'enter': 'enter.wav'
        }
        
        # Sounds klasörünü oluştur
        if not os.path.exists(self.sounds_dir):
            os.makedirs(self.sounds_dir)
            Logger.warning(f"SoundManager: '{self.sounds_dir}' klasörü oluşturuldu")
            Logger.warning("SoundManager: Ses dosyalarını bu klasöre ekleyin")
        
        # Her ses dosyasını yüklemeye çalış
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(self.sounds_dir, filename)
            
            if os.path.exists(filepath):
                try:
                    sound = SoundLoader.load(filepath)
                    if sound:
                        sound.volume = self.volumes.get(sound_name, 0.5)
                        self.sounds[sound_name] = sound
                        Logger.info(f"SoundManager: '{filename}' yüklendi")
                    else:
                        Logger.warning(f"SoundManager: '{filename}' yüklenemedi")
                        self.sounds[sound_name] = None
                except Exception as e:
                    Logger.error(f"SoundManager: '{filename}' yüklenirken hata: {e}")
                    self.sounds[sound_name] = None
            else:
                Logger.warning(f"SoundManager: '{filepath}' bulunamadı")
                self.sounds[sound_name] = None
                
    def play(self, sound_name: str):
        """
        Ses çal
        
        Args:
            sound_name: Ses adı (key, correct, present, absent, win, lose, error, delete, enter)
        """
        if not self.enabled:
            return
            
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                # Ses zaten çalıyorsa durdur ve baştan başlat
                if self.sounds[sound_name].state == 'play':
                    self.sounds[sound_name].stop()
                self.sounds[sound_name].play()
            except Exception as e:
                Logger.error(f"SoundManager: '{sound_name}' çalınırken hata: {e}")
        else:
            Logger.debug(f"SoundManager: '{sound_name}' sesi bulunamadı veya yüklenmedi")
            
    def play_key_sound(self):
        """Tuş basma sesi çal"""
        self.play('key')
        
    def play_correct_sound(self):
        """Doğru harf sesi çal"""
        self.play('correct')
        
    def play_present_sound(self):
        """Yanlış pozisyon sesi çal"""
        self.play('present')
        
    def play_absent_sound(self):
        """Yanlış harf sesi çal"""
        self.play('absent')
        
    def play_win_sound(self):
        """Kazanma sesi çal"""
        self.play('win')
        
    def play_lose_sound(self):
        """Kaybetme sesi çal"""
        self.play('lose')
        
    def play_error_sound(self):
        """Hata sesi çal"""
        self.play('error')
        
    def play_delete_sound(self):
        """Silme sesi çal"""
        self.play('delete')
        
    def play_enter_sound(self):
        """Enter sesi çal"""
        self.play('enter')
        
    def set_volume(self, sound_name: str, volume: float):
        """
        Ses seviyesini ayarla
        
        Args:
            sound_name: Ses adı
            volume: Ses seviyesi (0.0 - 1.0)
        """
        volume = max(0.0, min(1.0, volume))  # 0-1 arası sınırla
        self.volumes[sound_name] = volume
        
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].volume = volume
            
    def set_master_volume(self, volume: float):
        """
        Ana ses seviyesini ayarla
        
        Args:
            volume: Ses seviyesi (0.0 - 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        
        for sound_name, sound in self.sounds.items():
            if sound:
                base_volume = self.volumes.get(sound_name, 0.5)
                sound.volume = base_volume * volume
                
    def enable(self):
        """Sesleri aktif et"""
        self.enabled = True
        Logger.info("SoundManager: Sesler aktif edildi")
        
    def disable(self):
        """Sesleri deaktif et"""
        self.enabled = False
        # Çalan sesleri durdur
        for sound in self.sounds.values():
            if sound and sound.state == 'play':
                sound.stop()
        Logger.info("SoundManager: Sesler deaktif edildi")
        
    def toggle(self) -> bool:
        """
        Sesleri aç/kapa
        
        Returns:
            Yeni durum (True: aktif, False: deaktif)
        """
        if self.enabled:
            self.disable()
        else:
            self.enable()
        return self.enabled
        
    def stop_all(self):
        """Tüm sesleri durdur"""
        for sound in self.sounds.values():
            if sound and sound.state == 'play':
                sound.stop()
                
    def reload_sounds(self):
        """Sesleri yeniden yükle"""
        self.stop_all()
        self.sounds.clear()
        self.load_sounds()
        Logger.info("SoundManager: Sesler yeniden yüklendi")
        
    def get_sound_status(self) -> Dict[str, bool]:
        """
        Ses durumlarını döndür
        
        Returns:
            {ses_adı: yüklendi_mi} dictionary'si
        """
        return {
            name: (sound is not None) 
            for name, sound in self.sounds.items()
        }
        
    def create_dummy_sounds(self):
        """
        Test için basit ses dosyaları oluştur
        NOT: Bu fonksiyon sadece geliştirme amaçlıdır
        """
        try:
            import numpy as np
            from scipy.io import wavfile
            
            # Ses klasörünü oluştur
            if not os.path.exists(self.sounds_dir):
                os.makedirs(self.sounds_dir)
            
            # Basit ses dalgaları oluştur
            sample_rate = 44100
            
            sounds_to_create = {
                'key': (440, 0.1),      # A notası, 0.1 saniye
                'correct': (523, 0.2),  # C notası, 0.2 saniye
                'present': (392, 0.15), # G notası, 0.15 saniye
                'absent': (349, 0.1),   # F notası, 0.1 saniye
                'win': (659, 0.5),      # E notası, 0.5 saniye
                'lose': (294, 0.3),     # D notası, 0.3 saniye
                'error': (220, 0.15),   # A notası (düşük), 0.15 saniye
                'delete': (330, 0.08),  # E notası (düşük), 0.08 saniye
                'enter': (494, 0.12)    # B notası, 0.12 saniye
            }
            
            for name, (freq, duration) in sounds_to_create.items():
                # Sinüs dalgası oluştur
                t = np.linspace(0, duration, int(sample_rate * duration))
                wave = np.sin(2 * np.pi * freq * t)
                
                # Fade out ekle
                fade_samples = int(0.02 * sample_rate)  # 20ms fade
                fade = np.linspace(1, 0, fade_samples)
                wave[-fade_samples:] *= fade
                
                # 16-bit integer'a çevir
                wave = (wave * 32767).astype(np.int16)
                
                # WAV dosyası olarak kaydet
                filepath = os.path.join(self.sounds_dir, f'{name}.wav')
                wavfile.write(filepath, sample_rate, wave)
                
            Logger.info("SoundManager: Test ses dosyaları oluşturuldu")
            return True
            
        except ImportError:
            Logger.error("SoundManager: numpy ve scipy gerekli (pip install numpy scipy)")
            return False
        except Exception as e:
            Logger.error(f"SoundManager: Ses dosyaları oluşturulurken hata: {e}")
            return False


# Test fonksiyonu
if __name__ == '__main__':
    """Modül testleri"""
    print("=== Ses Yöneticisi Test ===\n")
    
    # Ses yöneticisini oluştur
    sound_manager = SoundManager(sounds_dir='test_sounds')
    
    # Durum kontrolü
    print("=== Ses Durumları ===")
    status = sound_manager.get_sound_status()
    for sound_name, loaded in status.items():
        status_text = "✓ Yüklendi" if loaded else "✗ Yüklenmedi"
        print(f"{sound_name}: {status_text}")
    
    # Test sesleri oluştur (opsiyonel)
    print("\n=== Test Sesleri Oluşturma ===")
    try:
        if sound_manager.create_dummy_sounds():
            print("✓ Test sesleri oluşturuldu")
            # Yeniden yükle
            sound_manager.reload_sounds()
        else:
            print("✗ Test sesleri oluşturulamadı (numpy/scipy yok)")
    except:
        print("✗ Test sesleri oluşturulamadı")
    
    # Ses çalma testi
    print("\n=== Ses Çalma Testi ===")
    print("Sesler çalınıyor... (ses dosyaları varsa)")
    
    import time
    
    test_sounds = [
        ('key', 'Tuş sesi'),
        ('correct', 'Doğru sesi'),
        ('present', 'Mevcut sesi'),
        ('absent', 'Yok sesi'),
        ('win', 'Kazanma sesi')
    ]
    
    for sound_name, description in test_sounds:
        print(f"  ▶ {description}...")
        sound_manager.play(sound_name)
        time.sleep(0.5)
    
    # Ses kontrolü
    print("\n=== Ses Kontrolü ===")
    print(f"Sesler: {'Aktif' if sound_manager.enabled else 'Deaktif'}")
    
    sound_manager.toggle()
    print(f"Toggle sonrası: {'Aktif' if sound_manager.enabled else 'Deaktif'}")
    
    # Ses seviyesi ayarlama
    print("\n=== Ses Seviyesi ===")
    sound_manager.set_master_volume(0.5)
    print("Ana ses seviyesi: 50%")
    
    # Temizlik
    print("\n=== Temizlik ===")
    sound_manager.stop_all()
    if os.path.exists('test_sounds'):
        import shutil
        shutil.rmtree('test_sounds')
        print("✓ Test klasörü silindi")
    
    print("\n✓ Testler tamamlandı!")

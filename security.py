"""
Güvenlik Modülü
Kelime listesi şifreleme ve önbellek optimizasyonu
"""

import base64
import hashlib
import json
import os
from typing import List, Optional
from functools import lru_cache


class WordEncryption:
    """Kelime listesi şifreleme sınıfı"""
    
    def __init__(self, key: Optional[str] = None):
        """
        Şifreleme yöneticisini başlat
        
        Args:
            key: Şifreleme anahtarı (None ise otomatik oluşturulur)
        """
        if key is None:
            # Basit bir anahtar oluştur (gerçek uygulamada daha güvenli olmalı)
            key = "WORDLE_SECRET_KEY_2024"
        self.key = key.encode('utf-8')
        
    def encrypt_word(self, word: str) -> str:
        """
        Kelimeyi şifrele
        
        Args:
            word: Şifrelenecek kelime
            
        Returns:
            Şifrelenmiş kelime (base64)
        """
        # Basit XOR şifreleme (güvenlik için AES kullanılmalı)
        word_bytes = word.encode('utf-8')
        encrypted = bytearray()
        
        for i, byte in enumerate(word_bytes):
            key_byte = self.key[i % len(self.key)]
            encrypted.append(byte ^ key_byte)
            
        return base64.b64encode(bytes(encrypted)).decode('utf-8')
        
    def decrypt_word(self, encrypted_word: str) -> str:
        """
        Kelimeyi çöz
        
        Args:
            encrypted_word: Şifrelenmiş kelime (base64)
            
        Returns:
            Çözülmüş kelime
        """
        try:
            encrypted_bytes = base64.b64decode(encrypted_word.encode('utf-8'))
            decrypted = bytearray()
            
            for i, byte in enumerate(encrypted_bytes):
                key_byte = self.key[i % len(self.key)]
                decrypted.append(byte ^ key_byte)
                
            return bytes(decrypted).decode('utf-8')
        except Exception as e:
            print(f"Çözümleme hatası: {e}")
            return ""
            
    def encrypt_word_list(self, words: List[str]) -> List[str]:
        """
        Kelime listesini şifrele
        
        Args:
            words: Kelime listesi
            
        Returns:
            Şifrelenmiş kelime listesi
        """
        return [self.encrypt_word(word) for word in words]
        
    def decrypt_word_list(self, encrypted_words: List[str]) -> List[str]:
        """
        Kelime listesini çöz
        
        Args:
            encrypted_words: Şifrelenmiş kelime listesi
            
        Returns:
            Çözülmüş kelime listesi
        """
        return [self.decrypt_word(word) for word in encrypted_words]
        
    def save_encrypted_words(self, words: List[str], filename: str):
        """
        Şifrelenmiş kelimeleri dosyaya kaydet
        
        Args:
            words: Kelime listesi
            filename: Dosya adı
        """
        encrypted = self.encrypt_word_list(words)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'encrypted': True,
                    'words': encrypted
                }, f, indent=2)
            print(f"✓ {len(words)} kelime şifrelenerek {filename} dosyasına kaydedildi")
        except Exception as e:
            print(f"✗ Kaydetme hatası: {e}")
            
    def load_encrypted_words(self, filename: str) -> List[str]:
        """
        Şifrelenmiş kelimeleri dosyadan yükle
        
        Args:
            filename: Dosya adı
            
        Returns:
            Çözülmüş kelime listesi
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if data.get('encrypted'):
                decrypted = self.decrypt_word_list(data['words'])
                print(f"✓ {len(decrypted)} kelime {filename} dosyasından yüklendi")
                return decrypted
            else:
                print(f"! {filename} şifrelenmemiş")
                return []
                
        except FileNotFoundError:
            print(f"✗ {filename} bulunamadı")
            return []
        except Exception as e:
            print(f"✗ Yükleme hatası: {e}")
            return []


class WordCache:
    """Kelime listesi önbellek yöneticisi"""
    
    def __init__(self, cache_size: int = 128):
        """
        Önbellek yöneticisini başlat
        
        Args:
            cache_size: Önbellek boyutu
        """
        self.cache_size = cache_size
        self._cache = {}
        self._access_count = {}
        
    @lru_cache(maxsize=128)
    def get_word_hash(self, word: str) -> str:
        """
        Kelime için hash oluştur
        
        Args:
            word: Kelime
            
        Returns:
            SHA256 hash
        """
        return hashlib.sha256(word.encode('utf-8')).hexdigest()[:16]
        
    def cache_words(self, key: str, words: List[str]):
        """
        Kelimeleri önbelleğe al
        
        Args:
            key: Önbellek anahtarı
            words: Kelime listesi
        """
        if len(self._cache) >= self.cache_size:
            # LRU stratejisi: En az kullanılanı sil
            least_used = min(self._access_count.items(), key=lambda x: x[1])
            del self._cache[least_used[0]]
            del self._access_count[least_used[0]]
            
        self._cache[key] = words
        self._access_count[key] = 0
        
    def get_cached_words(self, key: str) -> Optional[List[str]]:
        """
        Önbellekten kelimeleri al
        
        Args:
            key: Önbellek anahtarı
            
        Returns:
            Kelime listesi veya None
        """
        if key in self._cache:
            self._access_count[key] += 1
            return self._cache[key]
        return None
        
    def is_cached(self, key: str) -> bool:
        """
        Önbellekte var mı kontrol et
        
        Args:
            key: Önbellek anahtarı
            
        Returns:
            Önbellekte varsa True
        """
        return key in self._cache
        
    def clear_cache(self):
        """Önbelleği temizle"""
        self._cache.clear()
        self._access_count.clear()
        print("✓ Önbellek temizlendi")
        
    def get_cache_stats(self) -> dict:
        """
        Önbellek istatistiklerini döndür
        
        Returns:
            İstatistik dictionary'si
        """
        return {
            'total_items': len(self._cache),
            'cache_size': self.cache_size,
            'usage_percent': (len(self._cache) / self.cache_size) * 100,
            'access_counts': dict(self._access_count)
        }


class SecureWordManager:
    """Güvenli kelime yöneticisi - Şifreleme ve önbellek ile"""
    
    def __init__(self, encryption_key: Optional[str] = None, cache_size: int = 128):
        """
        Güvenli kelime yöneticisini başlat
        
        Args:
            encryption_key: Şifreleme anahtarı
            cache_size: Önbellek boyutu
        """
        self.encryption = WordEncryption(encryption_key)
        self.cache = WordCache(cache_size)
        
    def convert_plaintext_to_encrypted(self, input_file: str, output_file: str):
        """
        Düz metin kelime listesini şifreli hale çevir
        
        Args:
            input_file: Giriş dosyası (düz metin)
            output_file: Çıkış dosyası (şifreli JSON)
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                words = [line.strip().upper() for line in f if line.strip()]
                
            self.encryption.save_encrypted_words(words, output_file)
            print(f"✓ {input_file} → {output_file} dönüştürüldü")
            
        except Exception as e:
            print(f"✗ Dönüştürme hatası: {e}")
            
    def load_words_secure(self, filename: str, word_length: int) -> List[str]:
        """
        Kelimeleri güvenli şekilde yükle (önbellekle)
        
        Args:
            filename: Dosya adı
            word_length: Kelime uzunluğu
            
        Returns:
            Kelime listesi
        """
        cache_key = f"{filename}_{word_length}"
        
        # Önbellekte var mı kontrol et
        cached = self.cache.get_cached_words(cache_key)
        if cached:
            print(f"✓ Önbellekten yüklendi: {len(cached)} kelime")
            return cached
            
        # Şifreli dosyadan yükle
        all_words = self.encryption.load_encrypted_words(filename)
        
        # İstenen uzunluktaki kelimeleri filtrele
        filtered_words = [w for w in all_words if len(w) == word_length]
        
        # Önbelleğe al
        self.cache.cache_words(cache_key, filtered_words)
        
        return filtered_words
        
    def get_cache_info(self):
        """Önbellek bilgilerini döndür"""
        return self.cache.get_cache_stats()


# Test fonksiyonu
if __name__ == '__main__':
    """Modül testleri"""
    print("=== Güvenlik Modülü Test ===\n")
    
    # 1. Şifreleme testi
    print("=== Şifreleme Testi ===")
    encryption = WordEncryption()
    
    test_words = ['ELMA', 'ARMUT', 'KARPUZ', 'PORTAKAL', 'MANGO']
    print(f"Orijinal kelimeler: {test_words}")
    
    encrypted = encryption.encrypt_word_list(test_words)
    print(f"Şifrelenmiş: {encrypted[:2]}...")  # İlk 2'si
    
    decrypted = encryption.decrypt_word_list(encrypted)
    print(f"Çözülmüş: {decrypted}")
    print(f"Başarılı: {'✓' if decrypted == test_words else '✗'}\n")
    
    # 2. Önbellek testi
    print("=== Önbellek Testi ===")
    cache = WordCache(cache_size=3)
    
    cache.cache_words('tr_5', ['ELMA', 'ARMUT'])
    cache.cache_words('en_5', ['APPLE', 'GRAPE'])
    cache.cache_words('tr_6', ['KARPUZ', 'KAVUN'])
    
    print(f"Önbellek boyutu: {len(cache._cache)}")
    print(f"tr_5 önbellekte: {cache.is_cached('tr_5')}")
    
    # Erişim
    words = cache.get_cached_words('tr_5')
    print(f"tr_5 kelimeleri: {words}")
    
    # LRU testi - 4. öğe eklendiğinde en az kullanılan silinmeli
    cache.cache_words('en_6', ['ORANGE', 'BANANA'])
    print(f"4. eklemeden sonra önbellek boyutu: {len(cache._cache)}")
    
    stats = cache.get_cache_stats()
    print(f"Önbellek doluluk: {stats['usage_percent']:.1f}%\n")
    
    # 3. Güvenli yönetici testi
    print("=== Güvenli Yönetici Testi ===")
    manager = SecureWordManager()
    
    # Test dosyası oluştur
    test_file = 'test_words.txt'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(['ELMA', 'ARMUT', 'KARPUZ', 'PORTAKAL', 'MANGO']))
    
    # Şifreli dosyaya çevir
    encrypted_file = 'test_words_encrypted.json'
    manager.convert_plaintext_to_encrypted(test_file, encrypted_file)
    
    # Yükle
    words = manager.load_words_secure(encrypted_file, 5)
    print(f"Yüklenen 5 harfli kelimeler: {words}")
    
    # Önbellek bilgisi
    cache_info = manager.get_cache_info()
    print(f"Önbellek kullanımı: {cache_info['usage_percent']:.1f}%")
    
    # Temizlik
    print("\n=== Temizlik ===")
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(encrypted_file):
        os.remove(encrypted_file)
    print("✓ Test dosyaları silindi")
    
    print("\n✓ Tüm testler tamamlandı!")

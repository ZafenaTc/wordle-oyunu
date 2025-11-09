"""
Kelime Yönetim Modülü
Kelime listelerini okur, önbelleğe alır ve rastgele kelime seçer
"""

import random
import os
from typing import Optional, List


class WordManager:
    """Kelime listelerini yöneten sınıf"""
    
    def __init__(self):
        """Kelime yöneticisini başlat"""
        self.word_cache = {
            'tr': {5: [], 6: [], 7: []},
            'en': {5: [], 6: [], 7: []}
        }
        self.cache_loaded = {
            'tr': {5: False, 6: False, 7: False},
            'en': {5: False, 6: False, 7: False}
        }
        
    def load_words(self, word_length: int, language: str) -> List[str]:
        """
        Belirtilen uzunluk ve dildeki kelimeleri yükle
        
        Args:
            word_length: Kelime uzunluğu (5, 6 veya 7)
            language: Dil kodu ('tr' veya 'en')
            
        Returns:
            Kelime listesi
        """
        # Önbellekte varsa direkt dön
        if self.cache_loaded[language][word_length]:
            return self.word_cache[language][word_length]
            
        # Dosya adını oluştur
        filename = f'kelimeler_{language}.txt'
        
        if not os.path.exists(filename):
            print(f"HATA: {filename} bulunamadı!")
            return []
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                # Tüm kelimeleri oku ve normalize et
                all_words = []
                for line in f:
                    word = line.strip().upper()
                    if word and len(word) == word_length:
                        # Sadece harf içeren kelimeleri al
                        if self.is_valid_word(word, language):
                            all_words.append(word)
                            
                # Önbelleğe al
                self.word_cache[language][word_length] = all_words
                self.cache_loaded[language][word_length] = True
                
                print(f"{language.upper()} - {word_length} harfli {len(all_words)} kelime yüklendi")
                return all_words
                
        except Exception as e:
            print(f"Kelimeler yüklenirken hata: {e}")
            return []
            
    def is_valid_word(self, word: str, language: str) -> bool:
        """
        Kelimenin geçerli olup olmadığını kontrol et
        
        Args:
            word: Kontrol edilecek kelime
            language: Dil kodu
            
        Returns:
            Geçerli ise True
        """
        if language == 'tr':
            # Türkçe karakterler
            valid_chars = set('ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ')
        else:
            # İngilizce karakterler
            valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            
        return all(c in valid_chars for c in word)
        
    def get_random_word(self, word_length: int, language: str) -> Optional[str]:
        """
        Rastgele bir kelime seç
        
        Args:
            word_length: Kelime uzunluğu
            language: Dil kodu
            
        Returns:
            Rastgele seçilen kelime veya None
        """
        words = self.load_words(word_length, language)
        
        if not words:
            print(f"UYARI: {language.upper()} dilinde {word_length} harfli kelime bulunamadı!")
            return None
            
        return random.choice(words)
        
    def is_word_in_list(self, word: str, word_length: int, language: str) -> bool:
        """
        Kelimenin listede olup olmadığını kontrol et
        
        Args:
            word: Kontrol edilecek kelime
            word_length: Kelime uzunluğu
            language: Dil kodu
            
        Returns:
            Listede ise True
        """
        words = self.load_words(word_length, language)
        return word.upper() in words
        
    def get_word_count(self, word_length: int, language: str) -> int:
        """
        Belirtilen kategorideki kelime sayısını döndür
        
        Args:
            word_length: Kelime uzunluğu
            language: Dil kodu
            
        Returns:
            Kelime sayısı
        """
        words = self.load_words(word_length, language)
        return len(words)
        
    def clear_cache(self):
        """Önbelleği temizle"""
        self.word_cache = {
            'tr': {5: [], 6: [], 7: []},
            'en': {5: [], 6: [], 7: []}
        }
        self.cache_loaded = {
            'tr': {5: False, 6: False, 7: False},
            'en': {5: False, 6: False, 7: False}
        }
        print("Kelime önbelleği temizlendi")


# Test fonksiyonu
if __name__ == '__main__':
    """Modül testleri"""
    manager = WordManager()
    
    print("=== Kelime Yöneticisi Test ===\n")
    
    # Türkçe kelimeler
    print("Türkçe Kelimeler:")
    for length in [5, 6, 7]:
        count = manager.get_word_count(length, 'tr')
        print(f"  {length} harfli: {count} kelime")
        if count > 0:
            word = manager.get_random_word(length, 'tr')
            print(f"  Örnek: {word}")
    
    print("\nİngilizce Kelimeler:")
    for length in [5, 6, 7]:
        count = manager.get_word_count(length, 'en')
        print(f"  {length} harfli: {count} kelime")
        if count > 0:
            word = manager.get_random_word(length, 'en')
            print(f"  Örnek: {word}")
    
    # Kelime kontrolü
    print("\n=== Kelime Kontrolü ===")
    test_words = [
        ('ELMA', 4, 'tr'),
        ('ELMALAR', 7, 'tr'),
        ('APPLE', 5, 'en'),
        ('HOUSE', 5, 'en')
    ]
    
    for word, length, lang in test_words:
        exists = manager.is_word_in_list(word, length, lang)
        print(f"{word} ({lang}): {'✓ Var' if exists else '✗ Yok'}")

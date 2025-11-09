"""
Oyun Mantığı Modülü
Tahmin kontrolü, doğru/yanlış harf analizi ve oyun durumu yönetimi
"""

from typing import List, Optional, Tuple
from collections import Counter


class GameLogic:
    """Wordle oyun mantığını yöneten sınıf"""
    
    def __init__(self, secret_word: str, max_attempts: int):
        """
        Oyun mantığını başlat
        
        Args:
            secret_word: Tahmin edilecek gizli kelime
            max_attempts: Maksimum tahmin hakkı
        """
        self.secret_word = secret_word.upper()
        self.max_attempts = max_attempts
        self.current_attempt = 0
        self.guesses = []
        self.results = []
        self.won = False
        
        print(f"Oyun başlatıldı: {len(secret_word)} harfli kelime, {max_attempts} deneme hakkı")
        # DEBUG: Geliştirme sırasında gizli kelimeyi göster
        print(f"[DEBUG] Gizli kelime: {self.secret_word}")
        
    def make_guess(self, guess: str) -> Optional[List[str]]:
        """
        Tahmin yap ve sonucu döndür
        
        Args:
            guess: Tahmin edilen kelime
            
        Returns:
            Her harf için durum listesi ['correct', 'present', 'absent']
            Geçersiz tahmin ise None
        """
        guess = guess.upper()
        
        # Validasyon kontrolleri
        if len(guess) != len(self.secret_word):
            print(f"HATA: Tahmin uzunluğu yanlış ({len(guess)} != {len(self.secret_word)})")
            return None
            
        if self.is_game_over():
            print("HATA: Oyun zaten bitti!")
            return None
            
        # Tahmini kaydet
        self.guesses.append(guess)
        self.current_attempt += 1
        
        # Tahmin sonucunu hesapla
        result = self.evaluate_guess(guess)
        self.results.append(result)
        
        # Kazandı mı kontrol et
        if all(status == 'correct' for status in result):
            self.won = True
            print(f"TEBRİKLER! {self.current_attempt}. denemede doğru kelimeyi buldunuz!")
        elif self.current_attempt >= self.max_attempts:
            print(f"Oyun bitti! Doğru kelime: {self.secret_word}")
            
        return result
        
    def evaluate_guess(self, guess: str) -> List[str]:
        """
        Tahmini değerlendir ve her harf için durum döndür
        
        Wordle kuralları:
        1. Doğru konumdaki harfler yeşil (correct)
        2. Kelimede var ama yanlış konumdaki harfler sarı (present)
        3. Kelimede olmayan harfler gri (absent)
        4. Aynı harften birden fazla varsa:
           - Önce doğru konumdakiler işaretlenir
           - Kalan harfler için kelimede kalan miktar kadar sarı verilir
        
        Args:
            guess: Tahmin edilen kelime
            
        Returns:
            Her pozisyon için durum listesi
        """
        result = ['absent'] * len(guess)
        secret_chars = list(self.secret_word)
        
        # 1. Adım: Doğru konumdaki harfleri işaretle (correct)
        for i in range(len(guess)):
            if guess[i] == self.secret_word[i]:
                result[i] = 'correct'
                secret_chars[i] = None  # Bu harf kullanıldı
                
        # 2. Adım: Yanlış konumdaki harfleri işaretle (present)
        for i in range(len(guess)):
            if result[i] == 'correct':
                continue  # Zaten doğru işaretlendi
                
            # Bu harf kelimede başka yerde var mı?
            if guess[i] in secret_chars:
                result[i] = 'present'
                # İlk bulduğunu işaretle (tekrar sayılmaması için)
                idx = secret_chars.index(guess[i])
                secret_chars[idx] = None
                
        return result
        
    def is_game_over(self) -> bool:
        """
        Oyun bitti mi kontrol et
        
        Returns:
            Oyun bittiyse True
        """
        return self.won or self.current_attempt >= self.max_attempts
        
    def is_won(self) -> bool:
        """
        Oyun kazanıldı mı?
        
        Returns:
            Kazanıldıysa True
        """
        return self.won
        
    def get_remaining_attempts(self) -> int:
        """
        Kalan tahmin hakkını döndür
        
        Returns:
            Kalan deneme sayısı
        """
        return max(0, self.max_attempts - self.current_attempt)
        
    def get_guess_history(self) -> List[Tuple[str, List[str]]]:
        """
        Tahmin geçmişini döndür
        
        Returns:
            (tahmin, sonuç) tuple'larının listesi
        """
        return list(zip(self.guesses, self.results))
        
    def get_keyboard_state(self) -> dict:
        """
        Klavye tuşlarının durumunu döndür
        Her harf için en iyi durumu (correct > present > absent) sakla
        
        Returns:
            {harf: durum} dictionary'si
        """
        keyboard_state = {}
        
        for guess, result in zip(self.guesses, self.results):
            for letter, status in zip(guess, result):
                # Daha iyi duruma öncelik ver
                if letter not in keyboard_state:
                    keyboard_state[letter] = status
                elif status == 'correct':
                    keyboard_state[letter] = 'correct'
                elif status == 'present' and keyboard_state[letter] != 'correct':
                    keyboard_state[letter] = 'present'
                elif status == 'absent' and keyboard_state[letter] not in ['correct', 'present']:
                    keyboard_state[letter] = 'absent'
                    
        return keyboard_state
        
    def get_statistics(self) -> dict:
        """
        Oyun istatistiklerini döndür
        
        Returns:
            İstatistik dictionary'si
        """
        return {
            'secret_word': self.secret_word,
            'attempts_used': self.current_attempt,
            'max_attempts': self.max_attempts,
            'remaining_attempts': self.get_remaining_attempts(),
            'won': self.won,
            'guesses': self.guesses,
            'results': self.results
        }


# Test fonksiyonu
if __name__ == '__main__':
    """Modül testleri"""
    print("=== Oyun Mantığı Test ===\n")
    
    # Test 1: Basit oyun
    print("Test 1: ELMA kelimesi")
    game = GameLogic('ELMA', 6)
    
    test_guesses = [
        ('ARMA', ['absent', 'absent', 'correct', 'correct']),  # A,R yok | M,A doğru
        ('ALMA', ['correct', 'correct', 'correct', 'correct']),  # A,L,M,A hepsi doğru
    ]
    
    for guess, expected in test_guesses:
        result = game.make_guess(guess)
        print(f"\nTahmin: {guess}")
        print(f"Sonuç: {result}")
        print(f"Beklenen: {expected}")
        print(f"Doğru: {'✓' if result == expected else '✗'}")
        
        if game.is_won():
            print("OYUN KAZANILDI!")
            break
    
    # Test 2: Tekrar eden harfler
    print("\n\n=== Test 2: Tekrar eden harfler (BOOKS) ===")
    game2 = GameLogic('BOOKS', 6)
    
    test_cases = [
        ('ROBOT', ['absent', 'present', 'present', 'present', 'absent']),
        ('SPOON', ['present', 'absent', 'present', 'correct', 'absent']),
        ('BOOKS', ['correct', 'correct', 'correct', 'correct', 'correct']),
    ]
    
    for guess, expected in test_cases:
        result = game2.make_guess(guess)
        print(f"\nTahmin: {guess}")
        print(f"Sonuç: {result}")
        print(f"Beklenen: {expected}")
        print(f"Doğru: {'✓' if result == expected else '✗'}")
        
        if game2.is_won():
            print("OYUN KAZANILDI!")
            break
    
    # İstatistikler
    print("\n\n=== Oyun İstatistikleri ===")
    stats = game2.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Klavye durumu
    print("\n=== Klavye Durumu ===")
    keyboard = game2.get_keyboard_state()
    for letter, status in sorted(keyboard.items()):
        print(f"{letter}: {status}")

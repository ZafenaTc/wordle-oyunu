"""
İstatistik Yönetim Modülü
Oyuncu performansını takip eder ve analiz eder
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class Statistics:
    """Oyun istatistiklerini yöneten sınıf"""
    
    def __init__(self, stats_file: str = 'statistics.json'):
        """
        İstatistik yöneticisini başlat
        
        Args:
            stats_file: İstatistik dosyasının yolu
        """
        self.stats_file = stats_file
        self.stats = self.load_stats()
        
    def load_stats(self) -> Dict:
        """
        İstatistikleri dosyadan yükle
        
        Returns:
            İstatistik dictionary'si
        """
        default_stats = {
            'games_played': 0,
            'games_won': 0,
            'current_streak': 0,
            'max_streak': 0,
            'guess_distribution': {
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
                '6': 0,
                '7': 0
            },
            'total_guesses': 0,
            'best_game': None,  # En az tahminde kazanma
            'last_played': None,
            'by_word_length': {
                '5': {'played': 0, 'won': 0},
                '6': {'played': 0, 'won': 0},
                '7': {'played': 0, 'won': 0}
            },
            'by_language': {
                'tr': {'played': 0, 'won': 0},
                'en': {'played': 0, 'won': 0}
            }
        }
        
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    loaded_stats = json.load(f)
                    # Eksik anahtarları ekle
                    for key, value in default_stats.items():
                        if key not in loaded_stats:
                            loaded_stats[key] = value
                    return loaded_stats
            except Exception as e:
                print(f"İstatistikler yüklenirken hata: {e}")
                
        return default_stats
        
    def save_stats(self):
        """İstatistikleri dosyaya kaydet"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"İstatistikler kaydedilirken hata: {e}")
            
    def record_game(self, won: bool, attempts: int, word_length: int, language: str):
        """
        Oyun sonucunu kaydet
        
        Args:
            won: Oyun kazanıldı mı
            attempts: Kullanılan tahmin sayısı
            word_length: Kelime uzunluğu
            language: Oyun dili
        """
        self.stats['games_played'] += 1
        self.stats['last_played'] = datetime.now().isoformat()
        
        # Kelime uzunluğuna göre istatistik
        length_key = str(word_length)
        if length_key in self.stats['by_word_length']:
            self.stats['by_word_length'][length_key]['played'] += 1
            
        # Dile göre istatistik
        if language in self.stats['by_language']:
            self.stats['by_language'][language]['played'] += 1
        
        if won:
            self.stats['games_won'] += 1
            self.stats['current_streak'] += 1
            self.stats['total_guesses'] += attempts
            
            # Kelime uzunluğuna göre kazanma
            if length_key in self.stats['by_word_length']:
                self.stats['by_word_length'][length_key]['won'] += 1
                
            # Dile göre kazanma
            if language in self.stats['by_language']:
                self.stats['by_language'][language]['won'] += 1
            
            # Maksimum seriyi güncelle
            if self.stats['current_streak'] > self.stats['max_streak']:
                self.stats['max_streak'] = self.stats['current_streak']
            
            # Tahmin dağılımını güncelle
            attempt_key = str(attempts)
            if attempt_key in self.stats['guess_distribution']:
                self.stats['guess_distribution'][attempt_key] += 1
            
            # En iyi oyunu güncelle
            if self.stats['best_game'] is None or attempts < self.stats['best_game']:
                self.stats['best_game'] = attempts
        else:
            # Kaybedildiğinde seriyi sıfırla
            self.stats['current_streak'] = 0
            
        self.save_stats()
        
    def get_win_rate(self) -> float:
        """
        Kazanma oranını hesapla
        
        Returns:
            Kazanma oranı (0-100)
        """
        if self.stats['games_played'] == 0:
            return 0.0
        return (self.stats['games_won'] / self.stats['games_played']) * 100
        
    def get_average_guesses(self) -> float:
        """
        Ortalama tahmin sayısını hesapla
        
        Returns:
            Ortalama tahmin sayısı
        """
        if self.stats['games_won'] == 0:
            return 0.0
        return self.stats['total_guesses'] / self.stats['games_won']
        
    def get_guess_distribution(self) -> Dict[str, int]:
        """
        Tahmin dağılımını döndür
        
        Returns:
            {tahmin_sayısı: oyun_sayısı} dictionary'si
        """
        return self.stats['guess_distribution']
        
    def get_distribution_percentages(self) -> Dict[str, float]:
        """
        Tahmin dağılımını yüzde olarak hesapla
        
        Returns:
            {tahmin_sayısı: yüzde} dictionary'si
        """
        total = self.stats['games_won']
        if total == 0:
            return {k: 0.0 for k in self.stats['guess_distribution'].keys()}
            
        return {
            k: (v / total) * 100 
            for k, v in self.stats['guess_distribution'].items()
        }
        
    def get_summary(self) -> Dict:
        """
        Özet istatistikleri döndür
        
        Returns:
            Özet istatistik dictionary'si
        """
        return {
            'games_played': self.stats['games_played'],
            'games_won': self.stats['games_won'],
            'win_rate': round(self.get_win_rate(), 1),
            'current_streak': self.stats['current_streak'],
            'max_streak': self.stats['max_streak'],
            'average_guesses': round(self.get_average_guesses(), 2),
            'best_game': self.stats['best_game'],
            'last_played': self.stats['last_played']
        }
        
    def get_detailed_stats(self) -> Dict:
        """
        Detaylı istatistikleri döndür
        
        Returns:
            Detaylı istatistik dictionary'si
        """
        summary = self.get_summary()
        summary['guess_distribution'] = self.get_guess_distribution()
        summary['distribution_percentages'] = self.get_distribution_percentages()
        summary['by_word_length'] = self.stats['by_word_length']
        summary['by_language'] = self.stats['by_language']
        return summary
        
    def reset_stats(self):
        """Tüm istatistikleri sıfırla"""
        self.stats = {
            'games_played': 0,
            'games_won': 0,
            'current_streak': 0,
            'max_streak': 0,
            'guess_distribution': {
                '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0
            },
            'total_guesses': 0,
            'best_game': None,
            'last_played': None,
            'by_word_length': {
                '5': {'played': 0, 'won': 0},
                '6': {'played': 0, 'won': 0},
                '7': {'played': 0, 'won': 0}
            },
            'by_language': {
                'tr': {'played': 0, 'won': 0},
                'en': {'played': 0, 'won': 0}
            }
        }
        self.save_stats()
        print("İstatistikler sıfırlandı")
        
    def export_stats(self, filename: str = 'stats_export.json'):
        """
        İstatistikleri dışa aktar
        
        Args:
            filename: Dışa aktarma dosyası
        """
        try:
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'statistics': self.stats
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            print(f"İstatistikler {filename} dosyasına aktarıldı")
        except Exception as e:
            print(f"İstatistikler dışa aktarılırken hata: {e}")


# Test fonksiyonu
if __name__ == '__main__':
    """Modül testleri"""
    print("=== İstatistik Sistemi Test ===\n")
    
    stats = Statistics('test_statistics.json')
    
    # Örnek oyunlar kaydet
    print("Örnek oyunlar kaydediliyor...")
    stats.record_game(won=True, attempts=3, word_length=5, language='tr')
    stats.record_game(won=True, attempts=4, word_length=5, language='tr')
    stats.record_game(won=False, attempts=6, word_length=6, language='en')
    stats.record_game(won=True, attempts=2, word_length=5, language='tr')
    stats.record_game(won=True, attempts=5, word_length=7, language='en')
    
    # Özet istatistikleri göster
    print("\n=== Özet İstatistikler ===")
    summary = stats.get_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # Tahmin dağılımı
    print("\n=== Tahmin Dağılımı ===")
    distribution = stats.get_guess_distribution()
    percentages = stats.get_distribution_percentages()
    
    for attempt, count in sorted(distribution.items()):
        if count > 0:
            percentage = percentages[attempt]
            bar = '█' * int(percentage / 5)  # Her 5% bir bar
            print(f"{attempt} tahmin: {count} oyun ({percentage:.1f}%) {bar}")
    
    # Kelime uzunluğuna göre
    print("\n=== Kelime Uzunluğuna Göre ===")
    for length, data in stats.stats['by_word_length'].items():
        if data['played'] > 0:
            win_rate = (data['won'] / data['played']) * 100
            print(f"{length} harf: {data['played']} oyun, {data['won']} kazanma ({win_rate:.1f}%)")
    
    # Dile göre
    print("\n=== Dile Göre ===")
    for lang, data in stats.stats['by_language'].items():
        if data['played'] > 0:
            win_rate = (data['won'] / data['played']) * 100
            print(f"{lang.upper()}: {data['played']} oyun, {data['won']} kazanma ({win_rate:.1f}%)")
    
    # Dışa aktar
    print("\n=== Dışa Aktarma ===")
    stats.export_stats('test_export.json')
    
    # Temizlik
    print("\n=== Temizlik ===")
    if os.path.exists('test_statistics.json'):
        os.remove('test_statistics.json')
    if os.path.exists('test_export.json'):
        os.remove('test_export.json')
    print("Test dosyaları silindi")

"""
Wordle Oyunu - Unit Testler
Tüm modüller için kapsamlı testler
"""

import unittest
import os
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock

# Modülleri import et
from game_logic import GameLogic
from words import WordManager
from statistics import Statistics
from themes import ThemeManager, Theme
from security import WordEncryption, WordCache, SecureWordManager


class TestGameLogic(unittest.TestCase):
    """Oyun mantığı testleri"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        self.game = GameLogic('ELMA', 6)
        
    def test_initialization(self):
        """Başlangıç testi"""
        self.assertEqual(self.game.secret_word, 'ELMA')
        self.assertEqual(self.game.max_attempts, 6)
        self.assertEqual(self.game.current_attempt, 0)
        self.assertFalse(self.game.won)
        
    def test_evaluate_guess_all_correct(self):
        """Tüm harfler doğru"""
        result = self.game.evaluate_guess('ELMA')
        expected = ['correct', 'correct', 'correct', 'correct']
        self.assertEqual(result, expected)
        
    def test_evaluate_guess_partial(self):
        """Kısmi doğru"""
        result = self.game.evaluate_guess('ALMA')
        # A doğru, L doğru, M doğru, A doğru
        self.assertEqual(result[0], 'present')  # A yanlış yerde
        self.assertEqual(result[1], 'correct')   # L doğru yerde
        self.assertEqual(result[2], 'correct')   # M doğru yerde
        self.assertEqual(result[3], 'correct')   # A doğru yerde
        
    def test_evaluate_guess_all_wrong(self):
        """Tüm harfler yanlış"""
        result = self.game.evaluate_guess('XYZT')
        expected = ['absent', 'absent', 'absent', 'absent']
        self.assertEqual(result, expected)
        
    def test_evaluate_guess_duplicate_letters(self):
        """Tekrar eden harfler"""
        game = GameLogic('BOOKS', 6)
        result = game.evaluate_guess('ROBOT')
        # R yok, O mevcut, B mevcut, O doğru, T yok
        self.assertEqual(result[0], 'absent')   # R
        self.assertEqual(result[1], 'present')  # O
        self.assertEqual(result[2], 'present')  # B
        self.assertEqual(result[3], 'correct')  # O
        self.assertEqual(result[4], 'absent')   # T
        
    def test_make_guess_valid(self):
        """Geçerli tahmin"""
        result = self.game.make_guess('ARMA')
        self.assertIsNotNone(result)
        self.assertEqual(self.game.current_attempt, 1)
        self.assertEqual(len(self.game.guesses), 1)
        
    def test_make_guess_invalid_length(self):
        """Geçersiz uzunluk"""
        result = self.game.make_guess('ABC')
        self.assertIsNone(result)
        
    def test_win_condition(self):
        """Kazanma durumu"""
        self.game.make_guess('ELMA')
        self.assertTrue(self.game.is_won())
        self.assertTrue(self.game.is_game_over())
        
    def test_lose_condition(self):
        """Kaybetme durumu"""
        for _ in range(6):
            self.game.make_guess('XYZT')
        self.assertFalse(self.game.is_won())
        self.assertTrue(self.game.is_game_over())
        
    def test_remaining_attempts(self):
        """Kalan hak sayısı"""
        self.assertEqual(self.game.get_remaining_attempts(), 6)
        self.game.make_guess('XYZT')
        self.assertEqual(self.game.get_remaining_attempts(), 5)
        
    def test_keyboard_state(self):
        """Klavye durumu"""
        self.game.make_guess('ALMA')
        keyboard = self.game.get_keyboard_state()
        self.assertEqual(keyboard['L'], 'correct')
        self.assertEqual(keyboard['M'], 'correct')
        self.assertIn(keyboard['A'], ['correct', 'present'])
        
    def test_statistics(self):
        """İstatistik bilgileri"""
        self.game.make_guess('ELMA')
        stats = self.game.get_statistics()
        self.assertEqual(stats['attempts_used'], 1)
        self.assertTrue(stats['won'])
        self.assertEqual(len(stats['guesses']), 1)


class TestWordManager(unittest.TestCase):
    """Kelime yöneticisi testleri"""
    
    def setUp(self):
        """Test için geçici dosyalar oluştur"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test_words.txt')
        
        # Test kelimeleri
        test_words = ['ELMA', 'ARMUT', 'KARPUZ', 'PORTAKAL', 'MANGO']
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_words))
            
        self.manager = WordManager()
        
    def tearDown(self):
        """Test sonrası temizlik"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    def test_is_valid_word_turkish(self):
        """Türkçe kelime validasyonu"""
        self.assertTrue(self.manager.is_valid_word('ELMA', 'tr'))
        self.assertTrue(self.manager.is_valid_word('ÇAĞRI', 'tr'))
        self.assertFalse(self.manager.is_valid_word('ELM@', 'tr'))
        
    def test_is_valid_word_english(self):
        """İngilizce kelime validasyonu"""
        self.assertTrue(self.manager.is_valid_word('APPLE', 'en'))
        self.assertFalse(self.manager.is_valid_word('APPLEŞ', 'en'))
        
    def test_cache_mechanism(self):
        """Önbellek mekanizması"""
        # İlk yükleme
        words1 = self.manager.load_words(5, 'tr')
        self.assertTrue(self.manager.cache_loaded['tr'][5])
        
        # İkinci yükleme (önbellekten)
        words2 = self.manager.load_words(5, 'tr')
        self.assertEqual(words1, words2)
        
    def test_clear_cache(self):
        """Önbellek temizleme"""
        self.manager.load_words(5, 'tr')
        self.assertTrue(self.manager.cache_loaded['tr'][5])
        
        self.manager.clear_cache()
        self.assertFalse(self.manager.cache_loaded['tr'][5])


class TestStatistics(unittest.TestCase):
    """İstatistik testleri"""
    
    def setUp(self):
        """Test için geçici dosya"""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', 
            delete=False, 
            suffix='.json'
        )
        self.temp_file.close()
        self.stats = Statistics(self.temp_file.name)
        
    def tearDown(self):
        """Temizlik"""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
            
    def test_initial_stats(self):
        """Başlangıç istatistikleri"""
        summary = self.stats.get_summary()
        self.assertEqual(summary['games_played'], 0)
        self.assertEqual(summary['games_won'], 0)
        self.assertEqual(summary['win_rate'], 0.0)
        
    def test_record_win(self):
        """Kazanma kaydı"""
        self.stats.record_game(won=True, attempts=3, word_length=5, language='tr')
        summary = self.stats.get_summary()
        self.assertEqual(summary['games_played'], 1)
        self.assertEqual(summary['games_won'], 1)
        self.assertEqual(summary['win_rate'], 100.0)
        self.assertEqual(summary['current_streak'], 1)
        
    def test_record_loss(self):
        """Kaybetme kaydı"""
        self.stats.record_game(won=False, attempts=6, word_length=5, language='tr')
        summary = self.stats.get_summary()
        self.assertEqual(summary['games_played'], 1)
        self.assertEqual(summary['games_won'], 0)
        self.assertEqual(summary['win_rate'], 0.0)
        self.assertEqual(summary['current_streak'], 0)
        
    def test_win_rate_calculation(self):
        """Kazanma oranı hesaplama"""
        # 3 kazanma, 1 kaybetme
        self.stats.record_game(True, 3, 5, 'tr')
        self.stats.record_game(True, 4, 5, 'tr')
        self.stats.record_game(True, 2, 5, 'tr')
        self.stats.record_game(False, 6, 5, 'tr')
        
        summary = self.stats.get_summary()
        self.assertEqual(summary['games_played'], 4)
        self.assertEqual(summary['games_won'], 3)
        self.assertEqual(summary['win_rate'], 75.0)
        
    def test_streak_tracking(self):
        """Seri takibi"""
        # 3 kazanma
        self.stats.record_game(True, 3, 5, 'tr')
        self.stats.record_game(True, 4, 5, 'tr')
        self.stats.record_game(True, 2, 5, 'tr')
        
        summary = self.stats.get_summary()
        self.assertEqual(summary['current_streak'], 3)
        self.assertEqual(summary['max_streak'], 3)
        
        # Kaybetme - seri sıfırlanmalı
        self.stats.record_game(False, 6, 5, 'tr')
        summary = self.stats.get_summary()
        self.assertEqual(summary['current_streak'], 0)
        self.assertEqual(summary['max_streak'], 3)
        
    def test_average_guesses(self):
        """Ortalama tahmin"""
        self.stats.record_game(True, 3, 5, 'tr')
        self.stats.record_game(True, 5, 5, 'tr')
        
        avg = self.stats.get_average_guesses()
        self.assertEqual(avg, 4.0)
        
    def test_guess_distribution(self):
        """Tahmin dağılımı"""
        self.stats.record_game(True, 3, 5, 'tr')
        self.stats.record_game(True, 3, 5, 'tr')
        self.stats.record_game(True, 4, 5, 'tr')
        
        dist = self.stats.get_guess_distribution()
        self.assertEqual(dist['3'], 2)
        self.assertEqual(dist['4'], 1)
        
    def test_reset_stats(self):
        """İstatistik sıfırlama"""
        self.stats.record_game(True, 3, 5, 'tr')
        self.stats.reset_stats()
        
        summary = self.stats.get_summary()
        self.assertEqual(summary['games_played'], 0)


class TestThemes(unittest.TestCase):
    """Tema testleri"""
    
    def setUp(self):
        """Tema yöneticisi oluştur"""
        self.theme_manager = ThemeManager()
        
    def test_default_theme(self):
        """Varsayılan tema"""
        theme = self.theme_manager.get_current_theme()
        self.assertEqual(theme.name, 'classic')
        
    def test_theme_switching(self):
        """Tema değiştirme"""
        success = self.theme_manager.set_current_theme('neon')
        self.assertTrue(success)
        
        theme = self.theme_manager.get_current_theme()
        self.assertEqual(theme.name, 'neon')
        
    def test_invalid_theme(self):
        """Geçersiz tema"""
        success = self.theme_manager.set_current_theme('nonexistent')
        self.assertFalse(success)
        
        # Varsayılan tema kalmalı
        theme = self.theme_manager.get_current_theme()
        self.assertEqual(theme.name, 'classic')
        
    def test_theme_colors(self):
        """Tema renkleri"""
        theme = self.theme_manager.get_theme('classic')
        
        # Renk döndürmeli
        correct_color = theme.get_color('correct')
        self.assertEqual(len(correct_color), 4)  # RGBA
        
        # Hex döndürmeli
        correct_hex = theme.get_hex_color('correct')
        self.assertTrue(correct_hex.startswith('#'))
        
    def test_all_themes_loaded(self):
        """Tüm temalar yüklendi mi"""
        themes = self.theme_manager.get_all_themes()
        self.assertGreaterEqual(len(themes), 8)
        
        # Her tema gerekli renklere sahip olmalı
        required_colors = ['correct', 'present', 'absent']
        for theme in themes:
            for color in required_colors:
                self.assertIn(color, theme.colors)


class TestSecurity(unittest.TestCase):
    """Güvenlik testleri"""
    
    def setUp(self):
        """Şifreleme oluştur"""
        self.encryption = WordEncryption(key="TEST_KEY")
        self.cache = WordCache(cache_size=3)
        
    def test_word_encryption_decryption(self):
        """Kelime şifreleme/çözme"""
        original = "ELMA"
        encrypted = self.encryption.encrypt_word(original)
        decrypted = self.encryption.decrypt_word(encrypted)
        
        self.assertEqual(original, decrypted)
        self.assertNotEqual(original, encrypted)
        
    def test_word_list_encryption(self):
        """Kelime listesi şifreleme"""
        words = ['ELMA', 'ARMUT', 'KARPUZ']
        encrypted = self.encryption.encrypt_word_list(words)
        decrypted = self.encryption.decrypt_word_list(encrypted)
        
        self.assertEqual(words, decrypted)
        
    def test_cache_storage(self):
        """Önbellek saklama"""
        words = ['ELMA', 'ARMUT']
        self.cache.cache_words('test_key', words)
        
        retrieved = self.cache.get_cached_words('test_key')
        self.assertEqual(words, retrieved)
        
    def test_cache_miss(self):
        """Önbellek kaçırma"""
        retrieved = self.cache.get_cached_words('nonexistent')
        self.assertIsNone(retrieved)
        
    def test_cache_lru(self):
        """LRU önbellek"""
        # 3 öğe ekle (cache_size=3)
        self.cache.cache_words('key1', ['A'])
        self.cache.cache_words('key2', ['B'])
        self.cache.cache_words('key3', ['C'])
        
        # key1'e eriş (kullanım sayısı artar)
        self.cache.get_cached_words('key1')
        
        # 4. öğe ekle - key2 silinmeli (en az kullanılan)
        self.cache.cache_words('key4', ['D'])
        
        self.assertTrue(self.cache.is_cached('key1'))
        self.assertFalse(self.cache.is_cached('key2'))
        self.assertTrue(self.cache.is_cached('key3'))
        self.assertTrue(self.cache.is_cached('key4'))
        
    def test_cache_clear(self):
        """Önbellek temizleme"""
        self.cache.cache_words('test', ['A'])
        self.assertTrue(self.cache.is_cached('test'))
        
        self.cache.clear_cache()
        self.assertFalse(self.cache.is_cached('test'))


class TestIntegration(unittest.TestCase):
    """Entegrasyon testleri"""
    
    def test_complete_game_flow(self):
        """Tam oyun akışı"""
        # Oyun başlat
        game = GameLogic('ELMA', 6)
        
        # Tahminler yap
        result1 = game.make_guess('ARMA')
        self.assertIsNotNone(result1)
        
        result2 = game.make_guess('ELMA')
        self.assertIsNotNone(result2)
        
        # Kazanıldı mı kontrol et
        self.assertTrue(game.is_won())
        self.assertEqual(game.current_attempt, 2)
        
    def test_statistics_integration(self):
        """İstatistik entegrasyonu"""
        stats_file = tempfile.NamedTemporaryFile(
            mode='w', 
            delete=False, 
            suffix='.json'
        )
        stats_file.close()
        
        try:
            stats = Statistics(stats_file.name)
            
            # Oyun oyna ve kaydet
            stats.record_game(True, 3, 5, 'tr')
            stats.record_game(True, 4, 5, 'tr')
            stats.record_game(False, 6, 5, 'tr')
            
            # İstatistikleri kontrol et
            summary = stats.get_summary()
            self.assertEqual(summary['games_played'], 3)
            self.assertEqual(summary['games_won'], 2)
            
            # Dosyaya kaydedildi mi
            self.assertTrue(os.path.exists(stats_file.name))
            
        finally:
            if os.path.exists(stats_file.name):
                os.remove(stats_file.name)


def run_all_tests():
    """Tüm testleri çalıştır"""
    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Test sınıflarını ekle
    suite.addTests(loader.loadTestsFromTestCase(TestGameLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestWordManager))
    suite.addTests(loader.loadTestsFromTestCase(TestStatistics))
    suite.addTests(loader.loadTestsFromTestCase(TestThemes))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurity))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Test runner
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Sonuçları yazdır
    print("\n" + "="*70)
    print(f"Çalıştırılan Testler: {result.testsRun}")
    print(f"Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız: {len(result.failures)}")
    print(f"Hata: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)

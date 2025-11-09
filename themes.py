"""
Tema Yönetim Modülü
Farklı renk temaları ve özelleştirme seçenekleri
"""

from kivy.utils import get_color_from_hex
from typing import Dict, Tuple, List


class Theme:
    """Tek bir tema tanımı"""
    
    def __init__(self, name: str, display_name: str, colors: Dict[str, str], 
                 description: str = ""):
        """
        Tema oluştur
        
        Args:
            name: Tema kodu (classic, colorblind, vb.)
            display_name: Görünen ad
            colors: Renk tanımları (hex kodları)
            description: Tema açıklaması
        """
        self.name = name
        self.display_name = display_name
        self.description = description
        self.colors = colors
        
    def get_color(self, color_name: str) -> Tuple[float, float, float, float]:
        """
        Renk kodunu Kivy formatında döndür
        
        Args:
            color_name: Renk adı (correct, present, absent, vb.)
            
        Returns:
            RGBA renk tuple'ı (0-1 arası)
        """
        hex_color = self.colors.get(color_name, '#FFFFFF')
        return get_color_from_hex(hex_color)
        
    def get_hex_color(self, color_name: str) -> str:
        """
        Hex renk kodunu döndür
        
        Args:
            color_name: Renk adı
            
        Returns:
            Hex renk kodu (#RRGGBB)
        """
        return self.colors.get(color_name, '#FFFFFF')


class ThemeManager:
    """Tema yönetim sınıfı"""
    
    def __init__(self):
        """Tema yöneticisini başlat ve temaları yükle"""
        self.themes: Dict[str, Theme] = {}
        self.current_theme_name = 'classic'
        self.load_themes()
        
    def load_themes(self):
        """Tüm temaları yükle"""
        
        # 1. Klasik Tema (Orijinal Wordle)
        self.themes['classic'] = Theme(
            name='classic',
            display_name='Klasik',
            description='Orijinal Wordle renkleri',
            colors={
                'correct': '#6aaa64',      # Yeşil
                'present': '#c9b458',      # Sarı/Altın
                'absent': '#787c7e',       # Gri
                'correct_dark': '#538d4e', # Koyu yeşil
                'present_dark': '#b59f3b', # Koyu sarı
                'absent_dark': '#3a3a3c',  # Koyu gri
                'background': '#ffffff',    # Beyaz
                'background_dark': '#121213', # Siyah
                'text': '#000000',         # Siyah metin
                'text_dark': '#ffffff',    # Beyaz metin
                'border': '#d3d6da',       # Açık gri
                'border_dark': '#3a3a3c',  # Koyu gri
                'keyboard': '#d3d6da',     # Klavye rengi
                'keyboard_dark': '#818384' # Koyu klavye
            }
        )
        
        # 2. Renkli Körlük Dostu Tema
        self.themes['colorblind'] = Theme(
            name='colorblind',
            display_name='Renkli Körlük Dostu',
            description='Yüksek kontrast, ayırt edilebilir renkler',
            colors={
                'correct': '#f5793a',      # Turuncu
                'present': '#85c0f9',      # Mavi
                'absent': '#787c7e',       # Gri
                'correct_dark': '#f5793a',
                'present_dark': '#85c0f9',
                'absent_dark': '#3a3a3c',
                'background': '#ffffff',
                'background_dark': '#121213',
                'text': '#000000',
                'text_dark': '#ffffff',
                'border': '#d3d6da',
                'border_dark': '#3a3a3c',
                'keyboard': '#d3d6da',
                'keyboard_dark': '#818384'
            }
        )
        
        # 3. Neon Tema
        self.themes['neon'] = Theme(
            name='neon',
            display_name='Neon',
            description='Canlı neon renkler',
            colors={
                'correct': '#00ff00',      # Neon yeşil
                'present': '#ffff00',      # Neon sarı
                'absent': '#ff00ff',       # Neon mor
                'correct_dark': '#00cc00',
                'present_dark': '#cccc00',
                'absent_dark': '#cc00cc',
                'background': '#0a0a0a',
                'background_dark': '#000000',
                'text': '#00ffff',         # Neon cyan
                'text_dark': '#00ffff',
                'border': '#00ffff',
                'border_dark': '#008888',
                'keyboard': '#1a1a1a',
                'keyboard_dark': '#0f0f0f'
            }
        )
        
        # 4. Pastel Tema
        self.themes['pastel'] = Theme(
            name='pastel',
            display_name='Pastel',
            description='Yumuşak pastel renkler',
            colors={
                'correct': '#a8e6cf',      # Pastel yeşil
                'present': '#ffd3b6',      # Pastel turuncu
                'absent': '#d4a5a5',       # Pastel pembe
                'correct_dark': '#88c9a8',
                'present_dark': '#ddb396',
                'absent_dark': '#b48585',
                'background': '#fff9f0',
                'background_dark': '#2a2a2a',
                'text': '#5a5a5a',
                'text_dark': '#e0e0e0',
                'border': '#e8d5c4',
                'border_dark': '#4a4a4a',
                'keyboard': '#f5e6d3',
                'keyboard_dark': '#3a3a3a'
            }
        )
        
        # 5. Yüksek Kontrast Tema
        self.themes['high_contrast'] = Theme(
            name='high_contrast',
            display_name='Yüksek Kontrast',
            description='Maksimum kontrast, erişilebilirlik için',
            colors={
                'correct': '#00ff00',      # Parlak yeşil
                'present': '#ffff00',      # Parlak sarı
                'absent': '#ff0000',       # Parlak kırmızı
                'correct_dark': '#00cc00',
                'present_dark': '#cccc00',
                'absent_dark': '#cc0000',
                'background': '#ffffff',
                'background_dark': '#000000',
                'text': '#000000',
                'text_dark': '#ffffff',
                'border': '#000000',
                'border_dark': '#ffffff',
                'keyboard': '#cccccc',
                'keyboard_dark': '#333333'
            }
        )
        
        # 6. Gece Mavi Tema
        self.themes['night_blue'] = Theme(
            name='night_blue',
            display_name='Gece Mavisi',
            description='Göz dostu gece teması',
            colors={
                'correct': '#4a9eff',      # Mavi
                'present': '#ffa64d',      # Turuncu
                'absent': '#6b7280',       # Gri
                'correct_dark': '#3a7ed0',
                'present_dark': '#d98840',
                'absent_dark': '#4b5563',
                'background': '#1e3a5f',
                'background_dark': '#0f1e3a',
                'text': '#e5e7eb',
                'text_dark': '#f3f4f6',
                'border': '#334155',
                'border_dark': '#1e293b',
                'keyboard': '#2d4a6f',
                'keyboard_dark': '#1a2d4a'
            }
        )
        
        # 7. Sonbahar Tema
        self.themes['autumn'] = Theme(
            name='autumn',
            display_name='Sonbahar',
            description='Sıcak sonbahar renkleri',
            colors={
                'correct': '#d97706',      # Turuncu-sarı
                'present': '#dc2626',      # Kırmızı
                'absent': '#92400e',       # Kahverengi
                'correct_dark': '#b45309',
                'present_dark': '#b91c1c',
                'absent_dark': '#78350f',
                'background': '#fef3c7',
                'background_dark': '#451a03',
                'text': '#451a03',
                'text_dark': '#fef3c7',
                'border': '#fbbf24',
                'border_dark': '#78350f',
                'keyboard': '#fcd34d',
                'keyboard_dark': '#92400e'
            }
        )
        
        # 8. Okyanus Tema
        self.themes['ocean'] = Theme(
            name='ocean',
            display_name='Okyanus',
            description='Sakin okyanus renkleri',
            colors={
                'correct': '#06b6d4',      # Cyan
                'present': '#8b5cf6',      # Mor
                'absent': '#64748b',       # Slate
                'correct_dark': '#0891b2',
                'present_dark': '#7c3aed',
                'absent_dark': '#475569',
                'background': '#e0f2fe',
                'background_dark': '#0c4a6e',
                'text': '#0c4a6e',
                'text_dark': '#e0f2fe',
                'border': '#7dd3fc',
                'border_dark': '#075985',
                'keyboard': '#bae6fd',
                'keyboard_dark': '#0369a1'
            }
        )
        
    def get_theme(self, theme_name: str) -> Theme:
        """
        Tema al
        
        Args:
            theme_name: Tema adı
            
        Returns:
            Theme objesi
        """
        return self.themes.get(theme_name, self.themes['classic'])
        
    def set_current_theme(self, theme_name: str) -> bool:
        """
        Aktif temayı değiştir
        
        Args:
            theme_name: Yeni tema adı
            
        Returns:
            Başarılı ise True
        """
        if theme_name in self.themes:
            self.current_theme_name = theme_name
            return True
        return False
        
    def get_current_theme(self) -> Theme:
        """
        Aktif temayı döndür
        
        Returns:
            Aktif Theme objesi
        """
        return self.get_theme(self.current_theme_name)
        
    def get_color(self, color_name: str, dark_mode: bool = False) -> Tuple:
        """
        Aktif temadan renk al
        
        Args:
            color_name: Renk adı
            dark_mode: Dark mode aktif mi
            
        Returns:
            RGBA renk tuple'ı
        """
        theme = self.get_current_theme()
        
        # Dark mode varsa dark versiyonunu kullan
        if dark_mode and f"{color_name}_dark" in theme.colors:
            color_name = f"{color_name}_dark"
            
        return theme.get_color(color_name)
        
    def get_hex_color(self, color_name: str, dark_mode: bool = False) -> str:
        """
        Aktif temadan hex renk al
        
        Args:
            color_name: Renk adı
            dark_mode: Dark mode aktif mi
            
        Returns:
            Hex renk kodu
        """
        theme = self.get_current_theme()
        
        if dark_mode and f"{color_name}_dark" in theme.colors:
            color_name = f"{color_name}_dark"
            
        return theme.get_hex_color(color_name)
        
    def get_all_themes(self) -> List[Theme]:
        """
        Tüm temaları döndür
        
        Returns:
            Theme listesi
        """
        return list(self.themes.values())
        
    def get_theme_names(self) -> List[str]:
        """
        Tema adlarını döndür
        
        Returns:
            Tema adları listesi
        """
        return list(self.themes.keys())
        
    def get_theme_display_names(self) -> Dict[str, str]:
        """
        Tema görünen adlarını döndür
        
        Returns:
            {tema_kodu: görünen_ad} dictionary'si
        """
        return {
            name: theme.display_name 
            for name, theme in self.themes.items()
        }


# Test fonksiyonu
if __name__ == '__main__':
    """Modül testleri"""
    print("=== Tema Yöneticisi Test ===\n")
    
    theme_manager = ThemeManager()
    
    # Tüm temaları listele
    print("=== Mevcut Temalar ===")
    for theme_name, display_name in theme_manager.get_theme_display_names().items():
        theme = theme_manager.get_theme(theme_name)
        print(f"\n{display_name} ({theme_name})")
        print(f"  Açıklama: {theme.description}")
        print(f"  Renkler:")
        print(f"    ✓ Doğru: {theme.get_hex_color('correct')}")
        print(f"    ~ Mevcut: {theme.get_hex_color('present')}")
        print(f"    ✗ Yok: {theme.get_hex_color('absent')}")
    
    # Tema değiştirme
    print("\n=== Tema Değiştirme ===")
    current = theme_manager.get_current_theme()
    print(f"Aktif tema: {current.display_name}")
    
    theme_manager.set_current_theme('neon')
    current = theme_manager.get_current_theme()
    print(f"Yeni tema: {current.display_name}")
    
    # Renk alma
    print("\n=== Renk Alma ===")
    print("Light mode:")
    print(f"  Correct: {theme_manager.get_hex_color('correct', dark_mode=False)}")
    print(f"  Present: {theme_manager.get_hex_color('present', dark_mode=False)}")
    print(f"  Absent: {theme_manager.get_hex_color('absent', dark_mode=False)}")
    
    print("\nDark mode:")
    print(f"  Correct: {theme_manager.get_hex_color('correct', dark_mode=True)}")
    print(f"  Present: {theme_manager.get_hex_color('present', dark_mode=True)}")
    print(f"  Absent: {theme_manager.get_hex_color('absent', dark_mode=True)}")
    
    # Renk önizlemesi (terminal destekliyorsa)
    print("\n=== Renk Önizleme ===")
    for theme in theme_manager.get_all_themes():
        correct = theme.get_hex_color('correct')
        present = theme.get_hex_color('present')
        absent = theme.get_hex_color('absent')
        
        print(f"{theme.display_name:20} | ✓ {correct} | ~ {present} | ✗ {absent}")
    
    print("\n✓ Testler tamamlandı!")

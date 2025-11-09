"""
Wordle Tarzı Kelime Oyunu - Geliştirilmiş Versiyon
Python 3.10+ | Kivy | KivyMD

YENİ ÖZELLİKLER:
- İstatistik sistemi
- Ses efektleri
- Çoklu tema desteği
- İstatistik ekranı
- Geliştirilmiş animasyonlar
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivy.clock import Clock
import json
import os
import time

from words import WordManager
from game_logic import GameLogic
from statistics import Statistics
from sounds import SoundManager
from themes import ThemeManager


class LetterBox(Label):
    """Gelişmiş harf kutusu"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(60), dp(60))
        self.font_size = sp(32)
        self.bold = True
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, *args):
        """Kutu kenarlığını güncelle"""
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            app = App.get_running_app()
            theme_manager = app.theme_manager
            dark_mode = app.settings['theme'] == 'Dark'
            
            # Border rengi
            border_color = theme_manager.get_color('border', dark_mode)
            Color(*border_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
        
    def animate_correct(self, theme_manager, dark_mode, sound_manager=None):
        """Doğru harf ve konum - Yeşil animasyon"""
        color = theme_manager.get_color('correct', dark_mode)
        self.animate_flip(color)
        if sound_manager and sound_manager.enabled:
            sound_manager.play_correct_sound()
        
    def animate_present(self, theme_manager, dark_mode, sound_manager=None):
        """Doğru harf ama yanlış konum - Sarı animasyon"""
        color = theme_manager.get_color('present', dark_mode)
        self.animate_flip(color)
        if sound_manager and sound_manager.enabled:
            sound_manager.play_present_sound()
        
    def animate_absent(self, theme_manager, dark_mode, sound_manager=None):
        """Yanlış harf - Gri animasyon + titreme"""
        color = theme_manager.get_color('absent', dark_mode)
        self.animate_flip(color)
        self.shake()
        if sound_manager and sound_manager.enabled:
            sound_manager.play_absent_sound()
        
    def animate_flip(self, bg_color):
        """Kart çevirme efekti"""
        anim1 = Animation(size=(dp(60), dp(10)), duration=0.15)
        anim2 = Animation(size=(dp(60), dp(60)), duration=0.15)
        
        def change_color(anim, widget):
            self.canvas.before.clear()
            with self.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(*bg_color)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
                Color(1, 1, 1, 1)
            self.color = (1, 1, 1, 1)
            
        anim1.bind(on_complete=change_color)
        anim1.bind(on_complete=lambda *args: anim2.start(self))
        anim1.start(self)
        
    def shake(self):
        """Titreme animasyonu"""
        original_x = self.x
        anim = (Animation(x=original_x - dp(5), duration=0.05) +
                Animation(x=original_x + dp(5), duration=0.05) +
                Animation(x=original_x - dp(5), duration=0.05) +
                Animation(x=original_x, duration=0.05))
        anim.start(self)


class KeyboardKey(MDRaisedButton):
    """Gelişmiş klavye tuşu"""
    
    def __init__(self, letter, callback, **kwargs):
        super().__init__(**kwargs)
        self.text = letter
        self.letter = letter
        self.font_size = sp(16)
        self.size_hint = (None, None)
        self.size = (dp(35), dp(50))
        
        app = App.get_running_app()
        theme_manager = app.theme_manager
        dark_mode = app.settings['theme'] == 'Dark'
        
        self.md_bg_color = theme_manager.get_color('keyboard', dark_mode)
        self.text_color = theme_manager.get_color('text', dark_mode)
        self.on_release = lambda: callback(letter)
        self.state = 'normal'
        
    def update_color(self, state, theme_manager, dark_mode):
        """Tuş rengini duruma göre güncelle"""
        self.key_state = state
        if state == 'correct':
            self.md_bg_color = theme_manager.get_color('correct', dark_mode)
            self.text_color = (1, 1, 1, 1)
        elif state == 'present':
            self.md_bg_color = theme_manager.get_color('present', dark_mode)
            self.text_color = (1, 1, 1, 1)
        elif state == 'absent':
            self.md_bg_color = theme_manager.get_color('absent', dark_mode)
            self.text_color = (1, 1, 1, 1)


class StatisticsScreen(Screen):
    """İstatistik ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'statistics'
        self.build_ui()
        
    def build_ui(self):
        """İstatistik arayüzünü oluştur"""
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Üst bar
        top_bar = BoxLayout(size_hint_y=0.08)
        back_btn = MDIconButton(icon='arrow-left', on_release=self.go_back)
        title = MDLabel(text="İSTATİSTİKLER", font_style='H5', halign='center')
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)
        top_bar.add_widget(Label())  # Spacer
        layout.add_widget(top_bar)
        
        # İstatistik kartları container
        self.stats_container = BoxLayout(orientation='vertical', spacing=dp(10))
        layout.add_widget(self.stats_container)
        
        # Butonlar
        button_box = BoxLayout(size_hint_y=0.15, spacing=dp(10))
        reset_btn = MDRaisedButton(
            text="İSTATİSTİKLERİ SIFIRLA",
            on_release=self.confirm_reset
        )
        button_box.add_widget(reset_btn)
        layout.add_widget(button_box)
        
        self.add_widget(layout)
        
    def on_enter(self):
        """Ekrana girildiğinde"""
        self.update_statistics()
        
    def update_statistics(self):
        """İstatistikleri güncelle"""
        self.stats_container.clear_widgets()
        
        app = App.get_running_app()
        stats = app.statistics.get_detailed_stats()
        
        # Özet kartı
        summary_card = self.create_summary_card(stats)
        self.stats_container.add_widget(summary_card)
        
        # Tahmin dağılımı kartı
        distribution_card = self.create_distribution_card(stats)
        self.stats_container.add_widget(distribution_card)
        
    def create_summary_card(self, stats):
        """Özet istatistik kartı oluştur"""
        card = MDCard(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(200)
        )
        
        # Başlık
        title = MDLabel(text="ÖZET", font_style='H6', size_hint_y=None, height=dp(30))
        card.add_widget(title)
        
        # İstatistikler grid
        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(150))
        
        stat_items = [
            ("Oynanan Oyun", str(stats['games_played'])),
            ("Kazanma Oranı", f"{stats['win_rate']}%"),
            ("Mevcut Seri", str(stats['current_streak'])),
            ("Maksimum Seri", str(stats['max_streak'])),
            ("Ortalama Tahmin", str(stats['average_guesses'])),
            ("En İyi Oyun", str(stats['best_game']) if stats['best_game'] else "-")
        ]
        
        for label_text, value_text in stat_items:
            item_box = BoxLayout(orientation='vertical', spacing=dp(5))
            label = MDLabel(text=label_text, halign='center', theme_text_color='Secondary')
            value = MDLabel(text=value_text, halign='center', font_style='H5')
            item_box.add_widget(label)
            item_box.add_widget(value)
            grid.add_widget(item_box)
            
        card.add_widget(grid)
        return card
        
    def create_distribution_card(self, stats):
        """Tahmin dağılımı kartı oluştur"""
        card = MDCard(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(250)
        )
        
        # Başlık
        title = MDLabel(text="TAHMİN DAĞILIMI", font_style='H6', size_hint_y=None, height=dp(30))
        card.add_widget(title)
        
        # Dağılım grafikleri
        dist_box = BoxLayout(orientation='vertical', spacing=dp(8))
        
        distribution = stats['guess_distribution']
        percentages = stats['distribution_percentages']
        max_count = max(distribution.values()) if distribution.values() else 1
        
        for attempt in sorted(distribution.keys()):
            count = distribution[attempt]
            percentage = percentages[attempt]
            
            row = BoxLayout(size_hint_y=None, height=dp(25), spacing=dp(5))
            
            # Tahmin numarası
            num_label = MDLabel(
                text=str(attempt),
                size_hint_x=None,
                width=dp(30),
                halign='right'
            )
            row.add_widget(num_label)
            
            # Progress bar
            bar_container = BoxLayout()
            if count > 0:
                bar_width = (count / max_count) if max_count > 0 else 0
                bar = MDRaisedButton(
                    text=str(count),
                    size_hint_x=bar_width,
                    md_bg_color=get_color_from_hex('#6aaa64')
                )
                bar_container.add_widget(bar)
                bar_container.add_widget(Label(size_hint_x=1 - bar_width))
            
            row.add_widget(bar_container)
            dist_box.add_widget(row)
            
        card.add_widget(dist_box)
        return card
        
    def confirm_reset(self, button):
        """İstatistik sıfırlama onayı"""
        dialog = MDDialog(
            title="İstatistikleri Sıfırla",
            text="Tüm istatistikler silinecek. Emin misiniz?",
            buttons=[
                MDFlatButton(
                    text="İPTAL",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SIFIRLA",
                    on_release=lambda x: self.reset_statistics(dialog)
                ),
            ],
        )
        dialog.open()
        
    def reset_statistics(self, dialog):
        """İstatistikleri sıfırla"""
        app = App.get_running_app()
        app.statistics.reset_stats()
        dialog.dismiss()
        self.update_statistics()
        
    def go_back(self, button):
        """Geri dön"""
        App.get_running_app().root.current = 'menu'


class MenuScreen(Screen):
    """Ana menü ekranı - Geliştirilmiş"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'menu'
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Başlık
        title = MDLabel(
            text="WORDLE OYUNU",
            font_style='H3',
            halign='center',
            size_hint_y=0.2
        )
        layout.add_widget(title)
        
        # Ayarlar menüsü
        settings_box = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=0.4)
        
        # Dil seçimi
        self.language_btn = MDRaisedButton(
            text="Dil: Türkçe",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.language_btn.bind(on_release=self.show_language_menu)
        settings_box.add_widget(self.language_btn)
        
        # Kelime uzunluğu
        self.word_length_btn = MDRaisedButton(
            text="Kelime Uzunluğu: 5",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.word_length_btn.bind(on_release=self.show_word_length_menu)
        settings_box.add_widget(self.word_length_btn)
        
        # Tema seçimi
        self.theme_btn = MDRaisedButton(
            text="Tema: Klasik",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.theme_btn.bind(on_release=self.show_theme_menu)
        settings_box.add_widget(self.theme_btn)
        
        # Ses açma/kapama
        self.sound_btn = MDRaisedButton(
            text="Ses: Açık",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.sound_btn.bind(on_release=self.toggle_sound)
        settings_box.add_widget(self.sound_btn)
        
        layout.add_widget(settings_box)
        
        # Butonlar
        button_box = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=0.4)
        
        # Başla butonu
        start_btn = MDRaisedButton(
            text="OYUNA BAŞLA",
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex('#6aaa64')
        )
        start_btn.bind(on_release=self.start_game)
        button_box.add_widget(start_btn)
        
        # İstatistikler butonu
        stats_btn = MDRaisedButton(
            text="İSTATİSTİKLER",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        stats_btn.bind(on_release=self.show_statistics)
        button_box.add_widget(stats_btn)
        
        layout.add_widget(button_box)
        
        self.add_widget(layout)
        
        # Dropdown menüler
        self.language_menu = None
        self.word_length_menu = None
        self.theme_menu = None
        
    def show_language_menu(self, button):
        """Dil seçim menüsü"""
        menu_items = [
            {"text": "Türkçe", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_language("tr", "Türkçe")},
            {"text": "English", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_language("en", "English")},
        ]
        self.language_menu = MDDropdownMenu(
            caller=button, items=menu_items, width_mult=4)
        self.language_menu.open()
        
    def show_word_length_menu(self, button):
        """Kelime uzunluğu menüsü"""
        menu_items = [
            {"text": "5 Harf", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_word_length(5)},
            {"text": "6 Harf", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_word_length(6)},
            {"text": "7 Harf", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_word_length(7)},
        ]
        self.word_length_menu = MDDropdownMenu(
            caller=button, items=menu_items, width_mult=4)
        self.word_length_menu.open()
        
    def show_theme_menu(self, button):
        """Tema seçim menüsü"""
        app = App.get_running_app()
        themes = app.theme_manager.get_theme_display_names()
        
        menu_items = [
            {"text": display_name, "viewclass": "OneLineListItem",
             "on_release": lambda t=theme_name, d=display_name: self.set_theme(t, d)}
            for theme_name, display_name in themes.items()
        ]
        self.theme_menu = MDDropdownMenu(
            caller=button, items=menu_items, width_mult=4)
        self.theme_menu.open()
        
    def set_language(self, lang_code, lang_name):
        """Dil ayarla"""
        app = App.get_running_app()
        app.settings['language'] = lang_code
        self.language_btn.text = f"Dil: {lang_name}"
        if self.language_menu:
            self.language_menu.dismiss()
        app.save_settings()
        
    def set_word_length(self, length):
        """Kelime uzunluğu ayarla"""
        app = App.get_running_app()
        app.settings['word_length'] = length
        self.word_length_btn.text = f"Kelime Uzunluğu: {length}"
        if self.word_length_menu:
            self.word_length_menu.dismiss()
        app.save_settings()
        
    def set_theme(self, theme_name, display_name):
        """Tema ayarla"""
        app = App.get_running_app()
        app.settings['color_theme'] = theme_name
        app.theme_manager.set_current_theme(theme_name)
        self.theme_btn.text = f"Tema: {display_name}"
        if self.theme_menu:
            self.theme_menu.dismiss()
        app.save_settings()
        
    def toggle_sound(self, button):
        """Ses aç/kapa"""
        app = App.get_running_app()
        enabled = app.sound_manager.toggle()
        app.settings['sound_enabled'] = enabled
        self.sound_btn.text = f"Ses: {'Açık' if enabled else 'Kapalı'}"
        app.save_settings()
        
    def start_game(self, button):
        """Oyunu başlat"""
        app = App.get_running_app()
        game_screen = app.root.get_screen('game')
        game_screen.initialize_game()
        app.root.current = 'game'
        
    def show_statistics(self, button):
        """İstatistikleri göster"""
        App.get_running_app().root.current = 'statistics'


# GameScreen sınıfı çok uzun olduğu için özellikleri ekliyoruz
# Tam kodu bir sonraki artifact'ta vereceğim
class GameScreen(Screen):
    """Tam özellikli oyun ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'game'
        self.game_logic = None
        self.letter_boxes = []
        self.keyboard_keys = {}
        self.current_guess = ""
        self.start_time = None
        self.game_metrics = {
            'start_time': None,
            'end_time': None,
            'total_time': 0,
            'key_presses': 0,
            'backspaces': 0,
            'enters': 0,
            'invalid_attempts': 0
        }
        
        # Ana layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Üst bar - Geri butonu ve zamanlayıcı
        top_bar = BoxLayout(size_hint_y=0.08, spacing=dp(10))
        back_btn = MDIconButton(icon='arrow-left', on_release=self.go_back)
        top_bar.add_widget(back_btn)
        
        self.timer_label = MDLabel(
            text="00:00",
            halign='center',
            font_style='H6'
        )
        top_bar.add_widget(self.timer_label)
        
        # Ayarlar butonu
        settings_btn = MDIconButton(icon='cog', on_release=self.show_game_settings)
        top_bar.add_widget(settings_btn)
        
        main_layout.add_widget(top_bar)
        
        # Tahmin grid'i
        self.grid_container = BoxLayout(orientation='vertical', size_hint_y=0.5)
        main_layout.add_widget(self.grid_container)
        
        # İlerleme göstergesi
        self.progress_box = BoxLayout(size_hint_y=0.05, spacing=dp(5))
        main_layout.add_widget(self.progress_box)
        
        # Spacer
        main_layout.add_widget(Label(size_hint_y=0.02))
        
        # Klavye
        self.keyboard_container = BoxLayout(
            orientation='vertical', 
            size_hint_y=0.35, 
            spacing=dp(5)
        )
        main_layout.add_widget(self.keyboard_container)
        
        self.add_widget(main_layout)
        
        # Zamanlayıcı event
        self.timer_event = None
        
    def initialize_game(self):
        """Oyunu başlat"""
        app = App.get_running_app()
        word_length = app.settings['word_length']
        max_attempts = word_length
        language = app.settings['language']
        
        # Metrikleri sıfırla
        self.game_metrics = {
            'start_time': time.time(),
            'end_time': None,
            'total_time': 0,
            'key_presses': 0,
            'backspaces': 0,
            'enters': 0,
            'invalid_attempts': 0
        }
        
        # Zamanlayıcıyı başlat
        self.start_time = time.time()
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1.0)
        
        # Kelime yöneticisini başlat
        from words import WordManager
        word_manager = WordManager()
        secret_word = word_manager.get_random_word(word_length, language)
        
        if not secret_word:
            self.show_error_dialog("Kelime listesi yüklenemedi!")
            return
            
        # Oyun mantığını başlat
        from game_logic import GameLogic
        self.game_logic = GameLogic(secret_word, max_attempts)
        self.current_guess = ""
        
        # Grid'i oluştur
        self.create_grid(max_attempts, word_length)
        
        # Klavyeyi oluştur
        self.create_keyboard(language)
        
        # İlerleme göstergesini oluştur
        self.create_progress_indicator(max_attempts)
        
        # İlk oyun tutorial'ı göster (sadece ilk kez)
        if app.settings.get('first_game', True):
            self.show_tutorial()
            app.settings['first_game'] = False
            app.save_settings()
            
    def update_timer(self, dt):
        """Zamanlayıcıyı güncelle"""
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.text = f"{minutes:02d}:{seconds:02d}"
            
    def create_grid(self, rows, cols):
        """Tahmin grid'ini oluştur"""
        self.grid_container.clear_widgets()
        self.letter_boxes = []
        
        grid = GridLayout(cols=cols, spacing=dp(5), size_hint=(None, None))
        grid.bind(minimum_size=grid.setter('size'))
        
        # Grid'i ortala
        grid_wrapper = BoxLayout()
        grid_wrapper.add_widget(Label())
        grid_wrapper.add_widget(grid)
        grid_wrapper.add_widget(Label())
        
        for row in range(rows):
            row_boxes = []
            for col in range(cols):
                box = LetterBox()
                grid.add_widget(box)
                row_boxes.append(box)
            self.letter_boxes.append(row_boxes)
            
        self.grid_container.add_widget(grid_wrapper)
        
    def create_keyboard(self, language):
        """QWERTY klavye oluştur"""
        self.keyboard_container.clear_widgets()
        self.keyboard_keys = {}
        
        if language == 'tr':
            rows = [
                ['E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Ğ', 'Ü'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ş', 'İ'],
                ['⏎', 'Z', 'C', 'V', 'B', 'N', 'M', 'Ö', 'Ç', '⌫']
            ]
        else:
            rows = [
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                ['⏎', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫']
            ]
            
        for row in rows:
            row_layout = BoxLayout(spacing=dp(4), size_hint_y=None, height=dp(50))
            row_layout.add_widget(Label(size_hint_x=0.05))
            
            for key in row:
                if key == '⏎':
                    app = App.get_running_app()
                    btn = MDRaisedButton(
                        text='GİR',
                        font_size=sp(14),
                        size_hint=(None, None),
                        size=(dp(50), dp(50)),
                        md_bg_color=app.theme_manager.get_color(
                            'correct', 
                            app.settings['theme'] == 'Dark'
                        )
                    )
                    btn.bind(on_release=lambda x: self.on_enter())
                elif key == '⌫':
                    btn = MDRaisedButton(
                        text='SİL',
                        font_size=sp(14),
                        size_hint=(None, None),
                        size=(dp(50), dp(50))
                    )
                    btn.bind(on_release=lambda x: self.on_backspace())
                else:
                    btn = KeyboardKey(key, self.on_key_press)
                    self.keyboard_keys[key] = btn
                    
                row_layout.add_widget(btn)
                
            row_layout.add_widget(Label(size_hint_x=0.05))
            self.keyboard_container.add_widget(row_layout)
            
    def create_progress_indicator(self, max_attempts):
        """İlerleme göstergesi oluştur"""
        self.progress_box.clear_widgets()
        
        for i in range(max_attempts):
            indicator = Label(
                text='○',
                size_hint_x=1.0/max_attempts,
                font_size=sp(20)
            )
            self.progress_box.add_widget(indicator)
            
    def update_progress_indicator(self):
        """İlerleme göstergesini güncelle"""
        current = self.game_logic.current_attempt
        
        for i, child in enumerate(self.progress_box.children[::-1]):
            if i < current:
                if self.game_logic.won:
                    child.text = '●'
                    child.color = (0.42, 0.67, 0.39, 1)  # Yeşil
                else:
                    child.text = '●'
                    child.color = (0.47, 0.49, 0.49, 1)  # Gri
            elif i == current:
                child.text = '◉'
                child.color = (0.77, 0.69, 0.35, 1)  # Sarı
            else:
                child.text = '○'
                child.color = (0.5, 0.5, 0.5, 1)
                
    def on_key_press(self, letter):
        """Harf tuşuna basıldığında"""
        if self.game_logic.is_game_over():
            return
            
        app = App.get_running_app()
        
        word_length = len(self.letter_boxes[0])
        if len(self.current_guess) < word_length:
            self.current_guess += letter
            self.update_current_row()
            
            # Ses çal
            if app.sound_manager.enabled:
                app.sound_manager.play_key_sound()
                
            # Metrik kaydet
            self.game_metrics['key_presses'] += 1
            
    def on_backspace(self):
        """Silme tuşuna basıldığında"""
        if self.current_guess:
            self.current_guess = self.current_guess[:-1]
            self.update_current_row()
            
            app = App.get_running_app()
            if app.sound_manager.enabled:
                app.sound_manager.play_delete_sound()
                
            self.game_metrics['backspaces'] += 1
            
    def on_enter(self):
        """Enter tuşuna basıldığında - GELİŞTİRİLMİŞ"""
        if self.game_logic.is_game_over():
            return
            
        app = App.get_running_app()
        word_length = len(self.letter_boxes[0])
        
        if len(self.current_guess) != word_length:
            self.show_info_dialog("Lütfen tam kelimeyi girin!")
            if app.sound_manager.enabled:
                app.sound_manager.play_error_sound()
            self.game_metrics['invalid_attempts'] += 1
            return
            
        # Ses çal
        if app.sound_manager.enabled:
            app.sound_manager.play_enter_sound()
            
        self.game_metrics['enters'] += 1
        
        # Tahmini kontrol et
        result = self.game_logic.make_guess(self.current_guess)
        
        if result is None:
            self.show_info_dialog("Geçersiz kelime!")
            if app.sound_manager.enabled:
                app.sound_manager.play_error_sound()
            self.game_metrics['invalid_attempts'] += 1
            return
            
        # Animasyonları başlat (ÖNEMLİ: Renk kodları burada uygulanıyor!)
        self.animate_guess(result)
        
        # Klavye renklerini güncelle (ÖNEMLİ: Klavye harfleri de renkleniyor!)
        self.update_keyboard_colors(result)
        
        # İlerleme göstergesini güncelle
        self.update_progress_indicator()
        
        # Tahmini temizle
        self.current_guess = ""
        
        # Oyun bitti mi kontrol et
        if self.game_logic.is_game_over():
            self.end_game()
            
    def update_current_row(self):
        """Mevcut satırı güncelle"""
        current_attempt = self.game_logic.current_attempt
        row_boxes = self.letter_boxes[current_attempt]
        
        for i, box in enumerate(row_boxes):
            if i < len(self.current_guess):
                box.text = self.current_guess[i]
            else:
                box.text = ""
                
    def animate_guess(self, result):
        """
        Tahmin animasyonlarını başlat
        ÖNEMLİ: Renk kodları burada uygulanıyor!
        - correct → Yeşil
        - present → Sarı
        - absent → Gri
        """
        current_attempt = self.game_logic.current_attempt - 1
        row_boxes = self.letter_boxes[current_attempt]
        app = App.get_running_app()
        theme_manager = app.theme_manager
        dark_mode = app.settings['theme'] == 'Dark'
        sound_manager = app.sound_manager
        
        for i, (box, status) in enumerate(zip(row_boxes, result)):
            # Sırayla animasyon başlat (cascade effect)
            Clock.schedule_once(
                lambda dt, b=box, s=status: self.animate_box(
                    b, s, theme_manager, dark_mode, sound_manager
                ),
                i * 0.1
            )
            
    def animate_box(self, box, status, theme_manager, dark_mode, sound_manager):
        """
        Tek bir kutuyu animasyonla renklendir
        ÖNEMLİ: Renk kodlarının uygulandığı yer!
        """
        if status == 'correct':
            box.animate_correct(theme_manager, dark_mode, sound_manager)
        elif status == 'present':
            box.animate_present(theme_manager, dark_mode, sound_manager)
        else:  # absent
            box.animate_absent(theme_manager, dark_mode, sound_manager)
            
    def update_keyboard_colors(self, result):
        """
        Klavye tuşlarının renklerini güncelle
        ÖNEMLİ: Klavye harflerinin renkleri burada değişiyor!
        """
        current_attempt = self.game_logic.current_attempt - 1
        guess = self.game_logic.guesses[current_attempt]
        app = App.get_running_app()
        theme_manager = app.theme_manager
        dark_mode = app.settings['theme'] == 'Dark'
        
        for letter, status in zip(guess, result):
            if letter in self.keyboard_keys:
                key = self.keyboard_keys[letter]
                # Daha iyi duruma öncelik ver
                if status == 'correct':
                    key.update_color('correct', theme_manager, dark_mode)
                elif status == 'present' and key.state != 'correct':
                    key.update_color('present', theme_manager, dark_mode)
                elif status == 'absent' and key.state == 'normal':
                    key.update_color('absent', theme_manager, dark_mode)
                    
    def end_game(self):
        """Oyunu bitir"""
        # Zamanlayıcıyı durdur
        if self.timer_event:
            self.timer_event.cancel()
            
        # Metrikleri kaydet
        self.game_metrics['end_time'] = time.time()
        self.game_metrics['total_time'] = (
            self.game_metrics['end_time'] - self.game_metrics['start_time']
        )
        
        # İstatistikleri kaydet
        app = App.get_running_app()
        app.statistics.record_game(
            won=self.game_logic.is_won(),
            attempts=self.game_logic.current_attempt,
            word_length=app.settings['word_length'],
            language=app.settings['language']
        )
        
        # Oyun sonu diyaloğunu göster
        Clock.schedule_once(lambda dt: self.show_game_over_dialog(), 0.5)
        
    def show_game_over_dialog(self):
        """Oyun sonu diyaloğunu göster"""
        app = App.get_running_app()
        
        if self.game_logic.is_won():
            title = "🎉 TEBRİKLER!"
            text = f"Kelimeyi {self.game_logic.current_attempt} tahminde buldunuz!\n"
            text += f"Süre: {int(self.game_metrics['total_time'])} saniye"
            
            if app.sound_manager.enabled:
                app.sound_manager.play_win_sound()
        else:
            title = "😢 Oyun Bitti"
            text = f"Doğru kelime: {self.game_logic.secret_word}\n"
            text += f"Süre: {int(self.game_metrics['total_time'])} saniye"
            
            if app.sound_manager.enabled:
                app.sound_manager.play_lose_sound()
            
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="TEKRAR OYNA",
                    on_release=lambda x: self.restart_game(dialog)
                ),
                MDFlatButton(
                    text="İSTATİSTİKLER",
                    on_release=lambda x: self.show_stats(dialog)
                ),
                MDRaisedButton(
                    text="ANA MENÜ",
                    on_release=lambda x: self.go_to_menu(dialog)
                ),
            ],
        )
        dialog.open()
        
    def restart_game(self, dialog):
        """Oyunu yeniden başlat"""
        dialog.dismiss()
        self.initialize_game()
        
    def show_stats(self, dialog):
        """İstatistikleri göster"""
        dialog.dismiss()
        App.get_running_app().root.current = 'statistics'
        
    def go_to_menu(self, dialog):
        """Ana menüye dön"""
        dialog.dismiss()
        if self.timer_event:
            self.timer_event.cancel()
        App.get_running_app().root.current = 'menu'
        
    def go_back(self, button):
        """Geri butonu"""
        if self.timer_event:
            self.timer_event.cancel()
        App.get_running_app().root.current = 'menu'
        
    def show_info_dialog(self, message):
        """Bilgi diyaloğu göster"""
        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(
                text="TAMAM", 
                on_release=lambda x: dialog.dismiss()
            )],
        )
        dialog.open()
        
    def show_error_dialog(self, message):
        """Hata diyaloğu göster"""
        dialog = MDDialog(
            title="HATA",
            text=message,
            buttons=[MDRaisedButton(
                text="TAMAM", 
                on_release=lambda x: dialog.dismiss()
            )],
        )
        dialog.open()
        
    def show_tutorial(self):
        """İlk oyun tutorial'ı"""
        tutorial_text = """
🎮 NASIL OYNANIR?

1️⃣ Kelimeyi tahmin edin
2️⃣ GİR tuşuna basın
3️⃣ Renk kodlarını izleyin:

🟩 Yeşil: Doğru harf, doğru yer
🟨 Sarı: Doğru harf, yanlış yer
⬜ Gri: Yanlış harf

4️⃣ {attempts} tahmin hakkınız var
5️⃣ Kelimeyi bulmaya çalışın!

İyi şanslar! 🍀
        """.format(attempts=self.game_logic.max_attempts)
        
        dialog = MDDialog(
            title="🎓 HOŞ GELDİNİZ",
            text=tutorial_text,
            buttons=[MDRaisedButton(
                text="BAŞLA", 
                on_release=lambda x: dialog.dismiss()
            )],
        )
        dialog.open()
        
    def show_game_settings(self, button):
        """Oyun içi ayarlar menüsü"""
        # TODO: Erişilebilirlik ayarları eklenebilir
        pass


class WordleApp(MDApp):
    """Ana uygulama sınıfı - Geliştirilmiş"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = self.load_settings()
        self.statistics = Statistics()
        self.sound_manager = SoundManager(enabled=self.settings.get('sound_enabled', True))
        self.theme_manager = ThemeManager()
        self.theme_manager.set_current_theme(self.settings.get('color_theme', 'classic'))
        
    def build(self):
        """Uygulamayı oluştur"""
        self.theme_cls.theme_style = self.settings['theme']
        self.theme_cls.primary_palette = "Green"
        
        # Ekran yöneticisi
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen())
        sm.add_widget(GameScreen())
        sm.add_widget(StatisticsScreen())
        
        return sm
        
    def load_settings(self):
        """Ayarları yükle"""
        default_settings = {
            'theme': 'Light',
            'language': 'tr',
            'word_length': 5,
            'sound_enabled': True,
            'color_theme': 'classic'
        }
        
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    for key, value in default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
        except Exception as e:
            print(f"Ayarlar yüklenirken hata: {e}")
            
        return default_settings
        
    def save_settings(self):
        """Ayarları kaydet"""
        try:
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ayarlar kaydedilirken hata: {e}")


if __name__ == '__main__':
    WordleApp().run()

"""
Wordle Tarzı Kelime Oyunu - v2.1 FINAL
Python 3.10+ | Kivy | KivyMD

DÜZELTİLEN SORUNLAR:
1. Yazarken harfler görünüyor (siyah metin)
2. Doğru kutular renkleniyor (grid kutuları)
3. Sol alt köşedeki boş kutu kaldırıldı
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
import json
import os
import time

from words import WordManager
from game_logic import GameLogic
from statistics import Statistics
from sounds import SoundManager
from themes import ThemeManager


class LetterBox(Label):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(60), dp(60))
        self.font_size = sp(32)
        self.bold = True
        self.halign = 'center'
        self.valign = 'middle'
        self.status = 'empty'
        
        # Bind pozisyon değişikliklerini
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        
    def update_graphics(self, *args):
        """Canvas'ı güncelle"""
        self.canvas.before.clear()
        
        app = App.get_running_app()
        if not app:
            return
            
        theme_manager = app.theme_manager
        dark_mode = app.settings.get('theme', 'Light') == 'Dark'
        
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle, Line
            
            if self.status == 'correct':
                # Yeşil arka plan
                Color(*theme_manager.get_color('correct', dark_mode))
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
                self.color = (1, 1, 1, 1)  # Beyaz metin
                
            elif self.status == 'present':
                # Sarı arka plan
                Color(*theme_manager.get_color('present', dark_mode))
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
                self.color = (1, 1, 1, 1)  # Beyaz metin
                
            elif self.status == 'absent':
                # Gri arka plan
                Color(*theme_manager.get_color('absent', dark_mode))
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
                self.color = (1, 1, 1, 1)  # Beyaz metin
                
            elif self.status == 'typing' and self.text:
                # DÜZELTME: Yazarken açık gri arka plan + SİYAH metin
                Color(0.9, 0.9, 0.9, 1)  # Açık gri arka plan
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
                self.color = (0, 0, 0, 1)  # SİYAH metin (GÖRÜNÜR!)
                
            else:
                # Boş - sadece border
                border_color = theme_manager.get_color('border', dark_mode)
                Color(*border_color)
                Line(
                    rounded_rectangle=(
                        self.x, self.y, 
                        self.width, self.height, 
                        dp(5)
                    ), 
                    width=2
                )
                # DÜZELTME: Boş kutuda da siyah metin
                self.color = (0, 0, 0, 1) if not dark_mode else (1, 1, 1, 1)
        
    def set_status(self, status):
        """Kutu durumunu ayarla"""
        self.status = status
        self.update_graphics()
        
    def animate_reveal(self, status, delay=0):
        """Flip animasyonu ile rengi ortaya çıkar"""
        def start_animation(dt):
            # Küçült
            anim1 = Animation(
                size=(self.width, dp(5)), 
                duration=0.12
            )
            # Büyüt
            anim2 = Animation(
                size=(self.width, dp(60)), 
                duration=0.12
            )
            
            def change_status(anim, widget):
                self.set_status(status)
                
            anim1.bind(on_complete=change_status)
            anim1.bind(on_complete=lambda *args: anim2.start(self))
            anim1.start(self)
            
        if delay > 0:
            Clock.schedule_once(start_animation, delay)
        else:
            start_animation(0)
            
    def shake(self):
        """Titreme animasyonu"""
        original_x = self.x
        anim = (
            Animation(x=original_x - dp(3), duration=0.05) +
            Animation(x=original_x + dp(3), duration=0.05) +
            Animation(x=original_x - dp(3), duration=0.05) +
            Animation(x=original_x, duration=0.05)
        )
        anim.start(self)


class KeyboardKey(MDRaisedButton):
    """Klavye tuşu"""
    
    def __init__(self, letter, callback, **kwargs):
        super().__init__(**kwargs)
        self.text = letter
        self.letter = letter
        self.font_size = sp(16)
        self.size_hint = (None, None)
        self.size = (dp(35), dp(50))
        self.status = 'normal'
        
        app = App.get_running_app()
        if app:
            theme_manager = app.theme_manager
            dark_mode = app.settings.get('theme', 'Light') == 'Dark'
            self.md_bg_color = theme_manager.get_color('keyboard', dark_mode)
            self.text_color = theme_manager.get_color('text', dark_mode)
        
        self.on_release = lambda: callback(letter)
        
    def update_color(self, status):
        """Tuş rengini güncelle"""
        self.status = status
        
        app = App.get_running_app()
        if not app:
            return
            
        theme_manager = app.theme_manager
        dark_mode = app.settings.get('theme', 'Light') == 'Dark'
        
        if status == 'correct':
            self.md_bg_color = theme_manager.get_color('correct', dark_mode)
            self.text_color = (1, 1, 1, 1)
        elif status == 'present':
            self.md_bg_color = theme_manager.get_color('present', dark_mode)
            self.text_color = (1, 1, 1, 1)
        elif status == 'absent':
            self.md_bg_color = theme_manager.get_color('absent', dark_mode)
            self.text_color = (1, 1, 1, 1)


class StatisticsScreen(Screen):
    """İstatistik ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'statistics'
        self.build_ui()
        
    def build_ui(self):
        from kivymd.uix.card import MDCard
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Üst bar
        top_bar = BoxLayout(size_hint_y=0.08)
        back_btn = MDIconButton(icon='arrow-left', on_release=self.go_back)
        title = MDLabel(text="İSTATİSTİKLER", font_style='H5', halign='center')
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)
        top_bar.add_widget(Label())
        layout.add_widget(top_bar)
        
        # İstatistik container
        self.stats_container = BoxLayout(orientation='vertical', spacing=dp(10))
        layout.add_widget(self.stats_container)
        
        # Sıfırla butonu
        button_box = BoxLayout(size_hint_y=0.15, spacing=dp(10))
        reset_btn = MDRaisedButton(
            text="İSTATİSTİKLERİ SIFIRLA",
            on_release=self.confirm_reset
        )
        button_box.add_widget(reset_btn)
        layout.add_widget(button_box)
        
        self.add_widget(layout)
        
    def on_enter(self):
        self.update_statistics()
        
    def update_statistics(self):
        from kivymd.uix.card import MDCard
        
        self.stats_container.clear_widgets()
        
        app = App.get_running_app()
        stats = app.statistics.get_detailed_stats()
        
        # Kartlar
        summary_card = self.create_summary_card(stats)
        self.stats_container.add_widget(summary_card)
        
        distribution_card = self.create_distribution_card(stats)
        self.stats_container.add_widget(distribution_card)
        
    def create_summary_card(self, stats):
        from kivymd.uix.card import MDCard
        
        card = MDCard(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(200)
        )
        
        title = MDLabel(
            text="ÖZET", 
            font_style='H6', 
            size_hint_y=None, 
            height=dp(30)
        )
        card.add_widget(title)
        
        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(150))
        
        stat_items = [
            ("Oynanan", str(stats['games_played'])),
            ("Kazanma", f"{stats['win_rate']}%"),
            ("Mevcut Seri", str(stats['current_streak'])),
            ("Max Seri", str(stats['max_streak'])),
            ("Ort. Tahmin", str(stats['average_guesses'])),
            ("En İyi", str(stats['best_game']) if stats['best_game'] else "-")
        ]
        
        for label_text, value_text in stat_items:
            item_box = BoxLayout(orientation='vertical', spacing=dp(5))
            label = MDLabel(
                text=label_text, 
                halign='center', 
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(20)
            )
            value = MDLabel(
                text=value_text, 
                halign='center', 
                font_style='H5',
                size_hint_y=None,
                height=dp(40)
            )
            item_box.add_widget(label)
            item_box.add_widget(value)
            grid.add_widget(item_box)
            
        card.add_widget(grid)
        return card
        
    def create_distribution_card(self, stats):
        from kivymd.uix.card import MDCard
        
        card = MDCard(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(250)
        )
        
        title = MDLabel(
            text="TAHMİN DAĞILIMI", 
            font_style='H6', 
            size_hint_y=None, 
            height=dp(30)
        )
        card.add_widget(title)
        
        dist_box = BoxLayout(orientation='vertical', spacing=dp(8))
        
        distribution = stats['guess_distribution']
        max_count = max(distribution.values()) if distribution.values() else 1
        
        for attempt in sorted(distribution.keys()):
            count = distribution[attempt]
            
            row = BoxLayout(size_hint_y=None, height=dp(25), spacing=dp(5))
            
            num_label = MDLabel(
                text=str(attempt),
                size_hint_x=None,
                width=dp(30),
                halign='right'
            )
            row.add_widget(num_label)
            
            bar_container = BoxLayout()
            if count > 0:
                bar_width = (count / max_count) if max_count > 0 else 0
                bar = MDRaisedButton(
                    text=str(count),
                    size_hint_x=bar_width if bar_width > 0 else 0.1,
                    md_bg_color=get_color_from_hex('#6aaa64')
                )
                bar_container.add_widget(bar)
                if bar_width < 1:
                    bar_container.add_widget(Label(size_hint_x=1 - bar_width))
            
            row.add_widget(bar_container)
            dist_box.add_widget(row)
            
        card.add_widget(dist_box)
        return card
        
    def confirm_reset(self, button):
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
        app = App.get_running_app()
        app.statistics.reset_stats()
        dialog.dismiss()
        self.update_statistics()
        
    def go_back(self, button):
        App.get_running_app().root.current = 'menu'

class MenuScreen(Screen):
    """Ana menü ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'menu'
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Başlık
        title = MDLabel(
            text="LÜGAT",
            font_style='H2',
            halign='center',
            size_hint_y=0.2
        )
        layout.add_widget(title)
        
        # Ayarlar
        settings_box = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=0.4)
        
        self.language_btn = MDRaisedButton(
            text="Dil: Türkçe",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.language_btn.bind(on_release=self.show_language_menu)
        settings_box.add_widget(self.language_btn)
        
        self.word_length_btn = MDRaisedButton(
            text="Kelime Uzunluğu: 5",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.word_length_btn.bind(on_release=self.show_word_length_menu)
        settings_box.add_widget(self.word_length_btn)
        
        self.theme_btn = MDRaisedButton(
            text="Tema: Klasik",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.theme_btn.bind(on_release=self.show_theme_menu)
        settings_box.add_widget(self.theme_btn)
        
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
        
        start_btn = MDRaisedButton(
            text="OYUNA BAŞLA",
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex('#6aaa64')
        )
        start_btn.bind(on_release=self.start_game)
        button_box.add_widget(start_btn)
        
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
        
        self.language_menu = None
        self.word_length_menu = None
        self.theme_menu = None
        
    def show_language_menu(self, button):
        menu_items = [
            {"text": "Türkçe", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_language("tr", "Türkçe")},
            {"text": "English", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_language("en", "English")},
        ]
        self.language_menu = MDDropdownMenu(caller=button, items=menu_items, width_mult=4)
        self.language_menu.open()
        
    def show_word_length_menu(self, button):
        menu_items = [
            {"text": "5 Harf", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_word_length(5)},
            {"text": "6 Harf", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_word_length(6)},
            {"text": "7 Harf", "viewclass": "OneLineListItem",
             "on_release": lambda: self.set_word_length(7)},
        ]
        self.word_length_menu = MDDropdownMenu(caller=button, items=menu_items, width_mult=4)
        self.word_length_menu.open()
        
    def show_theme_menu(self, button):
        app = App.get_running_app()
        themes = app.theme_manager.get_theme_display_names()
        
        menu_items = [
            {"text": display_name, "viewclass": "OneLineListItem",
             "on_release": lambda t=theme_name, d=display_name: self.set_theme(t, d)}
            for theme_name, display_name in themes.items()
        ]
        self.theme_menu = MDDropdownMenu(caller=button, items=menu_items, width_mult=4)
        self.theme_menu.open()
        
    def set_language(self, lang_code, lang_name):
        app = App.get_running_app()
        app.settings['language'] = lang_code
        self.language_btn.text = f"Dil: {lang_name}"
        if self.language_menu:
            self.language_menu.dismiss()
        app.save_settings()
        
    def set_word_length(self, length):
        app = App.get_running_app()
        app.settings['word_length'] = length
        self.word_length_btn.text = f"Kelime Uzunluğu: {length}"
        if self.word_length_menu:
            self.word_length_menu.dismiss()
        app.save_settings()
        
    def set_theme(self, theme_name, display_name):
        app = App.get_running_app()
        app.settings['color_theme'] = theme_name
        app.theme_manager.set_current_theme(theme_name)
        self.theme_btn.text = f"Tema: {display_name}"
        if self.theme_menu:
            self.theme_menu.dismiss()
        app.save_settings()
        
    def toggle_sound(self, button):
        app = App.get_running_app()
        enabled = app.sound_manager.toggle()
        app.settings['sound_enabled'] = enabled
        self.sound_btn.text = f"Ses: {'Açık' if enabled else 'Kapalı'}"
        app.save_settings()
        
    def start_game(self, button):
        app = App.get_running_app()
        game_screen = app.root.get_screen('game')
        game_screen.initialize_game()
        app.root.current = 'game'
        
    def show_statistics(self, button):
        App.get_running_app().root.current = 'statistics'


class GameScreen(Screen):
    """
    Oyun ekranı
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'game'
        self.game_logic = None
        self.letter_boxes = []
        self.keyboard_keys = {}
        self.current_guess = ""
        self.start_time = None
        self.timer_event = None
        
        # Ana layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Üst bar
        top_bar = BoxLayout(size_hint_y=0.08, spacing=dp(10))
        back_btn = MDIconButton(icon='arrow-left', on_release=self.go_back)
        top_bar.add_widget(back_btn)
        
        self.timer_label = MDLabel(
            text="00:00",
            halign='center',
            font_style='H6'
        )
        top_bar.add_widget(self.timer_label)
        
        # DÜZELTME: Boş Label kaldırıldı (sol alt köşe sorunu)
        top_bar.add_widget(MDIconButton(icon='', disabled=True))  # Spacer
        
        main_layout.add_widget(top_bar)
        
        # Grid container
        self.grid_container = BoxLayout(orientation='vertical', size_hint_y=0.57)
        main_layout.add_widget(self.grid_container)
        
        # Klavye
        self.keyboard_container = BoxLayout(
            orientation='vertical', 
            size_hint_y=0.35, 
            spacing=dp(5)
        )
        main_layout.add_widget(self.keyboard_container)
        
        self.add_widget(main_layout)
        
    def initialize_game(self):
        """Oyunu başlat"""
        app = App.get_running_app()
        word_length = app.settings['word_length']
        max_attempts = word_length
        language = app.settings['language']
        
        # Zamanlayıcı
        self.start_time = time.time()
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1.0)
        
        # Kelime seç
        word_manager = WordManager()
        secret_word = word_manager.get_random_word(word_length, language)
        
        if not secret_word:
            self.show_error_dialog("Kelime listesi yüklenemedi!")
            return
            
        # Oyun mantığı
        self.game_logic = GameLogic(secret_word, max_attempts)
        self.current_guess = ""
        
        # Grid ve klavye
        self.create_grid(max_attempts, word_length)
        self.create_keyboard(language)
        
        # Tutorial
        if app.settings.get('first_game', True):
            self.show_tutorial()
            app.settings['first_game'] = False
            app.save_settings()
            
    def update_timer(self, dt):
        """Zamanlayıcı"""
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.text = f"{minutes:02d}:{seconds:02d}"
            
    def create_grid(self, rows, cols):
        """
        Grid oluştur
        DÜZELTME: Referanslar doğru saklanıyor
        """
        self.grid_container.clear_widgets()
        self.letter_boxes = []
        
        # Grid layout
        grid = GridLayout(
            cols=cols, 
            spacing=dp(5), 
            size_hint=(None, None),
            padding=(0, 0, 0, 0)
        )
        grid.bind(minimum_size=grid.setter('size'))
        
        # Ortala
        grid_wrapper = BoxLayout()
        grid_wrapper.add_widget(Label(size_hint_x=0.1))  # Sol padding
        grid_wrapper.add_widget(grid)
        grid_wrapper.add_widget(Label(size_hint_x=0.1))  # Sağ padding
        
        # DÜZELTME: Kutuları doğru sırada sakla
        for row_idx in range(rows):
            row_boxes = []
            for col_idx in range(cols):
                box = LetterBox()
                grid.add_widget(box)
                row_boxes.append(box)  # Referansı sakla
            self.letter_boxes.append(row_boxes)  # Satırı sakla
            
        self.grid_container.add_widget(grid_wrapper)
        
    def create_keyboard(self, language):
        """Klavye oluştur"""
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
                    btn = MDRaisedButton(
                        text='GİR',
                        font_size=sp(14),
                        size_hint=(None, None),
                        size=(dp(50), dp(50)),
                        md_bg_color=get_color_from_hex('#6aaa64')
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
    
    def on_key_press(self, letter):
        """
        Harf tuşuna basıldığında
        DÜZELTME: Harfler görünür şekilde yazılıyor
        """
        if self.game_logic and self.game_logic.is_game_over():
            return
            
        app = App.get_running_app()
        word_length = len(self.letter_boxes[0])
        
        if len(self.current_guess) < word_length:
            self.current_guess += letter
            self.update_current_row()  # Harfleri göster
            
            # Ses
            if app.sound_manager and app.sound_manager.enabled:
                app.sound_manager.play_key_sound()
                
    def on_backspace(self):
        """Silme"""
        if self.current_guess:
            self.current_guess = self.current_guess[:-1]
            self.update_current_row()
            
            app = App.get_running_app()
            if app.sound_manager and app.sound_manager.enabled:
                app.sound_manager.play_delete_sound()
                
    def on_enter(self):
        """
        Enter tuşu
        DÜZELTME: Grid kutuları doğru renkleniyor
        """
        if self.game_logic and self.game_logic.is_game_over():
            return
            
        app = App.get_running_app()
        word_length = len(self.letter_boxes[0])
        
        if len(self.current_guess) != word_length:
            self.show_info_dialog("Lütfen tam kelimeyi girin!")
            if app.sound_manager and app.sound_manager.enabled:
                app.sound_manager.play_error_sound()
            self.shake_current_row()
            return
            
        # Ses
        if app.sound_manager and app.sound_manager.enabled:
            app.sound_manager.play_enter_sound()
        
        # Tahmin kontrolü
        result = self.game_logic.make_guess(self.current_guess)
        
        if result is None:
            self.show_info_dialog("Geçersiz kelime!")
            if app.sound_manager and app.sound_manager.enabled:
                app.sound_manager.play_error_sound()
            self.shake_current_row()
            return
            
        # DÜZELTME: Grid satırını renklendir (klavye altındaki değil!)
        self.reveal_current_row(result)
        
        # Klavyeyi güncelle
        Clock.schedule_once(
            lambda dt: self.update_keyboard_colors(result), 
            len(result) * 0.15 + 0.2
        )
        
        # Tahmini temizle
        self.current_guess = ""
        
        # Oyun bitti mi?
        if self.game_logic.is_game_over():
            Clock.schedule_once(lambda dt: self.end_game(), 1.0)
            
    def update_current_row(self):
        """
        Mevcut satırı güncelle
        DÜZELTME: Yazarken SİYAH metin, açık gri arka plan
        """
        if not self.game_logic:
            return
            
        current_attempt = self.game_logic.current_attempt
        if current_attempt >= len(self.letter_boxes):
            return
            
        row_boxes = self.letter_boxes[current_attempt]
        
        for i, box in enumerate(row_boxes):
            if i < len(self.current_guess):
                box.text = self.current_guess[i]
                box.set_status('typing')  # Açık gri arka plan + SİYAH metin
            else:
                box.text = ""
                box.set_status('empty')  # Border only
                
    def shake_current_row(self):
        """Mevcut satırı titret"""
        if not self.game_logic:
            return
            
        current_attempt = self.game_logic.current_attempt
        if current_attempt >= len(self.letter_boxes):
            return
            
        row_boxes = self.letter_boxes[current_attempt]
        for box in row_boxes:
            box.shake()
            
    def reveal_current_row(self, result):
        """
        MEVCUT satırı renklendir
        DÜZELTME: Doğru satır renkleniyor (current_attempt - 1)
        
        Args:
            result: ['correct', 'present', 'absent'] listesi
        """
        app = App.get_running_app()
        
        # DÜZELTME: Bir önceki satır (yeni onaylanan tahmin)
        current_attempt = self.game_logic.current_attempt - 1
        
        if current_attempt < 0 or current_attempt >= len(self.letter_boxes):
            print(f"HATA: Geçersiz satır indeksi: {current_attempt}")
            return
            
        # DÜZELTME: Doğru satırı al
        row_boxes = self.letter_boxes[current_attempt]
        
        print(f"DEBUG: Satır {current_attempt} renkleniyor, {len(row_boxes)} kutu var")
        
        # Sırayla animasyon
        for i, (box, status) in enumerate(zip(row_boxes, result)):
            delay = i * 0.15
            box.animate_reveal(status, delay)
            
            # Ses efekti
            if app.sound_manager and app.sound_manager.enabled:
                if status == 'correct':
                    Clock.schedule_once(
                        lambda dt, s=app.sound_manager: s.play_correct_sound(), 
                        delay + 0.1
                    )
                elif status == 'present':
                    Clock.schedule_once(
                        lambda dt, s=app.sound_manager: s.play_present_sound(), 
                        delay + 0.1
                    )
                    
    def update_keyboard_colors(self, result):
        """Klavye tuşlarını renklendir"""
        if not self.game_logic:
            return
            
        current_attempt = self.game_logic.current_attempt - 1
        if current_attempt >= len(self.game_logic.guesses):
            return
            
        guess = self.game_logic.guesses[current_attempt]
        
        for letter, status in zip(guess, result):
            if letter in self.keyboard_keys:
                key = self.keyboard_keys[letter]
                # Daha iyi duruma öncelik ver
                if status == 'correct':
                    key.update_color('correct')
                elif status == 'present' and key.status != 'correct':
                    key.update_color('present')
                elif status == 'absent' and key.status not in ['correct', 'present']:
                    key.update_color('absent')
                    
    def end_game(self):
        """Oyunu bitir"""
        if self.timer_event:
            self.timer_event.cancel()
            
        # İstatistik kaydet
        app = App.get_running_app()
        if self.start_time and self.game_logic:
            total_time = int(time.time() - self.start_time)
            app.statistics.record_game(
                won=self.game_logic.is_won(),
                attempts=self.game_logic.current_attempt,
                word_length=app.settings['word_length'],
                language=app.settings['language']
            )
        
        self.show_game_over_dialog()
        
    def show_game_over_dialog(self):
        """Oyun sonu diyaloğu"""
        app = App.get_running_app()
        
        if self.game_logic.is_won():
            title = "🎉 TEBRİKLER!"
            text = f"Kelimeyi {self.game_logic.current_attempt} tahminde buldunuz!"
            if self.start_time:
                elapsed = int(time.time() - self.start_time)
                text += f"\nSüre: {elapsed} saniye"
            
            if app.sound_manager and app.sound_manager.enabled:
                app.sound_manager.play_win_sound()
        else:
            title = "😢 Oyun Bitti"
            text = f"Doğru kelime: {self.game_logic.secret_word}"
            if self.start_time:
                elapsed = int(time.time() - self.start_time)
                text += f"\nSüre: {elapsed} saniye"
            
            if app.sound_manager and app.sound_manager.enabled:
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
        dialog.dismiss()
        self.initialize_game()
        
    def show_stats(self, dialog):
        dialog.dismiss()
        App.get_running_app().root.current = 'statistics'
        
    def go_to_menu(self, dialog):
        dialog.dismiss()
        if self.timer_event:
            self.timer_event.cancel()
        App.get_running_app().root.current = 'menu'
        
    def go_back(self, button):
        if self.timer_event:
            self.timer_event.cancel()
        App.get_running_app().root.current = 'menu'
        
    def show_info_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(
                text="TAMAM", 
                on_release=lambda x: dialog.dismiss()
            )],
        )
        dialog.open()
        
    def show_error_dialog(self, message):
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
        """Tutorial"""
        tutorial_text = f"""
🎮 NASIL OYNANIR?

1️⃣ Kelimeyi tahmin edin
2️⃣ GİR tuşuna basın
3️⃣ Renk kodlarını izleyin:

🟩 Yeşil: Doğru harf, doğru yer
🟨 Sarı: Doğru harf, yanlış yer
⬜ Gri: Yanlış harf

4️⃣ {self.game_logic.max_attempts if self.game_logic else 5} tahmin hakkınız var

İyi şanslar! 🍀
        """
        
        dialog = MDDialog(
            title="🎓 HOŞ GELDİNİZ",
            text=tutorial_text,
            buttons=[MDRaisedButton(
                text="BAŞLA", 
                on_release=lambda x: dialog.dismiss()
            )],
        )
        dialog.open()


class WordleApp(MDApp):
    """Ana uygulama sınıfı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = self.load_settings()
        self.statistics = Statistics()
        self.sound_manager = SoundManager(enabled=self.settings.get('sound_enabled', True))
        self.theme_manager = ThemeManager()
        self.theme_manager.set_current_theme(self.settings.get('color_theme', 'classic'))
        
    def build(self):
        """Uygulamayı oluştur"""
        self.theme_cls.theme_style = self.settings.get('theme', 'Light')
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
            'color_theme': 'classic',
            'first_game': True
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
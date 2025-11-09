"""
Oyun Ekranı Modülü - Tam Versiyon
Tüm özellikler entegre edilmiş
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.utils import get_color_from_hex
import time


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
        self.state = state
        if state == 'correct':
            self.md_bg_color = theme_manager.get_color('correct', dark_mode)
            self.text_color = (1, 1, 1, 1)
        elif state == 'present':
            self.md_bg_color = theme_manager.get_color('present', dark_mode)
            self.text_color = (1, 1, 1, 1)
        elif state == 'absent':
            self.md_bg_color = theme_manager.get_color('absent', dark_mode)
            self.text_color = (1, 1, 1, 1)


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

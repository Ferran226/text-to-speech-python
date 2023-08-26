import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from newspaper import Article
from gtts import gTTS
import pygame
import newspaper
import traceback
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox



# Descargar los recursos necesarios de NLTK
nltk.download("stopwords")
nltk.download("punkt")

# Mapeo de idiomas para convertir la selección
#  en códigos de idioma compatibles con gTTS
language_mapping = {
    "Inglés": "en",
    "Español": "es"
    }

# Mapeo de voces para convertir la selección en 
# opciones de voz compatibles con gTTS
voice_mapping = {
    "Predeterminado": "default",
    "Masculino": "male",
    "Femenino": "female"
    }


class TextToSpeechApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text to Speech News App")  # Titulo del la APP

        # Definir las variables language_var y voice_var
        self.language_var = tk.StringVar()
        self.voice_var = tk.StringVar()
        self.create_widgets()
        
    def play_audio(self):
        try:
            text = self.input_text.get("1.0", "end-1c")

            if not text:
                messagebox.showerror("Error", "Por favor ingresa un texto para convertir en voz.")
                return
            
            selected_option = self.option_var.get()  # Obtén la opción seleccionada (Texto o URL)
            language = language_mapping[self.language_var.get()]  # Obtén el código de idioma
            voice_option = self.voice_var.get()  # Obtén la opción de voz
            
            if selected_option == "URL":
                article = newspaper.Article(text)
                article.download()
                article.parse()
                text = article.text  # Obtén el contenido de la URL

            voice = voice_mapping[voice_option]  # Obtén la opción de voz correspondiente

            # Convertir el texto a voz y reproducirlo
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save("audio_output.mp3")


            # Reproducir el audio usando pygame
            pygame.mixer.init()
            pygame.mixer.music.load("audio_output.mp3")
            pygame.mixer.music.play()

            # Mantener la aplicación en espera hasta que termine de reproducirse el audio
            while pygame.mixer.music.get_busy():
                continue

            # Mostrar mensaje de éxito
        except Exception as e:
            # Mostrar mensaje de error en caso de problemas
            messagebox.showerror("Error", f"Hubo un problema: {str(e)}")
            

    def create_widgets(self):
        # Menú desplegable para elegir la opción (Texto o URL)
        self.option_label = ttk.Label(self, text="Elige una opción:")
        self.option_label.pack(padx=10)
        self.option_var = tk.StringVar()  # Variable para almacenar la opción seleccionada
        self.option_combobox = ttk.Combobox(self, textvariable=self.option_var, values=["Texto", "URL"])
        self.option_combobox.pack(padx=10)

        # Área de entrada de texto para el usuario o URL
        self.input_text_label = ttk.Label(self, text="Ingresa el texto o URL:")
        self.input_text_label.pack(padx=10)
        self.input_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10, width=50)
        self.input_text.pack(pady=5)

        # Opciones de voz
        self.language_label = ttk.Label(self, text="Selecciona el idioma:")
        self.language_label.pack(pady=5)
        self.language_combobox = ttk.Combobox(self, textvariable=self.language_var, values=["Inglés", "Español"])
        self.language_combobox.pack(pady=5)

        self.voice_label = ttk.Label(self, text="Selecciona la voz:")
        self.voice_label.pack(pady=5)
        self.voice_combobox = ttk.Combobox(self, textvariable=self.voice_var, values=["Predeterminado", "Masculino", "Femenino"])
        self.voice_combobox.pack(pady=5)

        # Botón para reproducir el resumen en voz
        self.play_button = ttk.Button(self, text="Reproducir", command=self.play_audio)
        self.play_button.pack(side=tk.LEFT, padx=10, pady=10)  # Alineado a la izquierda

        # Botón para salir de la aplicación
        self.quit_button = ttk.Button(self, text="Salir", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT, padx=10, pady=10)  # Alineado a la derecha


if __name__ == "__main__":
    app = TextToSpeechApp()
    app.mainloop()
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import time

class LCDView:
    def __init__(self):
        # Initialisation de l'écran LCD
        PCF8574_address = 0x27
        PCF8574A_address = 0x3F

        # Tentative de connexion aux adresses I2C
        try:
            self.mcp = PCF8574_GPIO(PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(PCF8574A_address)
            except:
                print('Erreur d\'adresse I2C!')
                exit(1)

        # Configuration de l'écran LCD
        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=self.mcp)

        # Activation du rétroéclairage
        self.mcp.output(3, 1)
        self.lcd.begin(16, 2)
    
    def afficher_texte(self, text, row=0, col=0):
        # Affichage de texte à une position spécifique
        self.lcd.setCursor(col, row)
        self.lcd.message(text)
    
    def effacer(self):
        # Nettoyage de l'écran
        try:
            self.lcd.clear()
            self.lcd.setCursor(0, 0)
            self.lcd.message("                ")
            self.lcd.setCursor(0, 1)
            self.lcd.message("                ")
            self.lcd.setCursor(0, 0)
        except:
            pass
    
    def eteindre(self):
        # Extinction de l'écran
        try:
            self.effacer()
            self.mcp.output(3, 0)
        except:
            pass
    
    def afficher_bienvenue(self):
        # Message d'accueil
        self.effacer()
        self.afficher_texte("Sys de mesure", 0, 0)
        self.afficher_texte("VERT = activer", 1, 0)
    
    def afficher_demarrage_systeme(self):
        # Message de démarrage
        self.effacer()
        self.afficher_texte("Systeme demarre", 0, 0)
        self.afficher_texte("ROUGE = mesure", 1, 0)
    
    def afficher_arret_systeme(self):
        # Message d'arrêt
        self.effacer()
        self.afficher_texte("Systeme arrete", 0, 0)
        time.sleep(1)
        self.effacer()
        self.afficher_bienvenue()
    
    def afficher_mesure(self, distance):
        # Affichage de la mesure ponctuelle
        self.effacer()
        distance_cm = distance * 100  # Conversion en cm
        self.afficher_texte(f"Distance: {distance_cm:.2f} cm", 0, 0)
        self.afficher_texte("Mesure prise", 1, 0)
    
    def afficher_mesure_periodique(self, distance):
        # Affichage de la mesure périodique
        self.effacer()
        distance_cm = distance * 100  # Conversion en cm
        self.afficher_texte(f"Distance: {distance_cm:.2f} cm", 0, 0)
        self.afficher_texte("Mise a jour auto", 1, 0)
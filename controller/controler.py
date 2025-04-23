import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.platine import Platine
from model.mesure import Mesure
from view.lcd_view import LCDView
import time
import threading
import atexit

class Controleur:
    def __init__(self):
        # Initialisation des composants
        self.platine = Platine()
        self.lcd_view = LCDView()
        self.mesures = []
        self.update_thread = None
        self.running = False
        self.last_button_press = 0
        
        # Configuration des boutons
        self.platine.btn_vert.when_pressed = self.basculer_systeme
        self.platine.btn_rouge.when_pressed = self.prendre_mesure
        
        atexit.register(self.nettoyer)
        self.lcd_view.afficher_bienvenue()
    
    def basculer_systeme(self):
        # Éviter les rebonds de bouton
        current_time = time.time()
        if current_time - self.last_button_press < 1.0:
            return
            
        self.last_button_press = current_time
        system_running = self.platine.basculer_systeme()
        
        if system_running:
            self.running = True
            self.lcd_view.afficher_demarrage_systeme()
            self.demarrer_mise_a_jour_auto()
        else:
            self.running = False
            self.lcd_view.afficher_arret_systeme()
            self.arreter_mise_a_jour_auto()
        
        time.sleep(1.0)
    
    def prendre_mesure(self):
        # Vérifier si le système est actif
        if not self.platine.est_systeme_actif():
            self.lcd_view.effacer()
            self.lcd_view.afficher_texte("Systeme inactif!", 0, 0)
            self.lcd_view.afficher_texte("VERT pour activer", 1, 0)
            time.sleep(1.5)
            self.lcd_view.afficher_bienvenue()
            return
        
        # Obtenir la mesure
        distance = self.platine.obtenir_distance()
        
        # Créer et sauvegarder la mesure
        mesure = Mesure(distance)
        self.mesures.append(mesure)
        
        Mesure.sauvegarder_en_json([mesure])
        
        # Afficher la mesure
        self.lcd_view.afficher_mesure(distance)
        time.sleep(2)
        
        if self.platine.est_systeme_actif():
            self.lcd_view.afficher_demarrage_systeme()
    
    def mise_a_jour_auto(self):
        # Boucle de mise à jour automatique des mesures
        while self.running and self.platine.est_systeme_actif():
            try:
                if not self.running or not self.platine.est_systeme_actif():
                    break
                
                distance = self.platine.obtenir_distance()
                
                if self.running and self.platine.est_systeme_actif():
                    self.lcd_view.afficher_mesure_periodique(distance)
                else:
                    break
                
                # Attendre 5 secondes
                for _ in range(50):
                    if not (self.running and self.platine.est_systeme_actif()):
                        break
                    time.sleep(0.1)
            except Exception as e:
                print(f"Erreur dans la mise à jour automatique: {e}")
                time.sleep(5)
    
    def demarrer_mise_a_jour_auto(self):
        # Démarrer un thread de mise à jour
        if not self.running or not self.platine.est_systeme_actif():
            return
            
        if self.update_thread is None or not self.update_thread.is_alive():
            self.update_thread = threading.Thread(target=self.mise_a_jour_auto)
            self.update_thread.daemon = True
            self.update_thread.start()
    
    def arreter_mise_a_jour_auto(self):
        # Arrêter le thread de mise à jour
        self.running = False
        
        if self.update_thread is not None and self.update_thread.is_alive():
            try:
                self.update_thread.join(2.0)
            except:
                pass
            
        self.update_thread = None
    
    def executer(self):
        # Boucle principale
        try:
            while True:
                if not self.platine.est_systeme_actif() and self.running:
                    self.running = False
                    self.arreter_mise_a_jour_auto()
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.nettoyer()
    
    def nettoyer(self):
        # Nettoyage des ressources
        print("Nettoyage des ressources...")
        self.running = False
        self.arreter_mise_a_jour_auto()
        
        if hasattr(self, 'platine'):
            self.platine.nettoyer()
        
        if hasattr(self, 'lcd_view'):
            try:
                self.lcd_view.effacer()
                self.lcd_view.afficher_texte("Systeme arrete", 0, 0)
                time.sleep(0.5)
                self.lcd_view.effacer()
            except:
                pass
        
        print("Programme terminé proprement.")

if __name__ == "__main__":
    print("Démarrage du contrôleur directement...")
    controleur = Controleur()
    controleur.executer()
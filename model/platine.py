from gpiozero import Button, DistanceSensor

class Platine:
    def __init__(self):
        # Initialisation des composants GPIO
        self.btn_vert = Button(5)  # Bouton de démarrage/arrêt
        self.btn_rouge = Button(27)  # Bouton de mesure
        
        # Capteur de distance ultrasonique
        self.capteur = DistanceSensor(echo=12,
                                     trigger=17,
                                     max_distance=3)
        
        self.system_running = False
    
    def obtenir_distance(self):
        # Récupération de la distance
        return self.capteur.distance
    
    def basculer_systeme(self):
        # Activation/désactivation du système
        self.system_running = not self.system_running
        return self.system_running
    
    def est_systeme_actif(self):
        # Vérification de l'état du système
        return self.system_running
    
    def nettoyer(self):
        # Nettoyage des ressources GPIO
        pass
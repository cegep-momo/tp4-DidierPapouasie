from controller.controler import Controleur
import signal
import sys
import time

def gestionnaire_signal(sig, frame):
    # Gestionnaire pour arrêt propre
    print("\nArrêt du programme...")
    if 'controleur' in globals():
        controleur.nettoyer()
    time.sleep(0.5)
    sys.exit(0)

if __name__ == "__main__":
    # Configuration des signaux d'interruption
    signal.signal(signal.SIGINT, gestionnaire_signal)
    signal.signal(signal.SIGTERM, gestionnaire_signal)
    
    print("Démarrage du système de mesure de distance...")
    
    # Création et exécution du contrôleur
    controleur = Controleur()
    try:
        controleur.executer()
    except Exception as e:
        print(f"Erreur dans le programme principal: {e}")
    finally:
        controleur.nettoyer()
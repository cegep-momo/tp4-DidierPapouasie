from datetime import datetime
import json

class Mesure:
    def __init__(self, dataMesure, dateHeureMesure=None):
        # Constructeur avec date par défaut
        self.dateHeureMesure = dateHeureMesure if dateHeureMesure else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dataMesure = dataMesure
    
    def __repr__(self):
        # Représentation textuelle
        return f"Mesure(dateHeureMesure='{self.dateHeureMesure}', dataMesure={self.dataMesure})"
    
    def afficherMesure(self):
        # Affichage formaté
        return f"Date et heure: {self.dateHeureMesure}\nMesure: {self.dataMesure}"
    
    def vers_dict(self):
        # Conversion en dictionnaire
        return {
            "dateHeureMesure": self.dateHeureMesure,
            "dataMesure": self.dataMesure
        }
    
    @staticmethod
    def sauvegarder_en_json(mesures, filename="mesures.json"):
        # Sauvegarde en JSON
        try:
            # Conversion en dictionnaires
            mesures_dict = [m.vers_dict() for m in mesures]
            
            # Lecture des données existantes
            try:
                with open(filename, 'r') as f:
                    existing_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = []
            
            # Ajout des nouvelles mesures
            existing_data.extend(mesures_dict)
            
            # Écriture dans le fichier
            with open(filename, 'w') as f:
                json.dump(existing_data, f, indent=4)
                
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des mesures: {e}")
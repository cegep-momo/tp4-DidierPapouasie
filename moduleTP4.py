class Mesure:
    def __init__(self, dateHeureMesure, dataMesure):
        # Constructeur de la classe
        self.dateHeureMesure = dateHeureMesure
        self.dataMesure = dataMesure
    
    def __repr__(self):
        # Représentation textuelle de l'objet
        return f"Mesure du {self.dateHeureMesure}: {self.dataMesure}"
    
    def afficherMesure(self):
        # Affichage formaté des données
        return f"Date et heure: {self.dateHeureMesure}\nDonnées: {self.dataMesure}"
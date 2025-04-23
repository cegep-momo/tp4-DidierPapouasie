import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.platine import Platine
from unittest.mock import patch, MagicMock

class TestBoutonPoussoir(unittest.TestCase):
    """Tests unitaires pour les boutons-poussoirs"""
    
    @patch('gpiozero.Button')
    def setUp(self, mock_button):
        """Initialisation avec boutons simulés"""
        self.mock_button = mock_button
        self.platine = Platine()
        self.calls = mock_button.call_args_list
        
    def test_initialisation_bouton(self):
        """Vérification de l'initialisation du bouton vert"""
        self.assertEqual(self.calls[0][0][0], 5, "Le bouton vert doit être sur GPIO 5")
        self.assertFalse(self.platine.est_systeme_actif(), "Système inactif à l'initialisation")
    
    def test_execution_bouton_vert(self):
        """Test du comportement du bouton vert"""
        self.assertFalse(self.platine.est_systeme_actif())
        
        resultat = self.platine.basculer_systeme()
        self.assertTrue(resultat, "Premier appui: activer le système")
        self.assertTrue(self.platine.est_systeme_actif())
        
        resultat = self.platine.basculer_systeme()
        self.assertFalse(resultat, "Second appui: désactiver le système")
        self.assertFalse(self.platine.est_systeme_actif())

if __name__ == '__main__':
    unittest.main()
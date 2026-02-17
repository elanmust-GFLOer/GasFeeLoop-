import yaml
import os
import json
from openai import OpenAI
from .xp_fraud_detector import XPFraudDetector
from .mev_guard import MEVGuard
from .dao_rationality import DAORationality

class GFLOAICore:
    def __init__(self):
        # 1. Modulok betöltése
        self.fraud_detector = XPFraudDetector()
        self.mev_guard = MEVGuard()
        self.dao_logic = DAORationality()
        
        # 2. Axiómák betöltése
        # A fájl elérési útjának pontosítása
        base_path = os.path.dirname(__file__)
        axiom_path = os.path.join(base_path, 'axioms.yaml')
        
        try:
            with open(axiom_path, 'r') as f:
                self.axioms = yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ Axiom load error: {e}")
            self.axioms = {}

        # 3. OpenAI kliens
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ WARNING: OPENAI_API_KEY is missing!")
        self.client = OpenAI(api_key=api_key) if api_key else None

        print("✅ AI Core initialized and modules loaded!")

    def evaluate_axiom_compliance(self, data):
        # Itt jön majd a logika...
        return True

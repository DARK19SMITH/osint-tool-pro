#!/usr/bin/env python3
"""
Module de vérification d'emails
by Dvrk_Smith
"""

import requests
import hashlib
import json
import time
from colorama import Fore, Style

class EmailChecker:
    def __init__(self):
        self.api_key = ""  # À remplacer dans config.py
        self.timeout = 10
        self.headers = {
            'User-Agent': 'OSINT-Tool-Pro by Dvrk_Smith',
            'hibp-api-key': self.api_key
        }
    
    def check_hibp(self, email):
        """Vérifie l'email dans Have I Been Pwned"""
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    "breached": True,
                    "breaches": response.json(),
                    "breach_count": len(response.json())
                }
            elif response.status_code == 404:
                return {"breached": False, "breaches": [], "breach_count": 0}
            else:
                return {"error": f"Statut API: {response.status_code}"}
        
        except Exception as e:
            return {"error": str(e)}
    
    def check_emailrep(self, email):
        """Vérifie la réputation de l'email via EmailRep.io"""
        try:
            url = f"https://emailrep.io/{email}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "reputation": data.get('reputation', 'unknown'),
                    "suspicious": data.get('suspicious', False),
                    "details": data.get('details', {})
                }
            else:
                return {"error": f"Statut: {response.status_code}"}
        
        except Exception as e:
            return {"error": str(e)}
    
    def check_hunter(self, email):
        """Vérifie si l'email existe via Hunter.io"""
        try:
            # Format: api_key = "ton_api_key"
            api_key = ""  # À remplacer
            if not api_key:
                return {"error": "API key manquante"}
            
            url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('data', {})
                return {
                    "exists": result.get('status') == 'valid',
                    "score": result.get('score', 0),
                    "sources": result.get('sources', [])
                }
            else:
                return {"error": f"Statut: {response.status_code}"}
        
        except Exception as e:
            return {"error": str(e)}
    
    def comprehensive_check(self, email):
        """Vérification complète d'un email"""
        print(Fore.YELLOW + f"\n🔍 Analyse approfondie de: {email}")
        print(Fore.CYAN + "─" * 50)
        
        results = {}
        
        # 1. Vérification HIBP
        print(Fore.WHITE + "1. Vérification des fuites de données...")
        hibp_result = self.check_hibp(email)
        results['hibp'] = hibp_result
        
        if 'breached' in hibp_result and hibp_result['breached']:
            print(Fore.RED + f"   ❌ TROUVÉ dans {hibp_result['breach_count']} fuite(s)")
            for breach in hibp_result['breaches'][:3]:
                print(Fore.YELLOW + f"     • {breach.get('Name')} ({breach.get('BreachDate')})")
        else:
            print(Fore.GREEN + "   ✅ Aucune fuite trouvée")
        
        # 2. Vérification réputation
        print(Fore.WHITE + "\n2. Vérification réputation...")
        rep_result = self.check_emailrep(email)
        results['reputation'] = rep_result
        
        if 'reputation' in rep_result:
            rep = rep_result['reputation']
            if rep in ['high', 'good']:
                print(Fore.GREEN + f"   ✅ Bonne réputation")
            elif rep == 'medium':
                print(Fore.YELLOW + f"   ⚠️  Réputation moyenne")
            else:
                print(Fore.RED + f"   ❌ Mauvaise réputation")
        
        # 3. Vérification existence
        print(Fore.WHITE + "\n3. Vérification existence...")
        hunter_result = self.check_hunter(email)
        results['hunter'] = hunter_result
        
        if 'exists' in hunter_result:
            if hunter_result['exists']:
                print(Fore.GREEN + "   ✅ Email valide et actif")
                if 'score' in hunter_result:
                    print(Fore.WHITE + f"     Score de confiance: {hunter_result['score']}%")
            else:
                print(Fore.YELLOW + "   ⚠️  Email peut-être invalide")
        
        # Recommandations
        print(Fore.CYAN + "\n" + "═" * 50)
        print(Fore.GREEN + "🛡️  RECOMMANDATIONS DE SÉCURITÉ:")
        
        if hibp_result.get('breached', False):
            print(Fore.WHITE + "1. CHANGEZ VOTRE MOT DE PASSE immédiatement")
            print(Fore.WHITE + "2. Activez l'authentification à deux facteurs")
            print(Fore.WHITE + "3. Utilisez un gestionnaire de mots de passe")
            print(Fore.WHITE + "4. Surveillez vos comptes financiers")
        else:
            print(Fore.WHITE + "1. Continuez à utiliser des mots de passe uniques")
            print(Fore.WHITE + "2. Activez la 2FA si ce n'est pas fait")
            print(Fore.WHITE + "3. Évitez de réutiliser les mots de passe")
        
        return results

# Fonction de test
if __name__ == "__main__":
    checker = EmailChecker()
    test_email = input("Email à tester: ")
    checker.comprehensive_check(test_email)

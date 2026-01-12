#!/usr/bin/env python3
"""
Module d'analyse de numéros de téléphone
by Dvrk_Smith
"""

import re
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from colorama import Fore, Style

class PhoneAnalyzer:
    def __init__(self):
        self.api_keys = {}
        self.timeout = 10
        
    def validate_phone(self, phone_number):
        """Valide et formate le numéro de téléphone"""
        try:
            # Nettoyage du numéro
            phone = re.sub(r'[^\d+]', '', phone_number)
            
            # Ajoute le + si absent mais commence par 33
            if phone.startswith('33') and not phone.startswith('+'):
                phone = '+' + phone
            
            # Parse avec phonenumbers
            parsed = phonenumbers.parse(phone, None)
            
            if phonenumbers.is_valid_number(parsed):
                return {
                    'valid': True,
                    'formatted': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                    'national': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                    'e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                    'parsed': parsed
                }
            else:
                return {'valid': False, 'error': 'Numéro invalide'}
                
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def get_carrier_info(self, parsed_number):
        """Obtenir l'opérateur du numéro"""
        try:
            carrier_name = carrier.name_for_number(parsed_number, "fr")
            return carrier_name if carrier_name else "Inconnu"
        except:
            return "Inconnu"
    
    def get_geolocation(self, parsed_number):
        """Obtenir la localisation géographique"""
        try:
            region = geocoder.description_for_number(parsed_number, "fr")
            return region if region else "Inconnue"
        except:
            return "Inconnue"
    
    def get_timezone(self, parsed_number):
        """Obtenir le fuseau horaire"""
        try:
            timezones = timezone.time_zones_for_number(parsed_number)
            return list(timezones)[0] if timezones else "Inconnu"
        except:
            return "Inconnu"
    
    def check_numverify(self, phone_number, api_key=""):
        """Vérifie le numéro via NumVerify API"""
        if not api_key:
            return {"error": "API key requise pour NumVerify"}
        
        try:
            url = f"http://apilayer.net/api/validate"
            params = {
                'access_key': api_key,
                'number': phone_number,
                'country_code': '',
                'format': 1
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'valid': data.get('valid', False),
                    'number': data.get('number', ''),
                    'local_format': data.get('local_format', ''),
                    'international_format': data.get('international_format', ''),
                    'country_prefix': data.get('country_prefix', ''),
                    'country_code': data.get('country_code', ''),
                    'country_name': data.get('country_name', ''),
                    'location': data.get('location', ''),
                    'carrier': data.get('carrier', ''),
                    'line_type': data.get('line_type', '')
                }
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def search_online(self, phone_number):
        """Génère des liens de recherche pour le numéro"""
        searches = {
            "Google": f"https://www.google.com/search?q={phone_number}",
            "Facebook": f"https://www.facebook.com/search/top/?q={phone_number}",
            "Truecaller": f"https://www.truecaller.com/search/fr/{phone_number}",
            "Tellows": f"https://www.tellows.fr/num/{phone_number}",
            "SpamCalls": f"https://spamcalls.net/fr/{phone_number}",
            "Copains d'Avant": f"https://copainsdavant.linternaute.com/p/{phone_number}"
        }
        return searches
    
    def analyze(self, phone_number):
        """Analyse complète d'un numéro"""
        print(Fore.YELLOW + f"\n🔍 Analyse du numéro: {phone_number}")
        print(Fore.CYAN + "═" * 50)
        
        # 1. Validation
        print(Fore.WHITE + "1. Validation du format...")
        validation = self.validate_phone(phone_number)
        
        if not validation['valid']:
            print(Fore.RED + f"   ❌ {validation.get('error', 'Numéro invalide')}")
            return None
        
        print(Fore.GREEN + f"   ✅ Numéro valide")
        print(Fore.WHITE + f"     Format international: {validation['formatted']}")
        print(Fore.WHITE + f"     Format national: {validation['national']}")
        
        parsed = validation['parsed']
        
        # 2. Informations de base
        print(Fore.WHITE + "\n2. Informations de base...")
        
        carrier_info = self.get_carrier_info(parsed)
        print(Fore.WHITE + f"   📞 Opérateur: {carrier_info}")
        
        location = self.get_geolocation(parsed)
        print(Fore.WHITE + f"   📍 Localisation: {location}")
        
        timezone_info = self.get_timezone(parsed)
        print(Fore.WHITE + f"   🕐 Fuseau horaire: {timezone_info}")
        
        # 3. Type de ligne (estimation)
        print(Fore.WHITE + "\n3. Analyse du type...")
        country_code = phonenumbers.region_code_for_number(parsed)
        
        # Estimation basée sur le format
        if country_code == "FR":
            if str(parsed.national_number).startswith(('6', '7')):
                print(Fore.WHITE + "   📱 Type: Mobile")
            elif str(parsed.national_number).startswith(('1', '2', '3', '4', '5', '8', '9')):
                print(Fore.WHITE + "   🏠 Type: Fixe")
            else:
                print(Fore.WHITE + "   ❓ Type: Indéterminé")
        else:
            print(Fore.WHITE + "   🌍 Pays: " + country_code)
        
        # 4. Recherches en ligne
        print(Fore.WHITE + "\n4. Recherches en ligne disponibles...")
        searches = self.search_online(phone_number.replace('+', ''))
        
        for site, url in searches.items():
            print(Fore.CYAN + f"   🔗 {site}: {url}")
        
        # 5. Conseils de sécurité
        print(Fore.CYAN + "\n" + "═" * 50)
        print(Fore.GREEN + "🛡️  CONSEILS DE SÉCURITÉ:")
        
        print(Fore.WHITE + "1. Vérifiez le numéro sur les sites anti-spam")
        print(Fore.WHITE + "2. Ne partagez pas d'informations sensibles")
        print(Fore.WHITE + "3. BloqueZ les numéros suspects")
        print(Fore.WHITE + "4. Signalez les appels malveillants")
        
        # Retourner les résultats
        return {
            'valid': True,
            'formatted': validation['formatted'],
            'carrier': carrier_info,
            'location': location,
            'timezone': timezone_info,
            'country_code': country_code,
            'searches': searches
        }

# Fonction de test
if __name__ == "__main__":
    analyzer = PhoneAnalyzer()
    test_phone = input("Numéro à analyser: ")
    analyzer.analyze(test_phone)

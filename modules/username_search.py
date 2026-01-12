#!/usr/bin/env python3
"""
Module de recherche de noms et usernames
by Dvrk_Smith
"""

import requests
import re
import json
from colorama import Fore, Style
from urllib.parse import quote

class UsernameSearch:
    def __init__(self):
        self.timeout = 10
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; OSINT-Tool-Pro/1.2; by Dvrk_Smith)'
        }
    
    def search_social_media(self, full_name):
        """Recherche un nom complet sur les réseaux sociaux"""
        print(Fore.YELLOW + f"\n🔍 Recherche de '{full_name}'...")
        print(Fore.CYAN + "═" * 50)
        
        results = {}
        
        # Liste des plateformes à vérifier
        platforms = {
            "Google": f"https://www.google.com/search?q={quote(full_name)}",
            "Facebook": f"https://www.facebook.com/public/{quote(full_name)}",
            "LinkedIn": f"https://www.linkedin.com/search/results/people/?keywords={quote(full_name)}",
            "Twitter": f"https://twitter.com/search?q={quote(full_name)}&f=user",
            "Instagram": f"https://www.instagram.com/web/search/topsearch/?query={quote(full_name)}",
            "GitHub": f"https://github.com/search?q={quote(full_name)}&type=users",
            "TikTok": f"https://www.tiktok.com/search/user?q={quote(full_name)}",
            "YouTube": f"https://www.youtube.com/results?search_query={quote(full_name)}&sp=EgIQAg%253D%253D"
        }
        
        print(Fore.WHITE + "📊 PLATEFORMES DISPONIBLES:")
        print(Fore.CYAN + "─" * 40)
        
        for platform, url in platforms.items():
            print(Fore.WHITE + f"   🔗 {platform}: {url}")
            results[platform] = url
        
        return results
    
    def check_username_availability(self, username):
        """Vérifie la disponibilité d'un username sur différentes plateformes"""
        print(Fore.YELLOW + f"\n🔍 Vérification du username '{username}'...")
        print(Fore.CYAN + "═" * 50)
        
        # Liste des sites populaires
        sites = {
            "Instagram": f"https://www.instagram.com/{username}/",
            "Twitter": f"https://twitter.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "Pinterest": f"https://pinterest.com/{username}/",
            "Twitch": f"https://www.twitch.tv/{username}",
            "Spotify": f"https://open.spotify.com/user/{username}",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Telegram": f"https://t.me/{username}"
        }
        
        print(Fore.WHITE + "📊 RÉSULTATS DE DISPONIBILITÉ:")
        print(Fore.CYAN + "─" * 40)
        
        results = {}
        
        for site, url in sites.items():
            try:
                response = requests.head(url, headers=self.headers, timeout=5, allow_redirects=True)
                
                if response.status_code == 200:
                    print(Fore.RED + f"   ❌ {site}: Utilisé ({url})")
                    results[site] = {"available": False, "url": url}
                elif response.status_code == 404:
                    print(Fore.GREEN + f"   ✅ {site}: Disponible")
                    results[site] = {"available": True, "url": url}
                else:
                    print(Fore.YELLOW + f"   ⚠️  {site}: Statut {response.status_code}")
                    results[site] = {"available": None, "url": url}
                    
            except Exception:
                print(Fore.YELLOW + f"   ⚠️  {site}: Impossible à vérifier")
                results[site] = {"available": None, "url": url}
        
        return results
    
    def generate_google_dorks(self, full_name, email=None, phone=None):
        """Génère des Google Dorks pour la recherche"""
        print(Fore.YELLOW + f"\n🔎 GOOGLE DORKS GÉNÉRÉS:")
        print(Fore.CYAN + "═" * 50)
        
        dorks = []
        
        # Dorks pour le nom
        dorks.extend([
            f'"{full_name}" site:linkedin.com/in',
            f'"{full_name}" site:facebook.com',
            f'"{full_name}" site:twitter.com',
            f'"{full_name}" site:instagram.com',
            f'"{full_name}" filetype:pdf',
            f'"{full_name}" "CV" OR "resume" OR "curriculum"',
            f'intitle:"{full_name}"',
            f'inurl:"{full_name}"'
        ])
        
        # Dorks pour email (si fourni)
        if email:
            dorks.extend([
                f'"{email}"',
                f'"{email}" filetype:txt OR filetype:csv',
                f'"{email}" "password" OR "leak" OR "breach"',
                f'intext:"{email}"'
            ])
        
        # Dorks pour téléphone (si fourni)
        if phone:
            clean_phone = re.sub(r'\D', '', phone)
            if clean_phone:
                dorks.extend([
                    f'"{phone}"',
                    f'"{clean_phone}"',
                    f'"{phone}" site:truecaller.com OR site:whocalledme.com'
                ])
        
        print(Fore.WHITE + "📋 COPIEZ CES REQUÊTES DANS GOOGLE:\n")
        
        for i, dork in enumerate(dorks[:15], 1):  # Limite à 15 dorks
            print(Fore.CYAN + f"   {i:2d}. " + Fore.WHITE + dork)
        
        return dorks
    
    def search_by_phone_number(self, phone_number):
        """Recherche d'informations par numéro de téléphone"""
        print(Fore.YELLOW + f"\n🔍 Recherche pour le numéro: {phone_number}")
        print(Fore.CYAN + "═" * 50)
        
        clean_phone = re.sub(r'\D', '', phone_number)
        
        searches = {
            "Truecaller": f"https://www.truecaller.com/search/fr/{clean_phone}",
            "Tellows": f"https://www.tellows.fr/num/{clean_phone}",
            "SpamCalls": f"https://spamcalls.net/fr/{clean_phone}",
            "NumBuster": f"https://www.numbuster.com/fr/{clean_phone}",
            "Google": f"https://www.google.com/search?q={quote(phone_number)}",
            "Facebook": f"https://www.facebook.com/search/top/?q={quote(phone_number)}",
            "Whitepages": f"https://www.whitepages.com/phone/{clean_phone}",
            "411.com": f"https://www.411.com/phone/{clean_phone}"
        }
        
        print(Fore.WHITE + "🔗 RECHERCHES DISPONIBLES:")
        print(Fore.CYAN + "─" * 40)
        
        for site, url in searches.items():
            print(Fore.WHITE + f"   🌐 {site}: {url}")
        
        return searches
    
    def comprehensive_search(self, query, search_type="name"):
        """Recherche complète selon le type"""
        print(Fore.CYAN + "\n" + "═" * 60)
        print(Fore.CYAN + "🔍 RECHERCHE COMPLÈTE OSINT")
        print(Fore.CYAN + "═" * 60)
        
        results = {}
        
        if search_type == "name":
            print(Fore.WHITE + f"\n📊 RECHERCHE POUR LE NOM: {query}")
            
            # 1. Recherche réseaux sociaux
            print(Fore.YELLOW + "\n1. RECHERCHE RÉSEAUX SOCIAUX...")
            social_results = self.search_social_media(query)
            results['social_media'] = social_results
            
            # 2. Génération Google Dorks
            print(Fore.YELLOW + "\n2. GÉNÉRATION GOOGLE DORKS...")
            dorks = self.generate_google_dorks(query)
            results['google_dorks'] = dorks
            
            # 3. Vérification username
            print(Fore.YELLOW + "\n3. VÉRIFICATION USERNAME...")
            # Extrait un username potentiel du nom
            username = query.lower().replace(' ', '.')
            username_results = self.check_username_availability(username)
            results['username_check'] = username_results
        
        elif search_type == "phone":
            print(Fore.WHITE + f"\n📊 RECHERCHE POUR LE NUMÉRO: {query}")
            phone_results = self.search_by_phone_number(query)
            results['phone_search'] = phone_results
        
        elif search_type == "username":
            print(Fore.WHITE + f"\n📊 RECHERCHE POUR USERNAME: {query}")
            username_results = self.check_username_availability(query)
            results['username_check'] = username_results
        
        # Conseils de sécurité
        print(Fore.CYAN + "\n" + "═" * 60)
        print(Fore.GREEN + "🛡️  CONSEILS DE PROTECTION DE LA VIE PRIVÉE:")
        
        print(Fore.WHITE + "1. Vérifiez vos paramètres de confidentialité")
        print(Fore.WHITE + "2. Utilisez des noms différents sur chaque plateforme")
        print(Fore.WHITE + "3. Évitez de partager trop d'informations personnelles")
        print(Fore.WHITE + "4. Utilisez l'authentification à deux facteurs")
        print(Fore.WHITE + "5. Revoyez régulièrement vos traces numériques")
        
        return results

# Fonction de test
if __name__ == "__main__":
    searcher = UsernameSearch()
    
    print("1. Recherche par nom")
    print("2. Recherche par username")
    print("3. Recherche par téléphone")
    
    choix = input("\nChoix: ")
    
    if choix == "1":
        nom = input("Nom complet: ")
        searcher.comprehensive_search(nom, "name")
    elif choix == "2":
        username = input("Username: ")
        searcher.comprehensive_search(username, "username")
    elif choix == "3":
        phone = input("Numéro: ")
        searcher.comprehensive_search(phone, "phone")

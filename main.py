#!/usr/bin/env python3
"""
OSINT TOOL PRO v1.3
by Dvrk_Smith
"""

import os
import sys
import time
import json
from datetime import datetime
from colorama import init, Fore, Style

# Initialisation Colorama
init(autoreset=True)

# Import des modules
MODULES_LOADED = False
PHONE_MODULE_LOADED = False
USERNAME_MODULE_LOADED = False

try:
    from modules.email_checker import EmailChecker
    MODULES_LOADED = True
except ImportError as e:
    print(Fore.YELLOW + f"⚠️  Module email non chargé: {e}")

try:
    from modules.phone_analyzer import PhoneAnalyzer
    PHONE_MODULE_LOADED = True
except ImportError as e:
    print(Fore.YELLOW + f"⚠️  Module phone non chargé: {e}")

try:
    from modules.username_search import UsernameSearch
    USERNAME_MODULE_LOADED = True
except ImportError as e:
    print(Fore.YELLOW + f"⚠️  Module username non chargé: {e}")

# Import de la configuration
try:
    import config
    CONFIG_LOADED = True
except ImportError:
    CONFIG_LOADED = False

class OSINTToolPro:
    def __init__(self):
        self.name = "OSINT Tool Pro"
        self.version = "1.3"
        self.author = "Dvrk_Smith"
        self.email_checker = EmailChecker() if MODULES_LOADED else None
        self.phone_analyzer = PhoneAnalyzer() if PHONE_MODULE_LOADED else None
        self.username_searcher = UsernameSearch() if USERNAME_MODULE_LOADED else None
        
    def clear_screen(self):
        """Nettoie l'écran"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def display_banner(self):
        """Affiche la bannière"""
        self.clear_screen()
        
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
{Fore.CYAN}║                                                      ║
{Fore.CYAN}║    {Fore.MAGENTA}╔═╗╔═╗╔╦╗╦╔═╗  ╔═╗╔═╗╔═╗  {Fore.CYAN}╔═╗╔═╗╔═╗      {Fore.CYAN}║
{Fore.CYAN}║    {Fore.MAGENTA}║ ╦╠═╣║║║║╔═╝  ╠═╝║ ║║     {Fore.CYAN}╠═╝║ ║╠═╝      {Fore.CYAN}║
{Fore.CYAN}║    {Fore.MAGENTA}╚═╝╩ ╩╩ ╩╩╚═╝  ╩  ╚═╝╚═╝  {Fore.CYAN}╩  ╚═╝╩        {Fore.CYAN}║
{Fore.CYAN}║                                                      ║
{Fore.CYAN}║                {Fore.YELLOW}Version {self.version} by {self.author}         {Fore.CYAN}║
{Fore.CYAN}║        {Fore.WHITE}Outil de Protection de la Vie Privée          {Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════════════════════════╝
        """
        
        print(banner)
        print(Fore.RED + "⚠️  AVERTISSEMENT: Utilisation Éthique Uniquement!")
        print(Fore.GREEN + "✅ Usage autorisé: Protection personnelle et familiale\n")
    
    def display_menu(self):
        """Affiche le menu amélioré"""
        menu = f"""
{Fore.CYAN}┌────────────────────────────────────────────────────┐
{Fore.CYAN}│                {Fore.WHITE}📋 MENU PRINCIPAL                {Fore.CYAN}│
{Fore.CYAN}├────────────────────────────────────────────────────┤
{Fore.CYAN}│                                                    │
{Fore.CYAN}│  {Fore.GREEN}📧  EMAIL & COMPTES                         {Fore.CYAN}│
{Fore.CYAN}│  {Fore.WHITE}  [1] Vérification complète d'email        {Fore.CYAN}│
{Fore.CYAN}│  {Fore.WHITE}  [2] Vérification fuites de données       {Fore.CYAN}│
{Fore.CYAN}│  {Fore.WHITE}  [3] Vérification réputation email        {Fore.CYAN}│
{Fore.CYAN}│                                                    │
{Fore.CYAN}│  {Fore.BLUE}📞  TÉLÉPHONE & NUMÉROS                      {Fore.CYAN}│
{Fore.CYAN}│  {Fore.WHITE}  [4] Analyse de numéro téléphone          {Fore.CYAN}│
{Fore.CYAN}│  {Fore.WHITE}  [5] Vérification opérateur               {Fore.CYAN}│
{Fore.CYAN}│  {Fore.WHITE}  [6] Détection de numéros spam           {Fore.CYAN}│
{Fore.CYAN}│                                                    │
{Fore.CYAN}│  {Fore.MAGENTA}👤  NOMS & IDENTITÉS                         {Fore.CYAN}│
{Fore.CYAN}│  {Fore.WHITE}  [7] Recherche nom/prénom                 {Fore.CYAN}│
{Fore.CYAN}│  {Fore.WHITE}  [8] Recherche nom d'utilisateur          {Fore.CYAN}│
{Fore.CYAN}│  {Fore.WHITE}  [9] Recherche réseaux sociaux            {Fore.CYAN}│
{Fore.CYAN}│                                                    │
{Fore.CYAN}├────────────────────────────────────────────────────┤
{Fore.CYAN}│  {Fore.YELLOW}[C] ⚙️  Configuration  {Fore.RED}[Q] 🚪 Quitter   {Fore.CYAN}│
{Fore.CYAN}└────────────────────────────────────────────────────┘
        """
        print(menu)
    
    def run_email_check(self):
        """Exécute la vérification d'email"""
        if not self.email_checker:
            print(Fore.RED + "❌ Module email non chargé!")
            return
        
        self.clear_screen()
        print(Fore.CYAN + "╔══════════════════════════════════════════╗")
        print(Fore.CYAN + "║       📧 VÉRIFICATION COMPLÈTE          ║")
        print(Fore.CYAN + "╚══════════════════════════════════════════╝")
        
        email = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Entrez l'email à analyser: ").strip()
        
        if not "@" in email or "." not in email.split("@")[1]:
            print(Fore.RED + "❌ Format d'email invalide!")
            input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée...")
            return
        
        print(Fore.YELLOW + f"\n🔍 Lancement de l'analyse pour: {email}")
        print(Fore.CYAN + "═" * 50)
        
        # Utilise le module email_checker
        results = self.email_checker.comprehensive_check(email)
        
        # Demander si l'utilisateur veut sauvegarder
        save = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Sauvegarder le rapport? (o/n): ").lower()
        if save == 'o':
            self.save_report(email, results)
        
        input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée pour continuer...")
    
    def run_phone_analysis(self):
        """Exécute l'analyse de numéro"""
        if not self.phone_analyzer:
            print(Fore.RED + "❌ Module téléphone non chargé!")
            return
        
        self.clear_screen()
        print(Fore.CYAN + "╔══════════════════════════════════════════╗")
        print(Fore.CYAN + "║       📞 ANALYSE DE NUMÉRO              ║")
        print(Fore.CYAN + "╚══════════════════════════════════════════╝")
        
        phone = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Entrez le numéro (ex: +33612345678): ").strip()
        
        if len(phone) < 8:
            print(Fore.RED + "❌ Numéro trop court!")
            input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée...")
            return
        
        print(Fore.YELLOW + f"\n🔍 Lancement de l'analyse pour: {phone}")
        print(Fore.CYAN + "═" * 50)
        
        # Utilise le module phone_analyzer
        results = self.phone_analyzer.analyze(phone)
        
        if results:
            # Demander si l'utilisateur veut sauvegarder
            save = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Sauvegarder le rapport? (o/n): ").lower()
            if save == 'o':
                self.save_report(f"phone_{phone}", results)
        
        input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée pour continuer...")
    
    def run_name_search(self):
        """Exécute la recherche de noms"""
        if not self.username_searcher:
            print(Fore.RED + "❌ Module recherche non chargé!")
            return
        
        self.clear_screen()
        print(Fore.CYAN + "╔══════════════════════════════════════════╗")
        print(Fore.CYAN + "║        👤 RECHERCHE DE NOMS             ║")
        print(Fore.CYAN + "╚══════════════════════════════════════════╝")
        
        print(Fore.YELLOW + "\n📋 TYPES DE RECHERCHE DISPONIBLES:")
        print(Fore.CYAN + "─" * 40)
        print(Fore.WHITE + "   [1] Recherche par nom complet")
        print(Fore.WHITE + "   [2] Recherche par username")
        print(Fore.WHITE + "   [3] Recherche par téléphone")
        
        search_type = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Type de recherche (1-3): ").strip()
        
        if search_type == "1":
            self.search_by_name()
        elif search_type == "2":
            self.search_by_username()
        elif search_type == "3":
            self.search_by_phone()
        else:
            print(Fore.RED + "❌ Type invalide!")
            input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée...")
    
    def search_by_name(self):
        """Recherche par nom complet"""
        print(Fore.CYAN + "\n" + "═" * 40)
        print(Fore.CYAN + "👤 RECHERCHE PAR NOM COMPLET")
        print(Fore.CYAN + "═" * 40)
        
        prenom = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Prénom: ").strip()
        nom = input(Fore.YELLOW + "[?] " + Fore.WHITE + "Nom: ").strip()
        
        if not prenom or not nom:
            print(Fore.RED + "❌ Nom incomplet!")
            input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée...")
            return
        
        full_name = f"{prenom} {nom}"
        
        print(Fore.YELLOW + f"\n🔍 Lancement de la recherche pour: {full_name}")
        print(Fore.CYAN + "═" * 50)
        
        results = self.username_searcher.comprehensive_search(full_name, "name")
        
        # Demander si l'utilisateur veut sauvegarder
        save = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Sauvegarder le rapport? (o/n): ").lower()
        if save == 'o':
            self.save_report(f"name_{full_name}", results)
        
        input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée pour continuer...")
    
    def search_by_username(self):
        """Recherche par username"""
        print(Fore.CYAN + "\n" + "═" * 40)
        print(Fore.CYAN + "🔍 RECHERCHE PAR USERNAME")
        print(Fore.CYAN + "═" * 40)
        
        username = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Username à rechercher: ").strip()
        
        if len(username) < 3:
            print(Fore.RED + "❌ Username trop court!")
            input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée...")
            return
        
        print(Fore.YELLOW + f"\n🔍 Vérification du username: {username}")
        print(Fore.CYAN + "═" * 50)
        
        results = self.username_searcher.comprehensive_search(username, "username")
        
        # Demander si l'utilisateur veut sauvegarder
        save = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Sauvegarder le rapport? (o/n): ").lower()
        if save == 'o':
            self.save_report(f"username_{username}", results)
        
        input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée pour continuer...")
    
    def search_by_phone(self):
        """Recherche par numéro de téléphone"""
        print(Fore.CYAN + "\n" + "═" * 40)
        print(Fore.CYAN + "📞 RECHERCHE PAR TÉLÉPHONE")
        print(Fore.CYAN + "═" * 40)
        
        phone = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Numéro à rechercher: ").strip()
        
        if len(phone) < 8:
            print(Fore.RED + "❌ Numéro trop court!")
            input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée...")
            return
        
        print(Fore.YELLOW + f"\n🔍 Recherche pour le numéro: {phone}")
        print(Fore.CYAN + "═" * 50)
        
        results = self.username_searcher.comprehensive_search(phone, "phone")
        
        # Demander si l'utilisateur veut sauvegarder
        save = input(Fore.YELLOW + "\n[?] " + Fore.WHITE + "Sauvegarder le rapport? (o/n): ").lower()
        if save == 'o':
            self.save_report(f"phone_search_{phone}", results)
        
        input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée pour continuer...")
    
    def save_report(self, target, data):
        """Sauvegarde un rapport"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/report_{target}_{timestamp}.json"
        
        try:
            os.makedirs("reports", exist_ok=True)
            with open(filename, 'w') as f:
                json.dump({
                    'target': target,
                    'date': timestamp,
                    'tool': self.name,
                    'version': self.version,
                    'author': self.author,
                    'results': data
                }, f, indent=4)
            
            print(Fore.GREEN + f"✅ Rapport sauvegardé: {filename}")
        except Exception as e:
            print(Fore.RED + f"❌ Erreur sauvegarde: {e}")
    
    def show_config(self):
        """Affiche la configuration"""
        self.clear_screen()
        print(Fore.CYAN + "╔══════════════════════════════════════════╗")
        print(Fore.CYAN + "║           ⚙️  CONFIGURATION              ║")
        print(Fore.CYAN + "╚══════════════════════════════════════════╝")
        
        print(Fore.GREEN + "\n📊 STATUT DE L'APPLICATION:")
        print(Fore.CYAN + "─" * 40)
        print(Fore.WHITE + f"   Nom: {self.name}")
        print(Fore.WHITE + f"   Version: {self.version}")
        print(Fore.WHITE + f"   Auteur: {self.author}")
        print(Fore.WHITE + f"   Module Email: {'✅ Chargé' if MODULES_LOADED else '❌ Erreur'}")
        print(Fore.WHITE + f"   Module Téléphone: {'✅ Chargé' if PHONE_MODULE_LOADED else '❌ Erreur'}")
        print(Fore.WHITE + f"   Module Recherche: {'✅ Chargé' if USERNAME_MODULE_LOADED else '❌ Erreur'}")
        print(Fore.WHITE + f"   Configuration: {'✅ Chargée' if CONFIG_LOADED else '❌ Erreur'}")
        
        print(Fore.YELLOW + "\n🔑 CONFIGURATION DES APIs:")
        print(Fore.CYAN + "─" * 40)
        print(Fore.WHITE + "   Pour améliorer les fonctionnalités:")
        print(Fore.CYAN + "   1. Have I Been Pwned:")
        print(Fore.WHITE + "      https://haveibeenpwned.com/API/Key")
        print(Fore.CYAN + "   2. Hunter.io:")
        print(Fore.WHITE + "      https://hunter.io/api-keys")
        
        print(Fore.GREEN + "\n📝 INSTRUCTIONS:")
        print(Fore.WHITE + "   1. Obtenez les clés API (gratuites)")
        print(Fore.WHITE + "   2. Ajoutez-les dans config.py")
        print(Fore.WHITE + "   3. Redémarrez l'application")
        
        input(Fore.YELLOW + "\n[↩] Appuyez sur Entrée pour continuer...")
    
    def run(self):
        """Fonction principale"""
        while True:
            try:
                self.display_banner()
                self.display_menu()
                
                choice = input(Fore.YELLOW + "\n[→] " + Fore.WHITE + "Votre choix: ").strip().lower()
                
                if choice in ['0', 'q', 'quit', 'exit']:
                    print(Fore.CYAN + "\n👋 Au revoir! Restez en sécurité!")
                    sys.exit(0)
                
                elif choice in ['1', '2', '3']:
                    self.run_email_check()
                
                elif choice in ['4', '5', '6']:
                    self.run_phone_analysis()
                
                elif choice in ['7', '8', '9']:
                    self.run_name_search()
                
                elif choice in ['c', 'config']:
                    self.show_config()
                
                else:
                    print(Fore.RED + "❌ Option invalide!")
                    print(Fore.YELLOW + "   Options valides: 1-9, C, Q")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n\n⚠️  Interruption par l'utilisateur")
                sys.exit(0)
            except Exception as e:
                print(Fore.RED + f"\n❌ Erreur: {e}")
                time.sleep(2)

def main():
    """Point d'entrée principal"""
    try:
        app = OSINTToolPro()
        app.run()
    except Exception as e:
        print(Fore.RED + f"❌ Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

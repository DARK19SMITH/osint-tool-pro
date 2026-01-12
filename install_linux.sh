#!/bin/bash
# ==============================================
# OSINT TOOL PRO - INSTALLATION SCRIPT
# by Dvrk_Smith
# ==============================================

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions
print_banner() {
    clear
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║                                                      ║"
    echo "║    ╔═╗╔═╗╔╦╗╦╔═╗  ╔═╗╔═╗╔═╗  ╔═╗╔═╗╔═╗              ║"
    echo "║    ║ ╦╠═╣║║║║╔═╝  ╠═╝║ ║║     ╠═╝║ ║╠═╝              ║"
    echo "║    ╚═╝╩ ╩╩ ╩╩╚═╝  ╩  ╚═╝╚═╝  ╩  ╚═╝╩                ║"
    echo "║                                                      ║"
    echo "║           ${YELLOW}OSINT TOOL PRO v1.3${BLUE}                   ║"
    echo "║            ${YELLOW}by Dvrk_Smith${BLUE}                          ║"
    echo "║                                                      ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

check_root() {
    if [[ $EUID -eq 0 ]]; then
        echo -e "${RED}[!] Ne pas exécuter en root !${NC}"
        echo -e "${YELLOW}Quittez et relancez sans sudo.${NC}"
        exit 1
    fi
}

check_os() {
    echo -e "${BLUE}[*] Vérification du système...${NC}"
    
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        OS=$(uname -s)
        VER=$(uname -r)
    fi
    
    echo -e "${GREEN}[+] Système détecté: $OS $VER${NC}"
    
    # Vérifie si c'est une distribution supportée
    if [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Ubuntu"* ]] || \
       [[ "$OS" == *"Kali"* ]] || [[ "$OS" == *"Parrot"* ]]; then
        echo -e "${GREEN}[+] Distribution supportée !${NC}"
    else
        echo -e "${YELLOW}[!] Distribution non testée, continuation...${NC}"
    fi
}

install_dependencies() {
    echo -e "${BLUE}[*] Mise à jour du système...${NC}"
    sudo apt update && sudo apt upgrade -y
    
    echo -e "${BLUE}[*] Installation des dépendances système...${NC}"
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        git \
        curl \
        wget \
        nano \
        tree
    
    echo -e "${GREEN}[+] Dépendances système installées.${NC}"
}

clone_repository() {
    echo -e "${BLUE}[*] Téléchargement d'OSINT Tool Pro...${NC}"
    
    if [[ -d "osint-tool-pro" ]]; then
        echo -e "${YELLOW}[!] Dossier existe déjà, mise à jour...${NC}"
        cd osint-tool-pro
        git pull origin main
    else
        git clone https://github.com/DARK19SMITH/osint-tool-pro.git
        cd osint-tool-pro
    fi
    
    echo -e "${GREEN}[+] Repository cloné/mis à jour.${NC}"
}

setup_python() {
    echo -e "${BLUE}[*] Configuration de l'environnement Python...${NC}"
    
    # Crée un environnement virtuel (optionnel)
    if [[ ! -d "venv" ]]; then
        python3 -m venv venv
        echo -e "${GREEN}[+] Environnement virtuel créé.${NC}"
    fi
    
    # Active l'environnement virtuel
    source venv/bin/activate 2>/dev/null || true
    
    # Installe les dépendances Python
    echo -e "${BLUE}[*] Installation des packages Python...${NC}"
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    pip3 install phonenumbers  # Au cas où
    
    echo -e "${GREEN}[+] Dépendances Python installées.${NC}"
}

setup_permissions() {
    echo -e "${BLUE}[*] Configuration des permissions...${NC}"
    
    chmod +x main.py
    chmod +x modules/*.py 2>/dev/null || true
    
    # Crée les dossiers nécessaires
    mkdir -p data reports logs
    
    echo -e "${GREEN}[+] Permissions configurées.${NC}"
}

create_config() {
    echo -e "${BLUE}[*] Configuration de l'application...${NC}"
    
    if [[ ! -f "config.py" ]]; then
        if [[ -f "config_example.py" ]]; then
            cp config_example.py config.py
            echo -e "${YELLOW}[!] Fichier config.py créé à partir de config_example.py${NC}"
            echo -e "${YELLOW}[!] Éditez config.py pour ajouter vos clés API${NC}"
        else
            echo -e "${YELLOW}[!] config_example.py non trouvé, création basique...${NC}"
            cat > config.py << 'CONFIG'
# Configuration OSINT Tool Pro
API_KEYS = {
    'hibp': 'VOTRE_CLE_API_ICI',
    'hunter': 'VOTRE_CLE_API_ICI',
}
CONFIG
        fi
    else
        echo -e "${GREEN}[+] config.py existe déjà.${NC}"
    fi
}

create_desktop_entry() {
    echo -e "${BLUE}[*] Création du raccourci (optionnel)...${NC}"
    
    DESKTOP_FILE="$HOME/.local/share/applications/osint-tool.desktop"
    
    cat > "$DESKTOP_FILE" << DESKTOP
[Desktop Entry]
Name=OSINT Tool Pro
Comment=Outil OSINT éthique by Dvrk_Smith
Exec=$(pwd)/venv/bin/python3 $(pwd)/main.py
Icon=utilities-terminal
Terminal=true
Type=Application
Categories=Utility;Security;
Path=$(pwd)
DESKTOP
    
    if [[ -f "$DESKTOP_FILE" ]]; then
        chmod +x "$DESKTOP_FILE"
        echo -e "${GREEN}[+] Raccourci créé dans le menu applications.${NC}"
    fi
}

create_launcher() {
    echo -e "${BLUE}[*] Création du lanceur système...${NC}"
    
    LAUNCHER_SCRIPT="$HOME/.local/bin/osint-tool"
    
    cat > "$LAUNCHER_SCRIPT" << 'LAUNCHER'
#!/bin/bash
cd "$HOME/osint-tool-pro"
if [[ -d "venv" ]]; then
    source venv/bin/activate
fi
python3 main.py
LAUNCHER
    
    chmod +x "$LAUNCHER_SCRIPT"
    echo -e "${GREEN}[+] Lanceur créé: tapez 'osint-tool' pour lancer l'application.${NC}"
}

test_installation() {
    echo -e "${BLUE}[*] Test de l'installation...${NC}"
    
    # Test Python
    python3 -c "import requests; import colorama; import phonenumbers; print('✅ Importations OK')" && \
        echo -e "${GREEN}[+] Test Python réussi.${NC}" || \
        echo -e "${RED}[-] Test Python échoué.${NC}"
    
    # Test de l'application
    echo -e "${BLUE}[*] Test rapide de l'application...${NC}"
    python3 -c "
from modules.email_checker import EmailChecker
from modules.phone_analyzer import PhoneAnalyzer
from modules.username_search import UsernameSearch
print('✅ Modules chargés avec succès')
" && echo -e "${GREEN}[+] Application fonctionnelle.${NC}"
}

show_instructions() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║                INSTALLATION TERMINÉE !               ║"
    echo "╠══════════════════════════════════════════════════════╣"
    echo "║                                                      ║"
    echo -e "║  ${GREEN}🎯 POUR LANCER L'APPLICATION :${BLUE}                     ║"
    echo -e "║  ${YELLOW}1. Depuis ce dossier : python3 main.py${BLUE}            ║"
    echo -e "║  ${YELLOW}2. Depuis terminal : osint-tool${BLUE}                   ║"
    echo -e "║  ${YELLOW}3. Menu applications : OSINT Tool Pro${BLUE}             ║"
    echo "║                                                      ║"
    echo -e "║  ${GREEN}🔧 CONFIGURATION :${BLUE}                                 ║"
    echo -e "║  ${YELLOW}1. Éditez config.py pour ajouter vos clés API${BLUE}    ║"
    echo -e "║  ${YELLOW}2. Obtenez des clés API gratuites :${BLUE}               ║"
    echo -e "║     ${YELLOW}- https://haveibeenpwned.com/API/Key${BLUE}           ║"
    echo -e "║     ${YELLOW}- https://hunter.io/api-keys${BLUE}                   ║"
    echo "║                                                      ║"
    echo -e "║  ${GREEN}📁 DOSSIERS :${BLUE}                                      ║"
    echo -e "║  ${YELLOW}data/   - Données temporaires${BLUE}                     ║"
    echo -e "║  ${YELLOW}reports/ - Rapports générés${BLUE}                       ║"
    echo -e "║  ${YELLOW}logs/   - Fichiers de log${BLUE}                         ║"
    echo "║                                                      ║"
    echo -e "║  ${GREEN}🐛 SUPPORT :${BLUE}                                       ║"
    echo -e "║  ${YELLOW}https://github.com/DARK19SMITH/osint-tool-pro${BLUE}     ║"
    echo "║                                                      ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ==============================================
# EXÉCUTION PRINCIPALE
# ==============================================

main() {
    print_banner
    echo -e "${YELLOW}[!] Installation d'OSINT Tool Pro v1.3${NC}"
    echo -e "${YELLOW}[!] by Dvrk_Smith${NC}"
    echo ""
    
    # Vérifications
    check_root
    check_os
    
    # Installation
    install_dependencies
    clone_repository
    setup_python
    setup_permissions
    create_config
    create_launcher
    
    # Optionnel - Desktop entry
    read -p "Créer un raccourci dans le menu applications? (o/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        create_desktop_entry
    fi
    
    # Tests
    test_installation
    
    # Instructions finales
    show_instructions
    
    # Lance l'application
    read -p "Lancer l'application maintenant? (o/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        echo -e "${GREEN}[*] Lancement d'OSINT Tool Pro...${NC}"
        python3 main.py
    fi
}

# Gestion des erreurs
trap 'echo -e "${RED}[!] Installation interrompue!${NC}"; exit 1' INT TERM

# Lance l'installation
main

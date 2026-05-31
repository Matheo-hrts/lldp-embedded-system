# Installation

## 1. Installation du système d'exploitation

Commencez par installer **Orange Pi OS (version Ubuntu)** sur votre Orange Pi Zero 3.

Une fois le système démarré, lancez l'outil de configuration :

```bash
orangepi-config
```

Naviguez ensuite dans :

```text
System → Hardware
```

Activez toutes les lignes contenant **spidev** puis redémarrez lorsque cela est demandé.

---

## 2. Mise à jour du système

Après le redémarrage, mettez le système à jour :

```bash
sudo apt update -y && sudo apt upgrade -y
```

---

## 3. Installation des dépendances

Installez les paquets nécessaires :

```bash
sudo apt install -y git python3.10-venv libpcap-dev python3-dev gpiod
```

---

## 4. Clonage du projet

Clonez le dépôt GitHub :

```bash
git clone https://github.com/Matheo-hrts/lldp-embedded-system.git
```

Placez-vous ensuite dans le dossier du projet :

```bash
cd lldp-embedded-system
```

---

## 5. Création de l'environnement virtuel Python

Créez l'environnement virtuel :

```bash
python3 -m venv .venv
```

Activez-le :

```bash
source .venv/bin/activate
```

Installez ensuite les dépendances Python du projet :

```bash
pip install -r requirements.txt
```

---

## 6. Configuration des permissions GPIO et SPI

Afin de permettre à l'application d'accéder aux périphériques GPIO et SPI sans utiliser `sudo`, créez un groupe dédié :

```bash
sudo groupadd lldp
sudo usermod -aG lldp $USER
```

### GPIO

Attribuez les droits sur les périphériques GPIO :

```bash
sudo chgrp lldp /dev/gpiochip0
sudo chmod 660 /dev/gpiochip0
```

Créez la règle udev :

```bash
sudo nano /etc/udev/rules.d/99-gpio.rules
```

Ajoutez :

```text
KERNEL=="gpiochip*", GROUP="lldp", MODE="0660"
```

### SPI

Attribuez les droits sur les périphériques SPI :

```bash
sudo chgrp lldp /dev/spidev*
```

Créez ensuite la règle :

```bash
sudo nano /etc/udev/rules.d/99-spi.rules
```

Ajoutez :

```text
KERNEL=="spidev*", GROUP="lldp", MODE="0660"
```

Rechargez les règles :

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Déconnectez-vous puis reconnectez-vous afin que l'ajout au groupe soit pris en compte.

---

## 7. Configuration du service systemd

Pour lancer automatiquement l'application au démarrage du système, créez un service systemd :

```bash
sudo nano /etc/systemd/system/lldp.service
```

Contenu du fichier :

```ini
[Unit]
Description=LLDP Embedded System
After=network.target

[Service]
Type=simple
User=orangepi
WorkingDirectory=/home/orangepi/lldp-embedded-system
ExecStart=/home/orangepi/lldp-embedded-system/.venv/bin/python main.py

Restart=always
RestartSec=2

AmbientCapabilities=CAP_NET_RAW CAP_NET_ADMIN
CapabilityBoundingSet=CAP_NET_RAW CAP_NET_ADMIN
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Activez ensuite le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now lldp
```

---

## 8. Redémarrage

Redémarrez l'Orange Pi :

```bash
sudo reboot
```

L'application démarrera automatiquement après le démarrage du système.


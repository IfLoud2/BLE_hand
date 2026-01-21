# BLE Hand Bridge

Ce projet assure la communication entre un capteur IMU (XIAO nRF52840 Sense) et un système hôte (PC/Raspberry Pi) via Bluetooth Low Energy (BLE).

Il inclut :
1. **Firmware Arduino** : Acquisition des données IMU, fusion de capteurs (Filtre Complémentaire), et transmission BLE.
2. **Pont Python** : Réception des données BLE sur Windows et retransmission via WebSocket pour visualisation.

## Architecture

```mermaid
graph LR
    A[XIAO nRF52840] -- BLE (Binary Struct) --> B[PC Windows (ble_bridge.py)]
    B -- WebSocket (JSON) --> C[Raspberry Pi / Client Neural Network]
```

## Structure du Projet

- `ble_bridge.py` : Script principal. Connecte le BLE et transmet en WebSocket.
- `ble_terminal_receiver.py` : Outil de diagnostic pour vérifier les données brutes dans le terminal.
- `XIAO_BLE_IMU/` : Code source Arduino (`.ino`) à flasher sur le microcontrôleur.

## Installation

### Prérequis
- Python 3.10+
- Windows (avec Bluetooth actif)

### Dépendances Python
```bash
pip install -r requirements.txt
# Ou manuellement :
pip install bleak websockets
```

## Usage

### 1. Flasher le XIAO
Ouvrir `XIAO_BLE_IMU/XIAO_BLE_IMU.ino` avec l'IDE Arduino et téléverser sur la carte XIAO nRF52840 Sense.
> **Note** : Laisser le capteur immobile pendant 3 secondes au démarrage pour la calibration du gyroscope.

### 2. Tester la réception (Diagnostic)
Pour voir si les données arrivent correctement :
```bash
python ble_terminal_receiver.py
```
*Devrait afficher des valeurs lisibles : `32.40, -0.57, 26.76 ...`*

### 3. Lancer le Pont (Production)
```bash
python ble_bridge.py --host <IP_CIBLE> --port 8765
```
*Options :*
- `--host` : IP du serveur WebSocket (ex: `192.168.1.50`).
- `--debug` : Affiche les logs détaillés.

## Protocole de Données

### BLE (XIAO -> PC)
Le service utilisé est un service série générique :
- **Service UUID** : `00001101-0000-1000-8000-00805f9b34fb`
- **Char UUID** : `00002101-0000-1000-8000-00805f9b34fb`

Format : **Binaire (Little Endian), 24 octets**
`[Roll, Pitch, Yaw, Ax, Ay, Az]` (6 x float 32-bit).

### WebSocket (PC -> Client)
Les données sont converties en JSON avant d'être envoyées :
```json
{
  "r": 32.4,
  "p": -0.5,
  "y": 26.7,
  "ax": -0.01,
  "ay": 0.54,
  "az": 0.87
}
```

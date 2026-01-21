# BLE Hand Bridge

Ce projet contient un script Python permettant de faire le pont entre une carte XIAO nRF52840 Sense (BLE) et un autre système (Raspberry Pi, PC, etc.) via WebSocket.

## Architecture

```mermaid
graph LR
    A[XIAO nRF52840] -- BLE (UART Service) --> B[PC Windows (ble_bridge.py)]
    B -- WebSocket --> C[Raspberry Pi / Client]
```

## Prérequis

- Python 3.10+
- Un adaptateur Bluetooth compatible (intégré au PC Windows)

## Installation

1. Cloner le repo :
   ```bash
   git clone <url_du_repo>
   cd BLE_hand
   ```

   ```bash
   pip install -r requirements.txt
   ```
   
   Ou manuellement :
   ```bash
   pip install bleak websockets
   ```

## Usage

Lancer le script de pont :

```bash
python ble_bridge.py --host <IP_DU_RPI> --port 8765 --debug
```

### Options

- `--target` : Nom du périphérique BLE à scanner (Défaut: "XIAO_IMU")
- `--host` : IP du serveur WebSocket destination (Défaut: "localhost")
- `--port` : Port destination (Défaut: 8765)
- `--debug` : Affiche les trames reçues dans la console

## Format des données

Le XIAO doit envoyer des données JSON sur le service UART Nordic (`6E400001-...`), charactéristique TX (`6E400003-...`).

Format attendu :
```json
{"r": -0.23, "p": 1.02, "y": 4.55}
```

## Logs

L'application utilise le module `logging` de Python pour afficher des infos claires avec timestamp.

Exemple de sortie :
```text
2023-10-27 10:00:01 - [INFO] - Starting BLE Bridge...
2023-10-27 10:00:05 - [INFO] - Found device: XIAO_IMU...
2023-10-27 10:00:06 - [INFO] - Connected to XIAO_IMU
2023-10-27 10:00:06 - [INFO] - RX: {"r": 0.1, "p": 0.2, "y": 0.0}
```

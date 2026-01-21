# Changelog

## [Unreleased]

## [1.0.0] - 2026-01-21
### Added
- **Firmware** : `XIAO_BLE_IMU.ino` intégrant :
    - Lecture capteur LSM6DS3 (Accel/Gyro).
    - Filtre Complémentaire pour Roll/Pitch.
    - Intégration du Yaw avec calibration au démarrage.
    - Transmission BLE binaire optimisée (24 bytes).
- **Python Bridge** : `ble_bridge.py`
    - Connexion automatique au périphérique "XIAO_IMU".
    - Décodage binaire `struct.unpack('<6f', data)`.
    - Serveur/Client WebSocket pour renvoi des données.
    - Gestion de la reconnexion automatique.
- **Tools** : `ble_terminal_receiver.py` pour le débogage rapide dans le terminal.

### Changed
- **Protocole de données** : Passage de JSON (texte) à Binaire (Struct) pour performance et simplicité côté Arduino.
- **UUIDs** : Adaptation aux UUIDs génériques (`1101`/`2101`) utilisés par `ArduinoBLE` par défaut pour ce service.

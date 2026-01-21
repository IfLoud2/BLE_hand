import asyncio
from bleak import BleakScanner, BleakClient

# Adapted to match the Nordic UART Service used by the XIAO nRF52840
# Original request had generic UUIDs, but we use the specific ones for this project.
# Corrected UUIDs based on device scan
SERVICE_UUID = "00001101-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "00002101-0000-1000-8000-00805f9b34fb"

async def run():
    print("🔍 Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"- {d.name} ({d.address})")

    target = next((d for d in devices if d.name == "XIAO_IMU"), None)
    if not target:
        print("❌ XIAO_IMU not found.")
        return

    async with BleakClient(target.address) as client:
        print(f"✅ Connected to {target.name}")

        print("🔍 Listing Services and Characteristics...")
        for service in client.services:
            print(f"[Service] {service.uuid} ({service.description})")
            for char in service.characteristics:
                print(f"  - [Char] {char.uuid} ({','.join(char.properties)})")

        # Subscribing to the characteristic
        def handle_notify(_, data):
            print("🔄", data.decode("utf-8"))

        await client.start_notify(CHARACTERISTIC_UUID, handle_notify)
        
        print("📡 Listening for notifications. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)

        print("📡 Listening for notifications. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())

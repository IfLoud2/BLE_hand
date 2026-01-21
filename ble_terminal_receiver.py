import asyncio
from bleak import BleakScanner, BleakClient

# Adapted to match the Nordic UART Service used by the XIAO nRF52840
# Original request had generic UUIDs, but we use the specific ones for this project.
SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHARACTERISTIC_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

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

        def handle_notify(_, data):
            print("🔄", data.decode("utf-8"))

        await client.start_notify(CHARACTERISTIC_UUID, handle_notify)

        print("📡 Listening for notifications. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())

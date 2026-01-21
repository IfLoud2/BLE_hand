import asyncio
import struct
from bleak import BleakScanner, BleakClient

# Corrected UUIDs based on device scan
SERVICE_UUID = "00001101-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "00002101-0000-1000-8000-00805f9b34fb"

async def run():
    print("🔍 Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    target = next((d for d in devices if d.name == "XIAO_IMU"), None)
    
    if not target:
        print("❌ XIAO_IMU not found.")
        return

    async with BleakClient(target.address) as client:
        print(f"✅ Connected to {target.name}")

        def handle_notify(_, data):
            # 24 bytes = 6 floats x 4 bytes
            if len(data) == 24:
                try:
                    # Unpack 6 floats (Little Endian)
                    v = struct.unpack('<6f', data)
                    print(f"📊 Decoded (6 floats): {v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f}, {v[3]:.2f}, {v[4]:.2f}, {v[5]:.2f}")
                except Exception as e:
                    print(f"❌ Decode Error: {e}")
            else:
                print(f"🔄 RAW ({len(data)}b): {data.hex()}")

        await client.start_notify(CHARACTERISTIC_UUID, handle_notify)
        
        print("📡 Listening for notifications. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())

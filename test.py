import asyncio
import winrt.windows.devices.enumeration as windows_devices


CAMERA_NAME = "Brio 300"

async def get_camera_info():
    return await windows_devices.DeviceInformation.find_all_async(4)

connected_cameras = asyncio.run(get_camera_info())
names = [camera.name for camera in connected_cameras]

if CAMERA_NAME not in names:
    print("Camera not found")
else:
    camera_index = names.index(CAMERA_NAME)
    print(camera_index)
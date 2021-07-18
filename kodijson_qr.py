import kodijson
import yaml
import evdev

with open('credentials.yaml', 'r') as file:
    credentials = yaml.load(file, Loader=yaml.FullLoader)

base_url = "http://127.0.0.1/jsonrpc"

kodi = kodijson.Kodi(base_url, credentials["username"], 
    credentials["password"])

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)

kodi.GUI.ShowNotification(title = "kodi_qr", message = "Kodi QR reader starting")

kodi.Player.PlayPause([kodijson.PLAYER_VIDEO])

kodi.Player.Stop([kodijson.PLAYER_VIDEO])

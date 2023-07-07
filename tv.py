import os
from pathlib import Path
from time import sleep

HOME = Path(os.path.expanduser("~"))
STORE_PATH = HOME / ".config" / "lgtvcreds" / "store.json"


def your_custom_storage_is_empty():
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return not STORE_PATH.exists()


def load_from_your_custom_storage():
    with STORE_PATH.open("r") as f:
        return json.load(f)


def persist_to_your_custom_storage(store):
    with STORE_PATH.open("w") as f:
        json.dump(store, f)


from pywebostv.discovery import *  # Because I'm lazy, don't do this.
from pywebostv.connection import *
from pywebostv.controls import *

# 1. For the first run, pass in an empty dictionary object. Empty store leads to an Authentication prompt on TV.
# 2. Go through the registration process. `store` gets populated in the process.
# 3. Persist the `store` state to disk.
# 4. For later runs, read your storage and restore the value of `store`.
if your_custom_storage_is_empty():
    store = {}
else:
    store = load_from_your_custom_storage()

if "host" in store:
    host = store["host"]
    client = WebOSClient(host)
else:
    # Scans the current network to discover TV. Avoid [0] in real code. If you already know the IP,
    # you could skip the slow scan and # instead simply say:
    #    client = WebOSClient("<IP Address of TV>")
    # or for newer models:
    #    client = WebOSClient("<IP Address of TV>", secure=True)
    client = WebOSClient.discover(secure=True)[
        0
    ]  # Use discover(secure=True) for newer models.

client.connect()

for status in client.register(store):
    if status == WebOSClient.PROMPTED:
        print("Please accept the connect on the TV!")
    elif status == WebOSClient.REGISTERED:
        print("Registration successful!")
        store["host"] = client.host

# Keep the 'store' object because it contains now the access token
# and use it next time you want to register on the TV.
print(store)  # {'client_key': 'ACCESS_TOKEN_FROM_TV'}

persist_to_your_custom_storage(store)

system = SystemControl(client)
system.notify("Setting up night mode...", icon_ext="png")

inp = InputControl(client)
inp.connect_input()
inp.menu()          # the menu for adjusting settings for the television 
sleep(2)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.ok()
sleep(4)
inp.right()
sleep(0.5)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.ok()
sleep(1)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.down()
sleep(0.5)
inp.ok()
sleep(1)
inp.back()
sleep(1)
inp.back()

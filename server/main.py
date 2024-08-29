from gui import KeyJackGUI
from networking import KeyJackNetwork
from controller import KeyJackController

IP = '10.10.245.140'
PORT = 10319

def main():
    network = KeyJackNetwork(IP, PORT)
    gui = KeyJackGUI(controller=None)
    controller = KeyJackController(gui, network)
    gui.controller = controller  # Set controller after initialization to avoid circular reference
    gui.bind_controller_events()  # Bind events after controller is assigned
    gui.start()

if __name__ == "__main__":
    main()


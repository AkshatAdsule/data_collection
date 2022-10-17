from tkgpio import TkCircuit
import collect_data
configuration = {
    "width": 300,
    "height": 200,
    "leds": [
        {"x": 50, "y": 40, "name": "recording", "pin": 9},
        {"x": 150, "y": 40, "name": "write", "pin": 8}
    ],
    "buttons": [
        {"x": 50, "y": 130, "name": "start/stop", "pin": 23},
    ]
}

circuit = TkCircuit(configuration)
@circuit.run
def main ():
    collect_data.run()
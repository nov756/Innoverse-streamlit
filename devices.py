class SmartHome:
    def __init__(self):
        self.devices = {
            "lampu": {
                "living_room": False,
                "bedroom": False
            },
            "ac": {
                "on": False,
                "temperature": 25
            },
            "pintu": False
        }
    
    def update_device(self, device, action, room=None, value=None):
        if device == "lampu" and room:
            self.devices["lampu"][room] = (action == "nyala")
            return f"Lampu {room} {'dinyalakan' if action == 'nyala' else 'dimatikan'}"
        
        elif device == "ac":
            if action == "nyala":
                self.devices["ac"]["on"] = True
                return "AC dinyalakan"
            elif action == "mati":
                self.devices["ac"]["on"] = False
                return "AC dimatikan"
            elif action == "atur" and value:
                self.devices["ac"]["temperature"] = value
                return f"AC diatur ke {value}°C"
        
        elif device == "pintu":
            self.devices["pintu"] = (action == "buka")
            return f"Pintu {'dibuka' if action == 'buka' else 'dikunci'}"
        
        return "Perintah tidak valid"
import uuid
from typing import Optional, List, Dict


class CommandCentre:
    
    def __init__(self):
        self._runways = []
        self._aircrafts = []
        self._aircraft_runway_map = {}  
    
    def register_runway(self, runway):
        self._runways.append(runway)
        runway.set_command_centre(self)
    
    def register_aircraft(self, aircraft):
        self._aircrafts.append(aircraft)
        aircraft.set_command_centre(self)
    
    def get_available_runway(self) -> Optional['Runway']:
        for runway in self._runways:
            if not self._is_runway_busy(runway):
                return runway
        return None
    
    def _is_runway_busy(self, runway) -> bool:
        return runway in [r for _, r in self._aircraft_runway_map.items()]
    
    def land(self, aircraft) -> bool:
        print(f"Aircraft {aircraft.name} is landing.")
        print("Checking runway.")
        
        runway = self.get_available_runway()
        if runway:
            print(f"Aircraft {aircraft.name} has landed.")
            self._aircraft_runway_map[aircraft] = runway
            runway.highlight_red()
            return True
        else:
            print("Could not land, all runways are busy.")
            return False
    
    def take_off(self, aircraft) -> bool:
        if aircraft in self._aircraft_runway_map:
            runway = self._aircraft_runway_map[aircraft]
            print(f"Aircraft {aircraft.name} is taking off.")
            del self._aircraft_runway_map[aircraft]
            runway.highlight_green()
            print(f"Aircraft {aircraft.name} has taken off.")
            return True
        else:
            print(f"Aircraft {aircraft.name} is not on any runway.")
            return False


class Aircraft:
    
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.is_taking_off = False
        self._command_centre = None
    
    def set_command_centre(self, command_centre):
        self._command_centre = command_centre
    
    def request_landing(self) -> bool:
        if self._command_centre:
            return self._command_centre.land(self)
        print("Command centre not assigned.")
        return False
    
    def request_take_off(self) -> bool:
        if self._command_centre:
            self.is_taking_off = True
            result = self._command_centre.take_off(self)
            self.is_taking_off = False
            return result
        print("Command centre not assigned.")
        return False


class Runway:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self._command_centre = None
    
    def set_command_centre(self, command_centre):
        self._command_centre = command_centre
    
    def highlight_red(self):
        print(f"Runway {self.id} is busy!")
    
    def highlight_green(self):
        print(f"Runway {self.id} is free!")


def main():
    command_centre = CommandCentre()
    runway1 = Runway()
    runway2 = Runway()
    command_centre.register_runway(runway1)
    command_centre.register_runway(runway2)
    aircraft1 = Aircraft("Boeing 747", 300)
    aircraft2 = Aircraft("Airbus A380", 350)
    aircraft3 = Aircraft("Boeing 777", 280)
    
    command_centre.register_aircraft(aircraft1)
    command_centre.register_aircraft(aircraft2)
    command_centre.register_aircraft(aircraft3)
    
    print("=== Demonstration of landing and taking off ===")
    aircraft1.request_landing()  
    aircraft2.request_landing() 
    aircraft3.request_landing() 
    
    print("\n=== Demonstration of taking off ===")
    aircraft1.request_take_off() 
    
    print("\n=== Demonstration of landing after runway is freed ===")
    aircraft3.request_landing()  
    
    print("\n=== Final demonstration ===")
    aircraft2.request_take_off()
    aircraft3.request_take_off()  

if __name__ == "__main__":
    main()
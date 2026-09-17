class ConversationManager:
    def __init__(self):
        self.memory = []
        self.slots = {
            "water_ph": None,
            "turbidity_ntu": None,
            "dissolved_oxygen_mgl": None,
            "upstream_land_use": None,
            "aquatic_species_richness": None,
            "pollution_level": None,
            "riparian_buffer_width_m": None,
            "rainfall_mm": None,
            "region": None,
        }

    def update_slots(self, data: dict):
        for key, value in data.items():
            if key in self.slots and value is not None:
                self.slots[key] = value

    def get_missing_slots(self):
        required = [
            "water_ph", "turbidity_ntu", "dissolved_oxygen_mgl",
            "upstream_land_use", "aquatic_species_richness",
            "pollution_level", "region"
        ]
        return [k for k in required if self.slots.get(k) is None]

    def add_message(self, role, content):
        self.memory.append({"role": role, "content": content})

    def get_context(self):
        return {"slots": self.slots, "memory": self.memory[-5:]}
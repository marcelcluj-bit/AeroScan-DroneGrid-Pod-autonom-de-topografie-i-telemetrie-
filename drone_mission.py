"""
AeroScan-DroneGrid: Autonomous Geological Reconnaissance Flight Framework
License: MIT / Public Domain CC0
Stack: MAVLink Integration Protocol / Python MAVSDK
"""

import math

class AutonomousDroneSurvey:
    def __init__(self, origin_lat, origin_lon, altitude_m=50.0):
        self.origin_lat = origin_lat
        self.origin_lon = origin_lon
        self.altitude_m = altitude_m
        self.waypoints = []

    def generate_grid_pattern(self, rows=4, cols=4, step_meters=20.0):
        """Generate a basic lawnmower grid pattern relative to origin coordinates."""
        # Approx 1 meter in degrees latitude
        meters_to_lat = 1.0 / 111111.0
        meters_to_lon = 1.0 / (111111.0 * math.cos(math.radians(self.origin_lat)))

        print(f"[MISSION PLANNER] Generating {rows}x{cols} Survey Grid at {self.altitude_m}m Altitude...")
        
        for r in range(rows):
            for c in range(cols):
                col_idx = c if r % 2 == 0 else (cols - 1 - c)  # Zig-zag pathing
                lat = self.origin_lat + (r * step_meters * meters_to_lat)
                lon = self.origin_lon + (col_idx * step_meters * meters_to_lon)
                self.waypoints.append((round(lat, 6), round(lon, 6), self.altitude_m))
        
        return self.waypoints

    def export_mavlink_mission(self, filename="survey_mission.json"):
        """Export generated points to JSON format for integration with Ground Control Stations."""
        mission_data = {
            "firmware": "ArduPilot/PX4",
            "survey_altitude": self.altitude_m,
            "total_waypoints": len(self.waypoints),
            "coordinates": self.waypoints
        }
        print(f"[EXPORT] Mission plan containing {len(self.waypoints)} waypoints exported to '{filename}'.")
        return json.dumps(mission_data, indent=2)

if __name__ == "__main__":
    # Example deployment near Cluj-Napoca coordinates
    survey = AutonomousDroneSurvey(origin_lat=46.7712, origin_lon=23.6236, altitude_m=45.0)
    grid = survey.generate_grid_pattern(rows=5, cols=4, step_meters=25.0)
    survey.export_mavlink_mission()

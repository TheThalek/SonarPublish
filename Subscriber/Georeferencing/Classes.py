from dataclasses import dataclass
from typing import List

@dataclass
class SonarData:
    pointX: List[float]
    pointY: List[float]
    beamIdx: List[int]
    quality: List[int]
    intensity: List[float]

@dataclass
class TelemetryDataPosition:
    latitude: float
    longitude: float
    position_timestep: int

@dataclass
class TelemetryDataPose:
    roll: float
    pitch: float
    pose_timestep: int

@dataclass
class TelemetryDataHeading:
    heading: float
    heading_timestep: int

@dataclass
class TelemetryDataDepth:
    depth: float
    depth_timestep: int

@dataclass
class TelemetryDataAltitude:
    altitude: float
    altitude_timestep: int
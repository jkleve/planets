import numpy as np
import datetime as dt
import math as m

from dataclasses import dataclass, field, InitVar

        
@dataclass
class Orbit:
    """Orbital elements
    
    Reference wiki for more information on orbital elements
    https://en.wikipedia.org/wiki/Orbital_elements
    """

    name: str
    e: float  # Eccentricity
    a: float  # Semi-major axis
    i: float  # Inclination
    RANN: float  # Right ascention of ascending node
    omega: float  # Argument of perigee

    b: float = field(init=False)  # Semi-minor axis
    c: float = field(init=False)  # Focal distance

    def __post_init__(self):
        # Semi-major axis
        self.b = self.a * m.sqrt(1 - self.e ** 2)
        
        # Focal distance
        self.c = self.a * self.e
    
    def to_xyz(self):
        """Convert orbital elements to cartesian coordinates"""
        # Rotation matrix multiplication
        R = np.array([
                [ m.cos(self.RANN),  - 1 * m.sin(self.RANN),                   0],
                [ m.sin(self.RANN),        m.cos(self.RANN),                   0],
                [                 0,                      0,                   1]
            ]) @ np.array([
                [                 1,                      0,                   0],
                [                 0,          m.cos(self.i), - 1 * m.sin(self.i)],
                [                 0,          m.sin(self.i),       m.cos(self.i)]
            ]) @ np.array([
                [ m.cos(self.omega), - 1 * m.sin(self.omega),                  0],
                [ m.sin(self.omega),       m.cos(self.omega),                  0],
                [                 0,                       0,                  1]
            ])

        # From 0 to 360 degrees, calculate a data point
        x, y, z = [], [], []
        for i in np.linspace(0, 2 * m.pi, 100):
            P = R @ np.array([
                    [ self.a * m.cos(i)],
                    [ self.b * m.sin(i)],
                    [                 0]
                ]) - R @ np.array([
                    [ self.c],
                    [      0],
                    [      0]
                ])
            x += [P[0]]
            y += [P[1]]
            z += [P[2]]

        return x, y, z

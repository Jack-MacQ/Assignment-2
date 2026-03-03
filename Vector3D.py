#!/usr/bin/env python3

"""

This script implements a 3D Cartesian vector class using object-oriented
programming principles and applies it to problems in geometry and
electromagnetic wave theory.

The program performs the following tasks:

1. Defines a Vector3D class capable of:
   - Initialisation with Cartesian components
   - Vector addition and subtraction
   - Magnitude calculation
   - Dot (scalar) product
   - Cross (vector) product

2. Uses the class to:
   - Compute the areas of four triangles defined by Cartesian vertices
     using the cross product method
   - Evaluate all internal angles of each triangle using the dot product
     formula

3. Extends the Vector3D class via inheritance to create a ComplexVector
   class, allowing complex-valued components and verification of selected
   properties of Hansen vectors for a plane-polarised electromagnetic wave.

License: MIT
Python Version: 3.9.21

"""

import math
from typing import Union



##############################
# TASK 1
##############################

"""

Design and implement an object class that can represent and manipulate
Cartesian vectors in 3D space.

Class should be able to intialise vector object with the components of the
vector as well as calculate and return the magnitude of the vectors, addition
and subtraction of vectors, and dot and cross products between vectors.

"""

Number = Union[int, float]

class Vector3D:
	"""
	
	Class representing a 3D cartesion vector
	
	"""
	
	def __init__(self, x: Number, y: Number, z: Number) -> None:
        	"""Initialise a 3D vector with components."""
        	self.x = float(x)
        	self.y = float(y)
        	self.z = float(z)

	def __str__(self) -> str:
        	"""Return a readable string representation."""
	        return f"Vector3D({self.x}, {self.y}, {self.z})"

	def __repr__(self) -> str:
        	"""Return unambiguous representation."""
        	return self.__str__()

	def magnitude(self) -> float:
        	"""Return the magnitude of the vector."""
        	return math.sqrt(self.x**2 + self.y**2 + self.z**2)

	def __add__(self, other: "Vector3D") -> "Vector3D":
        	"""Add two vectors."""
        	return Vector3D(
        	    self.x + other.x,
        	    self.y + other.y,
        	    self.z + other.z,
        	)

	def __sub__(self, other: "Vector3D") -> "Vector3D":
        	"""Subtract two vectors."""
        	return Vector3D(
        	    self.x - other.x,
        	    self.y - other.y,
        	    self.z - other.z,
        	)

	def dot(self, other: "Vector3D") -> float:
        	"""Return dot product of two vectors."""
        	return (
        	    self.x * other.x
        	    + self.y * other.y
        	    + self.z * other.z
        	)

	def cross(self, other: "Vector3D") -> "Vector3D":
        	"""Return cross product of two vectors."""
        	return Vector3D(
        	    self.y * other.z - self.z * other.y,
        	    self.z * other.x - self.x * other.z,
        	    self.x * other.y - self.y * other.x,
        	)



##############################
# TASK 2
##############################

"""

This script instantiates objects from the Vector3D class and
uses them to solve geometric problems in three-dimensional space.

More specifically, it computes the areas of four triangles defined by Cartesian
vertices using the cross product method and also evaluates all internal angles
of each triangle using the dot product and vector magnitudes.

"""

def triangle_area(a, b, c):
    """Return area of triangle with vertices a,b,c (Vector3D)."""
    ab = b - a
    ac = c - a
    return 0.5 * ab.cross(ac).magnitude()

def angle_between(u, v):
    """Return angle (in radians) between vectors u and v."""
    denom = u.magnitude() * v.magnitude()
    if denom == 0.0:
        raise ValueError("Cannot compute angle with a zero-length vector.")
    cos_theta = u.dot(v) / denom
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.acos(cos_theta)

def triangle_angles(a, b, c):
    """Return the 3 internal angles (in degrees) at vertices a,b,c."""
    ab = b - a
    ac = c - a
    ba = a - b
    bc = c - b
    ca = a - c
    cb = b - c

    ang_a = math.degrees(angle_between(ab, ac))
    ang_b = math.degrees(angle_between(ba, bc))
    ang_c = math.degrees(angle_between(ca, cb))
    return ang_a, ang_b, ang_c


# Define the triangles

triangles = [
    (
        "T1",
        Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(0, 1, 0)
    ),
    (
        "T2",
        Vector3D(-1, -1, -1), Vector3D(0, -1, -1), Vector3D(-1, 0, -1)
    ),
    (
        "T3",
        Vector3D(1, 0, 0), Vector3D(0, 0, 1), Vector3D(0, 0, 0)
    ),
    (
        "T4",
        Vector3D(0, 0, 0), Vector3D(1, -1, 0), Vector3D(0, 0, 1)
    ),
]

# Print results

for name, a, b, c in triangles:
    area = triangle_area(a, b, c)
    ang_a, ang_b, ang_c = triangle_angles(a, b, c)

    print(f"\n{name}")
    print(f"  Vertices: A={a}, B={b}, C={c}")
    print(f"  Area = {area:.12f}")
    print(f"  Angles (deg): A={ang_a:.6f}, B={ang_b:.6f}, C={ang_c:.6f} (sum={ang_a+ang_b+ang_c:.6f})")

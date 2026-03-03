#!/usr/bin/env python3

"""

An object class that can represent and manipulate Cartesian vectors in 3D space.

Class should be able to intialise vector object with the components of the
vector as well as calculate and return the magnitude of the vectors, addition
and subtraction of vectors, and dot and cross products between vectors.

License: MIT
Python Version: 3.9.21

"""

import math
from typing import Union

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

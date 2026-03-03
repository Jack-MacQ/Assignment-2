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
import cmath
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
	        return f"({self.x}, {self.y}, {self.z})"

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
    
    # Form two side vectors from common vertex a
    ab = b - a
    ac = c - a

    # Area = 1/2 |ab cross ac|
    return 0.5 * ab.cross(ac).magnitude()


def angle_between(u, v):
    """Return angle (in radians) between vectors u and v."""
    
    # Compute product of magnitudes (denominator of cosine formula)
    denom = u.magnitude() * v.magnitude()

    # Prevent division by zero if a zero-length vector is supplied
    if denom == 0.0:
        raise ValueError("Cannot compute angle with a zero-length vector.")

    # Cosine formula: cos(theta) = (u dot v) / (|u||v|)
    cos_theta = u.dot(v) / denom

    # Clamp value to [-1, 1] to avoid floating-point rounding errors
    cos_theta = max(-1.0, min(1.0, cos_theta))

    # Return angle in radians
    return math.acos(cos_theta)


def triangle_angles(a, b, c):
    """Return the 3 internal angles (in degrees) at vertices a,b,c."""

    # Construct vectors representing each pair of sides meeting at each vertex
    ab = b - a
    ac = c - a

    ba = a - b
    bc = c - b

    ca = a - c
    cb = b - c

    # Compute each internal angle using the angle_between function
    ang_a = math.degrees(angle_between(ab, ac))  # Angle at vertex A
    ang_b = math.degrees(angle_between(ba, bc))  # Angle at vertex B
    ang_c = math.degrees(angle_between(ca, cb))  # Angle at vertex C

    return ang_a, ang_b, ang_c


# -----------------------------
# Define the triangles
# -----------------------------

# Each triangle is stored as:
# (name, vertex A, vertex B, vertex C)

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


# -----------------------------
# Compute and print results
# -----------------------------

print("\n" + "#" * 60)
print(" " * 60)
print("-" * 60)
print("TASK 2: Triangle Areas and Internal Angles")
print("-" * 60)

for name, a, b, c in triangles:

    # Compute triangle area
    area = triangle_area(a, b, c)

    # Compute internal angles (in degrees)
    ang_a, ang_b, ang_c = triangle_angles(a, b, c)
    
    print("-" * 40)
    print(f"{name}")
    print(f"Vertices: A={a}, B={b}, C={c}")
    print(f"Area     = {area:.2f}")

    print(
        f"Angles (deg): "
        f"A={ang_a:.2f}, "
        f"B={ang_b:.2f}, "
        f"C={ang_c:.2f} "
        f"(sum={ang_a + ang_b + ang_c:.2f})"
    )
    print("-" * 40)

print("\n" + "#" * 60)

##############################
# TASK 3
##############################

"""

This section extends the Vector3D class via inheritance to define a
ComplexVector class with complex-valued components. The dot product
is implemented using the conjugate of the first vector.

The class is used to numerically evaluate the divergence and curl
of the Hansen vectors for a plane-polarised electromagnetic wave
with k = pi*(0,0,1). Spatial derivatives are computed using central
finite differences and compared with the analytic expressions to
verify the required vector identities.

"""

class ComplexVector(Vector3D):
    """
    Complex-valued 3D vector class inheriting from Vector3D.

    - Components are stored as complex numbers
    - Dot product uses conjugate of the first vector: a* dot b
      
    """

    def __init__(self, x, y, z):
        # Store as complex explicitly (do NOT force float)
        self.x = complex(x)
        self.y = complex(y)
        self.z = complex(z)

    def __str__(self):
        # complex tuple output
        return f"({self.x}, {self.y}, {self.z})"

    def magnitude(self) -> float:
        # For complex vectors, magnitude is sqrt(real(a* dot a))
        val = self.dot(self)
        return math.sqrt(val.real)

    def dot(self, other: "ComplexVector") -> complex:
        # Complex dot product: conjugate(self) dot other
        return (
            self.x.conjugate() * other.x
            + self.y.conjugate() * other.y
            + self.z.conjugate() * other.z
        )

    def cross(self, other: "ComplexVector") -> "ComplexVector":
        # Cross product formula works component-wise for complex numbers too
        return ComplexVector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


def vec_add(u: ComplexVector, v: ComplexVector) -> ComplexVector:
    return ComplexVector(u.x + v.x, u.y + v.y, u.z + v.z)


def vec_sub(u: ComplexVector, v: ComplexVector) -> ComplexVector:
    return ComplexVector(u.x - v.x, u.y - v.y, u.z - v.z)


def vec_scale(a: complex, v: ComplexVector) -> ComplexVector:
    return ComplexVector(a * v.x, a * v.y, a * v.z)


def vec_diff_norm(u: ComplexVector, v: ComplexVector) -> float:
    # Norm of difference
    return vec_sub(u, v).magnitude()


# Wavevector k = pi * (0,0,1)
K_MAG = math.pi


def phase(x: float, y: float, z: float) -> complex:
    # k dot x = pi * z
    _ = x, y  # unused, but keeps signature explicit
    return cmath.exp(1j * math.pi * z)


def M_field(x: float, y: float, z: float) -> ComplexVector:
    # M = (1,0,0) * exp(i k dot x)
    p = phase(x, y, z)
    return ComplexVector(p, 0.0, 0.0)


def N_field(x: float, y: float, z: float) -> ComplexVector:
    # N = (0,1,0) * exp(i k dot x)
    p = phase(x, y, z)
    return ComplexVector(0.0, p, 0.0)


# Numerical derivatives (central differences)

def partial_scalar(f, x, y, z, h, axis: str) -> complex:
    if axis == "x":
        return (f(x + h, y, z) - f(x - h, y, z)) / (2.0 * h)
    if axis == "y":
        return (f(x, y + h, z) - f(x, y - h, z)) / (2.0 * h)
    if axis == "z":
        return (f(x, y, z + h) - f(x, y, z - h)) / (2.0 * h)
    raise ValueError("axis must be 'x', 'y', or 'z'")


def divergence(F, x, y, z, h) -> complex:
    # div F = dFx/dx + dFy/dy + dFz/dz
    dfx_dx = partial_scalar(lambda X, Y, Z: F(X, Y, Z).x, x, y, z, h, "x")
    dfy_dy = partial_scalar(lambda X, Y, Z: F(X, Y, Z).y, x, y, z, h, "y")
    dfz_dz = partial_scalar(lambda X, Y, Z: F(X, Y, Z).z, x, y, z, h, "z")
    return dfx_dx + dfy_dy + dfz_dz


def curl(F, x, y, z, h) -> ComplexVector:
    # curl F = (dFz/dy - dFy/dz, dFx/dz - dFz/dx, dFy/dx - dFx/dy)
    dFz_dy = partial_scalar(lambda X, Y, Z: F(X, Y, Z).z, x, y, z, h, "y")
    dFy_dz = partial_scalar(lambda X, Y, Z: F(X, Y, Z).y, x, y, z, h, "z")

    dFx_dz = partial_scalar(lambda X, Y, Z: F(X, Y, Z).x, x, y, z, h, "z")
    dFz_dx = partial_scalar(lambda X, Y, Z: F(X, Y, Z).z, x, y, z, h, "x")

    dFy_dx = partial_scalar(lambda X, Y, Z: F(X, Y, Z).y, x, y, z, h, "x")
    dFx_dy = partial_scalar(lambda X, Y, Z: F(X, Y, Z).x, x, y, z, h, "y")

    return ComplexVector(
        dFz_dy - dFy_dz,
        dFx_dz - dFz_dx,
        dFy_dx - dFx_dy,
    )


# Results for these specific M,N
# With k = pi zhat and exp(i pi z):
# div M = 0, div N = 0
# curl N = (-i*pi)*M
# curl M = ( i*pi)*N
def curlN_analytic(x, y, z) -> ComplexVector:
    return vec_scale(-1j * math.pi, M_field(x, y, z))


def curlM_analytic(x, y, z) -> ComplexVector:
    return vec_scale(1j * math.pi, N_field(x, y, z))


# Run the checks at selected points (I have set h=1e-6)
def run_task3(points, h=1e-6):
    print(" " * 60)
    print(" " * 60)
    print("#" * 60)
    print("\n" + "-" * 60)
    print("TASK 3 - Hansen Vector Checks (numerical vs analytic)")
    print("-" * 60)
    print("-" * 60)
    print(f"Step size h = {h:g}")
    print(f"|k| = pi = {K_MAG:.6f}")
    print("-" * 60)

    for (x, y, z) in points:
        Mv = M_field(x, y, z)
        Nv = N_field(x, y, z)

        divM_num = divergence(M_field, x, y, z, h)
        divN_num = divergence(N_field, x, y, z, h)

        curlN_num = curl(N_field, x, y, z, h)
        curlM_num = curl(M_field, x, y, z, h)

        # Analytic curls for THIS M,N choice
        curlN_an = curlN_analytic(x, y, z)
        curlM_an = curlM_analytic(x, y, z)

        # RHS checks: curl N = M/|k|, curl M = N/|k|
        rhs_curlN = vec_scale(1.0 / K_MAG, Mv)
        rhs_curlM = vec_scale(1.0 / K_MAG, Nv)

        print("\n" + "-" * 60)
        print(f"Point (x,y,z) = ({x:g}, {y:g}, {z:g})")
        print("-" * 60)

        print(f"div M (num) = {divM_num}")
        print(f"div N (num) = {divN_num}")
        print("Expected (brief): div M = 0, div N = 0")

        print("\ncurl N (num) =", curlN_num)
        print("curl N (an)  =", curlN_an)
        print("M/|k| (RHS)  =", rhs_curlN)
        print(f"||curlN_num - curlN_an|| = {vec_diff_norm(curlN_num, curlN_an):.3e}")
        print(f"||curlN_num - M/|k||     = {vec_diff_norm(curlN_num, rhs_curlN):.3e}")

        print("\ncurl M (num) =", curlM_num)
        print("curl M (an)  =", curlM_an)
        print("N/|k| (RHS)  =", rhs_curlM)
        print(f"||curlM_num - curlM_an|| = {vec_diff_norm(curlM_num, curlM_an):.3e}")
        print(f"||curlM_num - N/|k||     = {vec_diff_norm(curlM_num, rhs_curlM):.3e}")

    print("\n" + "-" * 60)
    print("\n" + "#" * 60)

# Chosen points
task3_points = [
    (0.0, 0.0, 0.0),
    (0.12, 0.34, 0.56),
    (1.0, 1.0, 1.0),
]

run_task3(task3_points, h=1e-6)

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

# pylint: disable=invalid-name

import cmath
import math
from dataclasses import dataclass
from typing import Callable, Sequence, Tuple, Union

##############################
# TASK 1
##############################

TASK_1_DOC = """

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
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

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

TASK_2_DOC = """

This script instantiates objects from the Vector3D class and
uses them to solve geometric problems in three-dimensional space.

More specifically, it computes the areas of four triangles defined by Cartesian
vertices using the cross product method and also evaluates all internal angles
of each triangle using the dot product and vector magnitudes.

"""


def triangle_area(vertex_a: Vector3D, vertex_b: Vector3D, vertex_c: Vector3D) -> float:
    """Return area of triangle with vertices a,b,c (Vector3D)."""

    # Form two side vectors from common vertex a
    ab_vec = vertex_b - vertex_a
    ac_vec = vertex_c - vertex_a

    # Area = 1/2 |ab cross ac|
    return 0.5 * ab_vec.cross(ac_vec).magnitude()


def angle_between(vec_u: Vector3D, vec_v: Vector3D) -> float:
    """Return angle (in radians) between vectors u and v."""

    # Compute product of magnitudes (denominator of cosine formula)
    denom = vec_u.magnitude() * vec_v.magnitude()

    # Prevent division by zero if a zero-length vector is supplied
    if denom == 0.0:
        raise ValueError("Cannot compute angle with a zero-length vector.")

    # Cosine formula: cos(theta) = (u dot v) / (|u||v|)
    cos_theta = vec_u.dot(vec_v) / denom

    # Clamp value to [-1, 1] to avoid floating-point rounding errors
    cos_theta = max(-1.0, min(1.0, cos_theta))

    # Return angle in radians
    return math.acos(cos_theta)


def triangle_angles(
    vertex_a: Vector3D, vertex_b: Vector3D, vertex_c: Vector3D
) -> Tuple[float, float, float]:
    """Return the 3 internal angles (in degrees) at vertices a,b,c."""

    # Construct vectors representing each pair of sides meeting at each vertex
    ab_vec = vertex_b - vertex_a
    ac_vec = vertex_c - vertex_a

    ba_vec = vertex_a - vertex_b
    bc_vec = vertex_c - vertex_b

    ca_vec = vertex_a - vertex_c
    cb_vec = vertex_b - vertex_c

    # Compute each internal angle using the angle_between function
    ang_a = math.degrees(angle_between(ab_vec, ac_vec))  # Angle at vertex A
    ang_b = math.degrees(angle_between(ba_vec, bc_vec))  # Angle at vertex B
    ang_c = math.degrees(angle_between(ca_vec, cb_vec))  # Angle at vertex C

    return ang_a, ang_b, ang_c


# -----------------------------
# Define the triangles
# -----------------------------

# Each triangle is stored as:
# (name, vertex A, vertex B, vertex C)

triangles = [
    ("T1", Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(0, 1, 0)),
    ("T2", Vector3D(-1, -1, -1), Vector3D(0, -1, -1), Vector3D(-1, 0, -1)),
    ("T3", Vector3D(1, 0, 0), Vector3D(0, 0, 1), Vector3D(0, 0, 0)),
    ("T4", Vector3D(0, 0, 0), Vector3D(1, -1, 0), Vector3D(0, 0, 1)),
]


# -----------------------------
# Compute and print results
# -----------------------------

print("\n" + "#" * 60)
print(" " * 60)
print("=" * 60)
print("TASK 2: Triangle Areas and Internal Angles")
print("=" * 60)

for tri_name, v_a, v_b, v_c in triangles:
    # Compute triangle area
    area = triangle_area(v_a, v_b, v_c)

    # Compute internal angles (in degrees)
    tri_ang_a, tri_ang_b, tri_ang_c = triangle_angles(v_a, v_b, v_c)

    print("-" * 40)
    print(f"{tri_name}")
    print(f"Vertices: A={v_a}, B={v_b}, C={v_c}")
    print(f"Area     = {area:.2f}")

    print(
        f"Angles (deg): "
        f"A={tri_ang_a:.2f}, "
        f"B={tri_ang_b:.2f}, "
        f"C={tri_ang_c:.2f} "
        f"(sum={tri_ang_a + tri_ang_b + tri_ang_c:.2f})"
    )
    print("-" * 40)

print("\n" + "#" * 60)

##############################
# TASK 3
##############################

TASK_3_DOC = """

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

    def __init__(self, x: complex, y: complex, z: complex) -> None:
        """Initialise a complex vector (stores components as complex)."""
        # Call base init (pylint) then overwrite with complex components.
        super().__init__(0.0, 0.0, 0.0)
        self.x = complex(x)
        self.y = complex(y)
        self.z = complex(z)

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"({self.x}, {self.y}, {self.z})"

    def magnitude(self) -> float:
        """Return the magnitude of the complex vector."""
        # For complex vectors, magnitude is sqrt(real(a* dot a))
        val = self.dot(self)
        return math.sqrt(val.real)

    def dot(self, other: "ComplexVector") -> complex:
        """Return complex dot product: conjugate(self) dot other."""
        return (
            self.x.conjugate() * other.x
            + self.y.conjugate() * other.y
            + self.z.conjugate() * other.z
        )

    def cross(self, other: "ComplexVector") -> "ComplexVector":
        """Return cross product (component-wise, valid for complex numbers)."""
        return ComplexVector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


def vec_add(vec_u: ComplexVector, vec_v: ComplexVector) -> ComplexVector:
    """Return vec_u + vec_v (ComplexVector)."""
    return ComplexVector(vec_u.x + vec_v.x, vec_u.y + vec_v.y, vec_u.z + vec_v.z)


def vec_sub(vec_u: ComplexVector, vec_v: ComplexVector) -> ComplexVector:
    """Return vec_u - vec_v (ComplexVector)."""
    return ComplexVector(vec_u.x - vec_v.x, vec_u.y - vec_v.y, vec_u.z - vec_v.z)


def vec_scale(scale: complex, vec_v: ComplexVector) -> ComplexVector:
    """Return scale * vec_v (ComplexVector)."""
    return ComplexVector(scale * vec_v.x, scale * vec_v.y, scale * vec_v.z)


def vec_diff_norm(vec_u: ComplexVector, vec_v: ComplexVector) -> float:
    """Return the magnitude of (vec_u - vec_v)."""
    # Norm of difference
    return vec_sub(vec_u, vec_v).magnitude()


@dataclass(frozen=True)
class Point3D:
    """Small container for a 3D point."""
    x: float
    y: float
    z: float


# Wavevector k = pi * (0,0,1)
K_MAG = math.pi


def phase(x: float, y: float, z: float) -> complex:
    """Return exp(i k dot x) for k = pi*(0,0,1)."""
    # k dot x = pi * z
    _ = x, y  # unused, but keeps signature explicit
    return cmath.exp(1j * math.pi * z)


def M_field(x: float, y: float, z: float) -> ComplexVector:
    """Return M(x) for the chosen plane wave definition."""
    # M = (1,0,0) * exp(i k dot x)
    p = phase(x, y, z)
    return ComplexVector(p, 0.0, 0.0)


def N_field(x: float, y: float, z: float) -> ComplexVector:
    """Return N(x) for the chosen plane wave definition."""
    # N = (0,1,0) * exp(i k dot x)
    p = phase(x, y, z)
    return ComplexVector(0.0, p, 0.0)


def partial_scalar(
    func: Callable[[float, float, float], complex],
    point: Point3D,
    h: float,
    axis: str,
) -> complex:
    """Return central-difference partial derivative of a scalar field at point."""
    if axis == "x":
        return (func(point.x + h, point.y, point.z) - func(point.x - h, point.y, point.z)) / (
            2.0 * h
        )
    if axis == "y":
        return (func(point.x, point.y + h, point.z) - func(point.x, point.y - h, point.z)) / (
            2.0 * h
        )
    if axis == "z":
        return (func(point.x, point.y, point.z + h) - func(point.x, point.y, point.z - h)) / (
            2.0 * h
        )
    raise ValueError("axis must be 'x', 'y', or 'z'")


def divergence(
    field: Callable[[float, float, float], ComplexVector],
    point: Point3D,
    h: float,
) -> complex:
    """Return numerical divergence of a vector field at point."""
    # div F = dFx/dx + dFy/dy + dFz/dz
    dfx_dx = partial_scalar(lambda xx, yy, zz: field(xx, yy, zz).x, point, h, "x")
    dfy_dy = partial_scalar(lambda xx, yy, zz: field(xx, yy, zz).y, point, h, "y")
    dfz_dz = partial_scalar(lambda xx, yy, zz: field(xx, yy, zz).z, point, h, "z")
    return dfx_dx + dfy_dy + dfz_dz


def curl(
    field: Callable[[float, float, float], ComplexVector],
    point: Point3D,
    h: float,
) -> ComplexVector:
    """Return numerical curl of a vector field at point."""
    # curl F = (dFz/dy - dFy/dz, dFx/dz - dFz/dx, dFy/dx - dFx/dy)
    dfz_dy = partial_scalar(lambda xx, yy, zz: field(xx, yy, zz).z, point, h, "y")
    dfy_dz = partial_scalar(lambda xx, yy, zz: field(xx, yy, zz).y, point, h, "z")

    dfx_dz = partial_scalar(lambda xx, yy, zz: field(xx, yy, zz).x, point, h, "z")
    dfz_dx = partial_scalar(lambda xx, yy, zz: field(xx, yy, zz).z, point, h, "x")

    dfy_dx = partial_scalar(lambda xx, yy, zz: field(xx, yy, zz).y, point, h, "x")
    dfx_dy = partial_scalar(lambda xx, yy, zz: field(xx, yy, zz).x, point, h, "y")

    return ComplexVector(
        dfz_dy - dfy_dz,
        dfx_dz - dfz_dx,
        dfy_dx - dfx_dy,
    )


# Results for these specific M,N
# With k = pi zhat and exp(i pi z):
# div M = 0, div N = 0
# curl N = (-i*pi)*M
# curl M = ( i*pi)*N
def curlN_analytic(x: float, y: float, z: float) -> ComplexVector:
    """Return analytic curl(N) for the chosen M,N."""
    return vec_scale(-1j * math.pi, M_field(x, y, z))


def curlM_analytic(x: float, y: float, z: float) -> ComplexVector:
    """Return analytic curl(M) for the chosen M,N."""
    return vec_scale(1j * math.pi, N_field(x, y, z))


def fmt_complex(z: complex) -> str:
    """Format a complex number for printing."""
    return f"{z.real:.3g}{z.imag:+.3g}j"


def fmt_vec(vec_v: ComplexVector) -> str:
    """Format a ComplexVector as (x, y, z)."""
    return f"({fmt_complex(vec_v.x)}, {fmt_complex(vec_v.y)}, {fmt_complex(vec_v.z)})"


def print_task3_conclusion() -> None:
    """Print the Task 3 conclusion block (keeps output identical)."""
    print("\n" + "-" * 60)
    print(" " * 60)

    print("CONCLUSION:")
    print("- Numerical divergence of M and N is approximately zero.")
    print("- Numerical curls agree with the analytic curls to ~1e-10,")
    print("  confirming correct implementation of the finite difference scheme.")
    print("- However, the relations curl N = M/|k| and curl M = N/|k|")
    print("  are not satisfied for the chosen definitions of M and N,")
    print("  as indicated by the large residual error.")
    print("- This demonstrates which Hansen vector properties hold")
    print("  for the present normalisation and which do not.")

    print("\n" + "#" * 60)


def run_task3_point(x: float, y: float, z: float, h: float) -> None:
    """Run the Task 3 checks for a single point (prints identical output)."""
    point = Point3D(x=x, y=y, z=z)

    mv = M_field(x, y, z)
    nv = N_field(x, y, z)

    divM_num = divergence(M_field, point, h)
    divN_num = divergence(N_field, point, h)

    curlN_num = curl(N_field, point, h)
    curlM_num = curl(M_field, point, h)

    # Analytic curls for THIS M,N choice
    curlN_an = curlN_analytic(x, y, z)
    curlM_an = curlM_analytic(x, y, z)

    # RHS checks: curl N = M/|k|, curl M = N/|k|
    rhs_curlN = vec_scale(1.0 / K_MAG, mv)
    rhs_curlM = vec_scale(1.0 / K_MAG, nv)

    print("\n" + "*" * 60)
    print(f"Point (x,y,z) = ({x:g}, {y:g}, {z:g})")
    print("-" * 60)

    print("-" * 60)
    print("Divergence check:")
    print(f"div M (num) = {divM_num}")
    print(f"div N (num) = {divN_num}")
    print("Expected: div M = 0, div N = 0")
    print("-" * 60)

    # Curl outputs
    print("-" * 60)
    print("Curl comparison:")
    print("\ncurl N (num) =", fmt_vec(curlN_num))
    print("curl N (an)  =", fmt_vec(curlN_an))
    print("M/|k| (RHS)  =", fmt_vec(rhs_curlN))
    print(f"||curlN_num - curlN_an|| = {vec_diff_norm(curlN_num, curlN_an):.2e}")
    print(f"||curlN_num - M/|k||     = {vec_diff_norm(curlN_num, rhs_curlN):.2f}")
    print(" " * 60)

    print("\ncurl M (num) =", fmt_vec(curlM_num))
    print("curl M (an)  =", fmt_vec(curlM_an))
    print("N/|k| (RHS)  =", fmt_vec(rhs_curlM))
    print(f"||curlM_num - curlM_an|| = {vec_diff_norm(curlM_num, curlM_an):.2e}")
    print(f"||curlM_num - N/|k||     = {vec_diff_norm(curlM_num, rhs_curlM):.2f}")
    print("*" * 60)


# Run the checks at selected points (I have set h=1e-6)
def run_task3(points: Sequence[Tuple[float, float, float]], h: float = 1e-6) -> None:
    """Run Hansen vector checks at a set of points."""
    print(" " * 60)
    print(" " * 60)
    print("#" * 60)

    print("\n" + "=" * 60)
    print("TASK 3: Hansen Vector Checks (numerical vs analytic)")
    print("=" * 60)

    print("-" * 60)
    print(f"Step size h = {h:g}")
    print(f"|k| = pi = {K_MAG:.3f}")
    print("-" * 60)

    for x, y, z in points:
        run_task3_point(x, y, z, h)

    print_task3_conclusion()


# Chosen points
task3_points = [
    (0.0, 0.0, 0.0),
    (0.12, 0.34, 0.56),
    (1.0, 1.0, 1.0),
]

run_task3(task3_points, h=1e-6)

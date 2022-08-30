# File used for Vector maths
import math


class createVector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __ne__(self, other):
		return not (self.x == other.x and self.y == other.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __repr__(self):
		return f'({self.x}, {self.y})'

	def add(self, vec):
		self.x += vec.x
		self.y += vec.y

	def sub(self, vec):
		self.x -= vec.x
		self.y -= vec.y

	def div(self, vec):
		self.x /= vec.x
		self.y /= vec.y

	def mult(self, n):
		self.x *= n
		self.y *= n

	def limit(self, lim):
		angle = math.atan2(self.y, self.x)
		self.x = lim * math.cos(angle)
		self.y = lim * math.sin(angle)

	def setMag(self, mag):
		self.x *= mag
		self.y *= mag

	def mag(self):
		return math.sqrt((self.x * self.x) + (self.y * self.y))

	def normalize(self):
		mag = math.sqrt(self.x*self.x + self.y*self.y)
		self.x /= mag
		self.y /= mag

	def fromAngle(self, theta):
		self.x = math.cos(theta)
		self.y = math.sin(theta)


def sub2Vec(vec1: createVector, vec2: createVector):
	return createVector(vec1.x - vec2.x, vec1.y - vec2.y)


def add2Vec(vec1: createVector, vec2: createVector):
	return createVector(vec1.x + vec2.x, vec1.y + vec2.y)


def dotProduct(p1: createVector, p2: createVector) -> float:
	return (p1.x * p2.x) + (p1.y * p2.y)


def magnitude(p1: createVector) -> float:
	return math.sqrt((p1.x * p1.x) + (p1.y * p1.y))


def projection(a: createVector, b: createVector) -> float:
	"""Projection of 'a' onto 'b'"""
	return (dotProduct(a, b))/(magnitude(b))


def min(x, y):
	return x if x < y else y


def max(x, y):
	return x if x > y else y


def clamp(r1, r2, n):
	return max(r1, min(r2, n))
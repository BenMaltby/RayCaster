def intersects(ls1, ls2):
	x1 = ls2.x1
	y1 = ls2.y1
	x2 = ls2.x2
	y2 = ls2.y2

	x3 = ls1.x1
	y3 = ls1.y1
	x4 = ls1.x2
	y4 = ls1.y2

	den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
	if not den: return None

	t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
	u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

	return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)] if t >= 0 and t <= 1 and u >= 0 and u <= 1 else False
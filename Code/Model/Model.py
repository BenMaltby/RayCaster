def intersects(ls1, ls2):
    """Implements an equation to check if two line segments intersect and return the point if they do"""

    x1 = ls2.x1
    y1 = ls2.y1
    x2 = ls2.x2
    y2 = ls2.y2

    x3 = ls1.x1
    y3 = ls1.y1
    x4 = ls1.x2
    y4 = ls1.y2

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if not denominator: return None

    k = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    v = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

    return [x1 + k * (x2 - x1), y1 + k * (y2 - y1)] if 0 <= k <= 1 and 0 <= v <= 1 else False


class LineSegment:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def main():
    Wall = LineSegment(0, 0, 2, 4)
    Ray = LineSegment(0.5, 3, 1.5, 1)

    print(intersects(Wall, Ray))

if __name__ == "__main__":
    main()
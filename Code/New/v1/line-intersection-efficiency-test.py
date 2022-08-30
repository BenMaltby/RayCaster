import time


class lineSeg:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        return f'({self.x1}, {self.y1}) => ({self.x2}, {self.y2})'


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'


def intersects(ls1: lineSeg, ls2: lineSeg):
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


def main():
    startTime = time.time()
    ls1 = lineSeg(400, 400, 261, 10)
    ls2 = lineSeg(50, 50, 750, 50)

    for i in range(1):
        a = intersects(ls1, ls2)

    print(f'\nTime: {time.time() - startTime} \nAnswer: {a}\n')

    

if __name__ == "__main__":
    main()




import pandas


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, point):

        distance = ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

        return distance


if __name__ == '__main__':


    a = Point(1,1)
    b = Point(2,2)

    print(a.distance_to(b))

    фукнция дистдо(а, б)
    в = аб
    возврат в
    конецфункции

    в = дистдо(а,б)
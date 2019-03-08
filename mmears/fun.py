def test(a):
    return a[1]


points = [[3, 3], [5, -1], [-2, 4]]
points1 = [1, 3, 2, 5, 4]

points1.sort()
points.sort(key=lambda m: m[0]**2 + m[1]**2)
print(points)

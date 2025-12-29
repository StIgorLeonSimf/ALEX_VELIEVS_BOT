x1 = 0
y1 = 0
x2, y2 = map(int, input('x, y: ').split())
x3, y3, r = map(int, input('x, y, r: ').split())
cnt = 0
for x in range(x3 - r, x3 + r + 1):
    for y in range(y3 - r, y3 + r + 1):
        if (y3 - y) ** 2 + (x3 - x) ** 2 <= r ** 2:
            if x1 <= x <= x2 and y1 <= y <= y2:
                cnt += 1
print(cnt)
# rect = set()
# circle = set()
# for x in range(x3 - r, x3 + r + 1):
#     for y in range(y3 - r, y3 + r + 1):
#         if (y3 - y) ** 2 + (x3 - x) ** 2 <= r ** 2:
#             circle.add((x, y))
circle = {(x, y) for x in range(x3 - r, x3 + r + 1)
          for y in range(y3 - r, y3 + r + 1)
          if (y3 - y) ** 2 + (x3 - x) ** 2 <= r ** 2
          }
# for x in range(x1, x2 + 1):
#     for y in range(y1, y2 + 1):
#         rect.add((x, y))
rect = {(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}

print(len(rect & circle))


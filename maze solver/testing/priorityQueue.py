from heapq import heappop, heappush


queue = []

a = (1, "a")
b = (2, "b")
c = (3, "c")

heappush(queue, c)
heappush(queue, a)
heappush(queue, b)

while queue:
    print(heappop(queue))
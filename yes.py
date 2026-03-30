n = int(input())
arr = list(map(int, input().split()))

answer = []


for i in range(n):
    l = []
    count = 0
    for j in range(2, arr[i]):
        if arr[i] % j == 0:
            l.append(j)
    answer.append(sum(l))

print(*answer)

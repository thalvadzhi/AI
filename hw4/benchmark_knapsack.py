def knapSack(W, wt, val, n):
    K = [[0 for x in range(W + 1)] for x in range(n + 1)]

    # Build table K[][] in bottom up manner
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w:
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    return K[n][W]
weights = []
costs = []

p = 1000
r = 100
m = 10

max_weight, N = tuple(map(int, input().split()))

# first cost then weight
for i in range(N):
    ci, wi = tuple(map(int, input().split()))
    costs.append(ci)
    weights.append(wi)

print(knapSack(max_weight, weights, costs, N))
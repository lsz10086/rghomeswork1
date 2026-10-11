# test_code.py
def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def calc(nums):
    res = []
    for i in nums:
        if i % 2 == 0:
            res.append(fib(i))
        else:
            res.append(i * 2)
    return res

print(calc([3, 4, 5, 6]))
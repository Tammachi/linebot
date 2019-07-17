import math

p=3469
q=1481
e=709


n=p*q

def lcm(x,y):
    pq_lcm=(x*y) // math.gcd(x,y)
    return pq_lcm

print('最大公約数' + str(math.gcd(p,q)))
print('最小公倍数' + str(lcm(p,q)))

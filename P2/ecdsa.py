import sys
import random

def add(x, y, p):
    return (x + y) % p

def multiply(x, y, p):
    return (x * y) % p

def subtract(x, y, p):
    while 1:
        y -= p
        if y < 0:
            y *= -1
            break
    return add(x, y, p)

def divide(x, y, p):
    return multiply(x, pow(y, p - 2, p), p)

def elliptic_add(P, Q, p):
    #Hmmm...are these ops supposed to be with finite add,mult,etc? Yes, they are, how is this working? So the elliptic curves exist in a finite field
    if P == [None, None]:
        return Q
    if Q == [None, None]:
        return P
    if P[0] == Q[0]:
        if P[1] == Q[1]:
            #m = (3 * pow((P[0]), 2))/(2*P[1])
            m = divide(multiply(3, multiply(P[0], P[0], p), p), multiply(P[1], 2, p), p)
        else:
            return [None, None]
    else:
        #m = (Q[1] - P[1])/(Q[0] - P[0])
        m = divide(subtract(Q[1], P[1], p), subtract(Q[0], P[0], p), p)
    #R = [pow(m, 2) - P[0] - Q[0], 0]
    R = [subtract(subtract(multiply(m, m, p), P[0], p), Q[0], p), 0]
    #R[1] = m * (P[0] - R[0]) - P[1]
    R[1] = subtract(multiply(m, subtract(P[0], R[0], p), p), P[1], p)
    return R

def elliptic_multiply(k, P, p):
    #Get bit string of k, start from P, 2P, 4P...when bit is 1 add to running sum
    R = [None, None]
    powers_of_P = P
    k_bit_str = str(bin(k))[2:]
    for b in reversed(k_bit_str):
        if b == '1':
            R = elliptic_add(R, powers_of_P, p)
        powers_of_P = elliptic_add(powers_of_P, powers_of_P, p)
    return R

def userid():
    print("ks5hrx")
    return 0

def genkey(p, o, G_x, G_y):
    p = int(p)
    o = int(o)
    G_x = int(G_x)
    G_y = int(G_y)
    d = random.randint(1, int(o) - 1)
    Q = elliptic_multiply(d, [G_x, G_y], p)
    print(d)
    print(Q[0])
    print(Q[1])
    return 0

def sign(p, o, G_x, G_y, d, h):
    p = int(p)
    o = int(o)
    G_x = int(G_x)
    G_y = int(G_y)
    d = int(d)
    h = int(h)
    k = random.randint(1, o - 1)
    k = 17
    inv_k = pow(k, -1, o) #mod o bc k is point numbers
    R = elliptic_multiply(k, [G_x, G_y], p) #mod p bc cycling through point G on curve
    r = R[0]
    s = (inv_k * (h + r*d)) % o
    if r == 0 or s == 0:
        return sign(p, o, G_x, G_y, d, h)
    print(r)
    print(s)
    return r, s

def verify(p, o, G_x, G_y, Q_x, Q_y, r, s, h):
    p = int(p)
    o = int(o)
    G_x = int(G_x)
    G_y = int(G_y)
    Q_x = int(Q_x)
    Q_y = int(Q_y)
    r = int(r)
    s = int(s)
    h = int(h)
    inv_s = pow(s, -1, o)
    R = elliptic_add(elliptic_multiply(inv_s * h, [G_x, G_y], p), elliptic_multiply(inv_s * r, [Q_x, Q_y], p), p) #mod p even though it says mod o in slides?
    if R[0] == r:
        print(True)
    else:
        print(False)
    return 0

if __name__ == '__main__':
    #print(subtract(13, 10, 17))
    #print(subtract(15, 10, 17))
    #print(divide(1, 13, 17))
    #print(divide(13, 13, 7))
    #p = 43
    #print(elliptic_add([12, 12], [42, 36], p))
    #print("Answer: [12, 31]")
    #print(elliptic_add([42, 36], [42, -36], p))
    #print("Answer: [None, None]")
    #print(elliptic_add([2, 12], [42, 36], p))
    #print("Answer: [20, 3]")
    #print(elliptic_add([12, 12], [12, 31], p))
    #print("Answer: [None, None]")
    #print(elliptic_add([None, None], [12, 12], p))
    #print("Answer: [12, 12]")
    #print(elliptic_multiply(2, [7, 7], p))
    #print("Answer: [21, 18]")
    #print(elliptic_multiply(4, [25, 18], p))
    #print("Answer: [35, 22]")
    #print(elliptic_multiply(5, [2, 12], p))
    #print("Answer: [12, 12]")
    #print(elliptic_multiply(16, [37, 36], 43))
    #print("Answer: [34, 3]")
    if sys.argv[1] == 'userid':
        #0-arg
        globals()[sys.argv[1]]()
    elif sys.argv[1] == 'genkey':
        #4-arg
        globals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif sys.argv[1] == 'sign':
        #6-arg
        globals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    elif sys.argv[1] == 'verify':
        #9-arg
        globals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])

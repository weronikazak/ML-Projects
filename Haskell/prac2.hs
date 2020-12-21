sumsq::Int->Int
sumsq 0=0
sumsq n = n*n + sumsq (n - 1)

evenf::Int->Int
evenf 0=0
evenf n = n + evenf( n - 2 )

oddf::Int->Int
oddf 1=1
oddf n = n * oddf(n - 2)

prodsum::Int->Int
prodsum n 
 | div n 2 == 0 = evenf(n) * oddf(n - 1)
 | otherwise = evenf(n-1) * oddf(n)


divideCheck::Int->Int->Bool
divideCheck n x
 | n = 1 = True
 | x `div` n == 0 = False 


isitprime::Int->Bool
isitprime n = divideCheck(n-1, n)


factorial::Int->Int
factorial 0=1
factorial n = n * factorial(n-1)


comb::Int->Int->Int
comb n m = factorial(n) `div` (factorial(m) * factorial(n - m))

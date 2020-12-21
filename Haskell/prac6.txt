and2::[Bool]->Bool
and2 [] = True
and2 xs
 | xs!!0 == True = and2 (tail xs)
 | otherwise = False

concat2::[[Int]]->[Int]
concat2 [] = []
concat2 xs = xs!!0 ++ concat2(tail xs)

replicate2::Int->Int->[Int]
replicate2 l 0 = []
replicate2 l n = [l] ++ replicate2 l (n-1)

select::[Int]->Int->Int
select xs n = xs!!n

pyths::Int->[(Int, Int, Int)]
pyths n = [(x, y, z) | x <- [1..n], y <- [1..n], z <- [1..n], x^2 + y^2 == z^2]

groups::Int->[Int]->[[Int]]
groups k list
 | length list <= k = [list]
 | otherwise = [take k list] ++ groups k (drop k list)
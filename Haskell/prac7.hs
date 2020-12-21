dropEvery1::Eq a=>[a]->Int->[a]
dropEvery1 arr pos = [arr!!i | i <- [0..length arr - 1], (i+1) `mod` pos /= 0]

rdups::Eq a =>[a]->[a]
rdups [] = []
rdups [x] = [x]
rdups (x:xs) = x: [k | k<- rdups(xs), k /= x]

replace::Int->a->[a]->[a]
replace 0 a (x:xs) = a:xs
replace i a (x:xs) = x:(replace(i-1) a xs)

slice::[a]->Int->Int->[a]
slice l i k
 | i > k = []
 | otherwise = (take (k - i + 1) (drop (i - 1) l))

insertAt::Int->[Int]->Int->[Int]
insertAt number array pos
 | pos == 1 = [number]++array
 | otherwise = take (pos-1) array ++ [number] ++ drop (pos-1) array



qsort::[Int]->[Int]
qsort [] = []
qsort (x:xs) = qsort [y | y <-xs, y <=x ] ++ [x] ++ qsort [y | y<-xs, y>x]



-- merge::[Int]->[Int]->[Int]
-- merge as bs = qsort (as++bs)


merge ::[Int] -> [Int] -> [Int]
merge [] ys = ys
merge xs [] = xs
merge (x:xs) (y:ys) 
 |x < y = x : merge xs (y:ys)
 |otherwise =  y: merge (x:xs) ys 


msort ::[Int] -> [Int]
msort [] = []
msort [a] = [a]
msort xs = merge (msort ys) (msort zs)
 where
 h = (length xs)`div` 2
 ys = take h xs
 zs = drop h xs




-- halve::[Int]->[Int]
-- halve (x:xs)
-- | length xs == 1 = xs
-- | otherwise = ( merge x ) ++ ( merge xs )



line::Int->Char->String
line number sign
 | number == 0 = [sign]
 | otherwise = [sign] ++ line (number-1) sign
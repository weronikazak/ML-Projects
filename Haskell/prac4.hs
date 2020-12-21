sumLength::[[Int]]->Int
sumLength[] = 0
sumLength(n:ns) = length n + length ns

sumf::[Int]->Int
sumf[] = 0
sumf(x:xs) = x + sumf xs

-- makeList::Int->Int
-- makeList number position
--  |position `mod` 2 == 0 = (-1) * number
--  |otherwise              = number

-- sumAlternatingSigns::[(Int, Int)]->Int
-- sumAlternatingSigns xs = sumf[ makeList [(x, k) | (x, k)<- zip xs [0..length xs] ] ]

scalarproduct::[Int]->[Int]->Int
scalarproduct xs ys = sum [x*y | (x, y)<- zip xs ys]

perfects::Int->[Int]

dayhoursmins::Int->(Int, Int, Int)
dayhoursmins x = (x `div` 1440, x `mod` 1440 `div` 60, x `mod` 1440 `mod` 60)




suma::[Int]->Int
suma[] = 0
suma(x:xs) = x + suma xs

sumnegpos::[Int]->(Int, Int)
sumnegpos arr = (suma [n | n<-arr, n < 0], suma [n | n<-arr, n > 0])


removing::[Int]->[Int]
removing x = drop 2 (init (init x))

shuffle::[Int]->[Int]
shuffle x = tail(x++ [head x])

safetail::[Int]->[Int]

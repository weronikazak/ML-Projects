next::Int->Int
next x
 | mod x 2 == 0 = div x 2
 | otherwise    = ((x*2) + 1)


absolute::Int->Int
absolute x
 | x < 0 = x * (-1)
 | otherwise = x



trafficlights::String->String
trafficlights light
 | light == "red" || light == "green" = "orange"
 | otherwise                             = "red or green"

summinmax3::Int->Int->Int->Int
summinmax3 x y z = sum( min(x y z) max(x y z) )



k::Int->Int->Bool
k x y
 | x < 0 || y < 0 = True
 | otherwise  = False

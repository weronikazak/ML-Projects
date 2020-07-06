library(datasets)
head(iris)
hist(iris$Petal.Length)

summary(iris$Petal.Length)

summary(iris$Species)

hist(iris$Petal.Length[iris$Species == "versicolor"],
     main="Petal Length: VersiColor")

hist(iris$Petal.Length[iris$Species == "virginica"],
     main="Petal Length: VersiColor")

hist(iris$Petal.Length[iris$Species == "setosa"],
     main="Petal Length: VersiColor")

hist(iris$Petal.Length[iris$Petal.Length < 2],
     main="Petal Length < 2")

hist(iris$Petal.Length[iris$Species == "virginica" &
                         iris$Petal.Length < 5.5],
     main="Petal Length: Short Virginica")


i.setosa <- iris[iris$Species == "setosa",]

head(i.setosa)
summary(i.setosa)
hist(i.setosa$Petal.Length)

# rm(list = ls())


# DATA TYPES

n1 <- 15
n1
typeof(n1)

n2 <- 1.5
n2
typeof(n2)

c1 <- "c"
c1
typeof(c1)

c2 <- "a string of text"
c2
typeof(c2)

l1 <- TRUE
l1
typeof(l1)

l2 <- F
l2
typeof(l2)


v1 <- c(1, 2, 3, 4, 5)
v1
is.vector(v1)

v2 <- c("a", "b", "c")
v2
is.vector(v2)

v3 <- c(T, F, F, T)
v3
is.vector(v3)

m1 <- matrix(c(T, T, F, F, T, F), nrow=2)
m1

m2 <- matrix(c("a", "b", "c", "d"), nrow=2, byrow=T)

m2


a1 <- array(c(1:24), c(4, 3, 2))
a1


vn <- c(1, 2, 3)
vc <- c("a", "b", "c")
vl <- c(T, F, T, F, T, T, F, F, F)

dfa <- cbind(vn, vc, vl)
dfa

df <- as.data.frame(cbind(vn, vc, vl))
df

list1 = list(vn, vc, vl)
list1


list2 = list(vn, vc, vl, list1)
list2


# COERCE

(coernce1 <- c(1, "b", T))
typeof(coernce1)

coerce2 <- 5
typeof(coerce2)

coerce3 <- as.integer(2)
typeof(coerce3)


(coerce4 <- as.numeric(c("1", "2", "3")))
typeof(coerce4)


c6 <- matrix(1:9, nrow=3)
is.matrix(c6)

c6 <- as.data.frame(matrix(1:9, nrow=3))
is.matrix(c6)

rm(list = ls())


# FACTORS

x <- 1:3
y <- 1:9

df1 <- cbind.data.frame(x, y)
typeof(df1$x)
str(df1)

x = as.factor(c(1:3))
df1 <- cbind.data.frame(x, y)
typeof(df1$x)
str(df1)

x <- c(1:3)
df3 <- cbind.data.frame(x, y)
df3$x <- factor(df3$x, levels = c(1, 2, 3))
typeof(df3$x)
str(df3)

x <- c(1:3)
df <- cbind.data.frame(x, y)
df$x <- factor(df$x, levels=c(1, 2, 3),
               labels = c("macOS", "Windows", "Linux"))

df
typeof(df$x)
str(df)

x <- c(1:3)
df <- cbind.data.frame(x, y)
df$x <- ordered(df$x, levels=c(3, 1, 2),
                labels = c("No", 'Maybe', "Yes"))
df
str(df)
typeof(df$x)

rm(list = ls())


# ASSIGNING

x <- 0:10
x

# od 10 do 0
x <- 10:0
x

# ascending values (1:10)
x <-  seq(10)
x

x <- seq(30, 0, by= -2)
x

# przechodzisz do konsoli i wpisujesz wartosci jak leci
# ale tylko cyfry
x_console <-  scan()
x_console

x <- rep(TRUE, 5)
x

# T F T F T F ...
x <- rep(c(T, F), 6)
x

# T T T T F F F F
x <- rep(c(T, F), each=4)
x

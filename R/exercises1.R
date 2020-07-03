library(datasets)
head(iris)

?plot

plot(iris$Species)
plot(iris$Sepal.Length)
plot(iris$Species, iris$Petal.Width)
plot(iris$Petal.Length, iris$Petal.Width)
plot(iris)

plot(iris$Petal.Length, iris$Petal.Width,
     col="#cc0000",
     pch=19,
     main="Iris: Petal Length vs. Petal Width",
     xlab="Petal Length",
     ylab="Petal Width")

plot(cos, 0, 2*pi)
plot(exp, 1, 5)
plot(dnorm, -3, +3)

plot(dnorm, -3, +3,
     col="#cc0000",
     lwd=5,
     main="Standard Normal Disctribution",
     xlab="z-scores",
     ylab="Density")

detach("package:datasets", unload = TRUE)


library(datasets)
?mtcars
head(mtcars)

barplot(mtcars$cyl)

cylinders <- table(mtcars$cyl)
barplot(cylinders)

rm(list = ls())


hist(iris$Sepal.Length)
hist(iris$Sepal.Width)
hist(iris$Petal.Length)
hist(iris$Sepal.Width)

par(mfrow= c(3, 1))

hist(iris$Petal.Length [iris$Species == "setosa"],
     xlim = c(0, 3),
     breaks = 9,
     main = "Petal Width for Setosa",
     xlab = "",
     col = "red")

hist(iris$Sepal.Width [iris$Species == "versicolor"],
     xlim=c(0, 3),
     breaks = 9,
     main="Petal Width for Versicolor",
     xlab="",
     col="purple")

hist(iris$Petal.Width [iris$Species == "virginica"],
     xlim = c(0, 3),
     breaks=9,
     main="Petal Width for Virginica",
     xlab="",
     col="blue")

hist(mtcars$wt)
hist(mtcars$mpg)

plot(mtcars$wt, mtcars$mpg)

par(mfrow=c(1, 1))

plot(mtcars$wt, mtcars$mpg,
     pch=19,
     cex=1.5,
     col="#cc0000",
     main="MPG as a Function of Weight of Cars",
     xlab="Weight (in 1000 pounds)",
     ylab="MPG")


# -----------------
head(lynx)

hist(lynx,
     breaks=14,
     freq=FALSE, # axis shows density not freq
     col="thistle1",
     main=paste("Histogram of Annual Canadian Lynx", "Trappings 1921-1934"),
     xlab="Number of Lynx Trapped"
     )

curve(dnorm(x, mean = mean(lynx), sd = sd(lynx)),
      col="thistle4", #color of curve,
      lwd = 2,
      add = TRUE)

lines(density(lynx), col="blue", lwd=2)
lines(density(lynx, adjust=3), col="purple", lwd=2)  

rug(lynx, lwd=2, col="gray")


# ------------------------

head(iris)

summary(iris$Species)
summary(iris$Sepal.Length)
summary(iris)

# --------------------------
install.packages("psych")
library(psych)
library(pacman)
p_load(psych)

p_help(psych, web=F)

describe(iris$Sepal.Length)
describe(iris)

# SXD-SWE-Intern
## Math and Programming Exercises
Assume your team is building an application that attempts to find the optimal solution to a multivariate equation given a set of constraints. Feel free to solve the below in your programming language of choice.

### Part I: Math

Consider the following problem:

$Min Z = –3X1 + X2$

Subject to the following:

$X_{1} + X_{2} ≤ 5$

$2X_{1} + X_{2} ≤ 8$

$X_{1} ≥ 0, X_{2} ≥ 0$

What is the optimal solution?

```diff
**Answer** : This question is linear optimization problem where based on given conditions, we need to find maximum or minimum value of the objective function. As we could see that all the variables have power of 1, therefore, the common area shared between two set of equations (also called as feasible region) will provide the optimal solutions. We will use `Simplex Method` to solve the problem, which is widely used method for solving linear problems. Also, we know that if a linear problem as bounded solution then one of the corner points (which is part of shared/feasible region) provide the optimal solution. 

We used `linprog` library from `Scipy` to solve the equations. Additionaly, the algorithm is designed with OOPs concept. Moreover, we used Python rich visualisation tools to visualise the overall solution. I have added `question1.py` file as a solution for first problem. The final outputs are : for given objective function, the optimal value of `X1 = 4.0` and `X2 = 0.0`, which resulted in minimum value of `Z = -12.0`. The overall graphical solution can be seen as follows : 
```

<img src="https://github.com/kunalkumar1608/SXD-SWE-Intern/blob/main/sxd_question1.png" width="800" height="600">


### Part 2: Programming

Write a program that can iteratively (or recursively) solve for $X_{1}$ and $X_{2}$ for similar equations to the above. As a benchmark, when facing the following (similar) problem.

$Max Z = 3X1 + 4X2$

Subject to the following:

$15X1 + 10X2 ≤ 300$

$2.5X_{1} + 5X_{2} ≤ 110$

$X_{1} ≥ 0, X_{2} ≥ 0$

your program should output $X_{1} = 8, X_{2} = 18$, and $Z = 96$ as the optimal solution. Please focus on writing your program with best OOP practices in mind (class design, DRY, handling static variables, etc.).

```diff
**Answer** : 
As explained in `Question 1`, that we used `linprog` library from `Scipy` to solve the problem. Additionaly, the algorithm is designed with OOPs concept. Moreover, we used Python rich visualisation tools to visualise the overall solution. I have added `question2.py` file as a solution for second problem. As expected, the final outputs are - for given objective function, the optimal value of `X1 = 8.0` and `X2 = 18.0`, which resulted in maximum value of `Z = 96.0`. The overall graphical solution can be seen as follows : 
```

<img src="https://github.com/kunalkumar1608/SXD-SWE-Intern/blob/main/sxd_question2.png" width="800" height="600">


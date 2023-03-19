# SXD-SWE-Intern
## Math and Programming Exercises
Assume your team is building an application that attempts to find the optimal solution to a multivariate equation given a set of constraints. Feel free to solve the below in your programming language of choice.

### Part I: Math

Consider the following problem:

$Min Z = –3X_1 + X_2$

Subject to the following:

$X_{1} + X_{2} ≤ 5$

$2X_{1} + X_{2} ≤ 8$

$X_{1} ≥ 0, X_{2} ≥ 0$

_What is the optimal solution?_

#### Answer : 
This question is linear optimization problem where based on given conditions, we need to find maximum or minimum value of the objective function. As we could see that all the variables have power of 1, therefore, the common area shared between two set of equations (also called as feasible region) will provide the optimal solutions. We will use `Simplex Method` to solve the problem, which is widely used method for solving linear problems. Also, we know that if a linear problem as bounded solution then one of the corner points (which is part of shared/feasible region) provide the optimal solution. 

We used `linprog` library from `Scipy` to solve the equations. Additionaly, the algorithm is designed with OOPs concept. Moreover, we used Python rich visualisation tools to visualise the overall solution. I have added `question1.py` file as a solution for first problem. The final outputs are : for given objective function, the optimal value of `X1 = 4.0` and `X2 = 0.0`, which resulted in minimum value of `Z = -12.0`. The overall graphical solution can be seen as follows : 

<img src="https://github.com/kunalkumar1608/SXD-SWE-Intern/blob/main/sxd_question1.png" width="800" height="600">


### Part 2: Programming

Write a program that can iteratively (or recursively) solve for $X_{1}$ and $X_{2}$ for similar equations to the above. As a benchmark, when facing the following (similar) problem.

$Max Z = 3X_1 + 4X_2$

Subject to the following:

$15X_1 + 10X_2 ≤ 300$

$2.5X_{1} + 5X_{2} ≤ 110$

$X_{1} ≥ 0, X_{2} ≥ 0$

your program should output $X_{1} = 8, X_{2} = 18$, and $Z = 96$ as the optimal solution. Please focus on writing your program with best OOP practices in mind (class design, DRY, handling static variables, etc.).

#### Answer : 
As explained in `Question 1`, that we used `linprog` library from `Scipy` to solve the problem. Additionaly, the algorithm is designed with OOPs concept. Moreover, we used Python rich visualisation tools to visualise the overall solution. I have added `question2.py` file as a solution for second problem. As we are using Scipy's linprog library which works for minimization problem, hence, we mulitplied the objective function with -1 in both side. Therefore, our new objective function becomes $Min -Z = -3X_1 - 4X_2$. Therefore, with given constriants our algorithm returns optipal value of `Z` in inverse sign. Thus, we multiply with `-1` on final optimal value which will result in maximum optimal value of objective function. As expected, the final outputs are - for given objective function, the optimal value of `X1 = 8.0` and `X2 = 18.0`, which resulted in maximum value of `Z = 96.0`. The overall graphical solution can be seen as follows : 

<img src="https://github.com/kunalkumar1608/SXD-SWE-Intern/blob/main/sxd_question2.png" width="800" height="600">


### Part 3: Systems

Let’s assume that we are trying to roll out the program you wrote above to a production system and web UI with a set of end users. Instead of recalculating the optimal set of values for `X1` and `X2` every time a user changes the min/max function and associated constraints, let’s first implement a check against a backend database to see if a previous problem “already exists”. To check this, you would need to run a comparison between the coefficients that the user inputs into the web UI and whether they match any set of coefficients in the backend. The core ask here is to set up a dedicated backend database of your choice to store these inputs and retrieve them as quickly and efficiently as possible (sub-millisecond latency) to then render the “already computed solution” in the frontend.

Some questions to consider:

_3.1 What type of database would you choose? Why?_

**Answer** : As mentioned that, we need to store and retrieve the data with minimal possible latency, I would prefer NoSQL databases like `mongoDB` or `Cassandra`. The reason to choose such database is that they are highly scalable (which can efficiently handle large volume of data) and distributed (making it fast processing). Moreover, NoSQL databases are schema-less, thus making them superior in handling unstructured data which could be a case while storing the coefficients. We could use `Amazon DynamoDB`, which is also a NoSQL database providing previous benefits. Also, DynamoDB uses synchronous replication across multiple data center for high durability and availibility. Thus, if one replica has overloaded with request, the same request can be routed to another replica of share.

_3.2 Assume your target user audience are all math students in the US. How would you size your database accordingly? What strategies would you consider to prevent overloading a single database instance with requests?_

**Answer** : Now, we are given that the target audience are maths student in the US.

_3.3 Did you set up your database locally or on cloud infrastructure?_

**Answer** : 

As an example, for Part 2 above you would check to see if the same coefficients and max / min exist in the database for $Max Z = 3X_1 + 4X_2$ (need to store Max, 3, 4). Then you would need to do something similar for each of the constraints. To keep this problem simple, assume the following for all possible problems the user can input:

* Only constrained to either a Max or Min cost function for `Z`
* Only involve the two variables `X1` and `X2`
* The last constraint `X1` ≥ 0, `X2` ≥ 0 will never change

You do not need to program a dedicated web UI for this exercise. Please only focus on basic functionalities. However, it is recommended to write at least one integration test that checks for whether a given “problem pattern” exists in the backend.

**Answer** : 

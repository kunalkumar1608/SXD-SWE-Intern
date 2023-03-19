from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')

class LinearProgramming:
  def __init__(self, obj, constraint, bound, _type):
    self.objective = obj
    self.constraints = constraint
    self.bnd = bound
    self.type = _type
    self.lhs_inequation = [ row[:-1] for row in self.constraints ]
    self.rhs_inequation = [ row[-1] for row in self.constraints ]
  
  def getOptimalParams( self ):
    obj = self.objective if self.type=='minimize' else [-1*val for val in self.objective]
    opt = linprog(c=obj, A_ub=self.lhs_inequation, b_ub=self.rhs_inequation, bounds=self.bnd, method="revised simplex")
    if opt.status == 0:
      optimalX1, optimalX2 = opt.x[0], opt.x[1]
      optimalZ = opt.fun if self.type=='minimize' else -1*opt.fun
      return optimalX1, optimalX2, optimalZ
    else:
      raise Exception("No optimal solution exist!")

  def make_plot( self, x_1, x_2, Z ):
    # Shortening the maximum limits of the plot
    mxm_lim = 0
    for row in range(len(self.rhs_inequation)):
      mxm_lim = max(mxm_lim, self.rhs_inequation[row]/min(self.lhs_inequation[row]))

    # Values for grid lines
    x1 = np.linspace(0, mxm_lim, 2000)
    x2 = np.linspace(0, mxm_lim, 2000)
    x3 = (self.rhs_inequation[0] - self.lhs_inequation[0][0] * x1)/self.lhs_inequation[0][1]
    x4 = (self.rhs_inequation[1] - self.lhs_inequation[1][0] * x1)/self.lhs_inequation[1][1]

    # Filling the feasible regions
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.grid()
    d = np.linspace(0,mxm_lim,300)
    x_f,y_f = np.meshgrid(d,d)
    ax.imshow( ((x_f>=0) & (y_f>=0) & (y_f<=(self.rhs_inequation[0] - self.lhs_inequation[0][0]*x_f)/self.lhs_inequation[0][1]) & 
                (y_f<=(self.rhs_inequation[1] - self.lhs_inequation[1][0]*x_f)/self.lhs_inequation[1][1])).astype(int) , 
                    extent=(x_f.min(),x_f.max(),y_f.min(),y_f.max()),origin="lower", cmap="Greys", alpha = 0.3);


    # Plotting the result
    ax.plot(x1, x3, label=r'${x1_v}.x_1 + {x2_v}.x_2\leq{r_v}$'.format(x1_v=self.lhs_inequation[0][0], 
                                                                       x2_v=self.lhs_inequation[0][1], 
                                                                       r_v=self.rhs_inequation[0]))
    ax.plot(x1, x4, label=r'${x1_v}.x_1 + {x2_v}.x_2\leq{r_v}$'.format(x1_v=self.lhs_inequation[1][0], 
                                                                       x2_v=self.lhs_inequation[1][1], 
                                                                       r_v=self.rhs_inequation[1]))
    ax.plot(x_1, x_2, "*", color="black")
    ax.text(x_1-0.8, x_2+0.2, "Optimal Point({x_1}, {x_2})".format(x_1=x_1, x_2=x_2), size=9)
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel(r'$x_1$' +" " + r'$(x_1 \geq 0)$')
    plt.ylabel(r'$x_2$' +" " + r'$(x_2 \geq 0)$')
    plt.yticks(rotation=90)
    plt.xlim((0, mxm_lim))
    plt.ylim((0, mxm_lim))
    plt.title("Optimal Solution is Z = {val}".format(val=Z))
    plt.show()

objective = [3, 4]
constraints = [[15, 10, 300], [2.5, 5, 110]]
bound = [(0, float("inf")),  # Bounds of X1
         (0, float("inf"))]  # Bounds of X2

lp = LinearProgramming(objective, constraints, bound, "maximize")
optimalX1, optimalX2, optimalZ = lp.getOptimalParams()
print(f"For given objective function, the optimal X1 is = {optimalX1}, optimal X2 is = {optimalX2}, and optimal Z = {optimalZ}")

print("\nThe graphical representation of above solution is : \n")
lp.make_plot(optimalX1, optimalX2, optimalZ)

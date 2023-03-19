from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')

""" ## Linear Optimazation function from Question 1 and Quesrion 2 """
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



"""### Integration Test class"""
class integration_test:
  def __init__( self, max_min, objective, constraints, collection ):
    self.max_min = max_min
    self.objective = objective
    self.constraints = constraints
    self.key = self.create_key()
    self.collection = collection

  def create_key( self ):
    # Create a unique key based on the problem inputs

    # We use same bounds for X1 and X2 for all the testcases
    bound = [(0, float("inf")),  # Bounds of X1
             (0, float("inf"))]  # Bounds of X2

    key = {
        "max_min": self.max_min,
        "obj_coeffs": self.objective,
        "constraint_coeffs": self.constraints,
        "bound" : bound,
    }
    return key

  def insertOrCheckKeyValue( self ):
    # Check if the key exists in the database, we do not strore anything and returns the result
    retrieved_result = self.collection.find_one({'key' : self.key})

    # If the key exists, retrieve the optimal solution from the database
    if retrieved_result:
        optimal_params = retrieved_result["optimal_params"]
        return optimal_params, True
    else:
        # If the key does not exist, we will find the optimal params and store it in the database
        lp = LinearProgramming(self.key['obj_coeffs'], self.key['constraint_coeffs'], self.key['bound'], self.key['max_min'])
        optimalX1, optimalX2, optimalZ = lp.getOptimalParams()
        self.collection.insert_one({"key": self.key, "optimal_params": [optimalX1, optimalX2, optimalZ]})
        return [], False



"""## TestCases for Intergration Test"""
#! python -m pip install pymongo==3.7.2
#! pip3 install install 'pymongo[srv]'
import pymongo
import unittest
from pymongo import MongoClient

class test_integration_test(unittest.TestCase):

  def __init__( self ):
    self.collection = self.test_setUp()

  def test_setUp( self ):
    # Setting up pymongo cluster. `url` should be changed accordingly.
    url = "mongodb+srv://kunalkumar:mongodbpass123@cluster0.nmwcebs.mongodb.net/test"
    client = pymongo.MongoClient( url )
    db = client["problem_patterns"]
    collection = db["patterns"]
    return collection

  def test_create_key( self ):
    objective = [3, 4]
    constraints = [[15, 10, 300], [2.5, 5, 110]]
    max_min = "maximize"
    it = integration_test( max_min, objective, constraints, self.collection )
    calculated_key = it.create_key()
    expected_key = {
        "max_min": max_min,
        "obj_coeffs": objective,
        "constraint_coeffs": constraints,
        "bound" : [(0, float("inf")), (0, float("inf"))],
    }
    self.assertDictEqual(calculated_key, expected_key)

  def test1(self):
    # Define the problem inputs
    objective = [3, 4]
    constraints = [[15, 10, 300], [2.5, 5, 110]]
    max_min = "maximize"
    expected_value = [8.0, 18.0, 96.0]

    it = integration_test( max_min, objective, constraints, self.collection )
    calculated_value, checkIfExists = it.insertOrCheckKeyValue()
    #This key doesn't exists as of now
    if checkIfExists==False:
      print("The key didn't exists, so it got stored.")
      self.assertTrue(len(calculated_value)==0)
    else:
      print("The key already exists. Hence, it was not stored again.")
      self.assertTrue(calculated_value == expected_value)
  
  def test2(self):
    objective = [-3, 1]
    constraints = [[1, 1, 5], [2, 1, 8]]
    max_min = "minimize"
    expected_value = [ 4.0, 0.0, -12.0]

    it = integration_test( max_min, objective, constraints, self.collection )
    calculated_value, checkIfExists = it.insertOrCheckKeyValue()
    #This key doesn't exists as of now
    if checkIfExists==False:
      print("The key didn't exists, so it got stored.")
      self.assertTrue(len(calculated_value)==0)
    else:
      print("The key already exists. Hence, it was not stored again.")
      self.assertTrue(calculated_value == expected_value)

  def test3(self):
    objective = [3, 4]
    constraints = [[15, 10, 300], [2.5, 5, 110]]
    max_min = "maximize"
    expected_value = [8.0, 18.0, 96.0]
    it = integration_test( max_min, objective, constraints, self.collection )
    calculated_value, checkIfExists = it.insertOrCheckKeyValue()
    #This key exists, hence, it will not store anything
    if checkIfExists==False:
      print("The key didn't exists, so it got stored.")
      self.assertTrue(len(calculated_value)==0)
    else:
      print("The key already exists. Hence, it was not stored again.")
      self.assertTrue(calculated_value == expected_value)

# Testing above test cases
test_ip = test_integration_test()
test_ip.test_create_key()
test_ip.test1()
test_ip.test2()
test_ip.test3()
import numpy as np
import sympy

x = sympy.core.symbols('x')
y = sympy.core.symbols('y')

class Point():
     
    def __init__(self, x, y):
         self.x = x
         self.y = y

    def __repr__(self) :
        return 'Point({}, {})'.format(self.x, self.y)

    def distance(self, point):
        
        x1 = self.x
        y1 = self.y
        x2 = point.x
        y2 = point.y
        dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)
        return dist
    
class Line():

    def __init__(self, point1, point2):
        
        self.x1 = point1.x
        self.y1 = point1.y
        self.x2 = point2.x
        self.y2 = point2.y
        self.slope = (self.y1 - self.y2)/(self.x1 - self.x2)
        self.eq = (y - self.y1) - self.slope*(x - self.x1)

    def __repr__(self):
        return str(self.eq)

class Circle():

    def __init__(self,radius, centre=(0,0)):

        self.radius = radius
        self.centre_x = centre[0]
        self.centre_y = centre[1]
        self.eq = (x - self.centre_x)**2 + (y - self.centre_y)**2 - self.radius

    def __repr__(self):
        return str(self.eq)

class solve():

    def __init__(self, eq1, eq2):

        self.x = []
        self.eq1 = sympy.solve(eq1.eq, y)
        self.eq2 = sympy.solve(eq2.eq, y)
        
        for i in range(len(self.eq1)):
            for j in range(len(self.eq2)):    
                temp_x = sympy.Eq(self.eq1[i], self.eq2[j])
                print(temp_x)
                temp_x = sympy.solve(temp_x)
                self.x = self.x + temp_x
                
        self.y = list(map(lambda x : self.eq1[0].subs({x:self.x}), self.x))
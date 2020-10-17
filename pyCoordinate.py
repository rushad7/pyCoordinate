import sympy

class _variables:
    def __init__(self):
        self._x = sympy.core.symbols('x')
        self._y = sympy.core.symbols('y')

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
        dist = float(sympy.sqrt((x1-x2)**2 + (y1-y2)**2))
        return dist
    
class Line(_variables):

    def __init__(self, point1, point2):
        super().__init__()
        self.x1 = point1.x
        self.y1 = point1.y
        self.x2 = point2.x
        self.y2 = point2.y
        self.slope = (self.y1 - self.y2)/(self.x1 - self.x2)
        self.eq = (self._y - self.y1) - self.slope*(self._x - self.x1)

    def __repr__(self):
        return str(self.eq)

class Circle(_variables):

    def __init__(self,radius, centre=(0,0)):
        super().__init__()
        self.radius = radius
        self.centre_x = centre[0]
        self.centre_y = centre[1]
        self.eq = (self._x - self.centre_x)**2 + (self._y - self.centre_y)**2 - self.radius

    def __repr__(self):
        return str(self.eq)

class solve(_variables):

    def __init__(self, eq1, eq2):
        super().__init__()
        self.x = []
        self.eq1 = sympy.solve(eq1.eq, self._y)
        self.eq2 = sympy.solve(eq2.eq, self._y)
        
        for i in range(len(self.eq1)):
            for j in range(len(self.eq2)):    
                temp_x = sympy.Eq(self.eq1[i], self.eq2[j])
                temp_x = sympy.solve(temp_x)
                self.x = self.x + temp_x
        
        self.y = []
        for i in range(len(self.x)):
            self.y.append(self.eq1[i].subs({self._x:self.x[i]}))
        
        self.points = list(zip(self.x, self.y))
        
    def __repr__(self):
        rep = 'Intersection Points : \n'
        for i in range(len(self.points)):
            rep = rep + str(self.points[i]) + '\n'
        return rep

class ConicSection(_variables):

    def __init__(self, A,B,C,D,E,F):
        super().__init__()
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E
        self.F = F
        self.eq = self.A*self._x**2 + self.B*self._x*self._y + self.C*self._y**2 + self.D*self._x + self.E*self._y + self.F

    def __repr__(self):
        return str(self.eq)

    def ecc(self):

        e = self.B**2 - 4*self.A*self.C
        return e

    def conicType(self):

        e = self.ecc()

        if e == 0:
            conic_type = 'Parabola'
        elif e < 0:
            if self.A == self.C:
                conic_type = 'Circle'
            else:
                conic_type = 'Elipse'
        elif e > 0:
            conic_type = 'Hyperbola'

        return conic_type

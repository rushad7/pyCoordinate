import sympy
from collections import Counter
from itertools import combinations

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

    def __init__(self, eq1, eq2, return_complex=False):
        super().__init__()
        
        def most(List, n):
            c = Counter(List)
            return c.most_common(n)

        if (type(eq1) == Line) and (type(eq2) == Circle or type(eq2) == ConicSection):
            eq1, eq2 = eq2, eq1

        self.eq1 = sympy.solve(eq1.eq, self._y)
        self.eq2 = sympy.solve(eq2.eq, self._y) 

        if len(self.eq1[0].args) != 0 and self.eq1[0].args[0] != -1:
            pass
        else:
            self.eq1.reverse()

        if len(self.eq2[0].args) != 0 and self.eq2[0].args[0] != -1:
            pass
        else:
            self.eq2.reverse()

        self.x_points = []
        for i in range(len(self.eq1)):
            for j in range(len(self.eq2)):
                temp_eq = sympy.Eq(self.eq1[i], self.eq2[j])
                temp_sol = sympy.solve(temp_eq)

                if len(temp_sol) != 0:
                    if return_complex != False:
                        for i in range(len(temp_sol)):
                            if temp_sol[i].is_complex:
                                self.x_points = self.x_points + [temp_sol[i]]
                            else:
                                self.x_points = self.x_points + [temp_sol[i]]
                    elif return_complex == False:
                        self.x_points = self.x_points + temp_sol
                
        points = []
        eq = self.eq1 + self.eq2

        for i in range(len(eq)):
            for j in range(len(self.x_points)):
                y_point = eq[i].subs({self._x:self.x_points[j]})
                points.append((self.x_points[j], y_point))

        points = most(points, len(self.x_points))
        self.points = []

        for i in range(len(points)):
            self.points.append(points[i][0])

        def checkSol(eq, point):  
            lhs = point[1]
            rhs = eq.subs({self._x: point[0]})
            if lhs == rhs:
                return 1
            else:
                return 0

        def Comb():
            combinedList = self.eq1 + self.eq2 + self.points
            combs =  list(combinations(combinedList,2))
            comb = []
            try:
                for i in range(len(combs)):
                    if type(combs[i][0]) != tuple:
                        module1 = str(combs[i][0].__module__).split('.')[0]
                    else:
                        module1 = 'tuple'
                    if type(combs[i][1]) != tuple:
                        module2 = str(combs[i][1].__module__).split('.')[0]
                    else:
                        module2 = 'tuple'

                    if (module1 == 'sympy' and module2 == 'tuple') or (module2 == 'sympy' and module1 == 'tuple'):
                        comb.append(combs[i])       
            except:
                pass
                
            return(comb)

        comb = Comb()
        temp_points = []

        for i in range(len(comb)):
            check = checkSol(comb[i][0], comb[i][1])
            if check == 1:
                temp_points.append(comb[i][1])
            else:
                pass

        self.points = temp_points
        self.points = list(set(self.points))

        for i in range(len(self.points)):
            self.points[i] = Point(self.points[i][0], self.points[i][1])

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

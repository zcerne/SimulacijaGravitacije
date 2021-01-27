import pygame
import random
import numpy as np
import math

def TreeWalk(node, node0, thetamax=0.7, G=1.0):
    """
    Adds the contribution to the field at node0's point due to particles in node.
    Calling this with the topnode as node will walk the tree to calculate the total field at node0.
    """
    dx = node.COM - node0.COM    # vector between nodes' centres of mass
    r = np.sqrt(np.sum(dx**2))   # distance between them
    if r>0:
        # if the node only has one particle or theta is small enough,
        #  add the field contribution to value stored in node.g
        if (len(node.children)==0) or (node.size/r < thetamax):
            node0.g += G * node.mass * dx/r**3
        else:
            # otherwise split up the node and repeat
            for c in node.children: TreeWalk(c, node0, thetamax, G)

def GravAccel(delci, thetamax=0.7, G=1.):
    points = []
    masses = []
    for delec in delci:
        points.append([delec.x, delec.y])
        masses.append([delec.masa, delec.masa])
    points = np.array(points)
    masses = np.array(masses)

    center = (np.max(points,axis=0)+np.min(points,axis=0))/2       #center of bounding box
    topsize = np.max(np.max(points,axis=0)-np.min(points,axis=0))  #size of bounding box
    leaves = []  # want to keep track of leaf nodes
    topnode = OctNode(center, topsize, masses, points, np.arange(len(masses)), leaves) #build the tree
 
    accel = np.empty_like(points)
    for i, leaf in enumerate(leaves):
        TreeWalk(topnode, leaf, thetamax, G)  # do field summation
        accel[leaf.id] = leaf.g  # get the stored acceleration
    for i, delec in enumerate(delci):
        delec.a = accel[i]
        
        a_kot = math.atan2(delec.a[1], delec.a[0])
        a_posp = math.hypot(delec.a[0], delec.a[1])
        (delec.kot, delec.v) = addVectors(delec.kot, delec.v, a_kot, a_posp)

    #return accel

def addVectors(kot1, v1, kot2, v2):
    x = np.cos(kot1) * v1 + np.cos(kot2) * v2
    y = np.sin(kot1) * v1 + np.sin(kot2) * v2 

    length = np.hypot(x, y)
    angle = math.atan2(y, x) 
    return (angle, length)

def združi(p1, p2):
    if math.hypot(p1.x - p2.x, p1.y - p2.y) < p1.size + p2.size:

        total_masa = p1.masa + p2.masa
        p1.x = (p1.x*p1.masa + p2.x*p2.masa)/total_masa
        p1.y = (p1.y*p1.masa + p2.y*p2.masa)/total_masa
        (p1.kot, p1.v) = addVectors(p1.kot, p1.v*p1.masa/total_masa, p2.kot, p2.v*p2.masa/total_masa)

        #p1.v *= (p1.elastičnost*p2.elastičnost)
        p1.masa += p2.masa
        p1.collide_with = p2


def trk(k1, k2):
    dx = k1.x - k2.x
    dy = k1.y - k2.y
    d = math.hypot(dx, dy)

    if d <= k1.size + k2.size:
        tangent = math.atan2(dy, dx)
        k1.kot = 2 * tangent - k1.kot
        k2.kot = 2 * tangent - k2.kot
        (k1.v, k2.v) = (k2.v, k1.v)

        kot = 0.5 * math.pi + tangent
        k1.x += math.sin(kot)
        k1.y -= math.cos(kot)
        k2.x -= math.sin(kot)
        k2.y += math.cos(kot)

class OctNode:
    """Stores the data for an octree node, and spawns its children if possible"""
    def __init__(self, center, size, masses, points, ids, leaves=[]):
        self.center = center                    # center of the node's box
        self.size = size                        # maximum side length of the box
        self.children = []                      # start out assuming that the node has no children
 
        Npoints = len(points)
 
        if Npoints == 1:
            # if we're down to one point, we need to store stuff in the node
            leaves.append(self)
            self.COM = points[0]
            self.mass = masses[0]
            self.id = ids[0]
            self.g = np.zeros(2)        # at each point, we will want the gravitational field
        else:
            self.GenerateChildren(points, masses, ids, leaves)     # if we have at least 2 points in the node,
                                                             # spawn its children
 
            # now we can sum the total mass and center of mass hierarchically, visiting each point once!
            com_total = np.zeros(2) # running total for mass moments to get COM
            m_total = 0.            # running total for masses
            for c in self.children:
                m, com = c.mass, c.COM
                m_total += m
                com_total += com * m   # add the moments of each child
            self.mass = m_total
            self.COM = com_total / self.mass  
 
    def GenerateChildren(self, points, masses, ids, leaves):
        """Generates the node's children"""
        quadrant_index = (points > self.center)  #does all comparisons needed to determine points' octants
        for i in range(2): #looping over the 8 octants
            for j in range(2):
                in_quadrant = np.all(quadrant_index == np.bool_([i,j]), axis=1)
                if not np.any(in_quadrant): continue           # if no particles, don't make a node
                dx = 0.5*self.size*(np.array([i,j])-0.5)   # offset between parent and child box centers
                self.children.append(OctNode(self.center+dx,
                                                self.size/2,
                                                masses[in_quadrant],
                                                points[in_quadrant],
                                                ids[in_quadrant],
                                                leaves))

class Particle:
    def __init__(self, x, y, size, masa = 1):
        self.x = x
        self.y = y
        self.v = 0
        self.kot = 0
        self.size = size
        self.barva = (0, 0, 255)
        self.masa = masa
        self.thickness = 5
        self.upor = 1
        self.elastičnost = 0
        self.a = [0,0]

    def premik(self):
        
        
        self.x += np.cos(self.kot) * self.v
        self.y += np.sin(self.kot) * self.v
        self.v *= self.upor
        

    def pospešek(self, vector):
        (self.kot, self.v) = addVectors(self.kot, self.v, *vector)

    

    def pospešek3(self):
        a_kot = math.atan2(self.a[1], self.a[0])
        a_posp = math.hypot(self.a[0], self.a[1])
        (self.kot, self.v) = addVectors(self.kot, self.v, a_kot, a_posp)
    
    def upor(self):
        """ Slow particle down through drag """
        self.v *= self.upor
    
    def miška(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.kot = math.atan2(dy, dx)
        self.v = math.hypot(dx, dy) * 0.1
    
    def privlak(self, other):
        dx = (self.x - other.x)
        dy = (self.y - other.y)
        dist = math.hypot(dx, dy)
            
        theta = math.atan2(dy, dx)
        force = 0.2 * self.masa * other.masa / dist ** 2
        self.pospešek((theta + np.pi, force/self.masa))
        other.pospešek((theta, force/other.masa))
    
    


class Okolje:

    def __init__(self, širina, višina):
        self.širina = širina
        self.višina = višina
        self.delci = []
        self.položaji = []
        self.mase = []
        
        self.barva = (255,255,255)
        #self.mass_of_air = 0.2
        self.elastičnost = 1
        self.g = None

        self.particle_functions1 = []
        self.particle_functions2 = []
        self.function_dict = {
        'premik': (1, lambda p: p.premik()),
        'upor': (1, lambda p: p.upor()),
        'odboj': (1, lambda p: self.odboj(p)),
        'pospešek': (1, lambda p: p.pospešek(self.g)),
        'trk': (2, lambda p1, p2: trk(p1, p2)),
        "privlak": (2, lambda p1, p2: p1.privlak(p2)),
        "združi": (2, lambda p1, p2: združi(p1, p2)),
        "ohranitev_GK": (2, lambda p1, p2: združi(p1, p2))}

    def addFunctions(self, function_list):

        for func in function_list:
            (n, f) = self.function_dict.get(func, (-1, None))
            if n == 1:
                self.particle_functions1.append(f)
            elif n == 2:
                self.particle_functions2.append(f)
            else:
                print("No such function: %s" % f)

    
    def dodaj_delec(self, n=1, **kargs):
        """ Add n particles with properties given by keyword arguments """
        
        for i in range(n):
            size = kargs.get('size', random.randint(10, 20))
            masa = kargs.get('masa', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.širina - size))
            y = kargs.get('y', random.uniform(size, self.višina - size))

            delec = Particle(x, y, size, masa)
            delec.v = kargs.get('v', random.random())
            delec.kot = kargs.get('kot', random.uniform(0, math.pi*2))
            delec.barva = kargs.get('barva', (0, 0, 255))
            #particle.upor = (particle.masa/(particle.masa + self.masa_of_air)) ** particle.size

            self.delci.append(delec)

    def pospešek2(self):
        for delec in self.delci:
            a_kot = math.atan2(delec.a[1], delec.a[0])
            a_posp = math.hypot(delec.a[0], delec.a[1])
            (delec.kot, delec.v) = addVectors(delec.kot, delec.v, a_kot, a_posp)
    
    def update(self):
        #GravAccel(self.delci)
        #sez_posp = GravAccel(self.delci)
        #self.ohranitev_GK()
        GravAccel(self.delci) #ta funkcija jim že spremeni hitrost
        #self.pospešek2()
        for i, delec in enumerate(self.delci):
            for f in self.particle_functions1:
                f(delec)
            for delec2 in self.delci[i+1:]:
                for f in self.particle_functions2:
                    f(delec, delec2)
        
            
            

    def odboj(self, delec):
        if delec.x >= self.širina - delec.size and np.cos(delec.kot) >= 0:
            #delec.x = 2 * (self.širina - delec.size) - delec.x
            delec.kot = np.pi - delec.kot
            delec.v *= self.elastičnost
        elif delec.x <= delec.size and np.cos(delec.kot) <= 0:
            delec.x = 2 * delec.size - delec.x
            delec.kot = np.pi- delec.kot
            delec.v *= self.elastičnost
        if delec.y >= self.višina - delec.size and np.sin(delec.kot) >= 0:
            #delec.y = 2 * (višina - delec.size) - delec.y
            delec.kot *= -1
            delec.v *= self.elastičnost
        elif delec.y <= delec.size and np.sin(delec.kot) <= 0:
            #delec.y = 2 * delec.size - delec.y
            delec.kot *= -1
            delec.v *= self.elastičnost
     
    def najdi_delec(self, x, y):
        
        for delc in self.delci:
            if math.hypot(delc.x-x, delc.y-y) <= delc.size:
                return delc
        return None

    def ohranitev_GK(self):
        skupna_GK = np.array([0,0])
        skupna_Sila = np.array([0,0])
        for delec in self.delci:
            skupna_GK = addVectors(delec.kot, delec.v*delec.masa, *skupna_GK)
            a = np.array(delec.a)
            skupna_Sila = delec.masa*a + skupna_Sila


            #skupna_Sila = skupna_Sila + delec.a*delec.masa
            
            #skupna_Sila = skupna_Sila + delec.a*delec.masa

class Point:
    x=0
    y=0
    def __init__(self,a,b):
    	self.x=a
    	self.y=b

class Corners:
    tl = None
    tr = None
    bl = None
    br = None
    def __init__(self,w,h):
    	self.tl = Point(0,0)
    	self.tr = Point(w,0)
    	self.bl = Point(0,h)
    	self.br = Point(w,h)

class sixDOFRelativePose:
    xDist=None
    yDist=None
    zDist=None
    rotx=None
    roty=None
    rotz=None
    def __init__(self,args,f):
        self.xDist = args.x*1000 - 1500
        self.yDist = args.y*1000 - 1500
        self.zDist = args.z*1000 - 1250 + f
        self.rotx=90
        self.roty=90
        self.rotz=90
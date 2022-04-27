from DesignCSG import *
import numpy as np
import itertools

includeCL("LinAlg.cl")

def vec3(x,y,z):
	return np.array([x,y,z],dtype=float)

def normalize(v):
	if np.linalg.norm(v) < 1e-6:
		print(v)
	return v/np.linalg.norm(v)

class Triangle3:
	def __init__(self,A,B,C):
		self.A=A
		self.B=B
		self.C=C
		self.N=normalize(np.cross(C-A,B-A))

triangles = []
def addTriangle(tr):
	triangles.append(tr)

numtrs,data = readSTLData("Assets/Mesh/beto_lowpoly_flowalistik.STL")
def swapYZ(v):
	temp=v[1]
	v[1]=v[2]
	v[2]=temp
	return v

Apoints = []
Bpoints = []
Cpoints = []


for it in range(numtrs):
	A=vec3(data[it*12+3+0],data[it*12+3+1],data[it*12+3+2])
	B=vec3(data[it*12+6+0],data[it*12+6+1],data[it*12+6+2])
	C=vec3(data[it*12+9+0],data[it*12+9+1],data[it*12+9+2])
	A=swapYZ(A)
	B=swapYZ(B)
	C=swapYZ(C)
	Apoints.append(A)
	Bpoints.append(B)
	Cpoints.append(C)



minX = float("+inf")
maxX = float("-inf")
minY =float("+inf")
maxY=float("-inf")
minZ=float("+inf")
maxZ=float("-inf")

for point in itertools.chain(Apoints,Bpoints,Cpoints):
	minX = min(minX,point[0])
	maxX = max(maxX,point[0])
	minY = min(minY,point[1])
	maxY = max(maxY,point[1])
	minZ = min(minZ,point[2])
	maxZ = max(maxZ,point[2])

print(minX,maxX,minY,maxY,minZ,maxZ)

aspect = np.array([maxX-minX,maxY-minY,maxZ-minZ],dtype=float)
minaspect = np.min(aspect)
aspect/=minaspect


rescaleX = lambda x: (-1.0 + 2.0 * (x-minX)/(maxX-minX))*aspect[0]
rescaleY= lambda y: (-1.0 + 2.0 * (y-minY)/(maxY-minY))*aspect[1]
rescaleZ = lambda z: (-1.0 + 2.0 * (z-minZ)/(maxZ-minZ))*aspect[2]

rescaleVector  = lambda v: vec3(rescaleX(v[0]),rescaleY(v[1]),rescaleZ(v[2]))

for A,B,C in zip(Apoints,Bpoints,Cpoints):
	addTriangle(Triangle3(rescaleVector(A),rescaleVector(B),rescaleVector(C)))
			
data_num_triangles = [len(triangles)]
addArbitraryData("NUM_TRIANGLES",data_num_triangles)
data_triangles = []
for triangle in triangles:
	for coord in range(3):
		data_triangles.append(triangle.A[coord])
	for coord in range(3):
		data_triangles.append(triangle.B[coord])
	for coord in range(3):
		data_triangles.append(triangle.C[coord])
	for coord in range(3):
		data_triangles.append(triangle.N[coord])

addArbitraryData("TRIANGLE_DATA",data_triangles)

commit(shaders=""" 
float3 getTriangleN(int it);
float3 fragment(float3 gv, int it){
	return fabs(getTriangleN(it));
	//float d = length(gv-camera_g);
	//return f2f3(d/10.0);
	//return gv;
}
Triangle3f_t vertex(Triangle3f_t tr, int it) {return tr;}
""")
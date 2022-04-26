from DesignCSG import *

scene="""

#define MATERIAL_MATCH (SDF_EPSILON*TOLERANCE_FACTOR_MATERIAL)
#define FABS(a) (a>=0.0?a:-a)
#define VFABS(v) ((double3)(FABS(v.x),FABS(v.y),FABS(v.z)))
#define Vector3d(x,y,z) ((double3)(x,y,z))
#define RGT rgt_g
#define UPP upp_g
#define FWD fwd_g

//https://stackoverflow.com/a/4275343/5166365
float rand(float2 co){
	double i = 0;
    return fract(sin(dot(co, (float2)(12.9898, 78.233))) * 43758.5453,&i);
}

double fastBox(double3 v, double3 center, double3 halfDiameter){
	double3 _v = (double3)(FABS(v.x-center.x),FABS(v.y-center.y),FABS(v.z-center.z));
	double3 q = _v-halfDiameter;
	return T_max(q.x,T_max(q.y,q.z));
}

double grassblade(double3 v, double3 baseCenter, double3 normal){
	v=v-baseCenter;

	float h = dot(v,normal);
	double3 p = (double3)(h*normal.x,h*normal.y,h*normal.z);

	double3 r = v-p;
	float rho = r.x*r.x-r.z*r.z;
	return T_max(-h,T_max(h-1.0,rho-0.0025));

}


double wave(double x0, double z0,double x, double z, double amplitude){
	float t0 = x- x0;
	float t1 = z - z0;
	float r2 = t0*t0+t1*t1;
	return amplitude*exp(-r2);
}

double getHeight(double3 v){
	int N = 5;
	float h = 0.0;
	int ct = 0;
	for(int i=-N;i<=N;i++){
		for(int j=-N;j<=N;j++){
			float x0 = i*2.5/N;
			float z0 = j*2.5/N;
			float r = getAD(AD_RANDOM_VALUES,ct++);
			h+=wave(x0,z0,v.x,v.z,0.25*r);
		}
	}
	return h;
}

double sceneSDF(double3 v){
	float d = MAX_DISTANCE;

	int G = 31;
	float D = 5.0/(G-1);
	float xf = round(v.x/D)*D;
	float zf = round(v.z/D)*D;

	double h = getHeight(v);
	float d1 = v.y - (-2.4+h);

	double3 grassCenter = Vector3d(xf,h,zf);
	float d2 = grassblade(v,grassCenter,getNormal(grassCenter));
	
	d=T_min(d,d1);
	d=T_min(d,d2);


	return T_max(d,fastBox(v,Vector3d(0.0,0.0,0.0),Vector3d(2.5,2.5,2.5)));
}

double3 sceneMaterial(double3 gv, double3 lv, double3 n)
{

	return VFABS(n);

}

"""

np.random.seed(2022)
randomValues = []
for _ in range(256):
	randomValues.append(np.random.uniform())
addArbitraryData("RANDOM_VALUES",randomValues)

commit(scene=scene)
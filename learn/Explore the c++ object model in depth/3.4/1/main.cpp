#include <iostream>


using namespace std;

struct no_virts{
	
	int d1,d2;
	
};

class has_virts : public no_virts{
	
	public:
		has_virts(int v1,int v2,int v3){
			
			d1=v1;d2=v2;d3=v3;
		}
		virtual void foo(){};
	private:
		int d3;
};

void print(no_virts * p){
	cout << p->d1 << endl;
}

int main(int argc,char ** argv){
	
	no_virts * p = new has_virts(1,2,3);
	print(p);
	no_virts * p2 = new no_virts;
	print(p2);
	return 0;
}


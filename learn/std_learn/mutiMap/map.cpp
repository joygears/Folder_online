#include <map>
#include <iostream>

using namespace std;





int main(){
	multimap<string,int> m;
	m.insert(make_pair("ÕÅ·É", 80));
	m.insert(make_pair("ÕÔÔÆ", 70));
	m.insert(make_pair("ÕÅ·É", 40));
	m.insert(make_pair("ÕÔÔÆ", 30));

	for (multimap<string, int>::iterator it = m.begin(); it != m.end(); it++) {
		cout << (*it).first << " " << (*it).second;
	}
	
	return 0;
}
#include <algorithm>
#include <iostream>
#include <queue>
#include <stack>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct Product{string sku,name;int quantity;};
int binarySearch(const vector<Product>& a,const string& key){int l=0,r=(int)a.size()-1;while(l<=r){int m=l+(r-l)/2;if(a[m].name==key)return m;if(a[m].name<key)l=m+1;else r=m-1;}return -1;}
int main(){vector<Product> p={{"EL-01","Keyboard",12},{"EL-02","Mouse",5},{"ST-01","Notebook",30}};unordered_map<string,int> sku;for(int i=0;i<(int)p.size();i++)sku[p[i].sku]=i;cout<<"Hash lookup EL-02: "<<p[sku["EL-02"]].name<<"\\n";sort(p.begin(),p.end(),[](auto&a,auto&b){return a.name<b.name;});for(auto&x:p)cout<<x.name<<" qty="<<x.quantity<<"\\n";cout<<"Binary search Mouse index="<<binarySearch(p,"Mouse")<<"\\n";queue<string> q;q.push("Restock keyboard");q.push("Restock mouse");cout<<"FIFO: "<<q.front()<<"\\n";stack<string>s;s.push("Add keyboard");s.push("Issue mouse");cout<<"LIFO: "<<s.top()<<"\\n";}
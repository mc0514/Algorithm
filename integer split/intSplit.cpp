#include <iostream>
using namespace std;
int split(int n, int m)
{
 if (n == 1 || m == 1)
 {
  return 1;
 }
 if (n < m)
 {
  return split(n, n);
 }
 if (n == m)
 {
  return 1 + split(n, m-1);
 }
 if (n > m)
 {
  return split(n-m, m) + split(n, m-1);
 }
}

int main()
{
 int n,sum=0;
 cin>>n;
 for(int i=1;i<=n-1;i++)
  sum=sum+split(n-i,i);
  cout<<sum+1<<endl;
 return 0;
}

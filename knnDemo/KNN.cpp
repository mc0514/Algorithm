#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <cmath>
#include <cstdlib>
using namespace std;

//define the data struct
struct sample
{
  string filmname;
  string type;
  vector<double> features;
};

//define the distance to each type  
struct typeDistance

{
  string type;
  double distance;
};


//define the function to read the train data
  void readTraintData(const string &filename,vector<sample> &train)
  {
    ifstream fin(filename.c_str());
    if(!fin)
      {
	cout<<"tran data read failed!"<<endl;
	exit(1);
      }
    double d=0.00;
    string line;
    //string filmname;
    
    while(getline(fin,line))
      {
	istringstream filein(line);
	sample ts;
	filein >> ts.filmname;
	cout << "filmname: " << ts.filmname << " ";
	filein >> ts.type;
	cout << "type: " << ts.type << " ";
	while(filein >> d)
	  {
	    cout << "features: " << d << " ";
	    ts.features.push_back(d);
	  }
	cout << endl;
	train.push_back(ts);
	
	
	
      }
    fin.close();
  }

//define the function to read the test data
void readTestData(const string filename,vector<sample> &test)
{
   ifstream fin(filename.c_str());
    if(!fin)
      {
	cout<<"tran data read failed!"<<endl;
	exit(1);
      }
    double d=0.00;
    string line;
    // string filmname;
    
    while(getline(fin,line))
      {
	istringstream filein(line);
	sample ts;
	filein >> ts.filmname;
	cout << "filmname: " << ts.filmname << " ";
	ts.type="null";
	cout << "type: " << ts.type << " ";
	while(filein >> d)
	  {
	    cout << "features: " << d << " ";
	    ts.features.push_back(d);
	  }
	cout << endl;
	test.push_back(ts);
	
	
	
      }
    fin.close();
}
//calc the distance 
double getDistance(vector<double> d1,vector<double>d2)
{
  double temp=0.00;
  for(vector<double>::size_type i=0;i!=d1.size();i++)
    temp=temp+(d1[i]-d2[i])*(d1[i]-d2[i]);
  return sqrt(temp);
}

void bambooSort(vector<typeDistance> &v1)
{
  typeDistance temp;
  for(vector<typeDistance>::size_type i=0;i<v1.size();i++)
    for(vector<typeDistance>::size_type j=i;j<v1.size();j++)
      {
	if(v1[i].distance>v1[j].distance)
	  {
	    temp=v1[i];
	    v1[i]=v1[j];
	    v1[j]=temp;
	  }
      }
   cout<<"sort result:"<<endl;
   for(vector<typeDistance>::size_type i=0;i!=v1.size();i++)
     {
      
       cout<<v1[i].type<<": "<<v1[i].distance<<endl;
     }
}
void knn(vector<sample> testSample, vector<sample> trainSample, int k)
{
  vector<typeDistance> vectd;
  typeDistance td;
  int actcount=0;
  int lovecount=0;
  for(vector<sample>::size_type i=0;i!=testSample.size();i++)
    {
      for(vector<sample>::size_type j=0;j!=trainSample.size();j++)
	{
	  //cout<<"****calc the distance****"<<endl;
	  td.type=trainSample[j].type;
	  td.distance=getDistance(testSample[i].features,trainSample[j].features);
	  vectd.push_back(td);
	}
      bambooSort(vectd);
      cout<<testSample[i].filmname<<" ";
      for(vector<typeDistance>::size_type m=0;m<k;m++)
	{
	  cout<<vectd[m].type<<" ";
	  if(vectd[m].type=="action")
	    actcount++;
	  else if(vectd[m].type=="love")
	    lovecount++;
	 
	}
      cout<<endl;
      cout<<actcount<<" "<<lovecount<<endl; 
      cout<<"result is: "<<endl;
      cout<<"************************************************"<<endl;
      if(actcount>lovecount)
	cout<<testSample[i].filmname<<" "<<"action"<<endl; 
      else
       	cout<<testSample[i].filmname<<" "<<"love"<<endl;
      cout<<"************************************************"<<endl;
      
	
      
      vectd.clear();
      actcount=0;
      lovecount=0;
      
     
    }
}

int main()
{
  int k=3;
  vector<sample> train;
  vector<sample> test;
  readTraintData("tran.txt",train);
  cout<<"begin to read test data.........."<<endl;
  readTestData("test.txt",test);
  cout<<"begin to KNN processing.........."<<endl;
  knn(test,train,k);
  return 0;
}

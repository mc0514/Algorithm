#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <fstream>
#include <sstream>
#include <cassert>
#include <cmath>
#include <stdlib.h>
using namespace std;

//样例结构体，所属类型和特征向量
struct sample
{
	string type;
	vector<double> features;
};

// 类型和距离结构体，未用到
struct typeDistance
{
	string type;
	double distance;
};

bool operator < (const typeDistance& lhs, const typeDistance& rhs)
{
	return lhs.distance < rhs.distance;
}

// 读取训练样本
// 训练样本的格式是：每行代表一个样例
// 每行的第一个元素是类型名，后面的是样例的特征向量
// 例如：
/*
a    1 2 3 4 5
b    5 4 3 2 1
c    3 3 3 3 3
d    -3 -3 -3 -3 -3
a    1 2 3 4 4
b    4 4 3 2 1
c    3 3 3 2 4
d    0 0 1 1 -2
*/
void readTrain(vector<sample>& train, const string& file)
{
	ifstream fin(file.c_str());
	if (!fin)
	{
		cerr << "File error!" << endl;
		exit(1);
	}
	string line;
	double d = 0.0;
	while (getline(fin, line))
	{
		istringstream sin(line);
		sample ts;
		sin >> ts.type;
		while (sin >> d)
		{
			ts.features.push_back(d);
		}
		train.push_back(ts);
	}
	fin.close();
}

// 读取测试样本
// 每行代表一个样例
// 每一行是一个样例的特征向量
// 例如：
/*
1 2 3 2 4
2 3 4 2 1
8 7 2 3 5
-3 -2 2 4 0
-4 -4 -4 -4 -4
1 2 3 4 4
4 4 3 2 1
3 3 3 2 4
0 0 1 1 -2
*/
void readTest(vector<sample>& test, const string& file)
{
	ifstream fin(file.c_str());
	if (!fin)
	{
		cerr << "File error!" << endl;
		exit(1);
	}
	double d = 0.0;
	string line;
	while (getline(fin, line))
	{
		istringstream sin(line);
		sample ts;
		while (sin >> d)
		{
			ts.features.push_back(d);
		}
		test.push_back(ts);
	}
	fin.close();
}

// 计算欧氏距离
double euclideanDistance(const vector<double>& v1, const vector<double>& v2)
{
	assert(v1.size() == v2.size());
	double ret = 0.0;
	/*
	size_type由string类类型和vector类类型定义的类型，用以保存任意string对象或vector对象的长度，标准库类型将size_type定义为unsigned类型
	*/
	for (vector<double>::size_type i = 0; i != v1.size(); ++i)
	{
		ret += (v1[i] - v2[i]) * (v1[i] - v2[i]);
	}
	return sqrt(ret);
}

// 初始化距离矩阵
// 该矩阵是根据训练样本和测试样本而得
// 矩阵的行数为测试样本的数目，列数为训练样本的数目
// 每一行为一个测试样本到各个训练样本之间的欧式距离组成的数组
void initDistanceMatrix(vector<vector<double> >& dm, const vector<sample>& train, const vector<sample>& test)
{
	for (vector<sample>::size_type i = 0; i != test.size(); ++i)
	{
		vector<double> vd;
		for (vector<sample>::size_type j = 0; j != train.size(); ++j)
		{
			vd.push_back(euclideanDistance(test[i].features, train[j].features));
		}
		dm.push_back(vd);
	}
}

// K-近邻法的实现
// 设定不同的 k 值，给每个测试样例予以一个类型
// 距离和权重成反比
void knnProcess(vector<sample>& test, const vector<sample>& train, const vector<vector<double> >& dm, unsigned int k)
{
	for (vector<sample>::size_type i = 0; i != test.size(); ++i)
	{
		multimap<double, string> dts;  //保存与测试样本i距离最近的k个点
		for (vector<double>::size_type j = 0; j != dm[i].size(); ++j)
		{
			if (dts.size() < k) //把前面k个插入dts中
			{
				dts.insert(make_pair(dm[i][j], train[j].type)); //插入时会自动排序，按dts中的double排序，最小的排在最后
			}
			else
			{
				multimap<double, string>::iterator it = dts.end();
				--it;
				if (dm[i][j] < it->first) //把当前测试样本i到当前训练样本之间的欧氏距离与dts中最小距离比较，若更小就更新dts
				{
					dts.erase(it);
					dts.insert(make_pair(dm[i][j], train[j].type));
				}
			}
		}
		map<string, double> tds;
		string type = "";
		double weight = 0.0;
		//下面for循环主要是求出与测试样本i最邻近的k个样本点中大多数属于的类别，即将其作为测试样本点i的类别
		for (multimap<double, string>::const_iterator cit = dts.begin(); cit != dts.end(); ++cit)
		{
			// 不考虑权重的情况，在 k 个样例中只要出现就加 1
			// ++tds[cit->second];

			// 这里是考虑距离与权重的关系，距离越大权重越小
			tds[cit->second] += 1.0 / cit->first;
			if (tds[cit->second] > weight)
			{
				weight = tds[cit->second];
				type = cit->second;  //保存一下类别
			}
		}
		test[i].type = type;
	}
}

// 输出结果
// 输出的格式和训练样本的格式一样
// 每行表示一个样例，第一个元素是该样例的类型，后面是该样例的特征向量
// 例如：
/*
a    1 2 3 2 4 
b    2 3 4 2 1 
b    8 7 2 3 5 
a    -3 -2 2 4 0 
d    -4 -4 -4 -4 -4 
a    1 2 3 4 4 
b    4 4 3 2 1 
c    3 3 3 2 4 
d    0 0 1 1 -2 
*/
void writeTest(const vector<sample>& test, const string& file)
{
	ofstream fout(file.c_str());
	if (!fout)
	{
		cerr << "File error!" << endl;
		exit(1);
	}
	for (vector<sample>::size_type i = 0; i != test.size(); ++i)
	{
		fout << test[i].type << '\t';
		for (vector<double>::size_type j = 0; j != test[i].features.size(); ++j)
		{
			fout << test[i].features[j] << ' ';
		}
		fout << endl;
	}
}

// 封装
void knn(const string& file1, const string& file2, const string& file3, int k)
{
	vector<sample> train, test;
	readTrain(train, file1.c_str());
	readTest(test, file2.c_str());
	vector<vector<double> > dm;
	initDistanceMatrix(dm, train, test);
	knnProcess(test, train, dm, k);
	writeTest(test, file3.c_str());
}

// 测试
int main()
{
	knn("train.txt", "test.txt", "result.txt", 3);
	return 0;
}

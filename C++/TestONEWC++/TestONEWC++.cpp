// TestONEWC++.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <vector>
#include <stdio.h>
// 前向声明
int SumAb(int* a, int* b);
//int Search(int m);
void fun(char* w, int m);
//int main()
//{
//  
//    //int a = Search(5);
//    char a[] = "DCCAEFH";
//    fun(a, strlen(a));
//    puts(a);    
//}
int main() 
{
    //int count[128] = { 0 };char line[200];int k = 0;
    ////gets(line);
    //while (line[k] != '\0') count[line[k++]]++;
    //for (k = 0;k <= 127;k ++)
    //    if (count[k] > 0) printf("%c %dn", k, count[k]);

    /*FILE* fp; int i, k = 0, n = 0; 
    fopen_s(&fp,"d1.dat","w");
    for (i = 1;i < 4;i++) fprintf(fp, " %d", i);    
    fclose(fp);
    fopen_s(&fp,"d1.dat","r");
    fscanf_s(fp,"%d%d", &k, &n);
    printf(" %d, %d\n",k,n); 
    fclose(fp);*/

    /*int a[4][3] = { 1,2,3,4,5,6,7,8,9,10,11,12 };
    int(*ptr)[3] = a, *p = a[0];

    int w = a[1][2];

    int *A = (*ptr + 1) + 2;
    int B = *(*(a + 1) + 2);
    int C = *(*(p + 5));
    int D = *((ptr + 1)[2]);
    int *ss = *a + 1;
    int ssz = *(*a + 1);*/
   /* int a[3][4] = { 1,2,3,4,5,6,7,8,9,10,11,12 };
    int(*ptr)[4] = a, *p = a[0];
    int *A = (*ptr + 1) + 2;
    int B = *(*(a + 1) + 2);
    int C = *((ptr + 1)[2]);
    int *D = p + 1;
    int E = *(p + 8);
    int *H = *a + 1;
    int G = *(*a + 1);*/
    /*int a[2][3][2] = {1,2,3,4,5,6,7,8,9,10,11,12};
   
    int B = *(*(a + 1)[0] + 1);*/



}
int test51(int a[], int len1) {
    int b[100], i, j, k = 0;
    int max = a[0];
    for ( i = 1; i < len1; i++)
    {
        if (max<a[i])
        {
            max = a[i];
            b[k++] = i;
        }
        else if (max == a[i])
        {
            b[k++] = i;
        }        
    }
    for ( j = 0; j < k; j++)
    {
        printf("%d,%d", max, b[j]);
    }
    return max;
    
}

void fun(char* w, int m) 
{
    char s, *pl, *p2;
    pl = w;
    p2 = w + m - 1;
    while (pl < p2) {
        s = *pl++;
        *pl = *p2--;
        *p2 = s;
    }

}

//int Search(int m) 
//{
//    int t = 0, i;
//    while (t != 1) {
//        m = m + 1;
//        for (i = m - 1; i > 1;i--) {
//
//            if (m % i == 0) {
//                // 【1】                              
//            } ;
//        }
//            
//        if (i == 1)
//            t = 1;
//    }    
//    // 【2】
//}

int SumAb(int *a, int *b) {
    int c = *a + *b;
    return c;
}

// 定义一个函数来处理每个批次
template<typename T>
void ProcessBatch(const std::vector<T>& batch) {
    // 这里可以对批次进行具体的处理
    // 例如：计算总和、写入文件、发送到其他服务等
    std::cout << "Processing batch of " << batch.size() << " items." << std::endl;
}

// 分批处理函数
template<typename T>
void BatchProcess(const std::vector<T>& data, size_t batchSize) {
    if (batchSize <= 0) {
        throw std::invalid_argument("Batch size must be positive.");
    }

    const T* begin = data.data();
    const T* end = begin + data.size();

    while (begin < end) {
        const T* batchEnd = std::min(begin + batchSize, end);
        std::vector<T> batch(begin, batchEnd);
        ProcessBatch(batch);

        begin = batchEnd;
    }
}


// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件

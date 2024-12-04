#include <bits/stdc++.h>

using namespace std;


typedef struct node{
    int value;
    int* next;
}node;


class ListAdj{
    int n;
    int m;
    int neighbours;
    node list[];

    public: ListAdj() = default;

    int* neighbours(int index){
        

        node vertex = (*this).list[index]; 
        
        while (vertex.next != NULL){
            vertex.value;
        }
    }
};

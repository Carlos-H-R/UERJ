#include <bits/stdc++.h>

using namespace std;


typedef struct node{
    int value;
    int* next;
}node;


class ListAdj{
    private:
        int n;
        int m;
        int neighbours;
        node list[];

    public:

        ListAdj(int n, int m){
            this->n = n;
            this->m = m;

             
        }

    int* neighbours(int index){
        int ;

        node vertex = list[index]; 
        
        while (vertex.next != NULL){
            vertex.value;
        }
    }
};

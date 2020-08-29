#define MAX 10
// #include <stdio.h>

static void quicksort(int x[MAX],int first,int last) {
  if(first<last){
    int pivot = first;
    int i = first;
    int j  = last;

    while(i<j){
      while(x[i] <= x[pivot] && i<last) i++;
      
      while(x[j]>x[pivot]) j--;

      if(i<j){
        int temp = x[i];
        x[i] = x[j];
        x[j] = temp;
      }

      int temp = x[pivot];
      x[pivot] = x[j];
      x[j] = temp;
    }

    quicksort(x,first,j-1);
    quicksort(x,j+1,last);
  }
}

int main(int argc, char **argv) {
  int x[MAX];
  for(int i = 1;i<argc;i++) x[i-1] = argv[i][0] - '0';
  // for(int i = 0;i<argc-1;i++) printf("%d\n",x[i]);
  quicksort(x,0,argc-2);
  // printf("A:%d\n",x[0]);
  return x[0];
}
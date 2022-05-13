#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) 
{
    int m = atoi(argv[2]);
    int rands[8];
    srand(atoi(argv[1]));
    for (int i = 0; i <= 7; i++) rands[i] = rand();
    m -= rands[1] + rands[2] - rands[3] + rands[4] + rands[5] - rands[6] + rands[7];
    printf("%x\n", m);
    return 0;
}
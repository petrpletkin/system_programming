#include <stdio.h>

int main(){
    int array[10] = {0, 254, 126, 126, 126, 126, 126, 126, 126, 254};
    int sum_value = 0;
    for (int i = 0; i < 10; i++){
        if (array[i] & 128){
            sum_value += (~array[i] & 0xFF);
        }
        else sum_value += array[i];
    }
    printf("Sum: %u ", sum_value);
    return 0;

}
#include <mbed.h>

#define WAIT_TIME_MS 500
DigitalIn chA(PB_4);
DigitalIn chB(PB_5);
DigitalOut led_left(LED3);
DigitalOut led_right(LED2);

int main() {
  int A,B;
  float dim=24.5/360.0; //360 lines per inch (24.5 mm)
  float pos;
  int count=0;

  // put your setup code here, to run once:

  while(1) {

    A=chA.read();
    B=chB.read();
    if (A==B){
      count--;
      led_right=1;
      led_left=0;
    }
    else{
      count++;
      led_right=0;
      led_left=1;
    }

    printf("A=%d, B=%d\n",A,B);

    thread_sleep_for(WAIT_TIME_MS);
  }
}
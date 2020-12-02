#include "mbed.h"
#include "sensors/sensors.h"


#define WAIT_TIME_MS 80
BufferedSerial pc(USBTX, USBRX, 115200); // tx, rx

FileHandle *mbed::mbed_override_console(int fd)
{
  return &pc;
}

Nucleo_Encoder_16_bits lin_encoder(TIM3);

Sensors sensors(&lin_encoder);

int main(){

  float data;

  while(1){
    data=sensors.GetMeasureLin();
    printf("%4.2f\n",data);
    thread_sleep_for(WAIT_TIME_MS);
  }

  return 0;
}

// DigitalOut led_left(LED3);
// DigitalOut led_right(LED2);

// Nucleo_Encoder_16_bits lin_encoder(TIM3);

// int main() {
//   int32_t count;
//   float length;

//   while(1) {
//     count=lin_encoder.GetCounter();
//     length=count*25.4/360.0/4;
//     printf("%4.4f\n",length);

//     thread_sleep_for(WAIT_TIME_MS);
//   }
// }
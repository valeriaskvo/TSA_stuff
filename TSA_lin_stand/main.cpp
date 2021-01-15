#include "mbed.h"
#include "CanBus/CanBus.h"

#include "TimEncoders/Nucleo_Encoder_16_bits.h"
#include "Sensors/Sensors.h"

// #define M_PI 3.14159265358979323846

#define WAIT_TIME_MS 80
BufferedSerial pc(USBTX, USBRX, 115200); // tx, rx
FileHandle *mbed::mbed_override_console(int fd)
{
  return &pc;
}

/* Initialize the motor and linear encoders */
Nucleo_Encoder_16_bits linear_encoder_left(TIM3);
Nucleo_Encoder_16_bits linear_encoder_right(TIM4);

Sensors sensors(&linear_encoder_left, &linear_encoder_right);

CanBus can(PB_8, PB_9, 1000000, &sensors);

AnalogIn torque_sensor(PF_9);

int main()
{
  float data;
  data=4.4;


  while (1)
  {
    // // data=torque_sensor.read();
    // printf("torque: %4.4f\n",data);
    // thread_sleep_for(WAIT_TIME_MS);
  }
}
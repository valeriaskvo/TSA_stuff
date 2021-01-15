#include "mbed.h"
#include "CanBus/CanBus.h"

#include "TimEncoders/Nucleo_Encoder_16_bits.h"
#include "Sensors/Sensors.h"

// #define M_PI 3.14159265358979323846

// BufferedSerial pc(USBTX, USBRX, 115200); // tx, rx

// FileHandle *mbed::mbed_override_console(int fd)
// {
//   return &pc;
// }

/* Initialize the motor and linear encoders */
Nucleo_Encoder_16_bits linear_encoder_left(TIM3);
Nucleo_Encoder_16_bits linear_encoder_right(TIM4);

Sensors sensors(&linear_encoder_left, &linear_encoder_right);

CanBus can(PB_8, PB_9, 1000000, &sensors);

int main()

{
  while (1)
  {
  }
}
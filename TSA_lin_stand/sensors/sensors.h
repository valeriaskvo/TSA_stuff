#ifndef SENSORS_H
#define SENSORS_H
#include "mbed.h"
#include "TimEncoders/Nucleo_Encoder_16_bits.h"
    
class Sensors
{        
public :
    Sensors(Nucleo_Encoder_16_bits* lin_encoder);
    ~Sensors();
    float GetMeasureLin();
private :
    Nucleo_Encoder_16_bits* lin_encoder;        
};

#endif
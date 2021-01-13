#ifndef SENSORS_H
#define SENSORS_H
#include "mbed.h"
#include "TimEncoders/Nucleo_Encoder_16_bits.h"

enum encoder_type{
    LINEAR_ENCODER,
    ROTATIONAL_ENCODER
};

class Sensors
{        
public :
    Sensors(Nucleo_Encoder_16_bits* lin_encoder, Nucleo_Encoder_16_bits* rot_encoder);
    Sensors(Nucleo_Encoder_16_bits* encoder, encoder_type type);
    ~Sensors();
    int32_t GetMeasureLin();
    int32_t GetMeasureRot();
    int32_t GetMeasure();
private :
    Nucleo_Encoder_16_bits* lin_encoder;
    Nucleo_Encoder_16_bits* rot_encoder;
    Nucleo_Encoder_16_bits* encoder;
    encoder_type type;        
};

#endif
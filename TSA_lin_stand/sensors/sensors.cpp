#include "sensors.h"

float Sensors::GetMeasureLin(){
    return -lin_encoder->GetCounter()*25.4/(360.0*4.0);
}

Sensors::Sensors(Nucleo_Encoder_16_bits* lin_encoder):lin_encoder(lin_encoder) 
{
    
}

Sensors::~Sensors(){
    
}
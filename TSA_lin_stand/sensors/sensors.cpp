#include "sensors.h"

int32_t Sensors::GetMeasureLin(){
    return lin_encoder->GetCounter(); //*-1*25.4/(360.0*4.0);
}

int32_t Sensors::GetMeasureRot(){
    return rot_encoder->GetCounter(); //*360./(1024.*4.)
}



int32_t Sensors::GetMeasure(){
    int32_t measure;
    switch (type)
    {
    case LINEAR_ENCODER:
        lin_encoder=encoder;
        return GetMeasureLin();
        break;
    case ROTATIONAL_ENCODER:
        rot_encoder=encoder;
        return GetMeasureRot();
        break;
    
    default:
        return 0.;
        break;
    }
}

Sensors::Sensors(Nucleo_Encoder_16_bits* lin_encoder, Nucleo_Encoder_16_bits* rot_encoder):lin_encoder(lin_encoder),rot_encoder(rot_encoder) 
{
    
}

Sensors::Sensors(Nucleo_Encoder_16_bits* encoder, encoder_type type):encoder(encoder)
{
    this->type=type;
}

Sensors::~Sensors(){
    
}
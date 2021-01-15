#include "Sensors.h"

// class constructor
Sensors::Sensors(Nucleo_Encoder_16_bits *left_encoder,
                 Nucleo_Encoder_16_bits *right_encoder
                 ) : left_encoder(left_encoder),
                     right_encoder(right_encoder)
                     
{
    printf("Sensors object was constructed.\n");
}

void Sensors::resetLeftEncoder()
{
    left_encoder->ResetCounter();
}

void Sensors::resetRightEncoder()
{
    right_encoder->ResetCounter();
}

int16_t Sensors::getLeftCounts(void)
{
    return left_encoder->GetCounter();
}


int16_t Sensors::getRightCounts(void)
{
    return right_encoder->GetCounter();
}

// class destructor
Sensors::~Sensors()
{
    printf("Sensors object was destructed.\n");
}
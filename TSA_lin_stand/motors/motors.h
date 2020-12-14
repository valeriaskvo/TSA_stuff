#ifndef MOTORS_H
#define MOTORS_H
#include "mbed.h"
    
class Motors
{        
public :
    Motors();
    ~Motors();
    SetPosition(int pos);
private :
    CAN can;
    CANMessage msg_write, msg_read;        
};

#endif
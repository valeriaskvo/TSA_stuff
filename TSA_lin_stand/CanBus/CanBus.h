#ifndef CANBUS_H
#define CANBUS_H

/* Network settings */
#define txSize 8
#define rxSize 8
#define CAN_ID 1
#define CAN_MASTER_ID 0

#include <stdio.h>
#include "mbed.h"
#include "Sensors/Sensors.h"

class CanBus
{
public:
    enum
    {
        MSG_READ_DATA = 0x01,
        MSG_RESET = 0x02,
        MSG_CONFIG = 0x03,
    };

    // class constructor
    CanBus(PinName rd, PinName td, int hz, Sensors *sensors);
    // Message 
    void onMsgReceived();

    // cmd functions
    void configuration_mode(CANMessage &msg); // go to configuration mode 
    void reset_counters(CANMessage &msg); // reset counters for both encoders
    void read_encoders(CANMessage &msg); // read counters for both encoders
    void unknown_command(CANMessage &msg);

    // class destructor
    ~CanBus();

private:
    CAN can;
    CANMessage rxMsg;
    CANMessage txMsg;

    Sensors *sensors;
};

#endif
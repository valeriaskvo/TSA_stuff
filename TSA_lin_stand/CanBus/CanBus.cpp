#include "CanBus.h"
#include "mbed.h"


// class constructor
CanBus::CanBus(PinName rd, PinName td, int hz, Sensors *sensors) : can(rd, td, hz),
                                                                   sensors(sensors)
{

    NVIC_SetPriority(CAN1_RX0_IRQn, 1);
    can.filter(CAN_ID, 0xFFE00000, CANStandard, 0); //0xFFE00004
    txMsg.id = CAN_MASTER_ID;
    txMsg.len = txSize;
    rxMsg.len = rxSize;
    can.attach(callback(this, &CanBus::onMsgReceived), CAN::RxIrq);

    printf("CanBus object was constructed.\n");
}

void CanBus::onMsgReceived()
{
    if (!can.read(rxMsg))
        return;

    if (rxMsg.id == CAN_ID)
    {
        switch (rxMsg.data[0])
        {
        case MSG_READ_ENCODER:
            read_encoders(rxMsg);
            break;
        case MSG_READ_FORCE:
            read_force(rxMsg);
            break;
        case MSG_RESET:
            reset_counters(rxMsg);
            break;
        case MSG_CONFIG:
            configuration_mode(rxMsg);
            break;  
        default:
            unknown_command(rxMsg);
            break;
        }
    }
}

void CanBus::unknown_command(CANMessage &msg)
{
    txMsg.id = msg.id;
    memcpy(txMsg.data, msg.data, msg.len);
    can.write(txMsg);
}


void CanBus::reset_counters(CANMessage &msg)
{
    txMsg.id = msg.id;
    memcpy(txMsg.data, msg.data, msg.len);
    sensors-> resetLeftEncoder();
    sensors-> resetRightEncoder();
    can.write(txMsg);
    printf("Device was reseted.\n");
}


void CanBus::configuration_mode(CANMessage &msg)
{
    txMsg.id = msg.id;
    memcpy(txMsg.data, msg.data, msg.len);
    can.write(txMsg);
}


void CanBus::read_encoders(CANMessage &msg)
{
    txMsg.id = msg.id;
    txMsg.data[0] = msg.data[0];

    uint16_t leftEncoder = sensors->getLeftCounts(); 
    uint16_t rightEncoder = sensors->getRightCounts();
    
    txMsg.data[1] = 0x00;
    txMsg.data[2] = *(uint8_t *)(&leftEncoder);
    txMsg.data[3] = *((uint8_t *)(&leftEncoder) + 1);
    txMsg.data[4] = 0x00;
    txMsg.data[5] = *((uint8_t *)(&rightEncoder));
    txMsg.data[6] = *((uint8_t *)(&rightEncoder) + 1);
    txMsg.data[7] = 0x00;

    can.write(txMsg);
}

void CanBus::read_force(CANMessage &msg)
{
    txMsg.id = msg.id;
    txMsg.data[0] = msg.data[0];

    float force = sensors->getForce();
    uint8_t forceMsg[4];
    memcpy(forceMsg,&force,sizeof(force));
    
    for (int i=0;i<4;i++)
    { 
        txMsg.data[i+2] = forceMsg[i];
    }

    can.write(txMsg);
}


// class destructor
CanBus::~CanBus()
{
    printf("CanBus object was destructed.\n");
}
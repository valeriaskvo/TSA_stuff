#include "mbed.h"
#include "sensors/sensors.h"
#include <math.h>

#define WAIT_TIME_MS 5

#define TIME_STEP 30

Ticker ticker;
BufferedSerial pc(USBTX, USBRX, 115200); // tx, rx

FileHandle *mbed::mbed_override_console(int fd)
{
  return &pc;
}

CAN can(PB_8,PB_9,1000000);
Nucleo_Encoder_16_bits lin_encoder(TIM3);
Nucleo_Encoder_16_bits rot_encoder(TIM4);
Sensors sensors(&lin_encoder,&rot_encoder);
CANMessage msg_write;

// void Generate_msg(float res, int ind_1, int ind_2){
//   uint32_t floatBytes;
  
//   memcpy(&floatBytes,&res,sizeof floatBytes);
//   for (int i=ind_1; i<=ind_2;i++){
//     msg_write.data[i]=floatBytes>>8*(i-ind_1);
//   }
// }

void Generate_msg(int32_t res, int ind_1, int ind_2){
  uint32_t toBytes;
  
  memcpy(&toBytes,&res,sizeof toBytes);
  for (int i=ind_1; i<=ind_2;i++){
    msg_write.data[i]=toBytes>>8*(i-ind_1);
  }
}

int main(){
  int32_t lin_res,rot_res;
  msg_write.len=8;
  while(1){
    lin_res=sensors.GetMeasureLin();
    Generate_msg(lin_res,0,3);

    rot_res=sensors.GetMeasureRot();
    Generate_msg(rot_res,4,7);
    
    can.write(msg_write);
    // printf("%4.4f; %4.4f\n",lin_res,rot_res); 
    thread_sleep_for(WAIT_TIME_MS);
  }
}
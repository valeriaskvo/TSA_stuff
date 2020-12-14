#include "mbed.h"

#define WAIT_TIME_MS 80
BufferedSerial pc(USBTX, USBRX, 115200); // tx, rx

FileHandle *mbed::mbed_override_console(int fd)
{
  return &pc;
}

CAN can(PB_8,PB_9,1000000);

struct motor{
  CANMessage msg_write,msg_read;
  float time;
  float current;
  float speed;
  float position;
};

template <typename T>
T from_uint8_to_int(uint8_t data[],int low_ind,int high_ind){ 
  T result = 0;
  
  for (int i=high_ind;i>=low_ind;i--){
    result<<=8;
    result |= data[i];
  }
  return result;
}

void position_control(float target_position,motor * motor_1){
  int pos_msg=int(target_position*100);
  memcpy(motor_1->msg_write.data+4, &pos_msg, sizeof(pos_msg));
  motor_1->msg_write.data[0]=0xA3;
  
  can.write(motor_1->msg_write);
  can.read(motor_1->msg_read);

  motor_1->time=motor_1->time+10./1000;
  motor_1->current=int(from_uint8_to_int<int16_t>(motor_1->msg_read.data,2,3))*66./4056.;
  motor_1->speed=float(from_uint8_to_int<int16_t>(motor_1->msg_read.data,4,5));
  motor_1->position=int(from_uint8_to_int<int16_t>(motor_1->msg_read.data,6,7))*360./16383.;
  
  printf("%4.4f; %4.4f; %4.4f; %4.4f\n",motor_1->time,motor_1->current,motor_1->speed,motor_1->position);
}

int main(){
  float target_position=0.;
  motor motor_1;

  motor_1.msg_write.id=0x140+1;
  motor_1.msg_write.len=8;
  motor_1.msg_read.len=8;
  motor_1.time=0;

  while(1){
    position_control(target_position,&motor_1);
    thread_sleep_for(WAIT_TIME_MS);
  }
}
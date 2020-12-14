#include "mbed.h"
#include "sensors/sensors.h"
#include <math.h>

// #define WAIT_TIME_MS 80

#define TIME_STEP 30

Ticker ticker;
BufferedSerial pc(USBTX, USBRX, 115200); // tx, rx

FileHandle *mbed::mbed_override_console(int fd)
{
  return &pc;
}

CAN can(PB_8,PB_9,1000000);
Nucleo_Encoder_16_bits lin_encoder(TIM3);
Sensors sensors(&lin_encoder);

struct motor{
  CANMessage msg_write,msg_read;
  float time;
  float current;
  float speed;
  float position;
  float ee_position;
};
enum state_t
{
  zero,
  STATE1,
  STATE2, 
  STATE3, 
  STATE4, 
  STATE5
} state;

motor motor_1;
char buf[32] = {0};
float time_v;
int time_sent=0;
int time_int=10;

int encoder_data = 0;
uint16_t encoder_prev = 0;
uint16_t encoder_scale = 16384;
int motor_turns = 0;

template <typename T>
T from_uint8_to_int(uint8_t data[],int low_ind,int high_ind){ 
  T result = 0;
  for (int i=high_ind;i>=low_ind;i--){
    result<<=8;
    result |= data[i];
  }
  return result;
}

int multiturn_encoder(uint16_t encoder_data, uint16_t threshold = 8000)
  {
    if (encoder_prev - encoder_data >= threshold)
      motor_turns += 1;
    else if (encoder_prev - encoder_data <= -threshold)
      motor_turns += -1;

    encoder_prev = encoder_data;
    return encoder_data + (encoder_scale)*motor_turns;
  }

void position_control(float target_position,motor * motor_1){
  int pos_msg=int(target_position*100);
  memcpy(motor_1->msg_write.data+4, &pos_msg, sizeof(pos_msg));
  motor_1->msg_write.data[0]=0xA3;
  
  can.write(motor_1->msg_write);
  can.read(motor_1->msg_read);

  int16_t pos=from_uint8_to_int<int16_t>(motor_1->msg_read.data,6,7);


  motor_1->time=motor_1->time+TIME_STEP/1000.;
  motor_1->current=int(from_uint8_to_int<int16_t>(motor_1->msg_read.data,2,3))*66./4056.;
  motor_1->speed=float(from_uint8_to_int<int16_t>(motor_1->msg_read.data,4,5));
  motor_1->position=multiturn_encoder(pos)*360./16383.;
  motor_1->ee_position=sensors.GetMeasureLin();
  
  if (time_sent%time_int==0){
    printf("%4.4f; %4.4f; %4.4f; %4.4f; %4.4f; %4.4f\n",motor_1->time,target_position,motor_1->current,motor_1->speed,motor_1->position,motor_1->ee_position);
    time_sent=0;
  }
  time_sent++;

}

void initial_position(){
  float target_position=0.;
  position_control(target_position, &motor_1);
}

void trajectory_1(){
  int A=15;
  float t=15;
  float target_position=A*360.*sin(time_v*2*3.1415926/t);
  
  position_control(target_position,&motor_1);
}

void trajectory_2(){

}

void Update(){
  switch (state)
  {
  case STATE1:
    initial_position();
  case STATE2:
    trajectory_1();
  case STATE3:
    trajectory_2();

  default:
    break;
  }
  time_v=time_v+TIME_STEP/1000.;
}

int main(){
  motor_1.msg_write.id=0x140+1;
  motor_1.msg_write.len=8;
  motor_1.msg_read.len=8;
  motor_1.time=0;

  // ticker.attach(&trajectory_1, 10ms);
  
  ticker.attach(&Update, 30ms); // 25us

  state=zero;

  while(1){
    if(pc.read(buf, sizeof(buf))) {
      if(buf[0]=='q') {state = STATE1; time_v=0;}
      if(buf[0]=='w') {state = STATE2; time_v=0;}
      if(buf[0]=='e') {state = STATE3; time_v=0;}
    }
    // position_control(target_position,&motor_1);
    // thread_sleep_for(WAIT_TIME_MS);
  }
  
}
#include "mbed.h"

#define WAIT_TIME_MS 80
BufferedSerial pc(USBTX, USBRX, 115200); // tx, rx

FileHandle *mbed::mbed_override_console(int fd)
{
  return &pc;
}

CAN can(PB_8,PB_9);
CANMessage msg_write,msg_read;

int main(){
  msg_write.data[0]=0x90;
  msg_write.id=1;
  msg_write.len=8;

  msg_read.len=8;

  while(1){
    can.write(msg_write);
    can.read(msg_read);
    for (int i=0;i<8;i++){
      printf("%d, ",msg_read.id);
    }
    printf("\n");
    thread_sleep_for(WAIT_TIME_MS);
  }
}
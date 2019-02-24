#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <unistd.h>

#define ADDRESS 0x10
#define HANDSHAKE 123
#define ERROR 127

static const char *devName = "/dev/i2c-1";

int main(char** argv) {
  int file;
  if ((file = open(devName, O_RDWR)) < 0) {
    fprintf(stderr, "I2C: Failed to access %d\n", devName);
    printf("CANT OPEN BUS");
    exit(1);
  }

  if (ioctl(file, I2C_SLAVE, ADDRESS) < 0) {
    fprintf(stderr, "I2C: Failed to acquire bus access/talk to slave 0x%x\n", ADDRESS);
    printf("CANT TALK TO SLAVE");
    exit(1);
  }

  int arg;
  unsigned char cmd[16];
  int acknowledgment;
  cmd[0] = HANDSHAKE;
  if (write(file, cmd, 1) == 1) {
    usleep(1000);
    char buf[1];
    if (read(file, buf, 1) == 1)
      acknowledgment = (int) buf[0];
  }

  if (acknowledgment == ERROR) {
    printf("ACK ERROR");
    exit(1);
  }

  usleep(5000);

  cmd[0] = acknowledgment;
  if (write(file, cmd, 1) == 1) {
    usleep(1000);
    char buf[1];
    if (read(file, buf, 1) == 1)
      acknowledgment = (int) buf[0];
  }


  close(file);
  return acknowledgment == HANDSHAKE ? 0 : 1;
}

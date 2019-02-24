#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>

#define LATEST_BUILD "1.0"
#define EXPECTED_RESPONSE ">> HANDSHAKE OK <<"
#define OUTDATED_RESPONSE "!> 01 - Invalid HNDS version"

int main(int argc, char const *argv[]) {
    int serial = -1;

    serial = open("/dev/serial0", O_RDWR | O_NOCTTY | O_NDELAY); //Open in non blocking read/write mode
    if (serial == -1) {
        close(serial);
        exit(1);
    }

    struct termios options;
    tcgetattr(serial, &options);
    options.c_cflag = B230400 | CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(serial, TCIFLUSH);
    tcsetattr(serial, TCSANOW, &options);


    /* Send Handshake */
    unsigned char tx_buffer[20];
    unsigned char *p_tx_buffer;

    p_tx_buffer = &tx_buffer[0];
    *p_tx_buffer++ = '{';
    *p_tx_buffer++ = '{';
    *p_tx_buffer++ = '?';
    *p_tx_buffer++ = 'H';
    *p_tx_buffer++ = ';';
    for(int i = 0; i < strlen(LATEST_BUILD); i++) {
        *p_tx_buffer++ = LATEST_BUILD[i];
    }
    
    *p_tx_buffer++ = '}';
    *p_tx_buffer++ = '}';

    if (serial == -1) {
        close(serial);
        exit(1);
    }

    int count = write(serial, &tx_buffer[0], (p_tx_buffer - &tx_buffer[0]));
    if (count < 0) {
        printf("UART TX error\n");
    }

    usleep(5000);
    
    if (serial == -1) {
        close(serial);
        exit(1);
    }
    
    /* Read Response */
    unsigned char response[50];
    int rx_length = read(serial, (void*)response, 49);
    if (rx_length <= 0) {
        close(serial);
        exit(1);
    }
    
    int result = 1;
    response[rx_length] = '\0';
    int parse_end = rx_length - strlen(EXPECTED_RESPONSE);
    for(int i = 0; i < parse_end; i++) {
        if (response[i] == '\n') {
            if (response[i+1] == EXPECTED_RESPONSE[0]) {
                for(int j = 1; j < strlen(EXPECTED_RESPONSE); j++) {
                    if (response[i+j+1] != EXPECTED_RESPONSE[j]) {
                        close(serial);
                        exit(1);
                    }
                }
                result = 0;
            } else if (response[i+1] == OUTDATED_RESPONSE[0]) {
                for(int j = 0; j < strlen(OUTDATED_RESPONSE); j++) {
                    if (response[i+j+1] != OUTDATED_RESPONSE[j]) {
                        close(serial);
                        exit(1);
                    }
                }
                result = 2;
            }
        }
    }
    
    

    close(serial);
    
    return result;
}
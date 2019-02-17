#define BUF_SIZE 256
#define MASK 255

#define HEAD 0xA5
#define TAIL 0x5A

#define ST_WAIT_4_START 0x01
#define ST_HEAD_READ 0x02
#define ST_MODULE_READ 0x03
#define ST_LENGTH_READ 0x04
#define ST_DATA_READ 0x05
#define ST_CHECK_READ 0x06

#define ENCODER_MOTOR_GET_PARAM 0x01
#define ENCODER_MOTOR_SAVE_PARAM 0x02
#define ENCODER_MOTOR_TEST_PARAM 0x03
#define ENCODER_MOTOR_SHOW_PARAM 0x04
#define ENCODER_MOTOR_RUN_STOP 0x05
#define ENCODER_MOTOR_GET_DIFF_POS 0x06
#define ENCODER_MOTOR_RESET 0x07
#define ENCODER_MOTOR_SPEED_TIME 0x08
#define ENCODER_MOTOR_GET_SPEED 0x09
#define ENCODER_MOTOR_GET_POS 0x10
#define ENCODER_MOTOR_MOVE 0x11
#define ENCODER_MOTOR_MOVE_TO 0x12
#define ENCODER_MOTOR_DEBUG_STR 0xCC
#define ENCODER_MOTOR_ACKNOWLEDGE 0xFF

#ifndef ADDRESS
    #define ADDRESS 0x9
#endif

uint8_t buffer[BUF_SIZE];
uint8_t state = ST_WAIT_4_START;
uint32_t comms_in = 0;
uint32_t comms_out = 0;

uint32_t comms_length = 0;
uint8_t *comms_data = NULL;

uint32_t comms_length_read = 0;
uint32_t comms_data_pos = 0;

void request(byte *writeData, byte *readData, int wlen, int rlen);
uint8_t pushStr(uint8_t *str, uint32_t length);
uint8_t pushByte(uint8_t ch);
uint8_t getData(uint8_t *buf, uint32_t size);
uint8_t getByte(uint8_t *ch);
uint8_t send();
uint8_t calculateLRC(uint8_t *data, uint32_t length);
uint32_t pack(uint8_t * buf, uint32_t bufSize, uint8_t module, uint8_t * data, uint32_t length);

void request(byte *writeData, byte *readData, int wlen, int rlen)
{
    uint8_t rxByte;
    uint8_t index = 0;

    Wire.beginTransmission(ADDRESS);

    Wire.write(writeData, wlen);

    Wire.endTransmission();
    delayMicroseconds(2);
    Wire.requestFrom((int)ADDRESS, (int)rlen);
    delayMicroseconds(2);
    while (Wire.available())
    {
        rxByte = Wire.read();

        readData[index] = rxByte;
        index++;
    }
}

uint8_t pushStr(uint8_t *str, uint32_t length)
{
    if (length > ((comms_in + BUF_SIZE - comms_out - 1) & MASK))
    {
        return 0;
    }
    else
    {
        for (int i = 0; i < length; ++i)
        {
            pushByte(str[i]);
        }
    }
}

uint8_t pushByte(uint8_t ch)
{
    if (((comms_in + 1) & MASK) != comms_out)
    {
        buffer[comms_in] = ch;
        ++comms_in;
        comms_in &= MASK;
        return 1;
    }
    return 0;
}

uint8_t getData(uint8_t *buf, uint32_t size)
{
    int copySize = (size > comms_length) ? comms_length : size;
    if ((NULL != comms_data) && (NULL != buf))
    {
        memcpy(buf, comms_data, copySize);
        free(comms_data);
        comms_data = NULL;
        comms_length = 0;
        return copySize;
    }
    return 0;
}

uint8_t getByte(uint8_t *ch)
{
    if (comms_in != comms_out)
    {
        *ch = buffer[comms_out];
        ++comms_out;
        comms_out &= MASK;
        return 1;
    }
    return 0;
}

uint8_t send()
{
    uint8_t ch = 0;
    while (getByte(&ch))
        switch (state)
        {
        case ST_WAIT_4_START:
            if (HEAD == ch)
            {
                state = ST_HEAD_READ;
            }
            break;
        case ST_HEAD_READ:
            state = ST_MODULE_READ;
            break;
        case ST_MODULE_READ:
            //  read 4 bytes as "length"
            *(((uint8_t *)&comms_length) + comms_length_read) = ch;
            if (4 == ++comms_length_read)
            {
                comms_length_read = 0;
                state = ST_LENGTH_READ;
            }
            break;
        case ST_LENGTH_READ:
            //  alloc space for data
            if (0 == comms_data_pos)
            {
                if (comms_length > 255)
                {
                    state = ST_WAIT_4_START;
                    comms_data_pos = 0;
                    comms_length_read = 0;
                    comms_length = 0;
                    break;
                }
                comms_data = (uint8_t *)malloc(comms_length + 1);
                if (NULL == comms_data)
                {
                    state = ST_WAIT_4_START;
                    comms_data_pos = 0;
                    comms_length_read = 0;
                    comms_length = 0;
                    break;
                }
            }
            //  read data
            comms_data[comms_data_pos] = ch;
            ++comms_data_pos;
            if (comms_data_pos == comms_length)
            {
                comms_data_pos = 0;
                state = ST_DATA_READ;
            }
            break;
        case ST_DATA_READ:
            if (ch != calculateLRC(comms_data, comms_length))
            {
                state = ST_WAIT_4_START;
                if (NULL != comms_data)
                {
                    free(comms_data);
                    comms_data = NULL;
                }
                comms_data_pos = 0;
                comms_length_read = 0;
                comms_length = 0;
            }
            else
            {
                state = ST_CHECK_READ;
            }
            break;
        case ST_CHECK_READ:
            if (TAIL != ch)
            {
                if (NULL != comms_data)
                {
                    free(comms_data);
                    comms_data = NULL;
                }
                comms_length = 0;
            }
            state = ST_WAIT_4_START;
            comms_data_pos = 0;
            comms_length_read = 0;
            break;
        default:
            break;
        }
    return state;
}

uint32_t pack(uint8_t * buf, uint32_t bufSize, uint8_t module, uint8_t * data, uint32_t length) {
  uint32_t i = 0;

  buf[i++] = HEAD;
  buf[i++] = module;

  //  pack length
  *((uint32_t *)(buf + i)) = length;
  i+= 4;

  //  pack data
  for(uint32_t j = 0; j < length; ++j) {
    buf[i++] = data[j];
  }

  buf[i++] = calculateLRC(data, length);

  buf[i++] = TAIL;

  return i > bufSize ? 0 : i;
}

uint8_t calculateLRC(uint8_t *data, uint32_t length)
{
    uint8_t LRC = 0;
    for (uint32_t i = 0; i < length; ++i)
    {
        LRC ^= data[i];
    }
    return LRC;
}
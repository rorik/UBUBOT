#!/usr/bin/python3
from Pin.Pin import Pin, PinType
import configparser


def init_pins():
    pins = [None] * 40
    for i in range(0, len(pins)):
        pins[i] = Pin(i + 1)
        pins[i].pin_type = PinType.GPIO
        pins[i].name = 'GPIO '
    for i in [5, 8, 13, 19, 24, 29, 33, 38]:
        pins[i].name = 'Ground'
        pins[i].pin_type = PinType.GND
    for i in [0, 16]:
        pins[i].name = '3.3v'
        pins[i].pin_type = PinType.V3
    for i in [1, 3]:
        pins[i].name = '5v'
        pins[i].pin_type = PinType.V5
    for i in [26, 27]:
        pins[i].pin_type = PinType.I2C
    pins[2].name += '3'
    pins[4].name += '4'
    pins[6].name += '5'
    pins[7].name += '14'
    pins[9].name += '15'
    pins[10].name += '17'
    pins[11].name += '18'
    pins[12].name += '27'
    pins[14].name += '22'
    pins[15].name += '23'
    pins[17].name += '25'
    pins[18].name += '10'
    pins[20].name += '9'
    pins[21].name += '25'
    pins[22].name += '11'
    pins[23].name += '8'
    pins[25].name += '7'
    pins[26].name = 'ID_SD'
    pins[27].name = 'ID_SC'
    pins[28].name += '5'
    pins[30].name += '6'
    pins[31].name += '12'
    pins[32].name += '13'
    pins[34].name += '19'
    pins[35].name += '16'
    pins[36].name += '26'
    pins[37].name += '20'
    pins[39].name += '21'
    return pins


def init_config(path):
    config = {}
    configFile = configparser.ConfigParser()
    try:
        configFile.read(path)
        with open(path) as f:
            configFile.read_file(f)
    except IOError:
        print("File at \"", path, "\" not found.", sep="")
        exit(404)
    try:
        ratio = float(configFile.get("Main", "LeftToRightRatio"))
        config['C_Enabled'] = configFile.get("Main", "CamEnabled") == "true"
        config['MOT_DRF'] = int(configFile.get("Main", "ServoDriverFrequency"))
        if not 1 <= config['MOT_DRF'] <= 10000:
            raise configparser.ParsingError("Frequency out of bounds ({:d} OOR [1,10000])".format(config['MOT_DRF']))
        config['BUS'] = int(configFile.get("Main", "i2cBus"))
        if not 0 <= config['BUS'] <= 2:
            raise configparser.ParsingError("Bus out of bounds ({:d} OOR [0,2])".format(config['BUS']))

        config['US_Enabled'] = configFile.get("Sensors", "USEnabled") == "true"
        config['US_Rem_Dis'] = configFile.get("Sensors", "USRemoteDisable") == "true"
        config['US_Rem_IP'] = configFile.get("Sensors", "USRemoteInterruptPin") == "true"
        config['US_Method'] = int(configFile.get("Sensors", "USInterruptMethod"))
        if not 0 <= config['US_Method'] <= 3:
            raise configparser.ParsingError("Method {:d} not recognized".format(config['US_Method']))
        config['US_Lock'] = configFile.get("Sensors", "USLock") == "true"
        config['US_Distance'] = int(configFile.get("Sensors", "USDistanceInterrupt"))
        if config['US_Distance'] < 0:
            raise configparser.ParsingError("Distance cannot be negative ({:d} < 0)".format(config['US_Distance']))
        if config['US_Method'] == 2 and config['US_Distance'] > 29:
            raise configparser.ParsingError("Threshold out of bounds ({:d} OOR [0,29])".format(config['US_Distance']))
        config['US_Rate'] = int(configFile.get("Sensors", "USPollingRate"))
        if config['US_Method'] != 3 and not 1 <= config['US_Rate'] <= 100:
            raise configparser.ParsingError("Polling rate out of bounds ({:d} OOR [1,100])".format(config['US_Rate']))
        config['US_Delay'] = float(configFile.get("Sensors", "USDelay"))
        if config['US_Method'] != 3 and config['US_Delay'] <= 0:
            raise configparser.ParsingError("Delay must be positive number ({:d} <= 0)".format(config['US_Delay']))

        config['Interrupt'] = int(configFile.get("Pins", "InterruptPin"))
        config['MOT_LBF'], config['MOT_LBB'] = configFile.get("Pins", "LeftBack").split(",")
        config['MOT_RBF'], config['MOT_RBB'] = configFile.get("Pins", "RightBack").split(",")
        config['US_LE'] = int(configFile.get("Pins", "USLeftEcho"))
        config['US_RE'] = int(configFile.get("Pins", "USRightEcho"))
        config['US_FE'] = int(configFile.get("Pins", "USFrontEcho"))
        config['US_LT'] = int(configFile.get("Pins", "USLeftTrigger"))
        config['US_RT'] = int(configFile.get("Pins", "USRightTrigger"))
        config['US_FT'] = int(configFile.get("Pins", "USFrontTrigger"))
        config['MOT_DRL'] = int(configFile.get("Pins", "ServoDriverLeft"))
        config['MOT_DRR'] = int(configFile.get("Pins", "ServoDriverRight"))
        config['MOT_LBF'] = int(config['MOT_LBF'])
        config['MOT_LBB'] = int(config['MOT_LBB'])
        config['MOT_RBF'] = int(config['MOT_RBF'])
        config['MOT_RBB'] = int(config['MOT_RBB'])
        if ratio <= 1:
            config['MOT_LBR'] = ratio
            config['MOT_RBR'] = 1
        else:
            config['MOT_LBR'] = 1
            config['MOT_RBR'] = 1 / ratio
    except configparser.Error as error:
        print("Config file {} contains errors.".format(path))
        print(error)
        exit(408)
    return config

#!/usr/bin/python3

# Fuel Cell Data Logger

# Copyright (C) 2016  Simon Howroyd

#############################################################################

import time
import serial

class Controller():
    def __init__(self):
        self.start = 'STX'
        self.end = 'ETX'
        self.__raw_frame = ''
        self.__my_frame = {
            'timestamp' : '0',
            'RedLed' : 'on',
            'GrnLed' : 'on',
            'CartPwr' : 'on',
            'StkA' : 'dis',
            'StkB' : 'dis',
            'McuWake' : 'en',
            'HydStkA' : 'dis',
            'HydStkB' : 'dis',
            'TempStkA' : False,
            'TempStkB' : False,
            'Fan1' : '100',
            'Fan2' : '0',
            'AdcTrigger' : '100',
            'PurgeValve' : '0',
            'InletValve' : '0',
            'OutDaq' : 'en',  # Disable controller
            'InDaq' : 'en',
            'DataDump' : '500',
            'VStkA1' : False,
            'IStkA1' : False,
            'VStkA2' : False,
            'IStkA2' : False,
            'VStkA3' : False,
            'IStkA3' : False,
            'VStkB1' : False,
            'IStkB1' : False,
            'VStkB2' : False,
            'IStkB2' : False,
            'VStkB3' : False,
            'IStkB3' : False,
            'VBatIn' : False,
            'IBatIn' : False,
            'VBatOut' : False,
            'IBatOut' : False,
            'VLoad' : False,
            'ILoad' : False,
            }

    def get_frame(self):
        x = self.__my_frame
        out = self.start
        out += ',' + str(x['timestamp'])
        out += ',' + str(x['RedLed'])
        out += ',' + str(x['GrnLed'])
        out += ',' + str(x['CartPwr'])
        out += ',' + str(x['StkA'])
        out += ',' + str(x['StkB'])
        out += ',' + str(x['McuWake'])
        out += ',' + str(x['HydStkA'])
        out += ',' + str(x['HydStkB'])
        out += ',' + str(x['TempStkA'])
        out += ',' + str(x['TempStkB'])
        out += ',' + str(x['Fan1'])
        out += ',' + str(x['Fan2'])
        out += ',' + str(x['AdcTrigger'])
        out += ',' + str(x['PurgeValve'])
        out += ',' + str(x['InletValve'])
        out += ',' + str(x['OutDaq'])
        out += ',' + str(x['InDaq'])
        out += ',' + str(x['DataDump'])
        out += ',' + str(x['VStkA1'])
        out += ',' + str(x['IStkA1'])
        out += ',' + str(x['VStkA2'])
        out += ',' + str(x['IStkA2'])
        out += ',' + str(x['VStkA3'])
        out += ',' + str(x['IStkA3'])
        out += ',' + str(x['VStkB1'])
        out += ',' + str(x['IStkB1'])
        out += ',' + str(x['VStkB2'])
        out += ',' + str(x['IStkB2'])
        out += ',' + str(x['VStkB3'])
        out += ',' + str(x['IStkB3'])
        out += ',' + str(x['VBatIn'])
        out += ',' + str(x['IBatIn'])
        out += ',' + str(x['VBatOut'])
        out += ',' + str(x['IBatOut'])
        out += ',' + str(x['VLoad'])
        out += ',' + str(x['ILoad'])
        return out + ',' + self.end
        
        
    def parse_frame(self, __port):
        raw = str(__port.read(500))
        __full_frame = False
#        print(raw)        
        try:
            ptr = raw.index(self.start)
            self.__raw_frame = raw[ptr:]

            ptr = self.__raw_frame.index(self.end) + 3
            self.__raw_frame = self.__raw_frame[:ptr]
            __full_frame = True
        except ValueError:
            # STX not found
            try:
                print("Compiling")
                ptr = raw.index(self.end) + 3
                self.__raw_frame += raw[:ptr]
                __full_frame = True

            except ValueError:
                # No identifiers found, middle of frame
                self.__raw_frame += raw


            
        if __full_frame:

            __split_frame = self.__raw_frame.split(',')
            __full_frame = False
#            print("f_len = " + str(len(__split_frame)))
#            print(__split_frame)
            if len(__split_frame) is 42:
                # Full frame received!
                self.__my_frame['timestamp'] = __split_frame[1]
                self.__my_frame['RedLed'] = __split_frame[2]
                self.__my_frame['GrnLed'] = __split_frame[3]
                self.__my_frame['CartPwr'] = __split_frame[4]
                self.__my_frame['StkA'] = __split_frame[5]
                self.__my_frame['StkB'] = __split_frame[6]
                self.__my_frame['McuWake'] = __split_frame[7]
                self.__my_frame['HydStkA'] = __split_frame[8]
                self.__my_frame['HydStkB'] = __split_frame[9]
                self.__my_frame['TempStkB'] = __split_frame[10]
                self.__my_frame['TempStkA'] = __split_frame[11]
                self.__my_frame['Fan1'] = __split_frame[12]
                self.__my_frame['Fan2'] = __split_frame[13]
#                self.__my_frame['AdcTrigger'] = __split_frame[14]
#                self.__my_frame['PurgeValve'] = __split_frame[15]
#                self.__my_frame['InletValve'] = __split_frame[16]
#                self.__my_frame['OutDaq'] = __split_frame[17]
#                self.__my_frame['InDaq'] = __split_frame[18]
                self.__my_frame['DataDump'] = __split_frame[14]
                self.__my_frame['VStkA1'] = __split_frame[15]
                self.__my_frame['IStkA1'] = __split_frame[16]
                self.__my_frame['VStkA2'] = __split_frame[17]
                self.__my_frame['IStkA2'] = __split_frame[18]
                self.__my_frame['VStkA3'] = __split_frame[19]
                self.__my_frame['IStkA3'] = __split_frame[20]
                self.__my_frame['VStkB1'] = __split_frame[21]
                self.__my_frame['IStkB1'] = __split_frame[22]
                self.__my_frame['VStkB2'] = __split_frame[23]
                self.__my_frame['IStkB2'] = __split_frame[24]
                self.__my_frame['VStkB3'] = __split_frame[25]
                self.__my_frame['IStkB3'] = __split_frame[26]
                self.__my_frame['VBatIn'] = __split_frame[27]
                self.__my_frame['IBatIn'] = __split_frame[28]
                self.__my_frame['VBatOut'] = __split_frame[29]
                self.__my_frame['IBatOut'] = __split_frame[30]
                self.__my_frame['VLoad'] = __split_frame[31]
                self.__my_frame['ILoad'] = __split_frame[32]
                return True
            else:
                # Corrupt frame
                self.__raw_frame = ''
        return False

a=Controller()
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
log = open(("/media/usb/" + time.strftime("%y%m%d-%H%M%S") + "-AlexIE-" + ".tsv"), 'w')

# Main run function
if __name__ == "__main__":
    print("Datalogger 2016")

    
    while True:
        out = 'DataDump 100\n\r'
        port.write(out.encode())
#        print(out[:-2])
#        out = 'OutDaq dis\n\r'
#        port.write(out.encode())
#        print(out[:-2])
        print("Starting...")
        time_start = time.time()

        while time.time()-time_start < 5:
            if a.parse_frame(port):
                print(a.get_frame())
                log.write(a.get_frame())
                log.write("\n")
                time_start = time.time()


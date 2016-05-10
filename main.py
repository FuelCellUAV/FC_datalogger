#!/usr/bin/python3

# Fuel Cell Data Logger

# Copyright (C) 2016  Simon Howroyd, Alex Thirkell

#############################################################################
import argparse, sys, time, select, os
import serial
import RPi.GPIO as GPIO
from adc import adcpi
from mfc import mfc
from tdiLoadbank import loadbank
from scheduler import scheduler
from quick2wire.i2c import I2CMaster, reading

# Inspect user input arguments
def _parse_commandline():
    # Define the parser
    parser = argparse.ArgumentParser(description='Fuel Cell Datalogger Simon Howroyd 2016')
    
    # Define aguments
    parser.add_argument('--adc', action="store_true", help='Use ADCPI')
    parser.add_argument('--load', action="store_true", help='Use Loadbank')
    parser.add_argument('--quiet', action="store_true", help='Nothing on screen')
    parser.add_argument('--profile', type=str, default='', help='Name of flight profile file')
    parser.add_argument('--mfc', action="store_true", help='Use mass flow controller')

    # Return what was argued
    return parser.parse_args()

class Controller():
    def __init__(self):
        self.start = 'STX'
        self.end = 'ETX'
        self.__raw_frame = ''
        self.__parsed_frame = ''
#        self.__raw_frame = 'STX,1461803,0,0,0,0,0,1,1,1,0,1,0,100000,100,0,0,en,en,100000,100000,0,20350,20030,0,0,0,100,976,0,750,0,750,0,976,0,776,0,ETX,STX,1463803,0,0,0,0,0,0,1,1,0,1,0,100000,100,0,0,en,en,100000,0,0,20350,20030,0,0,0,100,976,0,750,0,750,0,976,0,776,0,ETX,STX,1465803,0,0,0,0,0,0,1,1,0,1,0,100000,100,0,0,en,en,100000,0,0,20350,20030,0,0,0,100,976,0,750,0,750,0,976,0,776,0,ETX'

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
            'TempStkA' : '0',
            'TempStkB' : '0',
            'Fan1' : '100',
            'Fan2' : '0',
            'AdcTrigger' : '100',
            'PurgeValve' : '0',
            'InletValve' : '0',
            'OutDaq' : 'en',  # Disable controller
            'InDaq' : 'en',
            'DataDump' : '500',
            'VStkA1' : '0',
            'IStkA1' : '0',
            'VStkA2' : '0',
            'IStkA2' : '0',
            'VStkA3' : '0',
            'IStkA3' : '0',
            'VStkB1' : '0',
            'IStkB1' : '0',
            'VStkB2' : '0',
            'IStkB2' : '0',
            'VStkB3' : '0',
            'IStkB3' : '0',
            'VBatIn' : '0',
            'IBatIn' : '0',
            'VBatOut' : '0',
            'IBatOut' : '0',
            'VLoad' : '0',
            'ILoad' : '0',
            }

    def get_parsed_frame(self):
        return self.__parsed_frame

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
        raw = self.__raw_frame + ((__port.read(10))).decode('UTF-8','ignore')
#        print(len(raw))
        __full_frame = False
       
        try:
            ptr = raw.index(self.start)
            raw = raw[ptr:].lstrip(',')

            if raw.index(self.end):
                __full_frame = True
            else: self.__raw_frame = raw

        except ValueError:
            self.__raw_frame = raw
            return False

        if __full_frame:
            ptr = raw.index(self.end) + 3
            __this_frame = raw[:ptr].rstrip(',')

            self.__raw_frame = raw[ptr:]

#            __this_frame = __this_frame.lstrip(',').rstrip(',')
            __this_frame = __this_frame.split(',')
            __full_frame = False
#            print(__this_frame)
            if len(__this_frame) is 42:
                self.__parsed_frame = raw[:ptr].rstrip(',')
                # Full frame received!
                self.__my_frame['timestamp'] = (__this_frame[1])
                self.__my_frame['RedLed']    = (__this_frame[2])
                self.__my_frame['GrnLed']    = (__this_frame[3])
                self.__my_frame['CartPwr']   = (__this_frame[4])
                self.__my_frame['StkA']      = (__this_frame[5])
                self.__my_frame['StkB']      = (__this_frame[6])
                self.__my_frame['McuWake']   = (__this_frame[7])
                self.__my_frame['HydStkA']   = (__this_frame[8])
                self.__my_frame['HydStkB']   = (__this_frame[9])
                self.__my_frame['TempStkB']  = (__this_frame[10])
                self.__my_frame['TempStkA']  = (__this_frame[11])
                self.__my_frame['Fan1']      = (__this_frame[12])
                self.__my_frame['Fan2']      = (__this_frame[13])
                self.__my_frame['DataDump']  = (__this_frame[14])
                self.__my_frame['VStkA1']    = (__this_frame[15])
                self.__my_frame['IStkA1']    = (__this_frame[16])
                self.__my_frame['VStkA2']    = (__this_frame[17])
                self.__my_frame['IStkA2']    = (__this_frame[18])
                self.__my_frame['VStkA3']    = (__this_frame[19])
                self.__my_frame['IStkA3']    = (__this_frame[20])
                self.__my_frame['VStkB1']    = (__this_frame[21])
                self.__my_frame['IStkB1']    = (__this_frame[22])
                self.__my_frame['VStkB2']    = (__this_frame[23])
                self.__my_frame['IStkB2']    = (__this_frame[24])
                self.__my_frame['VStkB3']    = (__this_frame[25])
                self.__my_frame['IStkB3']    = (__this_frame[26])
                self.__my_frame['VBatIn']    = (__this_frame[27])
                self.__my_frame['IBatIn']    = (__this_frame[28])
                self.__my_frame['VBatOut']   = (__this_frame[29])
                self.__my_frame['IBatOut']   = (__this_frame[30])
                self.__my_frame['VLoad']     = (__this_frame[31])
                self.__my_frame['ILoad']     = (__this_frame[32])
                return True

        return False

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23,0)

a=Controller()
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
try:
    log = open(("/media/usb/" + time.strftime("%y%m%d-%H%M%S") + "-AlexIE-" + ".tsv"), 'w')
except PermissionError:
    log = open(("/home/pi/FC_datalogger/" + time.strftime("%y%m%d-%H%M%S") + "-AlexIE-" + ".tsv"), 'w')

def get_i2c(address):
        try:
            # Using the I2C databus...
            with I2CMaster(1) as master:
                
                # Read two bytes of data
                msb, lsb = master.transaction(reading(address, 2))[0]
                
                # Assemble the two bytes into a 16bit integer
                temperature = ((( msb * 256 ) + lsb) >> 4 ) /10.0
                
                # Return the value
                return temperature

        # If I2C error return -1
        except IOError:
            return -1

# Method to get Current
def get_current(adc, channel):
        # Get current and calibrate
        current = abs(adc.get(channel) * 1000 / 6.89) * 1.075
        if current > 1000.0: current = 0.0 #TODO
        
        # Sensor only valid above a certain value
#        if current < 0.475:  # TODO can this be improved?
#            current = 0  # Account for opamp validity
            
        return current

    # method to get Voltage
def get_voltage(adc, channel):
        voltage = abs(adc.get(channel) * 1000.0 / 60.7)
        if voltage > 1000.0: voltage = 0.0 #TODO
        return voltage


# Main run function
if __name__ == "__main__":
    try:
        args = _parse_commandline()

        if args.mfc: Mfc = mfc.mfc()
        if args.load:
            load = loadbank.TdiLoadbank('158.125.152.225', 10001, 'fuelcell')
            if load.connect() == 0:
                load = ''
            else:
                load.zero()
                time.sleep(0.2)
                load.mode = 'CURRENT'
                time.sleep(0.2)
                load.range = '4'
                time.sleep(0.2)
                load.current_limit = '60.0'
                time.sleep(0.2)
                load.voltage_limit = '35.0'
                time.sleep(0.2)
                load.voltage_minimum = '5.0'
        else: load = ''

        if args.profile:
            profile = scheduler.Scheduler(args.profile)
            
            # If a loadbank is connected then define this as the output
            if load:
                output = "loadbank"
        else:
            profile = ''

        if args.adc:
            adc1 = adcpi.MCP3424(0x6E)
            adc2 = adcpi.MCP3424(0x6F)

        if not args.quiet: print("Datalogger 2016")

#    Mfc = mfc.mfc()
    
        while True:
            out = 'DataDump 100\n\r'
            port.write(out.encode())

            if not args.quiet: print("Restarting...")
            time_start = time.time()

            GPIO.output(23,1)

            while time.time()-time_start < 5:
                if a.parse_frame(port):
                    log.write(a.get_parsed_frame())
                    if not args.quiet:
                        print(a.get_frame(),end='')

                    if args.mfc:
                        log.write(',,')
                        log.write(str(Mfc.get(get_i2c, 0x2C)))
                        if not args.quiet:
                            print(',,',end='')
                            print(str(Mfc.get(get_i2c, 0x2C)),end='')

                    if profile:
                        setpoint = profile.run()
                        if "loadbank" in output and load:
                            if setpoint >= 0:
                                load.load = True
                                mode = load.mode
                                if "VOLTAGE" in mode:
                                    load.voltage_constant = str(setpoint)
                                elif "CURRENT" in mode:
                                    load.current_constant = str(setpoint)
                                elif "POWER" in mode:
                                    load.power_constant = str(setpoint)
                            else:
                                load.load = False

                    if load:
                        load.update()
                        if not args.quiet:
                            print(',,',end='')
                            print(str(load.mode.split()[0]),end='')
                            print(',',end='')
                            print(str(load.mode.split()[1]),end='')
                            print(',',end='')
                            print(str(load.voltage),end='')
                            print(',',end='')
                            print(str(load.current),end='')
                            print(',',end='')
                            print(str(load.power),end='')

                        log.write(',,')
                        log.write(str(load.mode.split()[0] + load.mode.split()[1]))
                        log.write(',')
                        log.write(str(load.voltage))
                        log.write(',')
                        log.write(str(load.current))
                        log.write(',')
                        log.write(str(load.power))

                    if args.adc:
                        data = [get_voltage(adc1, 0),
                                get_voltage(adc1, 1),
                                get_voltage(adc1, 2),
                                get_current(adc2, 1),
                                get_current(adc2, 2),
                                get_current(adc2, 3)]
                        log.write(',,')
                        for x in range(0,len(data)):
                            log.write(str(data[x]))
                            log.write(',')

                        if not args.quiet:
                            print(',,',end='')
                            for x in range(0,len(data)):
                                print(str(round(data[x],2)),end='')
                                print(',',end='')

                    print('\n',end='')
                    log.write("\n")
                    os.system("sync")
                    time_start = time.time()
    except:
        os.system("sync")
        GPIO.output(23,0)
        GPIO.cleanup()
        sys.exit()


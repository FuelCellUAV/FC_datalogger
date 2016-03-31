#!/usr/bin/python3

# Fuel Cell Data Logger

# Copyright (C) 2016  Simon Howroyd

#############################################################################

import time

class Controller():
    def __init__(self):
        self.__my_frame = {
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
            'OutDaq' : 'en',
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
        out = 'STX,' + str(time.time())
        out = out + ',' + str(x['RedLed'])
        out = out + ',' + str(x['GrnLed'])
        out = out + ',' + str(x['CartPwr'])
        out = out + ',' + str(x['StkA'])
        out = out + ',' + str(x['StkB'])
        out = out + ',' + str(x['McuWake'])
        out = out + ',' + str(x['HydStkA'])
        out = out + ',' + str(x['HydStkB'])
        out = out + ',' + str(x['TempStkA'])
        out = out + ',' + str(x['TempStkB'])
        out = out + ',' + str(x['Fan1'])
        out = out + ',' + str(x['Fan2'])
        out = out + ',' + str(x['AdcTrigger'])
        out = out + ',' + str(x['PurgeValve'])
        out = out + ',' + str(x['InletValve'])
        out = out + ',' + str(x['OutDaq'])
        out = out + ',' + str(x['InDaq'])
        out = out + ',' + str(x['DataDump'])
        out = out + ',' + str(x['VStkA1'])
        out = out + ',' + str(x['IStkA1'])
        out = out + ',' + str(x['VStkA2'])
        out = out + ',' + str(x['IStkA2'])
        out = out + ',' + str(x['VStkA3'])
        out = out + ',' + str(x['IStkA3'])
        out = out + ',' + str(x['VStkB1'])
        out = out + ',' + str(x['IStkB1'])
        out = out + ',' + str(x['VStkB2'])
        out = out + ',' + str(x['IStkB2'])
        out = out + ',' + str(x['VStkB3'])
        out = out + ',' + str(x['IStkB3'])
        out = out + ',' + str(x['VBatIn'])
        out = out + ',' + str(x['IBatIn'])
        out = out + ',' + str(x['VBatOut'])
        out = out + ',' + str(x['IBatOut'])
        out = out + ',' + str(x['VLoad'])
        out = out + ',' + str(x['ILoad'])
        return out + ',ETX,'

a=Controller()

# Main run function
if __name__ == "__main__":
    print(a.get_frame())


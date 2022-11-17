import spidev
import time
import RPi.GPIO as GPIO
import numpy as np
import jetFunctions as jf

jf.initSpiAdc()
jf.initStepMotorGpio()
try:
    type = input("pressure, motor or leave blank > ")
    msr_len = 500
    delta_len = 5
    msr = []

    if (type == "pressure"):
        for i in range(500):
            dat = jf.getAdc()
            print(dat)
            msr.append(dat)

        jf.save(msr, 0, type)

    elif (type == "motor"):
        steps = int(input("Steps > "))

        if (steps > 0):
            jf.stepForward(steps)
        else:
            jf.stepBackward(steps)
        len = int(input("movement in mm > "))
        filename = 'jet-data-cal-motor{}.txt'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

        with open(filename, "w") as outfile:
            outfile.write('- Jet Lab\n')
            outfile.write('- Date: {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            outfile.write('- Step: {} motor steps\n'.format(steps))
            outfile.write("0\n0\n")
            outfile.write(str(steps))
            outfile.write("\n")
            outfile.write(str(len))
    else:
        dist = int(input("distance > "))
        for i in range(int(msr_len/delta_len)):
            msr.append(jf.getMeanAdc(20))
            jf.stepForward(5)
        jf.stepBackward(msr_len)
        jf.save(msr, msr_len, "data", dist)
finally: 
    jf.deinitSpiAdc()
    jf.deinitStepMotorGpio()
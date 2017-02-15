from DataAcquisition.readModule import ADataAcquisition
from libs.Spark_ADC import Adc
import time

class EdisonRead(ADataAcquisition):

    def __init__(self, samplesQueue, samplesQueueLock, socketControl):
        super().__init__(samplesQueue, samplesQueueLock, socketControl)
        self.samples = []
        self.samplesNum = 500
        self.sampleTime = 0.1
        self.sampleInterval = self.sampleTime / self.samplesNum
        self.adcZero = self.socketControl.calibrate()


    def addDAQSample(self):
        self.samples = []
        startTime = time.time() - self.sampleInterval
        for i in range (self.samplesNum):
            # To give some time before reading again
            if ((time.time() - startTime) >= self.sampleInterval):
                # Centers read value at zero
                readValue = self.adc.adc_read() - self.adcZero
                self.samples.append(readValue)
                startTime += self.sampleInterval
        samplesToQueue = {"samples": self.samples, "timestamp": time.time()}
        #print("These are my samples: " + str(samplesToQueue))

        #TODO: ATTENTION!!! WHEN IT'S FULL IT WILL BLOCK THE PROCESS
        self.samplesQueueLock.acquire()
        self.samplesQueue.put(samplesToQueue)
        self.samplesQueueLock.release()
        #print("I'm Here #2")
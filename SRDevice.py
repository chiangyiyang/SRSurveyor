import traitlets
import threading
import numpy as np


class Device(traitlets.HasTraits):
    value = traitlets.Unicode()
    running = traitlets.Bool(default_value=False)
    
    def __init__(self, *args, **kwargs):
        self._running = False
            
    def read(self):
        if self._running:
            raise RuntimeError('Cannot read directly while device is running')
        self.value = self._read()
        return self.value
    
    def _capture_info(self):
        import serial
        ser = serial.Serial(port="/dev/ttyUSB1", baudrate=115200)
        while True:
            if not self._running:
                break
            l = ser.readline()
            if len(l) > 0:
                try:
#                     print('READ: ', l)
                    self.value = l.decode('ascii').strip()
                except:
                    print('ERR')            
            
    @traitlets.observe('running')
    def _on_running(self, change):
        if change['new'] and not change['old']:
            # transition from not running -> running
            self._running = True
            self.thread = threading.Thread(target=self._capture_info)
            self.thread.start()
        elif change['old'] and not change['new']:
            # transition from running -> not running
            self._running = False
            self.thread.join()
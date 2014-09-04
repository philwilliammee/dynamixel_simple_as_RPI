#!/usr/bin/python2.7
'''
Created on Nov 18, 2013

@author: philwilliammee

To test for available serial ports
dmesg | grep tty

For RPI only make sure user is a member of dialout group
sudo usermod -a -G tty yourUserName
sudo usermod -a -G dialout username
Log off and log on again for the changes to take effect

This has not been tested with multiple serial ports, I sugest only conecting one serial port for testing
'''
import serial

class Port():
    BAUDRATE = 1000000 #usb2dynamixel #arbotix baudrate 38400 # 
    TIME_OUT = 1
    def __init__(self):            
        self.s = serial.Serial()   # create a serial port object
        self.ports = findPorts()
        self.open_port() #this should be done manually 
        
    def open_port(self):
        #@todo this should have a pop up box to show available ports and ask to connect first
        self.s.baudrate = self.BAUDRATE             # baud rate, in bits/second
        self.s.timeout = self.TIME_OUT
        if self.ports:
            self.s.port = self.ports[0]
            self.s.open()
            if (self.s.isOpen() == False):
                print "error could not open", self.s
            else:
                print "port open at ", self.s.port
        else:
            print"no available ports"
            
    def test_ports(self):
        if len(self.ports) < 1:
            self.ports = findPorts()
            
        if self.s.isOpen() == False:#port is closed
            
            if self.ports:#if there is a port try and open it
                self.open_port()
                
            else:
                print "no available ports"
                return 'fail'
            
            if self.s.isOpen() == False:
                print "can not open port at this time"
                return 'fail'
            
        print self.s, "is open"
        return 'pass'
      
def findPorts():
    """ return a list of serial ports """
    ports = list()
    # windows first
    for i in range(20):
        try:
            sp = serial.Serial("COM"+str(i))
            sp.close()
            ports.append("COM"+str(i))
        except:
            pass
    if len(ports) > 0:
        return ports

    # linux/some-macs
    for k in ["/dev/ttyUSB","/dev/ttyACM","/dev/ttyS"]:
            for i in range(6):
                try:
                    sp = serial.Serial(k+str(i))
                    sp.close()
                    ports.append(k+str(i))
                except:
                    pass
    return ports

if __name__ == '__main__':
    p = Port()
    print p.test_ports()
    p.s.close()
    print "test complete"
    
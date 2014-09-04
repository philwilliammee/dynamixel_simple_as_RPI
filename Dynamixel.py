#!c:\Python27\python.exe
'''
Created on Jan 7, 2014

@author: Phil Williammee
to test serial port
dmesg | grep tty

sudo chmod a+rw /dev/"ttyUSB1"

'''
from Ports import Port

# commands
READDATA = 2
WRITE_DATA = 3
  
#----------------------START DYNAMIXEL CLASS ------------------------------------------------
#this class requires a open serial port to comunicate with the dynamixel
# I want this class to be the only one with serial access, so all others go through here
#there can only be one dynamixel class it doese not support multiple dynamixel objects
class dynamixel():
    def __init__(self, port=Port()):
        self.port = port  
        self.s_port = self.port.s
        self.kerrors = {0:'ERR_NONE', 1:'ERR_VOLTAGE', 2:'ERR_ANGLE_LIMIT', 3:'UNKNOWN',
                        4:'ERR_OVERHEATING', 8:'ERR_RANGE', 16:'ERR_CHECKSUM',
                        32:'ERR_OVERLOAD', 64:'ERR_INSTRUCTION'}
        
        #need to put these in a text file
        self.kins = ({'AX_READ_DATA':2, 'AX_WRITE_DATA':3})
            
    def __del__(self):#not needed just lets me know if dynamixel gets destroyed for some reason **remove this
        class_name = self.__class__.__name__
        print class_name, "class function deleted"
     
    #send an instruction to dynamixel
    #only difference between this and set reg is reg is a parameter 
    #parameter one is usually the register to write to  
    def set_reg(self, index, ins, params=[]):
        if self.s_port.isOpen():#should be able to remove the try and replace with if serial is available
            self.s_port.flushInput()
            length = 2 + len(params)#2=ins+checksum
            self.s_port.write(chr(0xFF)+chr(0xFF)+chr(index)+chr(length)+chr(ins))
            checksum = (index + length + ins)
            for val in params:
                self.s_port.write(chr(val))
                checksum += val
            checksum = 255 - ((checksum)%256)
            self.s_port.write(chr(checksum))
        else:
            print "dynamixel set_ax_reg error no port open"
            return False
        return True
  
    # set register values
    #values is the number of bytesValue in a register usually one or two 
    #if passing a long it is four bytes
    def set_ax_reg(self, ID, reg, values=list(), ins = WRITE_DATA):
        values.insert(0,reg)#add values to ID
        return self.set_reg(ID,ins,values)
    
    def get_reg(self, ID, ins=2, regstart=1, rlength=1):
        vals = list()
        #length = 4
        if self.s_port.isOpen():
            #checksum = 255 - (( 4 + ins + ID + regstart + rlength)%256)
            #pad, pad, id, length, ins, params[], checksum
            #params=(regstart, rlength, checksum)
            self.set_reg(ID, ins, params=[regstart,rlength] )
            #try:#if there is nothing to read ord will fail
            self.s_port.flushInput()
            (self.s_port.read()) # 0xff
            (self.s_port.read()) # 0xff
            vals.append(self.s_port.read()) # ID
            vals.append(self.s_port.read()) # length
            vals.append(self.s_port.read()) #error
            if '' in vals:
                print "error found '' in vals recieved", vals
                return None

            if vals[2] != '\x00':#ord=0
                print vals
                if vals[2] in self.kerrors.viewitems():
                    print 'dynamixel transmision error:', self.kerrors[ord(vals[2])]
                else: print "unknown error returned from arbotix"
                return None #list()
            ord_vals = [ord(val) for val in vals]
            checksum = sum(ord_vals)
            for _ in xrange(ord_vals[1]-2):#remove one for checksum
                c = ord(self.s_port.read())
                checksum += c
                ord_vals.append(c) 
            checksum = 255 -((checksum)%256)
            check = ord(self.s_port.read())
            if (checksum==check or checksum==check+1 or checksum==check-1):#rounding errors
                return ord_vals[3:]
            else:
                print 'rec error packet = ',ord_vals
                print "checksum sent = ", checksum, " != ", check, "checksum recieved"
                return None #vals #list()
        else: 
            print "no serial port open"#should I put in a question box to open the port
            
            
if __name__ == '__main__':
    import time
    speed = 75
    ID = 1
    SPEED_REG = 32
    POS_REG = 30
    positions_delay = list([(1000,4), (24,8), (512,4)])
    ax12 = dynamixel()
    #test serial ports
    print ax12.port.test_ports()
    #test motors
    print "moving dynamixel"
    ax12.set_ax_reg(ID, SPEED_REG, ([(speed%256),(speed>>8)]))
    #test that the speed is set corectly
    return_speed =  ax12.get_reg(ID, ins=READDATA, regstart=SPEED_REG, rlength=1)
    if return_speed:
        print "set speed = ", speed, " dynamixel returned speed of ", return_speed[0]
        if speed == return_speed[0]:
            print"data send recieve test passed"  
        for pos, delay in positions_delay:
            ax12.set_ax_reg(ID, POS_REG, ([(pos%256),(pos>>8)]))
            time.sleep(delay)
    else:
        print "error setting and getting ax data"
    print "test complete"
            

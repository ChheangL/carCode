from smbus import SMBus

addr = 0x8
bus = SMBus(1)
def send(angle1,angle2,duration1 = ((0x23)),duration2 = ((0x2<<4)+(0x3))):
    bus.write_byte(addr,angle1)
    bus.write_byte(addr,duration1)
    bus.write_byte(addr,angle2)
    bus.write_byte(addr,duration2)

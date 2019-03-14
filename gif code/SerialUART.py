import serial


def main():
    port = serial.Serial("/dev/ttyS0", baudrate =9600, timeout = 3.0)
    A = "ABCDEFG"
    while(1):
    	port.write(A.encode())
    rcv = port.read(2)
    print(rcv)
    exit(0)

if __name__ == "__main__":
   code = main()

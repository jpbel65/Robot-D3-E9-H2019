import maestro
servo = maestro.Controller()
servo.setAccel(4,30)
servo.setSpeed(4,30) 
servo.setAccel(5,30)
servo.setSpeed(5,30)
servo.setAccel(3,50)
servo.setSpeed(3,50)
servo.setRange(3,2000, 10000)
#find = False
#QRValue = ""
#servo.move(4,6000)
#servo.move(5,6000)
#while(find == False):
#    QRValue, find = maestro.QRCheck()
servo.move(3,2000)
servo.move(3,10000)
servo.move(3,6000)
    
#print(QRValue)
servo.close()

import maestro
servo = maestro.Controller()
servo.setAccel(4,30)
servo.setSpeed(4,30) 
servo.setAccel(5,30)
servo.setSpeed(5,30)
find = False
QRValue = ""
servo.move(4,6000)
servo.move(5,6000)
while(find == False):
    QRValue, find = maestro.QRCheck()

    
print(QRValue)
servo.close()

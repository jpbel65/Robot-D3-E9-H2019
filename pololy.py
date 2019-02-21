import maestro
servo = maestro.Controller()
servo.setAccel(0,30)
servo.setSpeed(0,30)
servo.setTarget(0,6000)  
servo.setAccel(1,30)
servo.setSpeed(1,30)
servo.setTarget(1,6000) 
servo.close()

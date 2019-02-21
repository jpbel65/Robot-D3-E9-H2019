

//Interruts pins for encoder
#define pin_enc1 18
#define pin_enc2 19
#define pin_enc3 20
#define pin_enc4 21

//pwm pins for motors
#define pwm_mot1 4
#define pwm_mot2 9
#define pwm_mot3 10
#define pwm_mot4 13

//pins for motor direction
#define pin1_mot1 26
#define pin1_mot2 27
#define pin1_mot3 28
#define pin1_mot4 29
#define pin2_mot1 30
#define pin2_mot2 31
#define pin2_mot3 32
#define pin2_mot4 33

//Averaging
#define nbSampleAveraging 5

//Global variables
long int t5_compare;
volatile long int speed1;
volatile long int speed2;
volatile long int speed3;
volatile long int speed4;
volatile float integrateError1;
volatile float integrateError2;
volatile float integrateError3;
volatile float integrateError4;
volatile long int lastSpeed1[nbSampleAveraging];
volatile long int lastSpeed2[nbSampleAveraging];
volatile long int lastSpeed3[nbSampleAveraging];
volatile long int lastSpeed4[nbSampleAveraging];
unsigned long pulseInTimeout = 100000;

//Motors PID values
#define P 1
#define I 2
#define command 500

//For PID calculs
volatile float error1;
volatile float error2;
volatile float error3;
volatile float error4;






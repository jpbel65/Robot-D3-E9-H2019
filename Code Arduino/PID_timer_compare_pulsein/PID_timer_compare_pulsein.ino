/*Ce code utilise le timer 5 afin de calculer les pwm à envoyer aux moteurs à des intervaux réguliers (100Hz).
 * Pour s'y faire, je règle la fréquence du compteur 5 à 65.5KHz et j'enable le output compare interrupt avec
 * le output compare register à 655. Dans la boucle, l'arduino ne fait que lire la fréquence des quatres signaux
 * en boucle et les mettre dans des tableaux. Une fois dans l'ISR (chaque 0.01s), l'arduino fait la moyenne des
 * cinq dernières fréquences et prend celle-ci pour calculer le pwm à appliquer à chacune des pins. Il resterait
 * quelques changements à faire. Premieèrement, il ne faudrait pas que l'arduino fasse de moyenne sur cinq valeurs
 * en régime transitoire, car à basse fréquence, l'arduino ne pourra pas prendre cinq échantillons de fréquences. Aussi,
 * la fréquence montant relativement rapidement (constante de temps de 0.2s), il faut prendre en considération seulement
 * la dernière fréquence mesurée sinon il va toujours sous estiméer la fréquence en régime transitoire. En régime permanent,
 * le moyenne serait une bonne chose par contre, car il stabilise la fréquence qui est mesurée. Il faudrait faire des struct
 * ou des classes pour conserver les numéros es pins des moteurs et mettre une méthode avance et recule pour chaque moteur.
 * Pour qu'un moteur avance, il faut mettre la pin1 à HIGH et la pin 2 à LOW. Pour que l'auto avance, il faut mettre le moteur
 * 1 vers l'avant et le moteur 3 vers l'arrière etc... Il faudrait aussi éviter de mesurer les quatres fréquences quand seulement
 * deux moteurs doivent avancer, car la fonction pulseIn relève un peu du pooling et ralentirait la lecture des autres fréquences.
 * Une autre bonne amélioration serait de lire les quatres fréquences avec des interrupts au lieu de la fonction pulseIn, il faudrait
 * utiliser un compteur au lieu de la fonction micros, car le compteur pour la fonction micros est utilisé par une
 * pin pwm. Cependant, vu qu'en régime permanant la fréqeunce lue devrait être dans les environs de 1000Hz, la fonction pulsIn
 * permet de lire les quatres fréquence en moins de 0.01 secondes (donc plus de 20 fois plus rapidement que la constante de 
 * temps des moteurs) et semble suffisante.
*/

#include "defines.h"


//////////////////////////////////////////////////////////////////////////////////////////////////////
//                                            Setup
//////////////////////////////////////////////////////////////////////////////////////////////////////

void setup() {

  //Setting pin modes
  pinMode(pin_enc1, INPUT_PULLUP);
  pinMode(pin_enc2, INPUT_PULLUP);
  pinMode(pin_enc3, INPUT_PULLUP);
  pinMode(pin_enc4, INPUT_PULLUP);
  pinMode(pwm_mot1, OUTPUT);
  pinMode(pwm_mot2, OUTPUT);
  pinMode(pwm_mot3, OUTPUT);
  pinMode(pwm_mot4, OUTPUT);
  pinMode(pin1_mot1, OUTPUT);
  pinMode(pin1_mot2, OUTPUT);
  pinMode(pin1_mot3, OUTPUT);
  pinMode(pin1_mot4, OUTPUT);
  pinMode(pin2_mot1, OUTPUT);
  pinMode(pin2_mot2, OUTPUT);
  pinMode(pin2_mot3, OUTPUT);
  pinMode(pin2_mot4, OUTPUT);
  
  //Writing PWM
  analogWrite(pwm_mot1, 100);
  analogWrite(pwm_mot2, 100);
  analogWrite(pwm_mot3, 100);
  analogWrite(pwm_mot4, 100);

  //t5_compare calculation
  t5_compare = 655;

  //Setting serial communication
  Serial.begin(9600);
  
  //Setting the clock speed of timer 5 to 65.5kHz (/256)
  TCCR5B &= ~(1 << CS50);
  TCCR5B &= ~(1 << CS51);
  TCCR5B |= (1 << CS52);

  //Setting timer 5
  TCCR5A = 0; //Clearing the counter settings
  OCR5A = t5_compare; //setting output compare register
  TIMSK5 |= (1 << OCIE5A); //Enable output compare interrupt

  //Setting the timer 5 to 0
  TCNT5 = 0;

  sei(); //Enable global interrupts
}

//////////////////////////////////////////////////////////////////////////////////////////////////////
//                                            Loop
//////////////////////////////////////////////////////////////////////////////////////////////////////
void loop() {

  //Measure frequencys
  for (int f = 0 ; f<nbSampleAveraging; f++)
  {
      lastSpeed1[f] = 1000000/(2*pulseIn(pin_enc1, HIGH, pulseInTimeout));
      lastSpeed2[f] = 1000000/(2*pulseIn(pin_enc2, HIGH, pulseInTimeout));
      lastSpeed3[f] = 1000000/(2*pulseIn(pin_enc3, HIGH, pulseInTimeout));
      lastSpeed4[f] = 1000000/(2*pulseIn(pin_enc4, HIGH, pulseInTimeout));
  }

}

//////////////////////////////////////////////////////////////////////////////////////////////////////
//                                            ISR
//////////////////////////////////////////////////////////////////////////////////////////////////////

ISR(TIMER5_COMPA_vect)
/*Ceci est l'ISR du timer compare interrupt. Ici, le PID est calculé et les pwm sont updatés*/
{
    //Resseting timer for next interrupt
    TCNT5 = 0;

    //disable timer compare interrupt (par sécurité)
    TIMSK5 &= ~(1 << OCIE5A);

    //Measuring frequency and averaging
    speed1 = 0;
    speed2 = 0;
    speed3 = 0;
    speed4 = 0;
    for (int k = 0; k<nbSampleAveraging; k++)
    {
        speed1 += lastSpeed1[k];
        speed2 += lastSpeed2[k];
        speed3 += lastSpeed3[k];
        speed4 += lastSpeed4[k];
    }
    speed1 = speed1/nbSampleAveraging;
    speed2 = speed2/nbSampleAveraging;
    speed3 = speed3/nbSampleAveraging;
    speed4 = speed4/nbSampleAveraging;

    Serial.println(String(speed1) + "   " + String(speed2) + "    " + String(speed3) + "    " + String(speed4)); //TODO : à enlever pour debbug
    
    //Calculation of the PID
    error1 = command - speed1;
    error2 = command - speed2;
    error3 = command - speed3;
    error4 = command - speed4;
    integrateError1 += (float) error1*0.1; //TODO : Dernière chose que j'ai changé si ça marche pas
    integrateError2 += (float) error2*0.1;
    integrateError3 += (float) error3*0.1;
    integrateError4 += (float) error4*0.1;

    //Updating pwm values
    analogWrite(pwm_mot1, P*error1 + I*integrateError1); //TODO : changer la fréquence des PWM
    analogWrite(pwm_mot2, P*error2 + I*integrateError2);
    analogWrite(pwm_mot3, P*error3 + I*integrateError3);
    analogWrite(pwm_mot4, P*error4 + I*integrateError4);
    

    //Enable timer compare interrupt
    TIMSK5 |= (1 << OCIE5A);
    
}

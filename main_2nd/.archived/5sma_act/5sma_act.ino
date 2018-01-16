/* If you have an SMA actuator as part of your kit, you can run this specific test.
    You will be able to actuate your SMA, upon waving an object in front of an IR sensor.
    Connect your High Current Device Module (HCDM) to port P2 (8P8C) on your Node Controller (NC).
    Connect your SMA actuator interface board to port C on your HCDM.
    Connect your IR sensor to port A on your HCDM.
    Power your HCDM through the barrel splitter + wall adapter.
    Power your NC either with a USB connection to laptop or through the wall adapter.
*/

//Global variables
#define SMA_PIN_1   9     //Pin # for SMA PWM on P2
#define SMA_PIN_2   10     //Pin # for SMA PWM on P2
#define SMA_PIN_3   22     //Pin # for SMA PWM on P2
#define SMA_PIN_4   23     //Pin # for SMA PWM on P2
#define SMA_PIN_5   29     //Pin # for SMA PWM on P2
#define LED_PIN   13    //Pin # for on-board Teensy LED
#define TIME_ON   1.5   //In Seconds (Less than 2s)
#define TIME_OFF  20    //In Seconds (At least 30s)
#define DUTY_CYCLE 30   //Percentage (0% = 0V, 100% = 5V)

#define WAIT_TIME 5
#define KEEP_TIME 2

// The PWM on your SMA will be conducted, since running 5V continuously will
// be too much for the SMA.  20% duty cycle has been applied.  Do not change the TIME_ON,
// TIME_OFF or DUTY_CYCLE values under any circumstance.

int IR_THRESHOLD = 30; // Value to get IR sensor to be triggered ... can change depending on difficulty in getting sensor to react
int valRead = 0;

void setup() {
  // Declarations for Sensor and Actuator Pins
  pinMode(SMA_PIN_1, OUTPUT);
  pinMode(SMA_PIN_2, OUTPUT);
  pinMode(LED_PIN, OUTPUT); // On-Board Indicator LED

  //Intialize Serial Communication
  Serial.begin(19200);
}

unsigned long now_time;
unsigned long delay_time;

int pin_no[5]={SMA_PIN_1,SMA_PIN_2,SMA_PIN_3,SMA_PIN_4,SMA_PIN_5};

#define SMA_ON 1
#define SMA_OFF 0

int i = 0;

unsigned long start_time = millis();
void loop() {
  analogWrite(pin_no[0], map(DUTY_CYCLE, 0, 100, 0, 255));
  now_time = millis();
  delay_time = now_time - start_time;
  if (delay_time > WAIT_TIME * 1000){
  analogWrite(pin_no[1], map(DUTY_CYCLE, 0, 100, 0, 255));
  }
  now_time = millis();
  delay_time = now_time - start_time;
  if (delay_time > WAIT_TIME * 1000*2){
  analogWrite(pin_no[2], map(DUTY_CYCLE, 0, 100, 0, 255));
  }
  now_time = millis();
  delay_time = now_time - start_time;
  if (delay_time > WAIT_TIME * 1000*3){
  analogWrite(pin_no[3], map(DUTY_CYCLE, 0, 100, 0, 255));
  }
  now_time = millis();
  delay_time = now_time - start_time;
  if (delay_time > WAIT_TIME * 1000*4){
  analogWrite(pin_no[4], map(DUTY_CYCLE, 0, 100, 0, 255));
  }
}

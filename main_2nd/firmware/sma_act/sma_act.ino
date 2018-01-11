/* If you have an SMA actuator as part of your kit, you can run this specific test.
    You will be able to actuate your SMA, upon waving an object in front of an IR sensor.
    Connect your High Current Device Module (HCDM) to port P2 (8P8C) on your Node Controller (NC).
    Connect your SMA actuator interface board to port C on your HCDM.
    Connect your IR sensor to port A on your HCDM.
    Power your HCDM through the barrel splitter + wall adapter.
    Power your NC either with a USB connection to laptop or through the wall adapter.
*/

//Global variables
#define SMA_PIN   9     //Pin # for SMA PWM on P2
#define LED_PIN   13    //Pin # for on-board Teensy LED
#define IR_PIN    14    //Pin # for analog-in IR on P2
#define TIME_ON   1.5   //In Seconds (Less than 2s)
#define TIME_OFF  20    //In Seconds (At least 30s)
#define DUTY_CYCLE 50   //Percentage (0% = 0V, 100% = 5V)

// The PWM on your SMA will be conducted, since running 5V continuously will
// be too much for the SMA.  20% duty cycle has been applied.  Do not change the TIME_ON,
// TIME_OFF or DUTY_CYCLE values under any circumstance.

int IR_THRESHOLD = 30; // Value to get IR sensor to be triggered ... can change depending on difficulty in getting sensor to react
int valRead = 0;

void setup() {
  // Declarations for Sensor and Actuator Pins
  pinMode(SMA_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT); // On-Board Indicator LED
  pinMode(IR_PIN, INPUT);


  //Intialize Serial Communication
  Serial.begin(19200);
}

void loop() {
  //Initialize SMA to resting position
  analogWrite(SMA_PIN, map(DUTY_CYCLE, 0, 100, 0, 255));
  digitalWrite(LED_PIN, HIGH);
  delay(TIME_ON * 1000); // SMA ON time (ms)
  analogWrite(SMA_PIN, 0);
  digitalWrite(LED_PIN, LOW);
  delay(TIME_OFF * 1000); // SMA Cool time (ms)
}




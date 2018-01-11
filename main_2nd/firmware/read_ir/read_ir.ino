//#include <Servo.h>
//Global variables
#define SMA_PIN   9     //Pin # for SMA PWM on P2
#define LED_PIN   13    //Pin # for on-board Teensy LED
#define IR_PIN A0
#define TIME_ON   1.5   //In Seconds (Less than 2s)
#define TIME_OFF  20    //In Seconds (At least 30s)

// グローバル変数の宣言
char input[4];  // 文字列格納用
int i = 0;      // 文字数のカウンタ
int val = 0;    // 受信した数値
int deg = 0;    // サーボの角度
int ir_value = 0;

void setup() {
  // Declarations for Sensor and Actuator Pins
  pinMode(SMA_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT); // On-Board Indicator LED
  pinMode(IR_PIN, INPUT);

  //Intialize Serial Communication
  Serial.begin(19200);
}

// メインループ
void loop() {
  Serial.println(analogRead(IR_PIN));
}

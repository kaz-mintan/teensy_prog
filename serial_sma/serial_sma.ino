//#include <Servo.h>
//Global variables
#define SMA_PIN   9     //Pin # for SMA PWM on P2
#define LED_PIN   13    //Pin # for on-board Teensy LED
#define TIME_ON   1.5   //In Seconds (Less than 2s)
#define TIME_OFF  20    //In Seconds (At least 30s)

// グローバル変数の宣言
char input[4];  // 文字列格納用
int i = 0;      // 文字数のカウンタ
int val = 0;    // 受信した数値
int deg = 0;    // サーボの角度

//int IR_THRESHOLD = 30; // Value to get IR sensor to be triggered ... can change depending on difficulty in getting sensor to react
//int valRead = 0;

void setup() {
  // Declarations for Sensor and Actuator Pins
  pinMode(SMA_PIN,OUTPUT);
  pinMode(LED_PIN,OUTPUT); // On-Board Indicator LED

  //Initialize SMA to resting position
  analogWrite(SMA_PIN,0);

  //Intialize Serial Communication
  Serial.begin(19200);
}

// シリアル通信で受信したデータを数値に変換
int serialNumVal(){
  // データ受信した場合の処理
  if (Serial.available()) {
    input[i] = Serial.read();
     // 文字数が3以上 or 末尾文字がある場合の処理
    if (i > 2 || input[i] == '\0') {
      val = atoi(input);    // 文字列を数値に変換
      Serial.write(input); // 文字列を送信
      Serial.write("\n");
      i = 0;      // カウンタの初期化
      return val;
    }
    else {
      i++;
      return 0;
    }
  }
}

// メインループ
void loop() {
  deg = serialNumVal();
  Serial.println(deg);

  if(deg>=0||deg<=100){
    //servo1.write(deg);  // deg度まで回転
    analogWrite(SMA_PIN,map(deg, 0, 100, 0, 255)); //75% duty cycle = 191, 50% = 127, etc.
    digitalWrite(LED_PIN,HIGH);
    delay(TIME_ON*1000); // SMA ON time (ms)
    analogWrite(SMA_PIN,0);
    digitalWrite(LED_PIN, LOW);
  }
}

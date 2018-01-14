//#include <Servo.h>
//Global variables
#define SMA_PIN   9     //Pin # for SMA PWM on P2
#define LED_PIN   13    //Pin # for on-board Teensy LED
#define IR_PIN A0
#define TIME_ON   1.5   //In Seconds (Less than 2s)
#define TIME_OFF_CO  0.16    //In Seconds (At least 30s)

// グローバル変数の宣言
char input[4];  // 文字列格納用
int i = 0;      // 文字数のカウンタ
int val = 0;    // 受信した数値
int deg = 0;    // サーボの角度
int wait_count = 50;
int wait_cool = 0;
int rcv_flg = 0;
int ir_val = 0;
int distance = 0;

void setup() {
  // Declarations for Sensor and Actuator Pins
  pinMode(SMA_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT); // On-Board Indicator LED
  pinMode(IR_PIN, INPUT);

  //Intialize Serial Communication
  Serial.begin(19200);
}

// シリアル通信で受信したデータを数値に変換
int serialNumVal() {
  // データ受信した場合の処理
  if (Serial.available()) {
    input[i] = Serial.read();
    // 文字数が3以上 or 末尾文字がある場合の処理
    if (i > 2 || input[i] == '\0') {
      val = atoi(input);    // 文字列を数値に変換
      Serial.println(input[i]);
      Serial.println(val);
      i = 0;      // カウンタの初期化
      return val;
    }
    else {
      i++;
      return 0;
    }
  }
}

// int型のデータを送信する関数
void sendIntData(int value) {
  Serial.write('H'); // ヘッダの送信
  Serial.write(highByte(value)); // 上位バイトの送信
  Serial.write(lowByte(value)); // 下位バイトの送信
}

unsigned long start_time;
unsigned long now_time;


// メインループ
void loop() {
  if(rcv_flg == 1){
  	deg = serialNumVal();
    if(deg>0 && deg<100){
      sendIntData(deg);
  	  rcv_flg = 2;//stop to receive pwm
      sendIntData(rcv_flg);
    }
  }else if(rcv_flg == 0){
	  wait_count++;
    now_time = millis();
    //sendIntData(5);
    //check possibility to get pwm
    if((now_time - start_time) > wait_cool){
    //if(wait_count>wait_cool){
      wait_count=0;
      rcv_flg = 1;//lets receive pwm val!
      sendIntData(rcv_flg);

      wait_cool=0;
    }
    ir_val = 0;
    for (i=0 ; i < 100 ; i++) {
      ir_val  = ir_val + analogRead(IR_PIN) ;   // 指定のアナログピン(0番端子)から読取ります
    }
    ir_val = ir_val/100.0;
    distance = 6762/(ir_val-9)-4;
    //sendIntData(distance);
  }else if(rcv_flg == 2){
    analogWrite(SMA_PIN, map(deg, 0, 100, 0, 255));
    digitalWrite(LED_PIN, HIGH);
    delay(TIME_ON * 1000); // SMA ON time (ms)
    analogWrite(SMA_PIN, 0);
    digitalWrite(LED_PIN, LOW);
	  wait_cool = (deg * TIME_OFF_CO) * 1000;
    //sendIntData(wait_cool);
    //delay(TIME_OFF_CO * 1000 * deg); // SMA Cool time (ms)
    start_time = millis();
	  rcv_flg = 0;
    deg = -1;
    sendIntData(rcv_flg);
  }
}



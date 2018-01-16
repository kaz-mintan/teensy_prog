//#include <Servo.h>
//Global variables

#define IR_PIN_1 A0
#define IR_PIN_2 A1
#define IR_PIN_3 A17
#define IR_PIN_4 A13
#define IR_PIN_5 A3
#define TIME_ON   1.5   //In Seconds (Less than 2s)
#define TIME_OFF  20    //In Seconds (At least 30s)

void setup() {
  // Declarations for Sensor and Actuator Pins
  pinMode(IR_PIN_1, INPUT);
  pinMode(IR_PIN_2, INPUT);
  pinMode(IR_PIN_3, INPUT);
  pinMode(IR_PIN_4, INPUT);
  pinMode(IR_PIN_5, INPUT);

  //Intialize Serial Communication
  Serial.begin(19200);
}

// int型のデータを送信する関数
void sendIntData(int ir[5]) {
  int k=0;
  Serial.write('H'); // ヘッダの送信
  for(k=0;k<5;k++){
	  Serial.write(highByte(ir[k])); // 上位バイトの送信
	  Serial.write(lowByte(ir[k])); // 下位バイトの送信
  }
}

int pin_no[5]={IR_PIN_1,IR_PIN_2,IR_PIN_3,IR_PIN_4,IR_PIN_5};

//グローバル変数の宣言
int i = 0;
int j = 0;
int ir_val[5] = {0};
int distance[5] = {0};

// メインループ
void loop() {
  ir_val[5] = {0};
  for (i=0 ; i < 100 ; i++) {
	  for (j =0;j<5;j++){
    	ir_val[j]  = ir_val[j] + analogRead(pin_no[j]) ;   // 指定のアナログピン(0番端子)から読取ります
	  }
  }
  for (j=0;j<5;j++){
	  ir_val[j] = ir_val[j]/100.0;
	  distance[j] = 6762/(ir_val[j]-9)-4;
   //Serial.println(j);
   //Serial.println(distance[j]);
  }

  sendIntData(distance);
  //delay(500);
  //Serial.println(distance);
}

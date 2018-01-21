//#include <Servo.h>
//Global variables

#define IR_PIN_1 A0
#define IR_PIN_2 A1
#define IR_PIN_3 A20
#define IR_PIN_4 A5
#define IR_PIN_5 A3

#define LED_PIN_1 9
#define LED_PIN_2 10
#define LED_PIN_3 22
#define LED_PIN_4 23
#define LED_PIN_5 5


void setup() {
  // Declarations for Sensor and Actuator Pins
  pinMode(IR_PIN_1, INPUT);
  pinMode(IR_PIN_2, INPUT);
  pinMode(IR_PIN_3, INPUT);
  pinMode(IR_PIN_4, INPUT);
  pinMode(IR_PIN_5, INPUT);

  pinMode(LED_PIN_1, OUTPUT);
  pinMode(LED_PIN_2, OUTPUT);
  pinMode(LED_PIN_3, OUTPUT);
  pinMode(LED_PIN_4, OUTPUT);
  pinMode(LED_PIN_5, OUTPUT);

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
int pin_led[5]={LED_PIN_1,LED_PIN_2,LED_PIN_3,LED_PIN_4,LED_PIN_5};

int thre = 5;
void brink(int no, int distance_input){

  if(distance_input<80 && distance_input>0){
    if(no==2){
      analogWrite(pin_led[no], map(-distance_input+15, 0, 100, 0, 255));
    }else{
      analogWrite(pin_led[no], map(-distance_input+15, 0, 100, 0, 255));
    }
  }
}



//グローバル変数の宣言
int i = 0;
int j = 0;
int ir_val[5] = {0};
int distance[5] = {0};

// メインループ
void loop() {
  //Serial.println(analogRead(pin_no[2]));
//}

//void test(){
  ir_val[5] = {0};
  for (i=0 ; i < 100 ; i++) {
	  for (j =0;j<5;j++){
    	ir_val[j]  = ir_val[j] + analogRead(pin_no[j]) ;   // 指定のアナログピン(0番端子)から読取ります
	  }
  }
  for (j=0;j<5;j++){
	  ir_val[j] = ir_val[j]/100.0;
	  distance[j] = 6762/(ir_val[j]-9)-4;

    brink(j,distance[j]);
  }


  sendIntData(distance);
  //delay(500);
  //Serial.println(distance);
}

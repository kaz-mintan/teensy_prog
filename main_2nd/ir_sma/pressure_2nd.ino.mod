const int pressure_pin = 0;
const int heart_pin = 1;
double R1 = 10;



void setup(){
  Serial.begin(115200);  // シリアル通信速度
  pinMode(0,INPUT);
  pinMode(1,INPUT);
 
  
}



// int型のデータを送信する関数
void sendIntData(int value1,int value2) {
  Serial.write('H'); // ヘッダの送信
  Serial.write(highByte(value1)); // 上位バイトの送信
  Serial.write(lowByte(value1)); // 下位バイトの送信
  Serial.write(highByte(value2)); // 上位バイトの送信
  Serial.write(lowByte(value2)); // 下位バイトの送信

}

int led_counter[2][7]={{0}};


void loop(){
  // 変数の宣言
  double Vo, Rf, fg;
  int ain1 = analogRead(pressure_pin);  
  int ain2 = analogRead(heart_pin);
  int ans = map(ain2,0,1023,0,500);
  ans = map(ans,50,220,50,4);

  sendIntData(ain1,ain2);

}



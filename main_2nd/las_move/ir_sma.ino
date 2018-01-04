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
  pinMode(SMA_PIN,OUTPUT);
  pinMode(LED_PIN,OUTPUT); // On-Board Indicator LED
  pinMode(IR_PIN,INPUT);

  //Intialize Serial Communication
  Serial.begin(9600);
}

// int型のデータを送信する関数
void sendIntData(int value) {
  Serial.write('H'); // ヘッダの送信
  Serial.write(highByte(value)); // 上位バイトの送信
  Serial.write(lowByte(value)); // 下位バイトの送信
}

// シリアル通信で受信したデータを数値に変換
int serialNumVal(){
  // データ受信した場合の処理
  if (Serial.available()) {
    input[i] = Serial.read();
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

int recv_data = 0;

int read_val(){
  if ( Serial.available() >= sizeof('H') + sizeof(int) ) {
    Serial.println("in");
      // ヘッダの確認
      if ( Serial.read() == 'H' ) {
        int low = Serial.read(); // 下位バイトの読み取り
        Serial.println(low);
        int high = Serial.read(); // 上位バイトの読み取り
        Serial.println(high);
        recv_data = makeWord(high,low); // 上位バイトと下位バイトを合体させてint型データを復元
      }
  }
  return recv_data;
}

int wait_count=0;
bool sma_on=0;
long ans ;

// メインループ
void loop() {
  ans = 0 ;

  //for (i=0 ; i < 100 ; i++) {
  //  ans  = ans + analogRead(IR_PIN) ;   // 指定のアナログピン(0番端子)から読取ります
  //}
  //val = ans/100;
  //if(val>0&&val<1024){
  //  sendIntData(val);
  //}

  deg=Serial.read();
  
  delay(100);
    
  if(deg>=10){
    
    analogWrite(SMA_PIN,map(deg, 0, 100, 0, 255)); //75% duty cycle = 191, 50% = 127, etc.
    digitalWrite(LED_PIN,HIGH);
    
    delay(TIME_ON*1000); // SMA ON time (ms)
    deg=0;
    analogWrite(SMA_PIN,0);
    digitalWrite(LED_PIN, LOW);
    wait_count=0;
  }
  
}



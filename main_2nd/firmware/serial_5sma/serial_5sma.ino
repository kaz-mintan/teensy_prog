//#include <Servo.h>
//Global variables

#define TIME_ON   1.5   //In Seconds (Less than 2s)
#define TIME_OFF_CO  0.125    //In Seconds (At least 30s)

#define SMA_PIN_1   9     //Pin # for SMA PWM on P2
#define SMA_PIN_2   10     //Pin # for SMA PWM on P2
#define SMA_PIN_3   22     //Pin # for SMA PWM on P2
#define SMA_PIN_4   23     //Pin # for SMA PWM on P2
#define SMA_PIN_5   25     //Pin # for SMA PWM on P2


// グローバル変数の宣言
char input[4];  // 文字列格納用
int i = 0;      // 文字数のカウンタ
int val = 0;    // 受信した数値
int deg = 0;    // サーボの角度

void setup() {
  // Declarations for Sensor and Actuator Pins
  pinMode(SMA_PIN_1, OUTPUT);
  pinMode(SMA_PIN_2, OUTPUT);
  pinMode(SMA_PIN_3, OUTPUT);
  pinMode(SMA_PIN_4, OUTPUT);
  pinMode(SMA_PIN_5, OUTPUT);
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
       //Serial.println(input);
      val = atoi(input);    // 文字列を数値に変換
      i = 0;      // カウンタの初期化
      return val;
    }
    else {
      i++;
      return 0;
    }
  }else{
	  return 0;
  }
}

int pin_no[5]={SMA_PIN_1,SMA_PIN_2,SMA_PIN_3,SMA_PIN_4,SMA_PIN_5};

void act_sma(int pin_no, int deg){
    analogWrite(pin_no, map(deg, 0, 100, 0, 255));
    //delay(TIME_ON*1000);
}

void stop_sma(int pin_no){
    analogWrite(pin_no, 0);
}

void send_all(int pwm_input,int keep,int delay_time){
	int i = 0;
	unsigned long start_time = millis();
	int move_array[5]={0,0,0,0,0};

	int stop_array[5]={keep*100,
		delay_time*100+keep*100,
		delay_time*2*100+keep*100,
		delay_time*3*100+keep*100,
		delay_time*4*100+keep*100};

	int start_array[5]={0,
		delay_time*100,
		delay_time*2*100,
		delay_time*3*100,
		delay_time*4*100};

	//act_sma(SMA_PIN_1,pwm_input);
	unsigned long now_time;
  int dt;

  while(move_array[4]!=2){
    now_time = millis();
	  dt = now_time - start_time;

  	for(i = 0; i<5; i++){
  		if(move_array[i]==0){
  			if(dt>start_array[i]){
  				act_sma(pin_no[i],pwm_input);
          move_array[i]=1;
  			}
  		}else if(move_array[i]==1){
  			if(dt>stop_array[i]){

  				stop_sma(pin_no[i]);
  				move_array[i]=2;
  			}
  		}
  	}
   
  }
}

int vals[3];
int k = 0;
unsigned long k_time;
unsigned long n_time;
// メインループ
void loop() {
  int pwm_input;
  float keep;
  float delay_time;
  n_time = millis();
  
  if(Serial.available()){
    vals[k] = serialNumVal();
    if(vals[k]>0 && vals[k]<=100){
      k++;
      k_time = millis();
    }else if(vals[k]>110){
      k=0;
      exit;
    }
    if(k_time-n_time>30000){
      Serial.println("k");
      k=0;
      exit;
    }
    //Serial.println(Serial.read());
    if(k>2){
      //*************
      pwm_input = vals[0];
      keep = vals[1];
      delay_time = vals[2];
      send_all(pwm_input,keep,delay_time);
      delay((keep+delay_time)*100);
      //*************
      int vals[3];
      k=0;
      pwm_input = 0;
      keep = 0;
      delay_time = 0;
    }
  }
}

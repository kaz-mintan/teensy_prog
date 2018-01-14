//#include <Servo.h>
//Global variables
#define LED_PIN   13    //Pin # for on-board Teensy LED
#define IR_PIN A0
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
  pinMode(LED_PIN, OUTPUT); // On-Board Indicator LED
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
  Serial.println("start time");
  Serial.println(start_time);
	int move_array[5]={0,0,0,0,0};

	int stop_array[5]={keep*1000,
		delay_time*1000+keep*1000,
		delay_time*2*1000+keep*1000,
		delay_time*3*1000+keep*1000,
		delay_time*4*1000+keep*1000};

	int start_array[5]={0,
		delay_time*1000,
		delay_time*2*1000,
		delay_time*3*1000,
		delay_time*4*1000};

	//act_sma(SMA_PIN_1,pwm_input);
	unsigned long now_time;
  int dt;



  while(move_array[4]!=2){
    Serial.println('b');
    now_time = millis();
	  dt = now_time - start_time;

  	for(i = 0; i<5; i++){
  		if(move_array[i]==0){
  			if(dt>start_array[i]){
          Serial.println("input");
          Serial.println(i);
  				act_sma(pin_no[i],pwm_input);
          move_array[i]=1;
  			}
  		}else if(move_array[i]==1){
  			if(dt>stop_array[i]){
          Serial.println("stop");
          Serial.println("i");

  				stop_sma(pin_no[i]);
  				move_array[i]=2;
  			}
  		}
  	}
   
  }
}


// メインループ
void loop() {
  //deg = serialNumVal();

	int pwm_input;
	int keep;
	int delay_time;
	int test_i = 0;

  start_str = serialNumVal();
  if(start_str == 'H'){
	pwm_input = serialNumVal();
	keep = serialNumVal();
	delay_time = serialNumVal();

	if(pwm_input > 0){
		for(test_i=0;test_i<5;test_i++){
			act_sma(i,pwm_input);
		}
		for(test_i=0;test_i<5;test_i++){
			stop_sma(i);
		}

		send_all(pwm_input,keep,delay_time);

		delay(10000);
	}
  }

}


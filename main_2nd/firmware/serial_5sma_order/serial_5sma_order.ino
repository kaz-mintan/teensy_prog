//#include <Servo.h>
//Global variables

#define TIME_ON   0.1   //In Seconds (Less than 2s)
#define TIME_OFF_CO  0.125    //In Seconds (At least 30s)

#define SMA_PIN_1   9     //Pin # forj SMA PWM on P2
#define SMA_PIN_2   10     //Pin # for SMA PWM on P2
#define SMA_PIN_3   3     //Pin # for SMA PWM on P2
#define SMA_PIN_4   32     //Pin # for SMA PWM on P2
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
       Serial.println(input);
      val = atoi(input);    // 文字列を数値に変換
      i = 0;      // カウンタの初期化
      return val;
    }
    else {
      i++;
      return 0;
    }
  }
  else{
    return 0;
  }
}

int pin_no[5]={SMA_PIN_1,SMA_PIN_2,SMA_PIN_3,SMA_PIN_4,SMA_PIN_5};
int order_array[22][2][5] =  {{{4,3,2,1,0},{-1,-1,-1,-1,-1}}, //0 single close
        {{0,1,2,3,4},{-1,-1,-1,-1,-1}}, //0 single apart
        {{4,3,2,1,-1},{-1,-1,-1,-1,-1}}, //1 single close
        {{0,1,-1,-1,-1},{-1,-1,-1,-1,-1}}, 
        {{1,2,3,4,-1},{-1,-1,-1,-1,-1}},//1 single apart
        {{1,0,-1,-1,-1},{-1,-1,-1,-1,-1}},
        {{4,3,2,1,-1},{-1,-1,0,-1,-1}},//1 double close
        {{1,2,3,4,-1},{-1,0,-1,-1,-1}},//1 double apart
        {{0,1,2,-1,-1},{-1,-1,-1,-1,-1}},//2 single close
        {{4,3,2,-1,-1},{-1,-1,-1,-1,-1}},
        {{2,1,0,-1,-1},{-1,-1,-1,-1,-1}},//2 single apart
        {{2,3,4,-1,-1},{-1,-1,-1,-1,-1}}, 
        {{0,1,2,-1,-1},{4,3,-1,-1,-1}},//2 double close
        {{2,1,0,-1,-1},{-1,3,4,-1,-1}},//2 double apart
        {{0,1,2,3,-1},{-1,-1,-1,-1,-1}},  //3 single close  
        {{4,3,-1,-1,-1},{-1,-1,-1,-1,-1}},  
        {{3,2,1,0,-1},{-1,-1,-1,-1,-1}},  //3 single apart  
        {{3,4,-1,-1,-1},{-1,-1,-1,-1,-1}},  
        {{0,1,2,3,-1},{-1,-1,4,-1,-1}}, //3 double close  
        {{3,2,1,0,-1},{-1,4,-1,-1,-1}}, //3 double apart
        {{0,1,2,3,4},{-1,-1,-1,-1,-1}}, //4 single close  
        {{4,3,2,1,0},{-1,-1,-1,-1,-1}}};  //4 single apart



void act_sma(int pin_no, int deg){
    analogWrite(pin_no, map(deg, 0, 100, 0, 255));
}

void stop_sma(int pin_no){
    analogWrite(pin_no, 0);
    Serial.println(millis());
}

void send_all(int pwm_input,int keep,int delay_time, int order_array[2][5]){
  
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
    Serial.println(delay_time);
	//act_sma(SMA_PIN_1,pwm_input);
	unsigned long now_time;
  unsigned long start_time_5[5];
  int dt,dt_stop;
  int t_1,t_2;

  while(move_array[4]!=2){
    now_time = millis();
	  dt = now_time - start_time;

  	for(i = 0; i<5; i++){
      if(move_array[i]==1){
        dt_stop = now_time -start_time_5[i];
      }
  		t_1 = order_array[0][i];
      t_2 = order_array[1][i];
  		if(dt>start_array[i] && move_array[i]==0){
                 Serial.println(i);
                 Serial.println(millis());
                 Serial.println("===");
        if(t_1!=-1){
				  act_sma(pin_no[t_1],pwm_input);
        }
        if(t_2!=-1){
          act_sma(pin_no[t_2],pwm_input);
        }
        move_array[i]=1;
        start_time_5[i]=millis();
  		}
  		if(dt_stop>3000){
                 Serial.println("===");
        if(t_1!=-1){
				  stop_sma(pin_no[t_1]);
        }
        if(t_2!=-1){
          stop_sma(pin_no[t_2]);
        }
				move_array[i]=2;
  		}
  	}
  }
}

int vals[4];
int k = 0;
unsigned long k_time;
unsigned long n_time;

// メインループ
int hoge=0;
  int hogehoge=0;
void loop() {
  int pwm_input;
  float keep;
  float delay_time;
  int array_num;

//  int order_array[2][5]={{0,1,2,3,4},{-1,-1,-1,-1,-1}};
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
    if(k>3){
      //*************
      pwm_input = vals[0];
      keep = vals[1];
      delay_time = vals[2];
      array_num = vals[3]-1;
      send_all(pwm_input,keep,delay_time,order_array[array_num]);
      delay(5000);
      //*************
      int vals[3];
      k=0;
      pwm_input = 0;
      keep = 0;
      delay_time = 0;
      array_num = 0;
    }
  }
}

// Living Architecture Systems
// ir_led.ino
// Turns on an LED after passing a pre-defined proximity threshold

// Hardware Setup:
// one node controller, one low current device module
// one LED, one IR sensor
// Connect node controller and RPi over USB
// Plug the device module into node controller port 1
// Plug IR sensor into device module port E
// Plug LED into device module port F

//IR SENSOR SETUP

// from 3.1 Device Module A schematics we see DM port C is connected to I/O pin 6
// from pinout diagram (or node controller schematics) NC port 1 pin 6 is connected to Teensy pin A13
// and if using node_ports library you'll find Port1.DMLow.getPin('C') == A13
int ir_pin = 14;
int ir_threshold = 30;
int output_energy = 0;
bool ir_trigger = false;
int ir_value = 0;

// LED SETUP
// from 3.1 Device Module A schematics we see DM port F is connected to DM pin 3
// from pinout diagram (or node controller schematics) NC port 1 pin 3 is connected to Teensy pin 6
// and if using node_ports library you'll find Port1.DMLow.getPin('F') == 6
int led_pin = 22;


// int型のデータを送信する関数
void sendIntData(int value1,int value2) {
  Serial.write('H'); // ヘッダの送信
  Serial.write(highByte(value1)); // 上位バイトの送信
  Serial.write(lowByte(value1)); // 下位バイトの送信
  Serial.write(highByte(value2)); // 上位バイトの送信
  Serial.write(lowByte(value2)); // 下位バイトの送信

}

void setup() {
  pinMode(ir_pin, INPUT);
  pinMode(led_pin, OUTPUT);
  Serial.begin(19200);
}

void loop() {
  ir_value = analogRead(ir_pin);
  delay(50);
//  int range = round((6787 / (ir_value * 1023 - 3) - 4));
  Serial.println(ir_value);
  //sendIntData(ir_value)
  ir_trigger = ir_value > ir_threshold;
  output_energy = map(ir_value, 0, 100, 0, 255);
  
  if (ir_value > 30){
    analogWrite(led_pin, ir_value*50);
  }
  else{
    digitalWrite(led_pin, LOW);
  }
  
}

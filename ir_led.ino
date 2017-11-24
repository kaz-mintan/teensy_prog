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
int ir_pin = A0;
int ir_threshold = 30;
int output_energy = 0;
bool ir_trigger = false;
int ir_value = 0;

// LED SETUP
// from 3.1 Device Module A schematics we see DM port F is connected to DM pin 3
// from pinout diagram (or node controller schematics) NC port 1 pin 3 is connected to Teensy pin 6
// and if using node_ports library you'll find Port1.DMLow.getPin('F') == 6
int led_pin = 22;


void setup() {
  pinMode(ir_pin, INPUT);
  pinMode(led_pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  ir_value = analogRead(ir_pin);
  delay(500);
  Serial.println(ir_value);
  ir_trigger = ir_value > ir_threshold;
  output_energy = map(ir_value, 0, 100, 0, 255);
  
  if (ir_value > 30){
    analogWrite(led_pin, ir_value*50);
  }
  else{
    digitalWrite(led_pin, LOW);
  }
  
}

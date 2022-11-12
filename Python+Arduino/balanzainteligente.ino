#include "HX711.h"
const int DOUT=A1;
const int CLK=A0;
#define RGB_BLUE 10
#define RGB_GREEN 11
#define RGB_RED 9
int distancia = 0;
int Switch= 4;//PIN Transistor
int Buzzer= 13;//PIN Buzzer 8
const int Trigger = 3;   //Pin digital 2 para el Trigger del sensor
const int Echo = 2;   //Pin digital 3 para el Echo del sensor
long readUltrasonicDistance(int triggerPin, int echoPin)
{
  pinMode(triggerPin, OUTPUT);  // Clear the trigger
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  // Sets the trigger pin to HIGH state for 10 microseconds
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);
  // Reads the echo pin, and returns the sound wave travel time in microseconds
  return pulseIn(echoPin, HIGH);
}
unsigned long tiempo1 = 0;
unsigned long tiempo2 = 0;
unsigned long diferenciaTiempo = 0;
char option=' ';
HX711 balanza;
float valor;
float calibration_factor = -224200; //-7050 worked for my 440lb max scale setup
void scale(){
  
}
void setup() {
  //Sensor de distancia
  pinMode(Trigger, OUTPUT); //pin como salida
  pinMode(Echo, INPUT);  //pin como entrada
  digitalWrite(Trigger, LOW);//Inicializamos el pin con 0
  //LEDS RGB
  pinMode (RGB_RED, OUTPUT);
  pinMode (RGB_GREEN, OUTPUT);
  pinMode (RGB_BLUE, OUTPUT);
  pinMode(Buzzer, OUTPUT); //pin como salida
  //Comunicacion
  Serial.begin(9600);
  //Celda de carga y HX711
  balanza.begin(DOUT, CLK);
  Serial.print("Factor Zero: ");
  Serial.println(balanza.read_average());
  balanza.set_scale(); // establecer escala
  balanza.tare(30);  //El peso actual es considerado Tara.
  pinMode(Switch, OUTPUT);
  digitalWrite(Switch, HIGH);
}
void Color(int G, int B, int R) {     
  analogWrite(RGB_GREEN, G) ;
  analogWrite(RGB_BLUE, B) ;
  analogWrite(RGB_RED, R) ;
}
void loop() {
  distancia = 0.01723 * readUltrasonicDistance(Trigger, Echo);
  balanza.set_scale(calibration_factor); //Adjust to this calibration factor
  valor=(balanza.get_units(), 3);
  if (distancia <=30){
    Serial.println("o");
    Color(0,255,0);
    delay(1000);
  }
  else if(distancia>30 && distancia <=70){
    Color(0,0,0);
    Serial.println("a");
    delay(1000);
  }
  if (Serial.available() > 0){
    option = Serial.read();
  if (distancia <=20 && option=='i' or distancia <=20 && valor>0.2){ //balanza python
    Serial.print(valor);
    Serial.println(" Kg");
    digitalWrite(Switch, LOW);
    Color(0,0,255);
    delay(2500);
    tone(Buzzer,260);
  }
  else{
    Serial.print("Distancia: ");
    Serial.println(distancia);
    Color(0,255,0);
    digitalWrite(Switch, HIGH);
    noTone(Buzzer);
    delay(500);
  }
  }
}

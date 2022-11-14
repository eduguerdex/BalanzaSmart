//Libreria
#include "HX711.h"
#include "math.h"
// Declaracion de pines
const int DOUT=A1;
const int CLK=A0;
#define RGB_BLUE 10
#define RGB_GREEN 11
#define RGB_RED 9
#define Buzzer 13//PIN Buzzer 8
#define LED 5
#define Switch 4//PIN Transistor
#define Trigger 3   //Pin digital 3 para el Trigger del sensor
#define Echo 2   //Pin digital 2 para el Echo del sensor
// Funcion de distancia
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
//Variables
unsigned long distanciaAnterior, distancia, tiempo2, tiempo1 = 0;
unsigned long diferenciaTiempo = 0;
char option=' ';
HX711 balanza;
float valor;
float memoria[30];
unsigned int pantalla;
unsigned int pantalla_ant=0;
int count;
int Limite=25;
unsigned long INTERVALO_TEMP = 5000UL;
unsigned long evento_temp;
int limitedis=30;
bool unaVez = true, unaVez2 = true;
float calibration_factor = -224200; //-7050 worked for my 440lb max scale setup
float suma,average;
int peso=0;
void DataScale(int peso){
int elementos=sizeof(memoria)/sizeof(memoria[0]);
int conteo=0;
 suma=0;
 for(int i=0;i<limitedis;i++){
  //Serial.print("memoria: ");
  valor=map(analogRead(A2),0,1023,0,255);
  //Serial.println(valor);
  //valor=(balanza.get_units(), 3); //Balanza valores
  memoria[i]=valor;
  if(peso==1){
  if (roundf(memoria[i])==roundf(memoria[i-1])){
    conteo+=1;
    suma=memoria[i]+suma;
    delay(100);
  }
  else if(roundf(memoria[i])<0.1){
    conteo=0;
    suma=0;
    elementos=0;
  }
  else{
    conteo=0;
    suma=0;
    elementos=0;
  }
  if(conteo>8){
    average=suma/conteo;
    peso=0;
    analogWrite(LED,average);
    Serial.println("pes:"+String(average/100,2));
    break;
  }
  delay(100);
 }}
}
void setup() {
  //Sensor de distancia
  pinMode(Trigger, OUTPUT); //pin como salida
  pinMode(Echo, INPUT);  //pin como entrada
  digitalWrite(Trigger, LOW);//Inicializamos el pin con 0
  //LEDS RGB
  pinMode (LED, OUTPUT);
  pinMode (RGB_RED, OUTPUT);
  pinMode (RGB_GREEN, OUTPUT);
  pinMode (RGB_BLUE, OUTPUT);
  pinMode(Buzzer, OUTPUT); //pin como salida
  //Comunicacion
  Serial.begin(9600);
  //Celda de carga y HX711
  balanza.begin(DOUT, CLK);
  Serial.print("Factor Zero: ");
  Serial.println(balanza.read());
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
  unsigned long actual = millis();
  distancia = 0.01723 * readUltrasonicDistance(Trigger, Echo);
  balanza.set_scale(calibration_factor); //Adjust to this calibration factor
  //DENTRO DEL LIMITE
  if(actual > evento_temp ){
  if ( distancia <= Limite )
    {
      Color(0,255,0);
      if ( unaVez == true )
      {
        Serial.println("o:"+String(100));
        INTERVALO_TEMP=10000UL;
        unaVez = false;
      }
      unaVez2 = true;
    }
    //FUERA DEL LIMITE
    else
    {
      peso=0;
      if (unaVez2 == true )
      {
        Color(0,0,0);
        Serial.println("a:"+String(0));
        INTERVALO_TEMP=5000UL;
        unaVez2 = false;
      }
      unaVez = true;
    }
    evento_temp += INTERVALO_TEMP;
    }
  delay(1000);
  if (Serial.available() > 0){
    option = Serial.read();
  if (distancia <=20 && option=='i'){ //balanza python  or distancia <=20 && valor>0.2
    digitalWrite(Switch, LOW);
    Color(0,0,255);
    peso=1;
    //Serial.print("pes:");
    //Serial.print(valor);
    DataScale(peso);
    tone(Buzzer,260);
  }
  else{
    peso=0;
    digitalWrite(Switch, HIGH);
    noTone(Buzzer);
    delay(500);
    if(actual > evento_temp ){
  if ( distancia <= Limite )
    {
      Color(0,255,0);
      if ( unaVez == true )
      {
        Serial.println("o:"+String(valor,2));
        INTERVALO_TEMP=10000UL;
        unaVez = false;
      }
      unaVez2 = true;
    }
    //FUERA DEL LIMITE
    else
    {
      if (unaVez2 == true )
      {
        Color(0,0,0);
        Serial.println("a:"+String(valor,2));
        INTERVALO_TEMP=5000UL;
        unaVez2 = false;
      }
      unaVez = true;
    }
    evento_temp += INTERVALO_TEMP;
    }
  delay(1000);
  }
  }
}

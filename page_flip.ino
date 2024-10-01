#include <Servo.h>

int signal=8;
int finish=10;
Servo myservo;
Servo flip;

int signalState=0;


void setup() {
  myservo.attach(9);
  flip.attach(6);
  pinMode(signal,INPUT);
  pinMode(finish,OUTPUT);
  Serial.begin(9600);
  digitalWrite(finish,LOW);
  
}

void loop() {
  signalState=digitalRead(signal);
  Serial.println(signalState);
  if (signalState==HIGH){
    for(int i=90;i>60;i--){
      myservo.write(i);
      delay(100);
    }
    delay(100);
    flip.write(180);
    delay(100);
    myservo.write(0);
    digitalWrite(finish,HIGH);
    delay(1000);
    flip.write(0);
    delay(2000);
    Serial.println("sending signal");
  }else{
    digitalWrite(finish,LOW);
  }
  delay(100);
}
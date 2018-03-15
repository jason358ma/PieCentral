#include <SevenSeg.h>

//SevenSeg disp(A3, 2, 3, 4, 5, 6, 7); // for uno
//corresponds to A3 = (segment) A, 2 = B, 3 = C, 4=D, 5=E, 6=F, 7=G etc.
//for Uno, 13=A, 12=B, 11=C, 10=D, 9=E, 8=F, 7=G
SevenSeg disp(13, 12, 11, 10, 9, 8, 7);

const int numOfDigits = 4;
//int digitPins[numOfDigits]={9, A0, A1, A2}; //for mini
//for Uno, use 6, 5, 4, 3
int digitPins[numOfDigits] = {6, 5, 4, 3}; //flipped by accident

//int buttonIn = 10; //this is for mini
int switchIn = 19; //for mega



int sensorVal = 0;
int counter = 0;
int switchVal = 0;
int prevSwitchVal = 0;
char incomingByte = ' ';

boolean buttonWasPressed = false;

//plug into VCC for power
//next time, integrate 7 segment display

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("begin");
//  pinMode(buttonIn, INPUT);
  disp.setDigitPins(numOfDigits, digitPins);
  pinMode(switchIn, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  switchVal = digitalRead(switchIn);
  if (switchVal != prevSwitchVal){
    Serial.println("changed to " + switchVal);
    prevSwitchVal = switchVal;
  }
  
//
//  disp.write(counter);
//  if (!sensorVal && buttonWasPressed){ 
//    // if button was released
//    buttonWasPressed = false;
//    counter++;
//  } else if (sensorVal && ! buttonWasPressed){
//    buttonWasPressed = true;
//  }
//
//  if (counter > 10000){
//    counter = 0;
//  }

//  if (Serial.available() > 0){
//    Serial.println("-----");
//    incomingByte = (char) Serial.read();
//    Serial.print("got: ");
//    Serial.println(incomingByte);
//  }


  if(switchVal){
    disp.write(420);
  } else {
    disp.write(69);
  }
  
} 

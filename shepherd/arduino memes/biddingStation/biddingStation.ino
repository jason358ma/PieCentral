#include <SevenSeg.h>
//for Uno, 13=A, 12=B, 11=C, 10=D, 9=E, 8=F, 7=G
SevenSeg disp(13, 12, 11, 10, 9, 8, 7);
const int numOfDigits = 4;
const int numOfButtons = 5;

//for Uno, use 6, 5, 4, 3
int digitPins[numOfDigits] = {6, 5, 4, 3};

int switchIn = 2;
int prevSwitchVal = 0;
int switchVal = 0;
boolean buttonWasPressed[numOfButtons] = {false, false, false, false, false};
int buttonPins[numOfButtons] = {14, 15, 16, 17, 18};
//int button1 = 14;
//int button2 = 15;
//int button3 = 16;
//int button4 = 17;
//int button5 = 18;
int submitButton = 19;
boolean submitPressed = false;
//we use 19 as submit, 14-18 as the 5 digits (14=1, 15=2, 16=3, 17=4, 18=5)



int currentGoal = 0;
int currentCode = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("begin");
  disp.setDigitPins(numOfDigits, digitPins);
  
//  pinMode(switchIn, INPUT);
//  pinMode(button1, INPUT);
//  pinMode(button2, INPUT);
//  pinMode(button3, INPUT);
//  pinMode(button4, INPUT);
//  pinMode(button5, INPUT);
  pinMode(submitButton, INPUT);
  for (int ii = 0; ii < numOfButtons; ii++){
    pinMode(buttonPins[ii], INPUT);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  switchVal = digitalRead(switchIn);
  if (switchVal != prevSwitchVal){
    Serial.print("switched to: ");
    if (switchVal){
      Serial.println("code mode");
    } else {
      Serial.println("bidding");
    }
    prevSwitchVal = switchVal;
  }
  if (switchVal){    
    processCode();
  } else {   
   processBidding();
  }

  //need code here to receive the data from 
  //shepherd

  
}

// process code input mode
void processCode(){  
  disp.write(currentCode);

  for (int ii = 0; ii < numOfButtons; ii++){
    int numSelected = buttonPressed(ii);
    if (numSelected != -1){
      if (currentCode == 0){
        currentCode = numSelected+1;
      } else {
        if (currentCode > 999){
          currentCode %= 1000;      
        }
        currentCode = currentCode * 10 + numSelected+1;   
      }
    }
  }
   

  if(!digitalRead(submitButton) && submitPressed){
    Serial.write(currentCode);
    Serial.println(currentCode);
    currentCode = 0;
    submitPressed = false;
  } else if (digitalRead(submitButton) && !submitPressed){
    submitPressed = true;
  }
}
// process billing mode
void processBidding(){  
  disp.write(currentGoal);

  int goalPressed = 0;
  for (int ii = 0; ii < numOfButtons; ii++){
    if (buttonPressed(ii) != -1){
      currentGoal = ii+1;
    }
  }
  switch(currentGoal) {
    // depending on which goal is chosen, display different bid amount?
    case 1:
      break;
    case 2:
      break;
    case 3:
      break;
    case 4:
      break;
    case 5:
      break;
  }

  
  if(!digitalRead(submitButton) && submitPressed){
    Serial.write(currentGoal);
    Serial.println(currentGoal);
    currentGoal = 0;
    submitPressed = false;
  } else if (digitalRead(submitButton) && !submitPressed){
    submitPressed = true;
  }
}

// detect if a button was pressed 
// returns number that the button represents. 
// sad code but it works :(
int buttonPressed(int button){
  int buttonVal = digitalRead(buttonPins[button]);
  if (!buttonVal && buttonWasPressed[button]) {
    //button released
    buttonWasPressed[button] = false;
    return button;
  } else if (buttonVal && !buttonWasPressed[button]){
    //button initially pressed down
    buttonWasPressed[button] = true;
  }
  return -1;
}



#include <SevenSeg.h>
//for Uno, 13=A, 12=B, 11=C, 10=D, 9=E, 8=F, 7=G
SevenSeg disp(13, 12, 11, 10, 9, 8, 7);
// mega: the same
const int numOfDigits = 4;
const int numOfButtons = 5;
const int numGoals = 5;

//for Uno, use 6, 5, 4, 3
int digitPins[numOfDigits] = {6, 5, 4, 3};
char bidGoals[numGoals] = {'a', 'b', 'c', 'd', 'e'};

int switchIn = 2;
int prevSwitchVal = 0;
int switchVal = 0;
boolean buttonWasPressed[numOfButtons] = {false, false, false, false, false};
//int buttonPins[numOfButtons] = {14, 15, 16, 17, 18};
//we use 19 as submit, 14-18 as the 5 digits (14=1, 15=2, 16=3, 17=4, 18=5)
//mega:
int buttonPins[numOfButtons] = {22, 23, 24, 25, 26};

//int submitButton = 19;
//mega:
int submitButton = 27;
/*
  int redPin = 30;
  int greenPin = 29;
  int bluePin = 28;
*/
//int redPins[numOfButtons] = {30, 33, 36, 39, 42};
//int greenPins[numOfButtons] = {29, 32, 35, 38, 41};
//int bluePins[numOfButtons] = {28, 31, 34, 37, 40};
//old
int redPins[numOfButtons] = {51, 50, 44, 38, 32};
int greenPins[numOfButtons] = {53, 48, 42, 36, 30};
int bluePins[numOfButtons] = {52, 46, 40, 34, 28};

boolean submitPressed = false;

int currentGoal = 0;
int currentCode = 0;
int currentPrice = 0;

//int biddingPrice[numGoals] = {3000, 4, 30, 1, 20};
//int goalOwner[numGoals] = {'g', 'b', ' ', 'g', ' '};
int goalOwner[numGoals] = {'n', 'n', 'n', 'n', 'n'};
int biddingPrice[numGoals] = {0, 0, 0, 0, 0};
// ' ' = no owner, 'b' = blue, 'g' = goal
int myScore = 100; //are these equivalent to the money a group has?
char myTeam = 'b'; //change this var for other side LMAO
char myEnemy = 'g';


//String pyInpStr = " ";
char pyInpStr[1023];
int inpStrIndex = 0;
char blank = " ";
boolean pyInpComplete = false;
char *pyInpBuffer = NULL;

int submitStage = 0;
int codeGoal = 0;
int cstatus = -1;

//to do: try to find out a way to take in serial input
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
//  Serial.println("begin");
  disp.setDigitPins(numOfDigits, digitPins);

  pinMode(submitButton, INPUT);
  for (int ii = 0; ii < numOfButtons; ii++) {
    pinMode(buttonPins[ii], INPUT);
    pinMode(redPins[ii], OUTPUT);
    pinMode(bluePins[ii], OUTPUT);
    pinMode(greenPins[ii], OUTPUT);
  }

}

void loop() {
  // put your main code here, to run repeatedly:
  switchVal = digitalRead(switchIn);
  if (switchVal != prevSwitchVal) {
//    Serial.print("switched to: ");
    if (switchVal) {
//      Serial.println("code mode");
    } else {
//      Serial.println("bidding");
    }
    prevSwitchVal = switchVal;
  }
  if (switchVal) {
    processCode();
  } else {
    processBidding();
  }
//  updateLEDs(switchVal);

  //need code here to receive the data from
  //shepherd
  if (pyInpComplete) {
//    Serial.print("pyInp is: ");
//    Serial.println(pyInpStr);
    
    pyInpBuffer = strtok(pyInpStr, ";");
//    Serial.print("first strtok: ");
//    Serial.println(pyInpBuffer);
    
    if (pyInpBuffer != NULL){
      if(strcmp(pyInpBuffer, "bp") == 0){
//        Serial.println("received bidding price info");
        int index = 0; 
        pyInpBuffer = strtok(NULL, ";");
        while(pyInpBuffer != NULL and index < numGoals){
//          Serial.print("At index ");
//          Serial.print(index);
//          Serial.print(" we receive value ");
//          Serial.println(pyInpBuffer);
          biddingPrice[index] = atoi(pyInpBuffer);
          
          pyInpBuffer = strtok(NULL, ";");
          index++;          
        }
      } else if (strcmp(pyInpBuffer, "go") == 0){
//        Serial.println("received goal owner info");
        int index = 0; 
        pyInpBuffer = strtok(NULL, ";");
        while(pyInpBuffer != NULL and index < numGoals){
//          Serial.print("At index ");
//          Serial.print(index);
//          Serial.print(" we receive goalOwner: ");
//          Serial.println(pyInpBuffer);
          
          goalOwner[index] = *pyInpBuffer;
//          Serial.print("goalOwner[");
//          Serial.print(index);
//          Serial.print("] is now ");
//          Serial.println(goalOwner[index]);
          
          pyInpBuffer = strtok(NULL, ";");
          index++;
        }
      } else if (strcmp(pyInpBuffer, "ts") == 0){
//        Serial.println("received team score info");
        pyInpBuffer = strtok(NULL, ";");
        if (pyInpBuffer == NULL){
//          Serial.println("received null for team score, error");
        } else {
//          Serial.print("my score previously ");
//          Serial.println(myScore);
          myScore = atoi(pyInpBuffer);          
//          Serial.print("my score now set to: ");
//          Serial.println(myScore);
        }
      } else if (strcmp(pyInpBuffer, "cstatus") == 0){
//        Serial.println("received code + goal status");
        pyInpBuffer = strtok(NULL, ";");
        if (pyInpBuffer == NULL){
//          Serial.println("null for code + goal status");
        } else {
          cstatus = atoi(pyInpBuffer);
        }
      }
    }
    pyInpStr[0] = '\0';
    pyInpComplete = false;
  }

}

void serialEvent() {
  while (Serial.available()) {
    char inChar[1];
    Serial.readBytes(inChar, 1);
    if (inChar[0] == '\n'){
      pyInpStr[inpStrIndex] = '\0';
      pyInpComplete = true;
      inpStrIndex = 0;
      
    } else {
      pyInpStr[inpStrIndex] = inChar[0];
      inpStrIndex++;
    }
    
  }
}

void changeLED(int ledID, char color = ' ', bool blink = false) {
  // ledID corresponds to the 5 buttons. 1->5,
  // color = 'r', 'g', 'b', ' ' == turn off

  switch (color) {
    case 'r':
      if (blink){
        analogWrite(redPins[ledID - 1], (millis()>>9 & 1) ? 255 : 0);
      } else {
        analogWrite(redPins[ledID - 1], 255);
      }      
      analogWrite(bluePins[ledID - 1], 0);
      analogWrite(greenPins[ledID - 1], 0);
      break;
    case 'g':
      if (blink){
        analogWrite(greenPins[ledID - 1], (millis() >> 9 & 1) ? 255: 0);
      } else {
        analogWrite(greenPins[ledID - 1], 255);
      }
      analogWrite(redPins[ledID - 1], 0);
      analogWrite(bluePins[ledID - 1], 0);
      break;
    case 'b':
      if (blink){
        analogWrite(bluePins[ledID - 1], (millis() >> 9 & 1) ? 255: 0);
      } else {
        analogWrite(bluePins[ledID - 1], 255);
      }
      analogWrite(redPins[ledID - 1], 0);
      analogWrite(greenPins[ledID - 1], 0);
      break;
    case 'c':
      analogWrite(redPins[ledID - 1], 0);
      analogWrite(bluePins[ledID - 1], 255);
      analogWrite(greenPins[ledID - 1], 255);
      break;
    case 'p':
      if (blink){
        analogWrite(redPins[ledID - 1], (millis() >> 9 & 1) ? 160: 0);
        analogWrite(bluePins[ledID - 1], (millis() >> 9 & 1) ? 32: 0);
        analogWrite(greenPins[ledID - 1], (millis() >> 9 & 1) ? 240: 0);
      } else {
        analogWrite(redPins[ledID - 1], 160);
        analogWrite(bluePins[ledID - 1], 32);
        analogWrite(greenPins[ledID - 1], 240);
      }      
      break;
    case ' ':
      analogWrite(redPins[ledID - 1], 0);
      analogWrite(bluePins[ledID - 1], 0);
      analogWrite(greenPins[ledID - 1], 0);
      break;
    default:
      break;
//      Serial.println("Wrong arg for changeLED, can take 'r', 'g' and 'b'");
  }
}

// process code input mode
void processCode() {
  disp.write(currentCode);
  clearLEDs();
  if (submitStage == 0) {
    for (int ii = 0; ii < numOfButtons; ii++) {
      int numSelected = buttonPressed(ii);
      if (numSelected != -1) {
        if (currentCode == 0) {
          currentCode = numSelected + 1;
        } else {
          if (currentCode > 999) {
            currentCode %= 1000;
          }
          currentCode = currentCode * 10 + numSelected + 1;
        }
      }
    }
  } else if (submitStage == 1) {

    for (int ii = 0; ii < numOfButtons; ii++) {
      if (buttonPressed(ii) != -1) {
        codeGoal = ii + 1;
      }
    }
    for (int ii = 1; ii <= 5; ii++) {
      if (ii != codeGoal) {
        changeLED(ii, ' ');
      } else {
        changeLED(ii, 'b');
      }
    }

  } else if (submitStage == 2) {
      // state when waiting for code to come back and resolve
      if (cstatus == 1){
        for (int ii = 1; ii <= numOfButtons; ii++) {
        changeLED(ii, 'g');
        }
        delay(150);
        for (int ii = 1; ii <= numOfButtons; ii++) {
          changeLED(ii, ' ');
        }
        delay(150);
        for (int ii = 1; ii <= numOfButtons; ii++) {
          changeLED(ii, 'g');
        }
        delay(150);
        currentCode = 0;
        submitStage = 0;
        codeGoal = 0;
        cstatus = -1;
      } else if (cstatus == 0){
        for (int ii = 1; ii <= numOfButtons; ii++) {
        changeLED(ii, 'r');
        }
        delay(150);
        for (int ii = 1; ii <= numOfButtons; ii++) {
          changeLED(ii, ' ');
        }
        delay(150);
        for (int ii = 1; ii <= numOfButtons; ii++) {
          changeLED(ii, 'r');
        }
        delay(150);
        currentCode = 0;
        submitStage = 0;
        codeGoal = 0;
        cstatus = -1;
      }      
    }

  
  // when submit button pressed
  if (!digitalRead(submitButton) && submitPressed) {
    if (submitStage == 0) {
//      Serial.print("currentCode: ");
//      Serial.print(currentCode);
//      Serial.println();
//      Serial.println("submit stage 0 to submit stage 1");

      for (int ii = 1; ii <= numOfButtons; ii++) {
        changeLED(ii, 'b');
      }
      delay(150);
      for (int ii = 1; ii <= numOfButtons; ii++) {
        changeLED(ii, ' ');
      }
      delay(150);
      for (int ii = 1; ii <= numOfButtons; ii++) {
        changeLED(ii, 'b');
      }
      delay(150);
      submitStage++;
    } else if (submitStage == 1) {
//      Serial.println("Submit stage 1 to stage 0");
//      Serial.print("currCode: ");
//      String code = String(currentCode);
      Serial.print("csub;");
      Serial.print(currentCode);
      Serial.print(";");
      Serial.println(bidGoals[codeGoal-1]);
//      Serial.write("\n");

      submitStage++;
    }
    submitPressed = false;

  } else if (digitalRead(submitButton) && !submitPressed) {
    submitPressed = true;
  }
}

// process billing mode
void processBidding() {
  //reset code mode things
  currentCode = 0;
  submitStage = 0;
  codeGoal = 0;
  disp.write(currentPrice);
  clearLEDs();
  for (int ii = 0; ii < numOfButtons; ii++) {
    if (buttonPressed(ii) != -1) {
      currentGoal = ii + 1;
    }
  }
  //update LEDs
  for (int goal = 0; goal < 5; goal++) {
    if (goalOwner[goal] == myTeam) {
      //owned by team
      changeLED(goal + 1, 'b');
    } else if (biddingPrice[goal] <= myScore && goalOwner[goal] != myEnemy && goalOwner[goal] != 'e') {
      // able to be bid (price less than score, owner isnt enemy)
      changeLED(goal + 1, 'g');
    } else if (goalOwner[goal] == 'e'){
      // enemy bid in progress
      changeLED(goal + 1, 'r', true);
    } else {
      changeLED(goal + 1, 'r');
    }
  }
  if (goalOwner[currentGoal-1] == 'n'){
    changeLED(currentGoal, 'b');
    currentPrice = biddingPrice[currentGoal-1];
  }
  
  
  // when button pressed
  if (!digitalRead(submitButton) && submitPressed) {
    Serial.print("bg;");
    Serial.println(bidGoals[currentGoal-1]);
//    Serial.write("\n");
    currentGoal = 0;
    submitPressed = false;
    for (int ii = 1; ii <= numOfButtons; ii++) {
      changeLED(ii, 'r');
    }
    delay(1000);
    for (int ii = 1; ii <= numOfButtons; ii++) {
      changeLED(ii, 'b');
    }
    delay(1000);
    for (int ii = 1; ii <= numOfButtons; ii++) {
      changeLED(ii, ' ');
    }
  } else if (digitalRead(submitButton) && !submitPressed) {
    submitPressed = true;
  }
}

void clearLEDs() {
  for (int ii = 1; ii <= numOfButtons; ii++) {
    changeLED(ii, ' ');
  }
}

// detect if a button was pressed
// returns number that the button represents.
// sad code but it works :(
int buttonPressed(int button) {
  int buttonVal = digitalRead(buttonPins[button]);
  if (!buttonVal && buttonWasPressed[button]) {
    //button released
    buttonWasPressed[button] = false;
    return button;
  } else if (buttonVal && !buttonWasPressed[button]) {
    //button initially pressed down
    buttonWasPressed[button] = true;
  }
  return -1;
}









int pins[] = {2, 3, 4, 5, 6, 7};
char goals[] = {'A', 'B', 'C', 'D', 'E', 'G'};
int states[] = {LOW, LOW, LOW, LOW, LOW, LOW};
//manually map out which pins correspond to which goal ids
  // 6 input pins for each Arduino board
  //2 Arduino Boards (ARDUINO NAME): GOLD and BLUE
  // GOAL ID: A, B, C, etc.
// read from each of those pins
// send message on pyserial
// "[ARDUINO NAME] [GOAL ID]" 
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // make the button's pin an input:
  for (int pin: pins) {
    pinMode(pin, INPUT);
  }
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  for (int i = 0; i < 6; i++) {
    int pinState = digitalRead(pins[i]);
    // print out the state of the button:
    if (pinState == LOW && states[i] == HIGH) {
      Serial.print("gold");
      Serial.println(goals[i]);
      states[i] = LOW;
    } else if (pinState == HIGH) {
      states[i] = HIGH;
    }
    Serial.println("hb");
  }
  delay(2);        // delay in between reads for stability
}

int pins[] = {2, 3, 4, 5, 6, 10};
char goals[] = {'A', 'B', 'C', 'D', 'E', 'G'};
int states[] = {LOW, LOW, LOW, LOW, LOW, LOW};
//map out which pins correspond to which goal ids
  // 6 input pins for each Arduino board
  //2 Arduino Boards (ARDUINO NAME): GOLD and BLUE
  // GOAL ID: A, B, C, etc.
void setup() {
  Serial.begin(9600);
  for (int pin: pins) {
    pinMode(pin, INPUT);
  }
}

void loop() {
  for (int i = 0; i < 6; i++) {
    int pinState = digitalRead(pins[i]);
    // to distinguish scoring from a sensor disconnect
    if (pinState == LOW && states[i] == HIGH) {
      Serial.print("gold");
      Serial.println(goals[i]);
      states[i] = LOW;
    } else if (pinState == HIGH) {
      states[i] = HIGH;
    }
  }
  //Serial.println("hb");
  delay(200);
}

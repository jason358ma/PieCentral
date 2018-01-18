int inPin = 4;
int sensorValue = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.print("memes");
  pinMode(inPin, INPUT);
  digitalWrite(inPin, HIGH); // turn on the pullup

  
}

void loop() {
  // put your main code here, to run repeatedly:
 sensorValue = digitalRead(inPin);
 Serial.println(sensorValue);
}


const int EXEC_PERIOD = 500; // [us]
const int soundPin    = A0;  // analogPin

unsigned long lastExecutionTime = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  while(micros() < lastExecutionTime + EXEC_PERIOD) {}
  lastExecutionTime = micros();

  Serial.println(analogRead(soundPin));
}
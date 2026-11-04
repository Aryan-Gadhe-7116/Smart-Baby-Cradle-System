#define SOUND_SENSOR A0

#define ENA 9
#define IN1 8
#define IN2 7
#define RELAY 4

int motorSpeed = 70;
int soundThreshold = 250;

bool motorRunning = false;
unsigned long soundStopTime = 0;

void setup() {

  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(RELAY, OUTPUT);

  // Motor OFF initially
  digitalWrite(RELAY, HIGH);
  analogWrite(ENA, 0);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  Serial.println("Baby Cradle Monitoring System Started");
}

void loop() {

  int sound = analogRead(SOUND_SENSOR);

  Serial.print("Sound Intensity: ");
  Serial.println(sound);

  if (sound > soundThreshold) {

    if (!motorRunning) {

      digitalWrite(RELAY, LOW);
      delay(100);

      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);

      analogWrite(ENA, motorSpeed);

      motorRunning = true;

      Serial.println("High Sound Detected - Motor Started");
    }

    soundStopTime = 0;
  }

  else {

    if (motorRunning) {

      if (soundStopTime == 0) {

        soundStopTime = millis();

        Serial.println("Sound Stopped - Waiting 1 Minute");
      }

      if (millis() - soundStopTime >= 60000) {

        analogWrite(ENA, 0);

        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);

        digitalWrite(RELAY, HIGH);

        motorRunning = false;
        soundStopTime = 0;

        Serial.println("No Sound for 1 Minute - Motor Stopped");
      }
    }
  }

  delay(100);
}

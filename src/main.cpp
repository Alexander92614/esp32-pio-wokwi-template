/*
 * ESP32 Serial Control for Wokwi
 *
 * Controls two LEDs based on commands from the Serial port.
 */

#include <Arduino.h>

// --- Pin Configuration ---
const int LED1 = 26;
const int LED2 = 27;

bool led1State = false;
bool led2State = false;

void sendLedStates() {
  Serial.print("LED1_");
  Serial.println(led1State ? "ON" : "OFF");
  Serial.print("LED2_");
  Serial.println(led2State ? "ON" : "OFF");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  digitalWrite(LED1, led1State);
  digitalWrite(LED2, led2State);
  Serial.println("ESP32 Ready. Send commands via Serial.");
  sendLedStates();
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    Serial.print("Received: ");
    Serial.println(line);

    if (line == "TOGGLE_1") {
      led1State = !led1State;
      digitalWrite(LED1, led1State);
      Serial.println("LED1 toggled");
      sendLedStates();
    } else if (line == "TOGGLE_2") {
      led2State = !led2State;
      digitalWrite(LED2, led2State);
      Serial.println("LED2 toggled");
      sendLedStates();
    } else if (line == "GET_STATE") {
      Serial.println("State requested");
      sendLedStates();
    }
  }
  // No delay needed, Serial event handling is fast
}
#include <Keyboard.h>
#include <ArduinoJson.h>
#include <Mouse.h>

void setup() {
  Serial1.begin(115200); // Communication with ESP8266
  Serial.begin(9600);    // For debugging
  Keyboard.begin();
  Mouse.begin();
}

void loop() {
  if (Serial1.available()) {
    String json = Serial1.readStringUntil('\n');
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, json);

    if (error) {
      Serial.println("Failed to parse JSON");
      return;
    }

    String command = doc["command"];
    String payload = doc["payload"];

    executeCommand(command, payload);
  }

  // Send any keystrokes back to ESP8266 if needed
  if (Serial.available()) {
    char c = Serial.read();
    DynamicJsonDocument doc(128);
    doc["type"] = "keystroke";
    doc["key"] = String(c);
    String json;
    serializeJson(doc, json);
    Serial1.println(json);
  }
}

void executeCommand(String command, String payload) {
  if (command == "STRING") {
    Keyboard.print(payload);
  } else if (command == "DELAY") {
    delay(payload.toInt());
  } else if (command == "ENTER") {
    Keyboard.write(KEY_RETURN);
  } else if (command == "GUI" || command == "WINDOWS") {
    Keyboard.press(KEY_LEFT_GUI);
    if (payload != "") Keyboard.print(payload);
    Keyboard.release(KEY_LEFT_GUI);
  } else if (command == "SHIFT") {
    Keyboard.press(KEY_LEFT_SHIFT);
    if (payload != "") Keyboard.print(payload);
    Keyboard.release(KEY_LEFT_SHIFT);
  } else if (command == "ALT") {
    Keyboard.press(KEY_LEFT_ALT);
    if (payload != "") Keyboard.print(payload);
    Keyboard.release(KEY_LEFT_ALT);
  } else if (command == "CTRL" || command == "CONTROL") {
    Keyboard.press(KEY_LEFT_CTRL);
    if (payload != "") Keyboard.print(payload);
    Keyboard.release(KEY_LEFT_CTRL);
  } else if (command == "CAPSLOCK") {
    Keyboard.write(KEY_CAPS_LOCK);
  } else if (command == "DELETE") {
    Keyboard.write(KEY_DELETE);
  } else if (command == "END") {
    Keyboard.write(KEY_END);
  } else if (command == "ESC" || command == "ESCAPE") {
    Keyboard.write(KEY_ESC);
  } else if (command == "HOME") {
    Keyboard.write(KEY_HOME);
  } else if (command == "INSERT") {
    Keyboard.write(KEY_INSERT);
  } else if (command == "PAGEUP") {
    Keyboard.write(KEY_PAGE_UP);
  } else if (command == "PAGEDOWN") {
    Keyboard.write(KEY_PAGE_DOWN);
  } else if (command == "TAB") {
    Keyboard.write(KEY_TAB);
  } else if (command == "SPACE") {
    Keyboard.write(' ');
  } else if (command == "REPEAT") {
    int times = payload.toInt();
    for (int i = 0; i < times; i++) {
      executeCommand(doc["lastCommand"], doc["lastPayload"]);
    }
  } else if (command == "MOUSEMOVE") {
    int commaIndex = payload.indexOf(',');
    if (commaIndex != -1) {
      int x = payload.substring(0, commaIndex).toInt();
      int y = payload.substring(commaIndex + 1).toInt();
      Mouse.move(x, y);
    }
  } else if (command == "MOUSECLICK") {
    if (payload == "LEFT") Mouse.click(MOUSE_LEFT);
    else if (payload == "RIGHT") Mouse.click(MOUSE_RIGHT);
    else if (payload == "MIDDLE") Mouse.click(MOUSE_MIDDLE);
  }
}

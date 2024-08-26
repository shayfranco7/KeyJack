#include <hidboot.h>
#include <usbhub.h>
#include "Keyboard.h"

//#define Serial Serial1


// Satisfy the IDE, which needs to see the include statement in the ino too.
#ifdef dobogusinclude
  #include <spi4teensy3.h>
  #include <SPI.h>
#endif

#include <SPI.h>
#include <SD.h>
#define MAX_RESET 7 // MAX3421E pin 12
#define MAX_GPX 8   // MAX3421E pin 17

bool shift = false;

USB Usb;
HIDBoot<USB_HID_PROTOCOL_KEYBOARD> HidKeyboard(&Usb);
uint32_t next_time;

class KbdRptParser : public KeyboardReportParser {
  public:
    uint8_t _parse(uint8_t key);
    String _getChar(uint8_t key);
  protected:
    void OnControlKeysChanged(uint8_t before, uint8_t after);
    void OnKeyDown(uint8_t mod, uint8_t key);
    void OnKeyUp(uint8_t mod, uint8_t key);
    void OnKeyPressed(uint8_t key);
    void _press(uint8_t key);
    void _release(uint8_t key);
};

void KbdRptParser::OnKeyDown(uint8_t mod, uint8_t key) {
  int parsedKey = _parse(key);
  if (parsedKey == key) {
    uint8_t c = OemToAscii(mod, key);
    OnKeyPressed(c);
    if (c != 0x20 && c != 0x00) _press(c);
    else _press(key);
  } else _press(parsedKey);
}

void KbdRptParser::OnKeyUp(uint8_t mod, uint8_t key) {
  int parsedKey = _parse(key);
  if (parsedKey == key) {
    uint8_t c = OemToAscii(mod, key);
    OnKeyPressed(c);
    if (c != 0x20 && c != 0x00) {
      _release(c);
      Serial.print((char)c);
    } else {
      _release(key);
      Serial.print("0x");
      Serial.print(key, HEX);
    }
  } else {
    _release(parsedKey);
    Serial.print(_getChar(key));
  }
}

void KbdRptParser::OnControlKeysChanged(uint8_t before, uint8_t after) {
  MODIFIERKEYS beforeMod;
  *((uint8_t*)&beforeMod) = before;

  MODIFIERKEYS afterMod;
  *((uint8_t*)&afterMod) = after;

  // left
  if (beforeMod.bmLeftCtrl != afterMod.bmLeftCtrl) {
    if (afterMod.bmLeftCtrl) Keyboard.press(KEY_LEFT_CTRL);
    else Keyboard.release(KEY_LEFT_CTRL);
    Serial.print("<ctrl " + (String)afterMod.bmLeftCtrl + ">");
  }

  if (beforeMod.bmLeftShift != afterMod.bmLeftShift) {
    if (afterMod.bmLeftShift) Keyboard.press(KEY_LEFT_SHIFT);
    else Keyboard.release(KEY_LEFT_SHIFT);
    shift = afterMod.bmLeftShift;
    // Serial.print("<shift "+(String)afterMod.bmLeftShift+">");
  }

  if (beforeMod.bmLeftAlt != afterMod.bmLeftAlt) {
    if (afterMod.bmLeftAlt) Keyboard.press(KEY_LEFT_ALT);
    else Keyboard.release(KEY_LEFT_ALT);
    Serial.print("<alt " + (String)afterMod.bmLeftAlt + ">");
  }

  if (beforeMod.bmLeftGUI != afterMod.bmLeftGUI) {
    if (afterMod.bmLeftGUI) Keyboard.press(KEY_LEFT_GUI);
    else Keyboard.release(KEY_LEFT_GUI);
    Serial.print("<gui " + (String)afterMod.bmLeftGUI + ">");
  }

  // right
  if (beforeMod.bmRightCtrl != afterMod.bmRightCtrl) {
    if (afterMod.bmRightCtrl) Keyboard.press(KEY_RIGHT_CTRL);
    else Keyboard.release(KEY_RIGHT_CTRL);
    Serial.print("<ctrl " + (String)afterMod.bmRightCtrl + ">");
  }

  if (beforeMod.bmRightShift != afterMod.bmRightShift) {
    if (afterMod.bmRightShift) Keyboard.press(KEY_RIGHT_SHIFT);
    else Keyboard.release(KEY_RIGHT_SHIFT);
    shift = afterMod.bmLeftShift;
    // Serial.print("<shift "+(String)afterMod.bmRightShift+">");
  }

  if (beforeMod.bmRightAlt != afterMod.bmRightAlt) {
    if (afterMod.bmRightAlt) Keyboard.press(KEY_RIGHT_ALT);
    else Keyboard.release(KEY_RIGHT_ALT);
    Serial.print("<alt " + (String)afterMod.bmRightAlt + ">");
  }

  if (beforeMod.bmRightGUI != afterMod.bmRightGUI) {
    if (afterMod.bmRightGUI) Keyboard.press(KEY_RIGHT_GUI);
    else Keyboard.release(KEY_RIGHT_GUI);
    Serial.print("<gui " + (String)afterMod.bmRightGUI + ">");
  }
}

void KbdRptParser::OnKeyPressed(uint8_t key) {
  // Serial.print("ASCII: \"");
  // Serial.print((char)key);
  /*Serial.print("\" = 0x");
  Serial.print(key, HEX);
  Serial.print("; ");*/
};

uint8_t KbdRptParser::_parse(uint8_t key) {
  /*
  Serial.print("0x");
  Serial.print(key, HEX);
  Serial.print(" = ");*/
  switch (key) {
    case 0x2C: return 0x20; break; // SPACE
    case 40: return KEY_RETURN; break;
    case 41: return KEY_ESC; break;
    case 42: return KEY_BACKSPACE; break;
    case 43: return KEY_TAB; break;
    case 58: return KEY_F1; break;
    case 59: return KEY_F2; break;
    case 60: return KEY_F3; break;
    case 61: return KEY_F4; break;
    case 62: return KEY_F5; break;
    case 63: return KEY_F6; break;
    case 64: return KEY_F7; break;
    case 65: return KEY_F8; break;
    case 66: return KEY_F9; break;
    case 67: return KEY_F10; break;
    case 68: return KEY_F11; break;
    case 69: return KEY_F12; break;
    case 73: return KEY_INSERT; break;
    case 74: return KEY_HOME; break;
    case 75: return KEY_PAGE_UP; break;
    case 76: return KEY_DELETE; break;
    case 77: return KEY_END; break;
    case 78: return KEY_PAGE_DOWN; break;
    case 79: return KEY_RIGHT_ARROW; break;
    case 80: return KEY_LEFT_ARROW; break;
    case 81: return KEY_DOWN_ARROW; break;
    case 82: return KEY_UP_ARROW; break;
    case 88: return KEY_RETURN; break;
    //=====[DE-Keyboard]=====//
    case 0x64: return 236; break; //
    case 0x32: return 92; break; // #
    //======================//
    default: {
      // Serial.print(" N/A ");
      return key;
    }
  }
}

String KbdRptParser::_getChar(uint8_t key) {
  switch (key) {
    case 0x2C: return " "; break;
    case 40: return "<RETURN>\n"; break;
    case 41: return "<ESC>\n"; break;
    case 42: return "<BACKSPCAE>"; break;
    case 43: return "<TAB>\n"; break;
    case 58: return "<F1>\n"; break;
    case 59: return "<F2>\n"; break;
    case 60: return "<F3>\n"; break;
    case 61: return "<F4>\n"; break;
    case 62: return "<F5>\n"; break;
    case 63: return "<F6>\n"; break;
    case 64: return "<F7>\n"; break;
    case 65: return "<F8>\n"; break;
    case 66: return "<F9>\n"; break;
    case 67: return "<F10>\n"; break;
    case 68: return "<F11>\n"; break;
    case 69: return "<F12>\n"; break;
    case 73: return "<INSERT>"; break;
    case 74: return "<HOME>\n"; break;
    case 75: return "<PAGE_UP>\n"; break;
    case 76: return "<DELETE>"; break;
    case 77: return "<END>\n"; break;
    case 78: return "<PAGE_DOWN>\n"; break;
    case 79: return "<RIGHT_ARROW>\n"; break;
    case 80: return "<LEFT_ARROW>\n"; break;
    case 81: return "<DOWN_ARROW>\n"; break;
    case 82: return "<UP_ARROW>\n"; break;
    case 88: return "<RETURN>\n"; break;
    //=====[DE-Keyboard]=====//
    case 0x64: {
      if (shift) return "<";
      else return ">";
      break;
    }
    case 0x32: {
      if (shift) return "'";
      else return "#";
      break;
    }
    //======================//
    default: {
      return "";
    }
  }
}

void KbdRptParser::_press(uint8_t key) {
  /*Serial.print("0x");
  Serial.print(key, HEX);
  Serial.println(" DOWN");*/
  Keyboard.press(key);
}

void KbdRptParser::_release(uint8_t key) {
  /*Serial.print("0x");
  Serial.print(key, HEX);
  Serial.println(" UP");
  Serial.println();*/
  Keyboard.release(key);
}

KbdRptParser parser;

void setup() {
  pinMode(MAX_GPX, INPUT);
  pinMode(MAX_RESET, OUTPUT);
  digitalWrite(MAX_RESET, LOW);
  delay(20); // wait 20ms
  digitalWrite(MAX_RESET, HIGH);
  delay(20); // wait 20ms
  Serial1.begin(115200);
  Serial.begin(115200);
  Keyboard.begin();
  delay(2000);

  if (Usb.Init() == -1) Serial.println("OSC did not start.");

  delay(200);

  next_time = millis() + 5000;

  HidKeyboard.SetReportParser(0, &parser);
}

void loop() {
  Usb.Task();
  receiveDataFromNodeMCU();
}

void receiveDataFromNodeMCU() {
  if (Serial1.available()) {
    String receivedData = Serial1.readString();
    //Serial.print(receivedData);
    //receivedData.trim();

    // Process the received data
    processReceivedData(receivedData);
  }
}

void processReceivedData(const String& data) {
  // Handle the received data here
  //Serial.println(data);
      String cmd = "";
        for(int i = 0; i<data.length(); i++){
          cmd = "";
          while(data.charAt(i) != '\n'){
            cmd += data.charAt(i);
            i++;
          }
            executeDuckyCommand(cmd);
            delay(100);
        }
  // Parse and execute Ducky Script commands
  executeDuckyCommand(data);
}
/*
void executeDuckyScript(const String& script) {
  String command;
  int index = 0;

  while ((index = script.indexOf('\n')) != -1) {
    command = script.substring(0, index);

    script.remove(0, index + 1);
    executeDuckyCommand(command);
  }
  if (script.length() > 0) {
    executeDuckyCommand(script);
  }
}
*/
void executeDuckyCommand(const String& command) {
  //Serial.print(command);
  //Serial.print("end");
  if (command.startsWith("STRING ")) {
      Serial.print("in string");
      //Serial.println(command);
      String s = "";
      int i = 0;
      for(; i < 50; i++)
      {
         s += command.charAt(i);

      }
      Serial.print(s.substring(7));
      //Keyboard.print(s.substring(7));
      delay(200);


      for(; i < command.length() - (command.length() % 50); i+= 50)
      {
        String temp = "";
        for(int j = i; j < i+50; j++){
           temp += command.charAt(j);
        }
          //Keyboard.print(temp);
          Serial.print(temp);
        delay(200);
      }
      String temp = "";
      for(; i < command.length(); i++){
         temp += command.charAt(i);
      }
    //Keyboard.print(temp);
    Serial.print(temp);
    //Serial.print("\n");

  } else if (command.startsWith("DELAY")) {
    //Serial.println(command);
    int delayTime = command.substring(6).toInt();
    delay(delayTime);
  } else if (command.startsWith("ENTER")) {
    //Serial.println(command);
    Keyboard.press(KEY_RETURN);
    Keyboard.release(KEY_RETURN);
  } else if (command.startsWith("TAB")) {
    Keyboard.press(KEY_TAB);
    Keyboard.release(KEY_TAB);
  } else if (command.startsWith("ESCAPE")) {
    Keyboard.press(KEY_ESC);
    Keyboard.release(KEY_ESC);
  } else if (command.startsWith("BACKSPACE")) {
    Keyboard.press(KEY_BACKSPACE);
    Keyboard.release(KEY_BACKSPACE);
  } else if (command.startsWith("UPARROW")) {
    Keyboard.press(KEY_UP_ARROW);
    Keyboard.release(KEY_UP_ARROW);
  } else if (command.startsWith("DOWNARROW")) {
    Keyboard.press(KEY_DOWN_ARROW);
    Keyboard.release(KEY_DOWN_ARROW);
  } else if (command.startsWith("LEFTARROW")) {
    Keyboard.press(KEY_LEFT_ARROW);
    Keyboard.release(KEY_LEFT_ARROW);
  } else if (command.startsWith("RIGHTARROW")) {
    Keyboard.press(KEY_RIGHT_ARROW);
    Keyboard.release(KEY_RIGHT_ARROW);
  } else if (command.startsWith("CTRL")) {
    Keyboard.press(KEY_LEFT_CTRL);
    Keyboard.release(KEY_LEFT_CTRL);
  } else if (command.startsWith("SHIFT")) {
    Keyboard.press(KEY_LEFT_SHIFT);
    Keyboard.release(KEY_LEFT_SHIFT);
  } else if (command.startsWith("ALT")) {
    Keyboard.press(KEY_LEFT_ALT);
    Keyboard.release(KEY_LEFT_ALT);
  } else if (command.startsWith("GUI r")) {
    //Serial.println(command);
    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press(0x72);
    Keyboard.release(KEY_LEFT_GUI);
    Keyboard.release(0x72);
  } else {
     Serial.println("Unknown command: ");
     Serial.print(command);
  }
}

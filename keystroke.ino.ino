#include <Keyboard.h>

void setup() {
  Serial1.begin(115200); // Initialize Serial1 with the desired baud rate
  Keyboard.begin();
}

void loop() {
  if (Serial1.available()) {  // Check if data is available from Serial1
    char keystroke = Serial1.read();  // Read the keystroke from Serial1
    Keyboard.write(keystroke);  // Send the keystroke to the computer
    Serial1.print("Sent keystroke: ");
    Serial1.println(keystroke);  // Print the sent keystroke to Serial1 for debugging
  }
}

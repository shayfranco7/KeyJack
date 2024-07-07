#include <SoftwareSerial.h> // Include the SoftwareSerial library for communication with ESP8266
#include <Keyboard.h>       // Include the Keyboard library for Leonardo

// SoftwareSerial pins
#define RX_PIN 10
#define TX_PIN 11

SoftwareSerial espSerial(RX_PIN, TX_PIN); // RX, TX

// WiFi credentials
const char* ssid = "Shays iphone"; // Replace with your Wi-Fi SSID
const char* password = "shayfranco1"; // Replace with your Wi-Fi password

// Server credentials
WiFiServer server(10319); // Port to listen on

void setup() {
  Serial.begin(115200);
  espSerial.begin(115200); // Initialize ESP8266 serial communication
  delay(10);

  // Connect to Wi-Fi
  Serial.printf("Connecting to %s ", ssid);
  sendCommand("AT+RST\r\n"); // Reset ESP8266
  sendCommand("AT+CWMODE=1\r\n"); // Set ESP8266 to station mode
  sendCommand("AT+CWJAP=\""+String(ssid)+"\",\""+String(password)+"\"\r\n"); // Connect to Wi-Fi
  Serial.println(" connected.");

  // Start the server
  server.begin();
  Serial.println("Server started");

  // Initialize keyboard
  Keyboard.begin();
}

void loop() {
  WiFiClient client = server.available();   // Listen for incoming clients

  if (client) {                             // If a new client connects,
    Serial.println("New client connected");
    while (client.connected()) {            // loop while the client's connected
      while (client.available()) {          // if there's bytes to read from the client,
        String command = client.readStringUntil('\n'); // read a line
        command.trim();                     // Remove any leading/trailing whitespace
        executeCommand(command.c_str());
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}

void executeCommand(const char* command) {
  String cmd = command;

  if (cmd.startsWith("DELAY ")) {
    int delayTime = cmd.substring(6).toInt();
    delay(delayTime);
  } else if (cmd.startsWith("STRING ")) {
    String text = cmd.substring(7);
    Keyboard.print(text);
  } else if (cmd == "ENTER") {
    Keyboard.write(KEY_RETURN); // Use KEY_RETURN instead of KEY_ENTER for Leonardo
  }
}

void sendCommand(String command) {
  espSerial.print(command);
  delay(100);
  while (espSerial.available()) {
    String response = espSerial.readStringUntil('\n');
    Serial.println(response);
  }
}

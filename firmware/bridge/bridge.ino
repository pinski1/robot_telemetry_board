
//#define TESTING 1
#ifdef TESTING
#define SERIAL_FORMAT SERIAL_8N1
#else
#define SERIAL_FORMAT SERIAL_8N1_RXINV_TXINV
#endif
#define SERIAL_BUFFER_SIZE 256

HardwareSerial *serial;

struct vescData {
  char vescnum;
  HardwareSerial *serial;
};

struct vescData vescs[4] =
  {{0, &Serial2},
   {1, &Serial3},
   {2, &Serial5},
   {3, &Serial7}};

void setup() {
  // Debug serial is always the default
  Serial.begin(115200);
  // VESC serials depend on whether we need inverted signals or not
  Serial2.begin(115200, SERIAL_FORMAT);
  Serial3.begin(115200, SERIAL_FORMAT);
  Serial5.begin(115200, SERIAL_FORMAT);
  Serial7.begin(115200, SERIAL_FORMAT);
  delay(5000);
  Serial.print("Serial intialized\n");
}

void loop() {
  /* Variables that need to persist across iterations of the main loop */
  static int vescbridge = 0;
  if (vescbridge < 0 || vescbridge > 3) {
    Serial.print("Vescbridge value out of range. Unknown value:");
    Serial.print(vescbridge);
    delay(5000);
  }

  while (vescs[vescbridge].serial->available()) {
    Serial.write(vescs[vescbridge].serial->read());
  }
  while (Serial.available()) {
    vescs[vescbridge].serial->write(Serial.read());
  }
}

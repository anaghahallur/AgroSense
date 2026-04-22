/*
  AgroSense ESP32 Firmware v2.0
  Reads Soil Moisture (YL-69) on D34
  Reads Temperature (Thermistor 10k) on D35
*/

const int moisturePin = 34;
const int tempPin = 35;

// Thermistor Parameters
const float B = 3950;       // Beta coefficient
const float R0 = 10000;     // Resistance at 25C
const float T0 = 298.15;    // 25C in Kelvin

void setup() {
  Serial.begin(115200);
  pinMode(moisturePin, INPUT);
  pinMode(tempPin, INPUT);
  Serial.println("{\"status\": \"initialized\"}");
}

void loop() {
  // 1. Soil Moisture
  int rawMoisture = analogRead(moisturePin);
  int moisturePercent = map(rawMoisture, 4095, 0, 0, 100);
  moisturePercent = constrain(moisturePercent, 0, 100);

  // 2. Temperature
  int rawTemp = analogRead(tempPin);
  // Calculate resistance from voltage divider
  float vOut = rawTemp * (3.3 / 4095.0);
  float rTherm = (3.3 * 10000.0) / vOut - 10000.0;
  
  // Beta formula
  float tempK = 1.0 / (1.0/T0 + log(rTherm/R0)/B);
  float tempC = tempK - 273.15;

  // 3. Output JSON
  Serial.print("{\"moisture\": ");
  Serial.print(moisturePercent);
  Serial.print(", \"temp\": ");
  Serial.print(tempC);
  Serial.println("}");

  delay(1000);
}

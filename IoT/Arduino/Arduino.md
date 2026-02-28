# Arduino Documentation

## 1. Origin of Arduino

**Arduino** is an open-source electronics platform based on easy-to-use hardware and software.

- **Founded:** 2005  
- **Origin:** Interaction Design Institute Ivrea (Italy)  
- **Founders:** Massimo Banzi, David Cuartielles, Tom Igoe, Gianluca Martino, David Mellis  
- **Purpose:** Make microcontroller development accessible to students, artists, and hobbyists  

Arduino was created to simplify embedded systems development by combining affordable hardware with a beginner-friendly programming environment.

---

## 2. What is Arduino?

Arduino is both:

- A **hardware platform** (microcontroller development boards)
- A **software platform** (Arduino IDE)

It allows users to read inputs (sensors, buttons) and control outputs (LEDs, motors, displays).

---

## 3. Arduino Architecture

Most classic Arduino boards are based on **Microchip ATmega** microcontrollers (AVR architecture).

### Core Components on a Board

- Microcontroller (e.g., ATmega328P)
- USB-to-Serial converter
- Voltage regulator
- Digital I/O pins
- Analog input pins
- Power pins
- Crystal oscillator

---

## 4. Popular Arduino Boards

### 4.1 Arduino Uno
- Microcontroller: ATmega328P
- Clock: 16 MHz
- Digital I/O Pins: 14
- Analog Inputs: 6
- Flash Memory: 32 KB
- Most widely used board

### 4.2 Arduino Nano
- Smaller version of Uno
- Breadboard friendly
- Same ATmega328P microcontroller

### 4.3 Arduino Mega 2560
- Microcontroller: ATmega2560
- 54 digital I/O pins
- 16 analog inputs
- 256 KB Flash
- Suitable for larger projects

### 4.4 Arduino Leonardo
- Microcontroller: ATmega32U4
- Built-in USB capability
- Can act as keyboard/mouse

### 4.5 Arduino Due
- Microcontroller: ARM Cortex-M3 (ATSAM3X8E)
- 32-bit architecture
- 84 MHz clock
- 3.3V logic

### 4.6 Arduino MKR Series
- Designed for IoT
- Built-in Wi-Fi / GSM / LoRa (varies by model)
- ARM Cortex-M0+

---

## 5. Key Features

### Hardware Features
- Digital input/output
- Analog input (10-bit ADC on AVR boards)
- PWM outputs
- SPI, I2C, UART communication
- External interrupts
- Timers and counters

### Software Features
- Simple C/C++ based programming
- Extensive built-in libraries
- Cross-platform IDE (Windows, macOS, Linux)
- Large community support

---

## 6. Arduino Programming Model

Arduino programs are called **sketches**.

Every sketch contains:

```cpp
void setup() {
  // Runs once at startup
}

void loop() {
  // Runs repeatedly
}

## Example Blink LED
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
```
## 7. Communication Interfaces
- UART (Serial)
- SPI
- I2C (TWI)
- USB
- CAN
## 8. Memory (Arduino Uno Example)
- FLASH: 32 KB
- SRAM: 2 KB
- EEPROM 1 KB
Memory is limited, so efficient coding is important.

## 9. Power Options
- USB (5V)
- External DC Jack (7–12V recommended)
- VIN Pin
- 5V Pin
# 10. Shields and Ecosystem
Arduino supports expansion boards called Shields:
- Ethernet Shield
- Wifi Shield
- Motor Driver Shield
- LCD Shield
- GSM Shield
- Sensors Shield
Large third-party ecosystem available.
# 11. Common Applications
- Robotics
- Sensor systems
- Educational Projects
- Hobby Projects
- Home automation
# 12. Advantages
-Beginner friendly
- Massive community
- Wide hardware compatibility
- Open-source hardware & software
# 13. Limitations
- Limited RAM (AVR boards)
- Lower processing power (8-bit AVR)
- Not ideal for heavy networking tasks
# 14 Arduino Comparison

| Feature      | Arduino Uno | ESP8266       | ESP32                |
| ------------ | ----------- | ------------- | -------------------- |
| Architecture | 8-bit AVR   | 32-bit Xtensa | 32-bit Xtensa/RISC-V |
| Wi-Fi        | No          | Yes           | Yes                  |
| Bluetooth    | No          | No            | Yes                  |
| Clock Speed  | 16 MHz      | 80–160 MHz    | Up to 240 MHz        |
| RAM          | 2 KB        | ~50 KB        | > 300 KB             |

# 15. Conclusion

Arduino is one of the most influential open-source hardware platforms ever created. It democratized electronics development and remains a top choice for learning embedded systems, rapid prototyping, and educational projects worldwide.

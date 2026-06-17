# IoT Security Scanning

Siyarix includes IoT security analysis covering firmware inspection, serial port enumeration, and device type identification. An enhanced `IoTScanner` with broader protocol support and hardware analysis is planned for a future release.

---

## Firmware Analysis

```bash
# Analyze firmware for security issues
siyarix run "scan IoT device firmware backup.bin"

# Natural language
siyarix run "analyze firmware file firmware.bin for vulnerabilities"
```

### Indicators Checked (16 Total)

| Indicator | What It Detects | Severity |
|-----------|----------------|----------|
| Hardcoded credentials | Plain-text passwords in firmware | CRITICAL |
| Debug mode enabled | Debug interfaces left active | HIGH |
| Telnet enabled | Unencrypted remote access | HIGH |
| Embedded certificates | Hardcoded TLS certificates | MEDIUM |
| OTA over HTTP | Firmware updates over cleartext | HIGH |
| UART/JTAG exposed | Hardware debug interfaces | MEDIUM |
| Hardcoded API keys | Embedded cloud service keys | CRITICAL |
| Default SSH keys | Known default SSH host keys | CRITICAL |

---

## Serial Port Scanning

```bash
# Scan IoT device serial interfaces
siyarix run "scan serial ports on IoT device"
```

Automatically detects baud rates across 12 standard rates (300 to 921600 baud).

---

## Device Type Detection

The scanner identifies device types from firmware characteristics:

| Device Type | Indicators |
|-------------|------------|
| ESP32 | ESP32-specific strings, WiFi libraries |
| Arduino | Arduino bootloader, avr-gcc strings |
| STM32 | STM32 HAL libraries, ARM Cortex-M strings |
| Raspberry Pi | BCM2835, Raspberry Pi kernel strings |
| Nordic nRF5x | SoftDevice, nRF5 SDK strings |

---

## Binary Analysis

Detects firmware image types:

- ELF binaries
- GZip compressed images
- UBIFS filesystem images
- Raw binary images

---

## Usage

```bash
# Full IoT assessment
siyarix run "scan IoT devices on the local network"

# Firmware analysis only
siyarix run "analyze firmware file firmware.bin for vulnerabilities"

# Serial port enumeration
siyarix run "enumerate serial ports on target device"
```

---

## Reporting

```bash
# Generate IoT security report
siyarix report generate --format html --include iot
```

---

## Planned Enhancements

A comprehensive `IoTScanner` is planned with:

- MQTT/CoAP protocol analysis
- Zigbee/Z-Wave radio analysis
- Real-time firmware emulation
- Hardware attack surface mapping
- OWASP IoT Top 10 coverage

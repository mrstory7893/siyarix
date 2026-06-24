# IoT Security Scanning (Under Active Development)

Siyarix's IoT security scanning capability is currently under active development. An `IoTScanner` stub has been created, and the full implementation — including firmware analysis, serial port scanning, and device detection — is on the roadmap.

---

## Current Status

An `IoTScanner` class exists as a stub. It accepts a target path and returns an empty result set. No actual firmware analysis, serial enumeration, or device identification has been implemented yet.

```python
from siyarix.chat.stubs import IoTScanner

scanner = IoTScanner()
result = scanner.scan_firmware("firmware.bin")
# result == {}  (stub - returns empty)
```

---

## Planned Capabilities

The IoT scanner roadmap includes:

### Firmware Analysis

- **Hardcoded credentials**: Detect embedded passwords and secrets
- **Debug interfaces**: Identify debug modes left active in production builds
- **Certificate inspection**: Find hardcoded TLS certificates and keys
- **OTA security**: Verify firmware update mechanisms

### Serial Port Scanning

- **Baud rate detection**: Auto-detect across standard rates
- **Interface enumeration**: Identify UART, JTAG, and SPI interfaces
- **Protocol identification**: Detect common IoT protocols

### Device Type Detection

- **Chipset identification**: ESP32, Arduino, STM32, Raspberry Pi, Nordic nRF5x
- **Binary analysis**: ELF, GZip, UBIFS, raw binary images
- **OS fingerprinting**: RTOS, embedded Linux, bare-metal

---

## Stay Tuned

The IoT scanner is being actively developed. Updates on supported device types, firmware formats, and release timelines will be shared as the implementation progresses.

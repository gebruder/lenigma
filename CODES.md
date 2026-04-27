# Error code reference

Auto-generated from `codes.json` by `tools/gen_codes_md.py`. If you edit `codes.json`, regenerate this file.

**204 codes** across 9 categories.

## Categories

- [BIOS](#bios) — 17 codes
- [Fans](#fans) — 27 codes
- [Power Supply](#power-supply) — 34 codes
- [Storage](#storage) — 5 codes
- [System](#system) — 8 codes
- [System Voltages & Power](#system-voltages-power) — 42 codes
- [Thermal](#thermal) — 55 codes
- [ThinkPad](#thinkpad) — 10 codes
- [USB](#usb) — 6 codes

## BIOS

| Code | Severity | Description | Solutions |
|------|----------|-------------|-----------|
| `B0xx` | critical | System halted during POST; the last two hex digits identify the POST stage | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `B201` | warn | Intel Management Engine reported a warning | — |
| `B202` | error | Intel Management Engine reported an error | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `B2Fx` | info | Intel Management Engine reset; the last hex digit identifies the reason | — |
| `B4FF` | critical | Simulated critical error (test harness only; not a real fault) | No action required.<br>If this were a real event, suggested actions to resolve the event would be listed in this section. |
| `B4x0` | error | Option ROM failed to initialise; the second hex digit is the slot | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>If the device listed in error title remains in the system, remove the device, or disable in BIOS setup.<br>Contact Lenovo service. |
| `B4x1` | error | Storage controller option ROM failed to initialise; the second hex digit is the slot | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>If the device listed in error title remains in the system, remove the device, or disable in BIOS setup.<br>Contact Lenovo service. |
| `B4x2` | error | Network card option ROM failed to initialise; the second hex digit is the slot | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>If the device listed in error title remains in the system, remove the device, or disable in BIOS setup.<br>Contact Lenovo service. |
| `B4x3` | error | Video card option ROM failed to initialise; the second hex digit is the slot | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>If the device listed in error title remains in the system, remove the device, or disable in BIOS setup.<br>Contact Lenovo service. |
| `B4x4` | error | I/O bus option ROM failed to initialise; the second hex digit is the slot | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>If the device listed in error title remains in the system, remove the device, or disable in BIOS setup.<br>Contact Lenovo service. |
| `B500` | info | Recorded model or serial number has changed since last boot | — |
| `B501` | warn | Installed hardware may draw more than the power supply can deliver | — |
| `B69x` | info | Faulty memory row on a CPU 1 DIMM was not repaired; the last hex digit is the DIMM slot | — |
| `B6Ax` | info | Faulty memory row on a CPU 2 DIMM was not repaired; the last hex digit is the DIMM slot | — |
| `B6xx` | info | A faulty memory row was repaired in place | — |
| `B7xx` | warn | Memory subsystem warning; the last two hex digits identify the specific fault | — |
| `B8xx` | critical | Critical memory error; system cannot continue | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove and reinstall all DIMMs to ensure good connection.<br>Remove all but one DIMM. If diagnostic alert continues, swap with another DIMM. Add back DIMMs one at a time to determine problem DIMM.<br>Swap CPU1 and CPU2. If only one CPU, reseat the CPU.  WARNING: Care must be taken when removing/addings CPUs.  If not familiar with this process, skip this step.<br>Contact Lenovo service. |

## Fans

| Code | Severity | Description | Solutions |
|------|----------|-------------|-----------|
| `F110` | warn | CPU 1 fan is running outside its expected speed range | — |
| `F111` | error | CPU 1 fan has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F120` | warn | CPU 2 fan is running outside its expected speed range | — |
| `F121` | error | CPU 2 fan has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F210` | warn | Upper front fan is running outside its expected speed range | — |
| `F211` | error | Upper front fan has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F220` | warn | Lower front fan is running outside its expected speed range | — |
| `F221` | error | Lower front fan has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F230` | warn | Rear fan is running outside its expected speed range | — |
| `F231` | error | Rear fan has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F240` | warn | Upper memory fan is running outside its expected speed range | — |
| `F241` | error | Upper memory fan has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F250` | warn | Lower memory fan is running outside its expected speed range | — |
| `F251` | error | Lower memory fan has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F310` | warn | Front fan is running outside its expected speed range | — |
| `F311` | error | Front fan has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F320` | warn | Rear fan 1 is running outside its expected speed range | — |
| `F321` | error | Rear fan 1 has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F330` | warn | Rear fan 2 is running outside its expected speed range | — |
| `F331` | error | Rear fan 2 has failed | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F410` | warn | Power supply fan 1 is running outside its expected speed range | — |
| `F411` | error | Power supply fan 1 has failed | Check for foreign object in power supply inlet inside the computer.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F420` | warn | Power supply fan 2 is running outside its expected speed range | — |
| `F421` | error | Power supply fan 2 has failed | Check for foreign object in power supply inlet inside the computer.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F430` | warn | Power supply fan is running outside its expected speed range | — |
| `F431` | error | Power supply fan has failed | Check for foreign object in power supply inlet inside the computer.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |
| `F5x1` | error | Quad M.2 adapter fan has failed; the second hex digit is the adapter index | Check for foreign object in fan.<br>Check that all fans are connected.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Contact Lenovo service. |

## Power Supply

| Code | Severity | Description | Solutions |
|------|----------|-------------|-----------|
| `P100` | warn | AC input voltage is below tolerance | — |
| `P101` | warn | AC input voltage is critically low; system may shut down | Check the power cord, outlet, and circuit breaker.<br>Try a different outlet.<br>If the power circuit is subject to regular disturbance (brown-out), consider a battery back-up unit.<br>Contact Lenovo service. |
| `P110` | critical | A power-supply output rail is critically low | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P120` | critical | A power-supply output rail is critically high | Contact Lenovo service. |
| `P131` | warn | CPU 1 power draw is high | — |
| `P132` | warn | Memory power draw is high | — |
| `P133` | warn | CPU 2 power draw is high | — |
| `P134` | warn | USB and other internal board components are drawing high power | — |
| `P135` | warn | Expansion slots 6, 7, 8 are drawing high power | — |
| `P136` | warn | Expansion slots 1, 2, 3, 4, 5 are drawing high power | — |
| `P137` | warn | Aux power cables P4 and P5 are delivering high current | — |
| `P138` | warn | Aux power cable P2 is delivering high current | — |
| `P139` | warn | Aux power cable P3 is delivering high current | — |
| `P141` | critical | CPU 1 power draw is critically high | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P142` | critical | Memory power draw is critically high | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P143` | critical | CPU 2 power draw is critically high | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P144` | critical | USB and other internal board components are drawing critically high power | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P145` | critical | Expansion slots 6, 7, 8 are drawing critically high power | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P146` | critical | Expansion slots 1, 2, 3, 4, 5 are drawing critically high power | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P147` | critical | Aux power cables P4 and P5 are delivering critically high current | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P148` | critical | Aux power cable P2 is delivering critically high current | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P149` | critical | Aux power cable P3 is delivering critically high current | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `P150` | warn | Total system power draw is high | — |
| `P151` | error | Total system power draw is critically high | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Evaluate total system power, and reduce device or replace devices with lower power alternatives.<br>Continued alerts indicate a condition that could reduce the life of the power supply, or other system components.<br>Contact Lenovo service. |
| `P210` | warn | Total system power draw is high | — |
| `P211` | error | Total system power draw is critically high | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Evaluate total system power, and reduce device or replace devices with lower power alternatives.<br>Continued alerts indicate a condition that could reduce the life of the power supply, or other system components.<br>Contact Lenovo service. |
| `P220` | warn | Total system power draw is high | — |
| `P221` | error | Total system power draw is critically high | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Evaluate total system power, and reduce device or replace devices with lower power alternatives.<br>Continued alerts indicate a condition that could reduce the life of the power supply, or other system components.<br>Contact Lenovo service. |
| `P230` | warn | Total system power draw is high | — |
| `P231` | error | Total system power draw is critically high | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Evaluate total system power, and reduce device or replace devices with lower power alternatives.<br>Continued alerts indicate a condition that could reduce the life of the power supply, or other system components.<br>Contact Lenovo service. |
| `P240` | warn | Total system power draw is high | — |
| `P241` | error | Total system power draw is critically high | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Evaluate total system power, and reduce device or replace devices with lower power alternatives.<br>Continued alerts indicate a condition that could reduce the life of the power supply, or other system components.<br>Contact Lenovo service. |
| `P250` | warn | Total system power draw is high | — |
| `P251` | error | Total system power draw is critically high | Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Evaluate total system power, and reduce device or replace devices with lower power alternatives.<br>Continued alerts indicate a condition that could reduce the life of the power supply, or other system components.<br>Contact Lenovo service. |

## Storage

| Code | Severity | Description | Solutions |
|------|----------|-------------|-----------|
| `C100` | info | Backplane S/X cable is connected incorrectly | — |
| `C31x` | error | Backplane P1 or P2 cable is connected incorrectly; the last hex digit is the drive index | The "P1" and "P2" cables may only be connected to Broadcom storage adapters.<br>The Broadcom adapter has four connectors: 0, 1, 2, 3.  "P1" must be connected to connector 0 or 2.  "P2" must be connected to connector immediately after "P1" - 1 or 3. |
| `C41x` | error | Backplane P1 or P2 cable is connected incorrectly; the last hex digit is the drive index | The "P1" and "P2" cables may only be connected to Broadcom storage adapters.<br>The Broadcom adapter has four connectors: 0, 1, 2, 3.  "P1" must be connected to connector 0 or 2.  "P2" must be connected to connector immediately after "P1" - 1 or 3. |
| `C500` | info | Could not read backplane cabling configuration | — |
| `D11x` | error | U.2 PCIe SSD is installed in the wrong slot; the last hex digit is the drive index | For P920, flip the tray so that the U.2 drive is on the bottom.  Install first U.2 in bay 4, then the next in bay 3, bay 2, and finally bay 1.<br>For P720, flip the tray so that the U.2 drive is on the top.  Install first U.2 in bay 1, then the 2nd drive in bay 2. |

## System

| Code | Severity | Description | Solutions |
|------|----------|-------------|-----------|
| `S100` | warn | CPU 1 reported a general alert | These events can be triggered by several events on the PCIe bus.  Most likely, no remediation is required.  But if other event codes occur, follow the actions for those codes. |
| `S101` | warn | CPU 2 reported a general alert | These events can be triggered by several events on the PCIe bus.  Most likely, no remediation is required.  But if other event codes occur, follow the actions for those codes. |
| `S110` | warn | CPU 1 reported a general error | These events can be triggered by several events on the PCIe bus.  Most likely, no remediation is required.  But if other event codes occur, follow the actions for those codes. |
| `S111` | warn | CPU 2 reported a general error | These events can be triggered by several events on the PCIe bus.  Most likely, no remediation is required.  But if other event codes occur, follow the actions for those codes. |
| `S120` | warn | CPU 1 general failure | These events can be triggered by several events on the PCIe bus.  Most likely, no remediation is required.  But if other event codes occur, follow the actions for those codes. |
| `S121` | warn | CPU 2 general failure | These events can be triggered by several events on the PCIe bus.  Most likely, no remediation is required.  But if other event codes occur, follow the actions for those codes. |
| `S200` | critical | Critical system alert | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Remove and reinstall all DIMMs to ensure good connection.<br>Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys.  Remove non-essential devices, reducing to minimize memory and adapters.  If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S201` | warn | System recovered from a general alert | — |

## System Voltages & Power

| Code | Severity | Description | Solutions |
|------|----------|-------------|-----------|
| `C000` | info | Chassis intrusion detected: the system cover was opened | — |
| `N000` | info | Power button was pressed | — |
| `S001` | warn | 3.3 V standby rail is above tolerance | — |
| `S002` | error | 3.3 V standby rail is critically high | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S003` | warn | 3.3 V standby rail is below tolerance | — |
| `S004` | error | 3.3 V standby rail is critically low | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S005` | critical | System failed to complete power-up initialisation | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S006` | critical | 5 V standby rail failed to come up | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S007` | warn | 5 V standby rail is above tolerance | — |
| `S008` | error | 5 V standby rail is critically high | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S009` | warn | 5 V standby rail is below tolerance | — |
| `S010` | error | 5 V standby rail is critically low | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S012` | critical | Startup sequence timing was out of spec | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S013` | critical | Startup sequence timing was out of spec | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S014` | critical | Startup sequence timing was out of spec | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S016` | critical | 12 V rail failed to come up | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S017` | warn | 12 V rail is above tolerance | — |
| `S018` | error | 12 V rail is critically high | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S019` | warn | 12 V rail is below tolerance | — |
| `S020` | error | 12 V rail is critically low | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S021` | critical | 3.3 V main rail failed to come up | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S022` | warn | 3.3 V main rail is above tolerance | — |
| `S023` | error | 3.3 V main rail is critically high | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S024` | warn | 3.3 V main rail is below tolerance | — |
| `S025` | error | 3.3 V main rail is critically low | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S026` | critical | 5 V main rail failed to come up | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S027` | warn | 5 V main rail is above tolerance | — |
| `S028` | error | 5 V main rail is critically high | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S029` | warn | 5 V main rail is below tolerance | — |
| `S030` | error | 5 V main rail is critically low | Shut off the system.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S031` | warn | Power supply or motherboard voltage regulation fault | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S033` | critical | CPU voltage rail failed to come up | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Swap CPU1 and CPU2. If only one CPU, reseat the CPU.  WARNING: Care must be taken when removing/addings CPUs.  If not familiar with this process, skip this step.<br>Contact Lenovo service. |
| `S034` | warn | CPU voltage rail is above tolerance | — |
| `S035` | error | CPU voltage rail is critically high | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Swap CPU1 and CPU2. If only one CPU, reseat the CPU.  WARNING: Care must be taken when removing/addings CPUs.  If not familiar with this process, skip this step.<br>Contact Lenovo service. |
| `S036` | warn | CPU voltage rail is below tolerance | — |
| `S037` | error | CPU voltage rail is critically low | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Swap CPU1 and CPU2. If only one CPU, reseat the CPU.  WARNING: Care must be taken when removing/addings CPUs.  If not familiar with this process, skip this step.<br>Contact Lenovo service. |
| `S040` | critical | Motherboard voltage regulator fault | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S041` | critical | Motherboard voltage regulator fault | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove and reinstall all DIMMs to ensure good connection.<br>Remove all but one DIMM. If diagnostic alert continues, swap with another DIMM. Add back DIMMs one at a time to determine problem DIMM.<br>Swap CPU1 and CPU2. If only one CPU, reseat the CPU.  WARNING: Care must be taken when removing/addings CPUs.  If not familiar with this process, skip this step.<br>Contact Lenovo service. |
| `S042` | critical | Motherboard voltage regulator fault | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Swap CPU1 and CPU2. If only one CPU, reseat the CPU.  WARNING: Care must be taken when removing/addings CPUs.  If not familiar with this process, skip this step.<br>Contact Lenovo service. |
| `S043` | warn | Motherboard voltage regulator is reporting a warning | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Remove any devices (adapters, memory, etc.) installed after the system was received from Lenovo.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S044` | critical | Startup sequence timing was out of spec | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Check for foreign objects on electronic components in the system.<br>Remove non-essential I/O such as USB keys. Remove non-essential devices, reducing to minimize memory and adapters. If the diagnostic alert is resolved, add back devices one at a time to determine problem device.<br>Contact Lenovo service. |
| `S050` | error | An external device is drawing leakage current | Replace the display port cable between system and monitor with a cable that meets VESA specifications.  The cable that shipped with your monitor should meet specifications. |

## Thermal

| Code | Severity | Description | Solutions |
|------|----------|-------------|-----------|
| `T110` | warn | CPU 1 is running hot | — |
| `T111` | warn | CPU 1 reached its maximum allowed temperature | — |
| `T112` | error | CPU 1 thermal limit exceeded; throttling or shutdown imminent | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Power the system down for serveral minutes, then power on and check for the error again.<br>Contact Lenovo service. |
| `T120` | warn | CPU 2 is running hot | — |
| `T121` | warn | CPU 2 reached its maximum allowed temperature | — |
| `T122` | error | CPU 2 thermal limit exceeded; throttling or shutdown imminent | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Power the system down for serveral minutes, then power on and check for the error again.<br>Contact Lenovo service. |
| `T200` | warn | CPU 1 memory bank 1 is running warm | — |
| `T201` | warn | CPU 1 memory bank 1 is running hot | — |
| `T202` | error | CPU 1 memory bank 1 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Remove all but one DIMM. If diagnostic alert continues, swap with another DIMM. Add back DIMMs one at a time to determine problem DIMM.<br>Contact Lenovo service. |
| `T210` | warn | CPU 1 memory bank 2 is running warm | — |
| `T211` | warn | CPU 1 memory bank 2 is running hot | — |
| `T212` | error | CPU 1 memory bank 2 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Remove all but one DIMM. If diagnostic alert continues, swap with another DIMM. Add back DIMMs one at a time to determine problem DIMM.<br>Contact Lenovo service. |
| `T220` | warn | CPU 2 memory bank 1 is running warm | — |
| `T221` | warn | CPU 2 memory bank 1 is running hot | — |
| `T222` | error | CPU 2 memory bank 1 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Remove all but one DIMM. If diagnostic alert continues, swap with another DIMM. Add back DIMMs one at a time to determine problem DIMM.<br>Contact Lenovo service. |
| `T230` | warn | CPU 2 memory bank 2 is running warm | — |
| `T231` | warn | CPU 2 memory bank 2 is running hot | — |
| `T232` | error | CPU 2 memory bank 2 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Remove all but one DIMM. If diagnostic alert continues, swap with another DIMM. Add back DIMMs one at a time to determine problem DIMM.<br>Contact Lenovo service. |
| `T240` | critical | Memory thermal protection triggered | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Remove all but one DIMM. If diagnostic alert continues, swap with another DIMM. Add back DIMMs one at a time to determine problem DIMM.<br>Contact Lenovo service. |
| `T250` | warn | CPU voltage regulator is running hot | — |
| `T252` | error | CPU voltage regulator thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T310` | warn | Chipset (PCH) is running hot | — |
| `T311` | error | Chipset (PCH) thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T400` | warn | Ambient temperature is high | — |
| `T401` | error | Ambient temperature is critically high | Confirm the front ambient temp cable is connected to the motherboard, and the front of the system is not blocked.<br>Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Reboot system, enter system setup, and increase the fan speed to setting 2 or 3.<br>Contact Lenovo service. |
| `T402` | warn | Ambient temperature is high | — |
| `T403` | error | Ambient temperature is critically high | Confirm the front ambient temp cable is connected to the motherboard, and the front of the system is not blocked.<br>Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Reboot system, enter system setup, and increase the fan speed to setting 2 or 3.<br>Contact Lenovo service. |
| `T410` | warn | Motherboard temperature sensor 1 is high | — |
| `T411` | error | Motherboard temperature sensor 1 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T420` | warn | Motherboard temperature sensor 2 is high | — |
| `T421` | error | Motherboard temperature sensor 2 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T430` | warn | Motherboard temperature sensor 3 is high | — |
| `T431` | error | Motherboard temperature sensor 3 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T440` | warn | Motherboard temperature sensor 4 is high | — |
| `T441` | error | Motherboard temperature sensor 4 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T510` | warn | Power supply 1 is running hot | — |
| `T511` | error | Power supply 1 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T520` | warn | Power supply 2 is running hot | — |
| `T521` | error | Power supply 2 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T621` | warn | Internal PCIe drive 1 is running hot | — |
| `T622` | warn | Internal PCIe drive 2 is running hot | — |
| `T623` | warn | Internal PCIe drive 3 is running hot | — |
| `T624` | warn | Internal PCIe drive 4 is running hot | — |
| `T631` | error | Internal PCIe drive 1 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T632` | error | Internal PCIe drive 2 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T633` | error | Internal PCIe drive 3 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T634` | error | Internal PCIe drive 4 thermal limit exceeded | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Contact Lenovo service. |
| `T7x1` | warn | Quad M.2 adapter card 1 is running hot; the second hex digit is the drive slot | — |
| `T7x2` | warn | Quad M.2 adapter card 2 is running hot; the second hex digit is the drive slot | — |
| `T7x3` | warn | Quad M.2 adapter card 3 is running hot; the second hex digit is the drive slot | — |
| `T7x4` | warn | Quad M.2 adapter card 4 is running hot; the second hex digit is the drive slot | — |
| `T7x5` | error | Quad M.2 adapter card 1 thermal limit exceeded; the second hex digit is the drive slot | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Remove the quad M.2 adapter from the system.  Remove the cover and heatsink.  Confirm thermal pads are in place and making good connection between the heatsink and M.2<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Reboot system, enter system setup, and increase the fan speed to setting 2 or 3.<br>Contact Lenovo service. |
| `T7x6` | error | Quad M.2 adapter card 2 thermal limit exceeded; the second hex digit is the drive slot | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Remove the quad M.2 adapter from the system.  Remove the cover and heatsink.  Confirm thermal pads are in place and making good connection between the heatsink and M.2<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Reboot system, enter system setup, and increase the fan speed to setting 2 or 3.<br>Contact Lenovo service. |
| `T7x7` | error | Quad M.2 adapter card 3 thermal limit exceeded; the second hex digit is the drive slot | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Remove the quad M.2 adapter from the system.  Remove the cover and heatsink.  Confirm thermal pads are in place and making good connection between the heatsink and M.2<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Reboot system, enter system setup, and increase the fan speed to setting 2 or 3.<br>Contact Lenovo service. |
| `T7x8` | error | Quad M.2 adapter card 4 thermal limit exceeded; the second hex digit is the drive slot | Check for ventilation clearance around system. Remove any dust of objects blocking air flow.<br>Check the ambient temperature in the room is within specified limits, typically 10-35 degrees celsius.<br>Remove the quad M.2 adapter from the system.  Remove the cover and heatsink.  Confirm thermal pads are in place and making good connection between the heatsink and M.2<br>Check diagnostic log for additional alerts, such as power, voltage, or fan alerts. Follow that repair action.<br>Check that all fans are connected.<br>Reboot system, enter system setup, and increase the fan speed to setting 2 or 3.<br>Contact Lenovo service. |

## ThinkPad

| Code | Severity | Description | Solutions |
|------|----------|-------------|-----------|
| `0001` | info | Platform reset line stayed asserted during boot; clear CMOS and retry | 1. Remove all power resources (the ac power adapter, removable battery, and coin-cell battery). If your computer has a built-in battery, reset the computer by inserting a straightened paper clip into the emergency-reset hole. Wait for one minute. Then reconnect all power resources. 2. Replace the system board (service provider only). |
| `0002` | info | Internal chipset bus failed a self-test | Replace the system board (service provider only). |
| `0281` | info | Embedded controller reported a generic fault | Replace the system board (service provider only). |
| `0282` | info | Memory module failed self-test; reseat DIMMs | 1. Reinstall or replace the memory module. 2. Replace the system board (service provider only). |
| `0283` | info | PCI bus resource assignment failed | 1. Remove PCIe devices (the M.2 card, PCIe card, and so on) (service provider only). 2. Replace the system board (service provider only). |
| `0284` | info | TCG subsystem fault; likely a BIOS code-integrity check failure | Replace the system board (service provider only). |
| `0285` | info | TCG subsystem fault; likely a TPM initialisation failure | Replace the system board (service provider only). |
| `0286` | info | Integrated GPU failed to initialise | Replace the system board (service provider only). |
| `0287` | info | Discrete GPU failed to initialise | 1. Reinstall or replace the discrete graphics card (service provider only). 2. Replace the system board (service provider only). |
| `0288` | info | Display panel failed to initialise | 1. Reconnect the display cable on both the system board side and the computer display side (service provider only). 2. Replace the system board (service provider only). |

## USB

| Code | Severity | Description | Solutions |
|------|----------|-------------|-----------|
| `U100` | error | Front-panel USB hub communication error | Unplug the system, wait 30 seconds, plug in the system, and power up.<br>Download and run the 'Lenovo Super IO and Front Panel Firmware update utility'. This can be found on Lenovo's website in your system's Drivers and Software page.<br>Contact Lenovo service. |
| `U110` | warn | Front-panel charging port is drawing high current | — |
| `U111` | error | Front-panel charging port is drawing critical over-current | Remove device from front USB port. |
| `U120` | warn | Front-panel non-charging ports are drawing high current | — |
| `U121` | error | Front-panel non-charging ports are drawing critical over-current | Remove device from front USB port. |
| `U130` | warn | Front-panel USB bus is drawing high current | — |

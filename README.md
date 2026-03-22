# 🦜 Dead Parrot Protocol

*It is an ex-workload. It has ceased to be.*

**Dead Parrot Protocol** is a custom, hardware-level stealth appliance built on the Raspberry Pi Pico. It is designed to emulate deeply human, distracted workflows to bypass modern enterprise Endpoint Detection and Response (EDR) behavioral heuristics. 

It does not just jiggle a mouse. It thinks, it breathes, it makes typos, and it muses procedurally about vintage computing architectures.

## ⚙️ Core Features

* **Procedural NLP Engine:** Generates unique, infinite strings of corporate jargon, hardware hacking thoughts, and tangents. It tracks topics, uses pronouns, and properly formats paragraphs.
* **Deep Human Slop Simulator:** Mimics transposition errors (typing "eh", deleting it, typing "he"), fat-fingers the Enter key, and pauses mid-sentence to "stare at the screen."
* **Advanced HID Spoofing:** `boot.py` amputates all default CircuitPython serial, storage, audio, and MIDI endpoints, successfully enumerating to the host OS strictly as a generic Logitech USB Receiver.
* **Analog Control Surface:** Features a potentiometer-driven Cylon LED scanner (with phase-accumulated anti-aliasing) to control mouse sweep intensity, and tactical switches for payload deployment.
* **Hardware Audio:** Mechanical tactile feedback via an active buzzer, and a passive PWM buzzer for status alerts. 

## 🛠️ Hardware Bill of Materials (BOM)

* 1x Raspberry Pi Pico or Pico 2(RP2040 or RP2350)
* 1x 10k Potentiometer
* 2x Tactile Push Buttons
* 1x 10-Segment LED Bar Graph
* 1x Common Anode RGB LED
* 1x Red (or similar) LED
* 1x Active Buzzer
* 1x Passive Buzzer
* 12x 220Ω Resistors
* Breadboard & Jumper Wires

*See the `/docs/Dead Parrot Protocol_bb.png` diagram for the complete pinout mapping. I've also included a Fritzing model to help clarify what's going on with the wires*

## 🚀 Installation & Deployment

1. Flash your Raspberry Pi Pico with the latest **CircuitPython** `.uf2` firmware.
2. Download the `src/` folder from this repository.
3. Hold the **Main Deployment Button (GP15)** while plugging the Pico into your computer via USB. This engages the "Escape Hatch," bypassing the cloaking protocol and mounting the `CIRCUITPY` drive.
4. Drag and drop `boot.py` and `code.py` onto the root of the drive.
5. Safely eject and unplug the Pico.
6. The next time the device is plugged in, it will cloak itself and execute the protocol.

## ⚠️ Disclaimer

This project is a hardware exploration of behavioral emulation, procedural text generation, and USB descriptor spoofing. It is built for educational purposes. Do not use this hardware to circumvent security policies on networks or equipment you do not own.

## License
MIT License. See `LICENSE` for details.

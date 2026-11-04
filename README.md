# Smart Baby Cradle Monitoring System

An Arduino-based baby cradle automation project that monitors sound intensity and automatically operates a cradle motor when sound exceeds a configured threshold. The project also includes a YOLOv8 `.pt` model file for a possible computer-vision component.

> **Important:** The supplied Arduino sketch implements sound-triggered motor control. The supplied `.pt` file is a YOLOv8 `DetectionModel` checkpoint, but its class labels, training dataset, and intended detection task are not provided. The model's integration with the Arduino sketch is therefore not assumed or documented as a working feature.

## Project Overview

The system continuously reads sound intensity from an analog sound sensor. When the reading rises above the configured threshold, the Arduino switches on the motor driver and starts the cradle motor. When the sound remains below the threshold for one minute, the motor is switched off.

### Main Features

- Continuous sound-intensity monitoring through an analog sensor.
- Automatic motor activation when sound exceeds a threshold.
- Motor speed control using PWM.
- Automatic motor shutdown after 60 seconds of continuously low sound.
- Relay-based motor power control.
- Serial Monitor messages for monitoring sensor readings and system state.
- Includes a YOLOv8 PyTorch checkpoint (`.pt`) for a separate or future vision-based component.

## Hardware Components

The Arduino sketch uses the following connections:

| Component / Signal | Arduino Pin |
|---|---:|
| Sound sensor analog output | `A0` |
| Motor driver enable (PWM) | `9` |
| Motor driver input 1 | `8` |
| Motor driver input 2 | `7` |
| Relay control | `4` |

Other hardware required will depend on the physical build:

- Arduino-compatible board
- Analog sound sensor / sound detection module
- DC motor suitable for the cradle mechanism
- Motor driver compatible with the motor
- Relay module compatible with the control circuit
- Suitable external motor power supply
- Jumper wires and breadboard / PCB

Check the voltage and current ratings of every component before wiring. Do not power a motor directly from an Arduino I/O pin.

## How It Works

1. The Arduino reads the analog value from the sound sensor on `A0`.
2. It prints the current sound reading to the Serial Monitor.
3. If the reading is greater than `soundThreshold` (`250`):
   - The relay is activated (`LOW`).
   - The motor direction pins are set.
   - PWM is applied to the motor enable pin.
   - The motor is marked as running.
4. When the reading falls to or below the threshold, the system starts a timer.
5. If the sound remains below the threshold for 60 seconds, the Arduino:
   - Sets motor PWM to zero.
   - Sets both direction pins to `LOW`.
   - Deactivates the relay (`HIGH`).
   - Resets the motor state and timer.
6. If sound rises above the threshold before the 60 seconds expire, the stop timer is reset and the motor continues running.

## Software Requirements

- [Arduino IDE](https://www.arduino.cc/en/software)
- Arduino board package and USB driver appropriate for your board
- No additional Arduino libraries are used by the supplied `.ino` sketch

The `.pt` file is a PyTorch model checkpoint associated with the Ultralytics YOLOv8 model format. Using it for inference generally requires a compatible Python environment and Ultralytics/PyTorch versions. The supplied files do not specify the exact environment or inference script.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

Replace the repository URL with your GitHub repository URL.

### 2. Connect the Hardware

Connect the sound sensor, motor driver, and relay control signal according to the pin table above. Connect the motor to the motor driver's output and use an appropriately rated external power supply.

**Safety:** Test the motor mechanism without a baby present. Use a mechanically safe cradle design, secure wiring, appropriate electrical isolation, and independent safeguards. A sound threshold and timer alone are not a reliable baby-monitoring or safety system. Never leave an infant unattended with a prototype device.

### 3. Upload the Arduino Code

1. Open the `.ino` file in Arduino IDE.
2. Select the correct board from **Tools → Board**.
3. Select the correct port from **Tools → Port**.
4. Verify the pin connections and motor power arrangement.
5. Click **Verify**, then **Upload**.

### 4. Monitor Sensor Readings

Open **Tools → Serial Monitor** and set the baud rate to **9600**. The sketch prints sound intensity readings and status messages when the motor starts or stops.

## Configuration

The main settings are defined near the top of the Arduino sketch:

| Variable | Default | Description |
|---|---:|---|
| `motorSpeed` | `70` | PWM value sent to the motor enable pin |
| `soundThreshold` | `250` | Sound reading above which the motor starts |
| Stop delay | `60000 ms` | Time below the threshold before the motor stops |

### Adjusting the Sound Threshold

Sensor readings vary with the sensor module and surrounding environment. Observe the Serial Monitor in quiet and noisy conditions, then adjust `soundThreshold` to a suitable test value.

### Adjusting Motor Speed

`motorSpeed` is passed to `analogWrite()` on pin `9`. On common Arduino boards with 8-bit PWM, the range is `0` to `255`. The actual motor speed also depends on the motor, driver, and power supply.

## Serial Monitor Output

Example messages produced by the sketch include:

```text
Baby Cradle Monitoring System Started
Sound Intensity: 180
Sound Intensity: 320
High Sound Detected - Motor Started
Sound Stopped - Waiting 1 Minute
No Sound for 1 Minute - Motor Stopped
```

The numeric readings above are illustrative; actual sensor values will vary.

## YOLOv8 Model File

The repository also contains a `.pt` checkpoint whose internal metadata identifies it as an Ultralytics YOLOv8 `DetectionModel`.

The provided files do not include:
- The model's class names or class mapping.
- Its training dataset or training configuration.
- A Python inference script.
- A connection between model predictions and the Arduino motor-control logic.

Consequently, the model should be treated as an included checkpoint until its intended task and inference workflow are confirmed. Do not assume that it detects babies, crying, or any particular object without validating its labels and predictions.

## Current Project Scope

| Functionality | Status based on supplied files |
|---|---|
| Sound sensor reading | Implemented in Arduino sketch |
| Threshold-based motor activation | Implemented in Arduino sketch |
| PWM motor speed control | Implemented in Arduino sketch |
| One-minute low-sound stop timer | Implemented in Arduino sketch |
| Relay control | Implemented in Arduino sketch |
| YOLOv8 model checkpoint | Included; task and labels not specified |
| YOLO-to-Arduino integration | Not shown in supplied files |

## Future Improvements

- Add a documented computer-vision inference script after confirming the model's classes and intended task.
- Calibrate the sound threshold for the selected sensor and environment.
- Add adjustable settings rather than hard-coded threshold and speed values.
- Add fault handling for sensor disconnection and motor-driver errors.
- Add independent hardware safety limits and a manual emergency stop.
- Test reliability and mechanical safety before any real-world use.

## Contributing

Contributions and suggestions are welcome. For substantial changes, open an issue first to discuss the proposed improvement. Please include wiring changes, software requirements, and test results when submitting a pull request.

## License

No project license was supplied with the source files. Add a `LICENSE` file and update this section before publishing or reusing the project. The model checkpoint may have separate licensing or usage conditions; verify its provenance and terms before redistribution.

## Acknowledgements

- [Arduino](https://www.arduino.cc/)
- [Ultralytics YOLO](https://docs.ultralytics.com/)

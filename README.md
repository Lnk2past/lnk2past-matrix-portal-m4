# lnk2past-matrix-portal-m4

Adafruit Matric Portal M4 App initial made for RUCHacks Spring '23 (written for the [`Adafruit Matrix Portal - CircuitPython Powered Internet Display`](https://www.adafruit.com/product/4745)).

## Setup

Following the assembly and prep instructions [here](https://learn.adafruit.com/adafruit-matrixportal-m4/prep-the-matrixportal). You will need to flash the board with the [bootloader](https://learn.adafruit.com/adafruit-matrixportal-m4/install-circuitpython). A known working version is included here, but you can download and test newer versions too.

Once the board is configured, just copy the contents of [`./src`](./src) to the root of the board's drive (**do not include `src`, just its contents!**). If you plan on using the WiFi capabilities you will need to configure the `secrets.py` file with your 2.4Gz WiFi access point.

## Usage & Modes

There are 4 default modes provided:

* Text Splash
* Conway's Game of Life
* Matrix Code Rain
* Weather Report

Once loaded you can use the `UP` button on the board to cycle through the modes. They mostly cover the base capabilities of the board. The weather mode by default is commented out, as it needs a local server running (feel free to change how this works!). The local server is detailed in the next section.

## Utilities

### Debug

When connected to your computer you can use a serial connection to access the board and view any printed output. The file `debug.py` uses the Python package `pyserial v3.5` to connect to the board. This has been tested on Windows, and you'll likely need to change the COM port referenced in the code. Just run the script and if it works then you should see output from the Matrix Portal board.

### Server 

The current weather mode uses a stripped down response from `https://api.weather.gov/gridpoints/PHI/40,75/forecast` - the response is generally too big for the Matrix Portal to handle, so this webserver runs on a local PC (a raspberry pi perhaps!) which can handle the response. Install `flask` and run:

```shell
flask --app utilities.server.app run --host 0.0.0.0
```

This will show 2 IP addresses in the output. For example, on my system I see:

```text
flask --app utilities.server.app run --host 0.0.0.0
>>
 * Serving Flask app 'utilities.server.app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.159:5000
Press CTRL+C to quit
```

The address that the Matrix Portal can see is `http://192.168.1.159:5000` and so we want to place that URL in `code.py`. Note that your valid address may be different depending on your router/modem!. Once there the weather mode should pull the weather for the location specified in the server (the bit `PHI/40,75` is approximately Camden COunty)

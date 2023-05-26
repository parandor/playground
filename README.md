# playground

This n that

## Docker

1. influxdb (storage)
2. grafana (visualization)
3. chronograf (for influxdb web UI)
4. telegraf (optional: host machine  performance specs)

## Google Cloud API

This is optional used to upload files to the Google Drive using Google Cloud Services API.

Run the following to install required libraries:

`pip install google-api-python-client`

## Raspberry Pi

### Ultrasonic Distance Sensor

This is used to power the Ultrasonic HC-SR04 Distance Detector Module

`sudo apt-get update`\
`sudo apt-get install python3-rpi.gpio`

### Storage

#### Database

Install influxdb api to interact with the influxdb docker server

`pip install influxdb`

### Detection

Install scipy for trough detection of multidimentional x,y series data

`pip install scipy`

## Test

Used to generate a data set to test trigger notification events,\
which are issued by the Peak/Valley/Trough Detectors

`pip install numpy`

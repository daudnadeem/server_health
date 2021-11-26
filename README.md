# magnificent

## Installation

To run the server health monitor, you are required to have python3.7 (or greater) on your machine

```
# Install pip package
pip install src/
# To uninstall
pip uninstall server_health
```
## Usage

### To run server monitor

```
# This will generate a report every 60 seconds, and ping the server every 10 seconds
mag_hlth
# This will generate a report every 120 seconds, and ping the server every 12 seconds
maghlth -t 120
# This will generate a report every 100 seconds, and ping the server every 2 seconds
maghlth -t 100 -p 2
# You may also use argparse when calling this as a script
python3 src/server_health/health_monitor.py -t 100 -p 2
```

You may run this service as default (shown above) which will ping the server every 10 seconds and generate a report after 1 minute OR you may wish to parse arguments to the service to generate a report based on your needs.

`-t` - (s) time between report generation
`-p` - (s) time between each ping to the server 

## Logging
Logs are generated to the console, which are simple logs. More detailed logs are logged to a dynamic location `python3.x/site-packages/*/magnificent_health.log` - this value is logged to the console at the start of each session.

Logging is generated from the `logger` class and feeds off of `logging.yaml` - which is the configutation file used to set up logging.


## Notes

- `constants.py` contains hardcoded values - Possible to extract these to environment variables, but there is no need since nothing is 'secret'

- `setup.py` used to package this into a python module - Implemented for ease of use

- `health_monior.py` - This is the main script
    - contains main()
    - contains MagServer class

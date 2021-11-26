from time import sleep
import requests
from server_health.logger import setup_logging
from server_health.constants import server, active, inactive
import logging
import argparse

logger, mag_loc = setup_logging()

main_parser = argparse.ArgumentParser(
    description="Basic requirements for any type of run")

main_parser.add_argument('-t', '--time_interval', type=int,
                         help="Amount of time before report generation", default = 60)

main_parser.add_argument('-p', '--ping_interval', type=int,
                         help="Amount of time before pinging the server")



args = main_parser.parse_args()
user_selection = vars(args)

class MagServer:
    # Currently, our server is quite simple as we are just calling a host/URL
    # But if we were to add more functionality, we can easily update this class
    def __init__(self, host=server, port=None):
        self.host = host
        self.port = port
        self.status = None
        self.status_report = {
            "Healthy" : 0,
            "Unhealthy" : 0,
            "No Response" : 0
        }

    def ping_server(self):
        # This is the main method that we will call to get a response from
        # the server
        # Headers may be needed when trying to GET with authentication
        res = requests.get(self.host, headers=None, stream=True)
        # Since the server responds as binary, we must conver to
        # string by decoding
        str_response = res.raw.read().decode("utf-8")
        try:
            if res.status_code == 200:
                logger.info(f'{str_response}')
            elif res.status_code == 500:
                logger.info(f'{str_response}')
            else:
                # Since we have only coded for 2 status_code(s), if we
                # get any unexpected server response, we can still log
                # it in full detail
                logger.error(str_response)

        except Exception as e:
            # Incase an error occurs, we can except the error, log it
            # but not disrupt the server health monitor
            logger.error(e)

        return str_response

    def status_update(self, minute_check):
        healthy = 0
        unhealthy = 0
        no_response = 0
        total_updates = len(minute_check)
        # Since minute_check is always 6 items, this is O(1)
        for each_update in minute_check:
            if each_update == active:
                healthy += 1
            elif each_update == inactive:
                unhealthy += 1
            else:
                no_response += 1
       
        # Generate percentages and round them off to 2 decimal place 
        self.status_report["Healthy"] = round(healthy/total_updates * 100, 2)
        self.status_report["Unhealthy"] = round(unhealthy/total_updates * 100, 2)
        self.status_report["No Response"] = round(no_response/total_updates * 100, 2)
        
        # Also give a more abstract value for the status of the server
        if self.status_report["Healthy"] > 70.0:
            self.status = "Healthy"
        elif self.status_report["Healthy"] <= 70.0 and self.status_report["Unhealthy"] >= 30.0:
            self.status = "Relatively Healthy"
        else:
            self.status = "Unhealthy!"

        # If we ever recieve an unexpected response, report it straight away.
        if no_response > 0:
            logger.info(
                f"The server did not respond for {no_response} times in the last minute"
            )

        return self.status, self.status_report

    def generate_report(self, status_report):
        # Generate the report and neatly parse the dictionary to a single 
        # line for logging
        logger.info(f"Below is the report for Magnificent at a time interval of: {args.time_interval} seconds")
        logger.info(' '.join(['{0} : {1}%  |'.format(k, v) for k,v in status_report.items()]))
        logger.info("")
            


def main():
    # This is being installed as a package (for OS independence)
    # We log the location of the log file at the beginging to the console log
    logger.info(f'You may find the log file at: {mag_loc}')

    # The user may wish to input his/her own time intervals 
    # By default the server will ping every 10 seconds
    # And generate a report every 60 seconds

    if args.time_interval:
        time_interval = args.time_interval

    if args.ping_interval:
        ping_intrvl = args.ping_interval
    else:
        ping_intrvl = int(time_interval/6)
    
    if args.time_interval and args.ping_interval:
        _range = int(time_interval/ping_intrvl)
    else:
        _range = int(time_interval/10)
    
        
    # Since we want to inevitably check the health of the server,
    # we run this as an infinite while loop
    while (True):
        minute_status_checker = []
        for health in range(_range):
            magServer = MagServer()
            minute_status_checker.append(magServer.ping_server())
            # sleep for 10 seconds, then re-check server status and log to console + log file
            sleep(ping_intrvl)
        # Update health status after each minute
        server_health, server_report = magServer.status_update(minute_status_checker)
        magServer.generate_report(server_report)
        logger.info(f"Server Health Status Update: Magnificent is {server_health}")


if __name__ == "__main__":
    main()

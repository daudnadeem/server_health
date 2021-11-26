# That will never change - so it is okay to hardcode these.
root_repo_name = "server_health"
default_logger = "magnificent_logger"
active = "Magnificent!"
inactive = "Internal Server Error"
# Incase we wish to check the health of any other URL
# we can simply change this value here - but for the sake of
# this project, this is considered absolute
server = "https://api.us-west-1.saucelabs.com/v1/magnificent/"
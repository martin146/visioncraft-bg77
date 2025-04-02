
from argparse import ArgumentParser, Namespace
import sys

from schema import SchemaError

import services
from config import ConfigService
from bg77 import BG77
import signal
from logging.handlers import TimedRotatingFileHandler
import logging.config
from consts import *


def handler(sig, frame):
    print('Exiting...')
    sys.exit(0)


signal.signal(signal.SIGINT, handler)


def initialize_app() -> None:
    services.logger = logging.getLogger('VCraft-BG77')
    services.config = ConfigService('config.yml')
    services.module = BG77()

    config = services.config
    services.logger.setLevel(config.get_log_level())

    if LOG_FILE in config.config[LOG_SECTION] and config.config[LOG_SECTION][LOG_FILE]:
        file_handler = TimedRotatingFileHandler(config.config[LOG_SECTION][LOG_FILE], when='midnight', interval=1,
                                                backupCount=30, utc=True)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        stdout_handler = logging.StreamHandler(sys.stdout)
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().addHandler(stdout_handler)

    # Check configuration
    try:
        services.config.validate_config()
        services.logger.debug("Config successfully validated")
    except SchemaError as e:
        services.logger.critical(e.autos[-1])
        exit(-1)


def run_app(app_args: Namespace) -> None:
    if app_args.mode == 'att':
        services.module.reg_to_network()
    elif app_args.mode == 'cmd':
        print(app_args.command)
        timeout = int(app_args.timeout) if app_args.timeout else services.config.config[CMD_TOUT]
        rec = services.module.send_command_timeout(app_args.command, timeout)
        if len(rec) > 0:
            print(rec)
    elif app_args.mode == 'link':
        services.module.get_reg_status()
    elif app_args.mode == 'stat':
        services.module.get_signal_stats()


if __name__ == '__main__':
    parser = ArgumentParser(prog='app')
    parser.add_argument('-m', '--mode', choices=['att', 'cmd', 'link', 'stat'], required=True, help='Select mode')
    parser.add_argument('-c', '--command', help='Command required in "cmd" mode')
    parser.add_argument('-t', '--timeout', help='Command timeout in seconds')

    args = parser.parse_args()
    if args.mode == "cmd" and args.command is None:
        parser.error('-c is required when mode is "cmd"')
    initialize_app()
    run_app(args)
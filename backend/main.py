# Copyright (c) 2024 AuspicesAI
#
# This file is part of ScytheEx.
#
# ScytheEx is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3.0 as
# published by the Free Software Foundation.
#
# ScytheEx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ScytheEx. If not, see <https://www.gnu.org/licenses/>.

import toml
import sys
from core.logging import setup_logging, log_event, log_error
from core.packet_capture import start_capture


def load_config():
    try:
        with open("config/config.toml", "r") as config_file:
            config = toml.load(config_file)
        if "ScytheEx" not in config:
            raise ValueError("Missing 'ScytheEx' section in config")
        return config["ScytheEx"]
    except Exception as e:
        print(f"Failed to load or validate config: {e}")
        raise


def main():
    try:
        config = load_config()
        error_logger, traffic_logger = setup_logging(config)
        log_event(traffic_logger, "System started successfully")
        print("Configuration loaded and validated successfully:", config)

        # Start packet capture
        start_capture(config, traffic_logger, error_logger)

    except KeyboardInterrupt:
        print("\r[x] stopping (Ctrl-C pressed)")
        log_event(traffic_logger, "System stopped by user")
    except Exception as e:
        # log_error(error_logger, f"Error in system startup: {e}")
        print(f"Error in system setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

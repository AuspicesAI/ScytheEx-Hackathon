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

import os
import logging


def setup_logging(config):
    if not os.path.exists(config["log_directory"]):
        os.makedirs(config["log_directory"])

    # Configure error logging
    error_logger = logging.getLogger("errors")
    error_handler = logging.FileHandler(config["error_logs_path"])
    error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)
    error_logger.setLevel(logging.ERROR)

    # Configure traffic logging
    traffic_logger = logging.getLogger("traffic")
    traffic_handler = logging.FileHandler(config["traffic_logs_path"])
    traffic_formatter = logging.Formatter("%(asctime)s - %(message)s")
    traffic_handler.setFormatter(traffic_formatter)
    traffic_logger.addHandler(traffic_handler)
    traffic_logger.setLevel(logging.INFO)

    return error_logger, traffic_logger


def log_event(logger, message):
    logger.info(message)


def log_error(logger, message):
    logger.error(message)

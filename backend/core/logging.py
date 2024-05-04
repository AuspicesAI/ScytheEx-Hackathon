# Copyright (c) 2024 AuspicesAI
#
# This file is part of ScytheEx.
#
# ScytheEx is free software: you can redistribute it and/or modify
# it under the terms of the Apache License 2.0 as published by
# the Apache Software Foundation, either version 2 of the License, or any later version.
#
# ScytheEx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache License 2.0 for more details.
#
# You should have received a copy of the Apache License 2.0
# along with ScytheEx. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.

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

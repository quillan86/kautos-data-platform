import warnings
import logging
from datetime import timedelta

from dagster import Definitions
from dagster._core.definitions.freshness import InternalFreshnessPolicy
from dagster._utils.warnings import BetaWarning, PreviewWarning

warnings.filterwarnings("ignore", category=PreviewWarning)
warnings.filterwarnings("ignore", category=BetaWarning)

import dagster as dg
import kautos_data_platform.defs

global_freshness_policy = InternalFreshnessPolicy.time_window(fail_window=timedelta(hours=23))

logging.basicConfig(level=logging.DEBUG) # Set root logger to DEBUG
logging.getLogger("dlt").setLevel(logging.DEBUG) # Specifically for DLT
logging.getLogger("requests").setLevel(logging.DEBUG) # For underlying requests library
logging.getLogger("urllib3").setLevel(logging.DEBUG) # For underlying http lib

defs = Definitions.merge(dg.components.load_defs(kautos_data_platform.defs))

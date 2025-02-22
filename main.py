import os,time,logging,sys,datetime,zoneinfo
from modules.pollen import Pollen
from modules.pollen_dataclasses import PollenTypeInfo, PlantInfo
from operator import attrgetter
from prometheus_client import CollectorRegistry, start_http_server
import modules.prometheus as prom

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
COORDINATES = os.environ["COORDINATES"]
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en")
INTERVAL = int(os.environ.get("INTERVAL", 60 * 60 * 6)) # 6 hours
HTTP_PORT = os.environ.get('PORT', 8000)
LOGLEVEL = os.environ.get('LOGLEVEL', logging.INFO)
CONF_FILE = 'config/metrics.yml'

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=LOGLEVEL, format='%(asctime)s - %(levelname)s : %(message)s', datefmt="%Y-%m-%dT%H:%M:%S%z")

    metrics_definitions = prom.load_pollen_metrics_configs(CONF_FILE)

    registry = CollectorRegistry()
    start_http_server(int(HTTP_PORT), registry=registry)

    if len(COORDINATES.split(",")) != 2:
        logging.error("Invalid coordinates.")
        sys.exit(1)
    lat = COORDINATES.split(",")[0].strip()
    long = COORDINATES.split(",")[1].strip()

    pollen = Pollen(apiKey=GOOGLE_API_KEY)
    root_metrics = {}
    labels = {"latitude": lat, "longitude": long}

    while True:
        for category in metrics_definitions.categories:
            logging.debug(f"gathering {category.name} data...")
            if not category.name in root_metrics:
                root_metrics[category.name] = {}

            metrics = pollen.get_forecast(lat, long, languageCode=LANGUAGE_CODE)
            if metrics == None:
                logging.warning(f"getting {category.name} process was failed.")
                continue
            elif len(metrics.dailyInfo) == 0:
                logging.warning(f"{category.name} data was not found.")
                continue
            latest_metrics = metrics.dailyInfo[-1]

            for m in category.metrics:
                iterator = m.iterator if m.iterator != None else m.name
                extractor = attrgetter(iterator)
                infos:list[PollenTypeInfo|PlantInfo] = extractor(latest_metrics)
                for info in infos:
                    if not info.inSeason:
                        logging.info(f"{category.prefix}{m.name}: {info.displayName} is not in season.")
                        continue
                    if info.indexInfo != None:
                        logging.debug(f"{category.prefix}{m.name}: {info.indexInfo.value}")
                        if not m.name in root_metrics[category.name]:
                            root_metrics[category.name][m.name] = prom.create_metric_instance(m, registry, category.prefix)
                        labels["code"] = info.code
                        labels["displayName"] = info.displayName
                        prom.set_metrics(root_metrics[category.name][m.name], labels.values(), info.indexInfo.value)
            logging.info(f"gathering {category.name} metrics successful.")

        logging.info("gathering all metrics successful.")
        time.sleep(INTERVAL)

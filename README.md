# google-pollen-exporter

[![Badge](https://img.shields.io/badge/docker-legnoh/google--pollen--exporter-blue?logo=docker&link=https://hub.docker.com/r/legnoh/google-pollen-exporter)](https://hub.docker.com/r/legnoh/google-pollen-exporter) [![publish](https://github.com/legnoh/google-pollen-exporter/actions/workflows/ci.yml/badge.svg)](https://github.com/legnoh/google-pollen-exporter/actions/workflows/ci.yml)

Prometheus(OpenMetrics) exporter for [Google Pollen API](https://developers.google.com/maps/documentation/pollen).

## Usage

### Registration

At first, Set up API and create API Key.

- [Set up the Pollen API  |  Google for Developers](https://developers.google.com/maps/documentation/pollen/get-api-key-v2)

Check your target coordinates(lat/long) in google maps.

- [Get the coordinates of a place in Google Maps](https://support.google.com/maps/answer/18539?hl=en#:~:text=Get%20the%20coordinates%20of%20a%20place%20in%20Google%20Maps)

### Start(Docker)

The simplest way to use it is with Docker.

```
docker run -p 8000:8000 \
     -e GOOGLE_API_KEY="yourapikeyhere" \
     -e COORDINATES="35.685385800250806, 139.75336965608045" \
     -e LANGUAGE_CODE="ja" \
    legnoh/google-pollen-exporter
```

### Start(source)

Alternatively, it can be started from the source.

```sh
# clone
git clone https://github.com/legnoh/google-pollen-exporter.git && cd google-pollen-exporter
uv sync

# prepare .env file for your apps
cat << EOS > .env
GOOGLE_API_KEY="yourapikeyhere"
COORDINATES="35.685385800250806, 139.75336965608045"
LANGUAGE_CODE="ja"
EOS

# run exporter
uv run main.py
```

## Metrics

please check [metrics.yml](./config/metrics.yml) or [example](./example/pollen.prom)

## Disclaim

- This script is NOT authorized by Google.
  - We are not responsible for any damages caused by using this script.
- This script is not intended to overload these sites or services.
  - When using this script, please keep your request frequency within a sensible range.

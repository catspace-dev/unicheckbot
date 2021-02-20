from aioinflux import InfluxDBClient
from typing import Dict
from ..config import INFLUX_DB, INFLUX_HOST, INFLUX_PORT, INFLUX_PASSWORD, INFLUX_USERNAME


async def push_metric(measurement, tags: Dict, fields: Dict):
    try:
        point = {
            'measurement': measurement,
            'tags': tags,
            'fields': fields
        }
        async with InfluxDBClient(
            host=INFLUX_HOST,
            port=INFLUX_PORT,
            username=INFLUX_USERNAME,
            password=INFLUX_PASSWORD,
            db=INFLUX_DB,
            mode='async'
        ) as client:
            await client.write(point)
    except Exception as e:
        print(e)
        pass


async def push_api_request_status(status_code: int, endpoint: str):
    await push_metric(
        measurement="bot_api_request",
        fields=dict(
            value=1,
        ),
        tags=dict(
            status=status_code,
            endpoint=endpoint
        )
    )


async def push_status_metric(status, api_endpoint):
    await push_metric(
        measurement="bot_prepared_messages",
        fields=dict(
            value=1,
        ),
        tags=dict(
            rsp_status=status,
            api_endpoint=api_endpoint
        )
    )

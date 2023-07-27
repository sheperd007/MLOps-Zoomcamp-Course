import math
from datetime import timedelta

from fastapi import Depends
from redis import Redis

from clients.redis import get_redis_client
from decorators import cache_result, calculate_execution_time


COURIERS_AVG_SPEED = 30     # km/h
EARTH_MEAN_RADIUS = 6371.0  # km


#@calculate_execution_time
@cache_result
async def estimate_travel_time(src_lat, src_lon, dst_lat, dst_lon) -> timedelta:
    """
    Takes the geographical coordinates of two points in WGS84 (EPSG:4326),
    calculates the Great Circle Distance between them using Haversine formula,
    and estimates the travel time based on the couriers average speed.
    """
    # convert decimal degrees to radians
    src_lat = math.radians(src_lat)
    src_lon = math.radians(src_lon)
    dst_lat = math.radians(dst_lat)
    dst_lon = math.radians(dst_lon)

    # calculate haversine distance
    dlat = dst_lat - src_lat
    dlon = dst_lon - src_lon
    # a is the square of the half-chord length between the points, or (sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)).
    a = math.sin(dlat / 2)**2 + math.cos(src_lat) * math.cos(dst_lat) * math.sin(dlon / 2)**2
    # c is the angular distance in radians between the points, or 2 * atan2( √a, √(1−a) ).
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = EARTH_MEAN_RADIUS * c

    # calculate average travel time for a courier
    travel_time_hours = distance_km / COURIERS_AVG_SPEED

    # convert travel time to minutes and round to nearest minute
    travel_time_minutes = round(travel_time_hours * 60)

    return timedelta(minutes=travel_time_minutes)


async def get_mean_travel_time_to_retailer(retailer_id: str,
                                           redis: Redis = Depends(redis_client.get_redis_client)) -> timedelta:
    """
    Mean travel time to a retailer is a rough representation for accessibility of a retailer.
    It is computed through a batch pipeline and cached in Redis.
    """
    """
    SELECT AVG(avg_travel_time) as total_avg
    FROM (SELECT source_name, AVG(travel_time) AS avg_travel_time
          FROM (SELECT trip_id, source_name, travel_time
                FROM (SELECT trip_id,
                            DATEDIFF(MINUTE,
                                  MIN(CASE WHEN from_status = 'ASSIGNED' AND to_status = 'ACK' THEN created_at END),
                                  MIN(CASE WHEN from_status = 'ACK' AND to_status = 'AT_RESTAURANT' THEN created_at END)
                            ) AS travel_time
                      FROM TripStatusHistory
                      WHERE created_at >= DATEADD(DAY, -30, GETDATE())
                      GROUP BY trip_id) AS tmp
                INNER JOIN Trip
                    ON trip_id = id
                WHERE travel_time IS NOT NULL) AS tmp2
          GROUP BY source_name) AS tmp3
    """
#    mean_travel_time_to_retailer = int(redis.get(f'avg_time_to_retailer:{retailer_id}') or '5')
    mean_travel_time_to_retailer = 5
    return timedelta(minutes=mean_travel_time_to_retailer)

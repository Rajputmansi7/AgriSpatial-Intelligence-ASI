import json

from shapely.geometry import Point
from shapely.geometry import shape


AGRO_ZONE_MAPPING = {
    "ANAND": "MIDDLE_GUJARAT",
    "KHEDA": "MIDDLE_GUJARAT",
    "VADODARA": "MIDDLE_GUJARAT",

    "AMRELI": "SOUTH_SAURASHTRA",
    "BHAVNAGAR": "SOUTH_SAURASHTRA",
    "JUNAGADH": "SOUTH_SAURASHTRA",
    "PORBANDAR": "SOUTH_SAURASHTRA",
    "RAJKOT": "SOUTH_SAURASHTRA",

    "JAMNAGAR": "NORTH_SAURASHTRA",
    "SURENDRANAGAR": "NORTH_SAURASHTRA",

    "BANASKANTHA": "NORTH_GUJARAT",
    "GANDHINAGAR": "NORTH_GUJARAT",
    "PATAN": "NORTH_GUJARAT",

    "KACHCHH": "NORTH_WEST_ARID",

    "BHARUCH": "SOUTH_GUJARAT",
    "NARMADA": "SOUTH_GUJARAT",
    "SURAT": "SOUTH_GUJARAT",

    "NAVSARI": "SOUTH_GUJARAT_HEAVY",
    "VALSAD": "SOUTH_GUJARAT_HEAVY",
    "DAHOD": "SOUTH_GUJARAT"
}


class DistrictService:

    def __init__(self):

        with open(
            "backend/data/gujarat_districts.geojson",
            "r",
            encoding="utf-8"
        ) as f:

            self.geojson = json.load(f)

    def _normalize_district_name(
        self,
        district: str
    ) -> str:

        return (
            district.upper()
            .strip()
            .replace(" ", "")
            .replace("-", "")
        )

    def get_location_info(
        self,
        latitude: float,
        longitude: float
    ):

        point = Point(
            longitude,
            latitude
        )

        for feature in self.geojson["features"]:

            geometry = shape(
                feature["geometry"]
            )

            if geometry.contains(point):

                district = str(
                    feature["properties"]["NAME_2"]
                ).upper().strip()

                district_key = (
                    self._normalize_district_name(
                        district
                    )
                )

                agro_zone = AGRO_ZONE_MAPPING.get(
                    district_key,
                    "UNKNOWN"
                )

                return {
                    "district": district,
                    "agro_zone": agro_zone
                }

        return {
            "district": "UNKNOWN",
            "agro_zone": "UNKNOWN"
        }


district_service = DistrictService()

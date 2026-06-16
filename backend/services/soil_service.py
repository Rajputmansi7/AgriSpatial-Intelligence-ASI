import requests


class SoilService:

    def __init__(self):

        self.base_url = (
            "https://kaegro.com/farms/api/soil"
        )

    def get_soil_data(
        self,
        latitude: float,
        longitude: float
    ):

        try:

            response = requests.get(
                self.base_url,
                params={
                    "lat": latitude,
                    "lon": longitude
                },
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            physical = data.get(
                "physical",
                {}
            )

            chemical = data.get(
                "chemical",
                {}
            )

            water = data.get(
                "water",
                {}
            )

            soil_type = data.get(
                "soil_type",
                {}
            )

            return {

                "bulk_density_g_cm3":
                    physical.get(
                        "bulk_density_g_cm3"
                    ),

                "sand_pct":
                    physical.get(
                        "sand_pct"
                    ),

                "silt_pct":
                    physical.get(
                        "silt_pct"
                    ),

                "clay_pct":
                    physical.get(
                        "clay_pct"
                    ),

                "ph_h2o":
                    chemical.get(
                        "ph_h2o"
                    ),

                "organic_matter_pct":
                    chemical.get(
                        "organic_matter_pct"
                    ),

                "nitrogen_g_kg":
                    chemical.get(
                        "nitrogen_g_kg"
                    ),

                "cec_cmol_kg":
                    chemical.get(
                        "cec_cmol_kg"
                    ),

                "capacity_field_vol_pct":
                    water.get(
                        "capacity_field_vol_pct"
                    ),

                "capacity_wilt_vol_pct":
                    water.get(
                        "capacity_wilt_vol_pct"
                    ),

                "texture_class":
                    soil_type.get(
                        "texture_class"
                    ),

                "fao_classification":
                    soil_type.get(
                        "fao_classification"
                    )
            }

        except Exception as e:

            print(
                f"Soil API Error: {e}"
            )

            # Safe fallback values

            return {

                "bulk_density_g_cm3": 1.4,

                "sand_pct": 35.0,
                "silt_pct": 35.0,
                "clay_pct": 30.0,

                "ph_h2o": 7.1,

                "organic_matter_pct": 0.85,
                "nitrogen_g_kg": 0.55,
                "cec_cmol_kg": 18.0,

                "capacity_field_vol_pct": 29.0,
                "capacity_wilt_vol_pct": 14.0,

                "texture_class": "Loam",

                "fao_classification": "Calcisols"
            }


soil_service = SoilService()
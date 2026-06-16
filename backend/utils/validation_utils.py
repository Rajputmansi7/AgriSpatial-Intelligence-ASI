def validate_farm(
    area_ha: float,
    district: str
):

    if area_ha <= 0:
        return False, "Invalid farm area."

    if area_ha < 0.01:
        return False, "Farm area too small."

    if area_ha > 10000:
        return False, (
            "Farm area unusually large."
        )

    if district is None:
        return False, (
            "Location outside supported region."
        )

    return True, "Valid"
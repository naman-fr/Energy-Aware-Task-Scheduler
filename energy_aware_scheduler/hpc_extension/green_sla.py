import requests
import logging

logger = logging.getLogger(__name__)

class GreenSLAEnforcer:
    def __init__(self, carbon_api_url="https://api.electricitymap.org/v3/carbon-intensity/latest", api_key=None):
        self.carbon_api_url = carbon_api_url
        self.api_key = api_key

    def get_current_carbon_intensity(self, region="US"):
        headers = {}
        if self.api_key:
            headers["auth-token"] = self.api_key
        try:
            response = requests.get(self.carbon_api_url, headers=headers, params={"zone": region})
            response.raise_for_status()
            data = response.json()
            intensity = data.get("data", {}).get("carbonIntensity", None)
            logger.info(f"Current carbon intensity for {region}: {intensity} gCO2eq/kWh")
            return intensity
        except Exception as e:
            logger.error(f"Failed to fetch carbon intensity: {e}")
            return None

    def enforce_sla(self, tasks, threshold=100):
        """
        Schedule or delay tasks based on carbon intensity threshold.
        """
        intensity = self.get_current_carbon_intensity()
        if intensity is None:
            logger.warning("Carbon intensity unavailable, proceeding without SLA enforcement")
            return tasks  # No change

        if intensity > threshold:
            # Delay or reschedule non-critical tasks
            filtered_tasks = [t for t in tasks if getattr(t, "critical", False)]
            logger.info(f"Delaying {len(tasks) - len(filtered_tasks)} non-critical tasks due to high carbon intensity")
            return filtered_tasks
        else:
            logger.info("Carbon intensity below threshold, scheduling all tasks")
            return tasks

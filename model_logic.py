# model_logic.py
# Full storage compartment simulator with AI predictions

from collections import defaultdict

# ---- Item storage profiles ----
ITEM_PROFILES = {
    "banana": {"ideal_temp": 13, "ideal_humidity": 85, "shelf_life": 5,  "zone": "A"},
    "tomato": {"ideal_temp": 10, "ideal_humidity": 80, "shelf_life": 7,  "zone": "B"},
    "onion":  {"ideal_temp": 4,  "ideal_humidity": 65, "shelf_life": 30, "zone": "C"},
    "potato": {"ideal_temp": 6,  "ideal_humidity": 90, "shelf_life": 25, "zone": "D"}
}

# Gas thresholds for spoilage detection
GAS_THRESHOLDS = {
    "ethylene": 0.4,
    "ammonia": 0.05,
    "h2s": 0.06,
    "co2": 0.2
}

# ---- Single item AI decision ----
def analyze_item(item_data):
    label = item_data.get("label", "banana").lower()
    profile = ITEM_PROFILES.get(label, ITEM_PROFILES["banana"])

    temp = item_data.get("temperature", profile["ideal_temp"])
    hum  = item_data.get("humidity", profile["ideal_humidity"])

    # Temperature Optimization
    diff = temp - profile["ideal_temp"]
    if abs(diff) < 1:
        temp_priority = "low"
        temp_action = "Temperature is optimal for this product."
    elif diff > 0:
        temp_priority = "high"
        temp_action = f"Reduce temperature by {abs(diff):.1f}°C to prevent spoilage and save energy."
    else:
        temp_priority = "medium"
        temp_action = f"Increase temperature by {abs(diff):.1f}°C to save energy while maintaining quality."
    temp_conf = round(min(1.0, 0.8 + abs(diff)/10), 3)

    # Spoilage Risk Detection
    eth = item_data.get("ethylene", 0)
    nh3 = item_data.get("ammonia", 0)
    h2s_val = item_data.get("h2s", 0)
    co2_val = item_data.get("co2", 0)

    gas_score = (
        eth / GAS_THRESHOLDS["ethylene"] +
        nh3 / GAS_THRESHOLDS["ammonia"] +
        h2s_val / GAS_THRESHOLDS["h2s"] +
        co2_val / GAS_THRESHOLDS["co2"]
    ) / 4

    if gas_score < 0.6:
        spoil_risk = "low"
    elif gas_score < 1.0:
        spoil_risk = "medium"
    else:
        spoil_risk = "high"
    spoil_conf = round(min(1.0, gas_score), 3)

    # Energy Optimization
    energy_action = "Schedule cooling during peak solar hours to maximize renewable energy usage."
    energy_conf = 0.85
    energy_save = "Optimize zone patterns to save energy while maintaining product quality."
    energy_save_conf = 0.8

    # Alerts
    alerts = []
    if spoil_risk == "high":
        alerts.append({"type": "Critical Alert", "message": f"{label.title()} spoilage risk detected!"})
    elif spoil_risk == "medium":
        alerts.append({"type": "Warning Alert", "message": f"{label.title()} may spoil soon."})
    
    if temp_priority == "high":
        alerts.append({"type": "Warning Alert", "message": f"{label.title()} zone temperature exceeds safe range!"})

    return {
        "item": label.title(),
        "zone": profile["zone"],
        "temperature": temp,
        "humidity": hum,
        "shelf_life_days": profile["shelf_life"],
        "temperature_optimization": {
            "priority": temp_priority,
            "action": temp_action,
            "confidence": temp_conf
        },
        "spoilage_risk_detection": {
            "risk": spoil_risk,
            "confidence": spoil_conf
        },
        "energy_optimization": {
            "action": energy_action,
            "confidence": energy_conf
        },
        "energy_savings_recommendation": {
            "action": energy_save,
            "confidence": energy_save_conf
        },
        "active_alerts": alerts
    }

# ---- Storage compartment aggregation ----
def aggregate_storage(items_list):
    """
    items_list: list of item JSONs, each with sensor data
    Returns storage-level dashboard like Zone A/B/C/D
    """
    zones = defaultdict(list)
    all_alerts = []

    # Analyze items and assign to zones
    for item in items_list:
        label = item.get("label","banana").lower()
        zone = ITEM_PROFILES.get(label, ITEM_PROFILES["banana"])["zone"]
        analyzed = analyze_item(item)
        zones[zone].append(analyzed)
        all_alerts.extend(analyzed["active_alerts"])

    dashboard = {}
    for zone, items in zones.items():
        # Compute zone-level aggregates
        avg_temp = round(sum(i["temperature"] for i in items)/len(items),1)
        avg_hum  = round(sum(i["humidity"] for i in items)/len(items),1)

        # Highest spoilage risk in zone
        risk_order = {"low":0, "medium":1, "high":2}
        max_risk = max(items, key=lambda x: risk_order[x["spoilage_risk_detection"]["risk"]])
        max_risk_level = max_risk["spoilage_risk_detection"]["risk"].title()

        # Peltier duty % based on risk
        peltier = 50 + {"low":0, "medium":20, "high":40}[risk_order[max_risk["spoilage_risk_detection"]["risk"]]]

        dashboard[f"Zone {zone}"] = {
            "risk_level": max_risk_level,
            "items_stored": len(items),
            "temperature": avg_temp,
            "humidity": avg_hum,
            "peltier_duty": f"{peltier}%",
            "items": items
        }

    return {
        "storage_compartments": dashboard,
        "active_alerts": all_alerts
    }

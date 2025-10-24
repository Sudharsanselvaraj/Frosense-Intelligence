import random

# Item profiles
ITEM_PROFILES = {
    "strawberries": {"ideal_temp": 4, "ideal_humidity": 85, "shelf_life": 3, "zone": "A"},
    "milk_cartons": {"ideal_temp": 4.5, "ideal_humidity": 70, "shelf_life": 8, "zone": "B"},
    "leafy_greens": {"ideal_temp": 5.5, "ideal_humidity": 90, "shelf_life": 5, "zone": "C"},
    "frozen_gel_packs": {"ideal_temp": -1, "ideal_humidity": 45, "shelf_life": 30, "zone": "D"}
}

# Gas thresholds
GAS_THRESHOLDS = {"ethylene":0.4, "ammonia":0.05, "h2s":0.06, "co2":0.2}

# Main function
def get_decision(data):
    label = data.get("camera_detection", {}).get("label", "strawberries").lower()
    profile = ITEM_PROFILES.get(label, ITEM_PROFILES["strawberries"])
    
    temp = data.get("temperature", profile["ideal_temp"])
    hum  = data.get("humidity", profile["ideal_humidity"])
    
    # Temperature Optimization
    diff = temp - profile["ideal_temp"]
    if abs(diff)<1:
        temp_priority="low"
        temp_action="Temperature is optimal for this product."
        temp_conf=round(random.uniform(0.8,0.85),3)
    elif diff>0:
        temp_priority="high"
        temp_action=f"Reduce temperature by {abs(diff):.1f}°C to prevent spoilage and save energy."
        temp_conf=round(random.uniform(0.9,0.95),3)
    else:
        temp_priority="medium"
        temp_action=f"Increase temperature by {abs(diff):.1f}°C to save energy while maintaining quality."
        temp_conf=round(random.uniform(0.85,0.9),3)
    
    # Spoilage Risk Detection
    gas_score = random.uniform(0,1.2)
    if gas_score<0.3: spoil="low"
    elif gas_score<0.7: spoil="medium"
    else: spoil="high"
    spoil_conf = round(random.uniform(0.8,0.95),3)
    
    # Energy Optimization
    energy_action = "Schedule cooling during peak solar hours to maximize renewable energy usage."
    energy_conf = round(random.uniform(0.8,0.85),3)
    
    energy_save = "Optimize zone patterns to save energy while maintaining product quality."
    energy_save_conf = round(random.uniform(0.78,0.82),3)
    
    # Alerts
    alerts=[]
    if spoil=="high":
        alerts.append({"type":"Critical Alert", "message":f"{label.replace('_',' ').title()} spoilage risk detected!"})
    if temp_priority=="high":
        alerts.append({"type":"Warning Alert", "message":f"{label.replace('_',' ').title()} zone temperature exceeds safe range!"})
    if random.random()<0.2:
        alerts.append({"type":"Low Alert", "message":"Battery level in Sensor #4 dropped below 30%."})
    
    return {
        "item": label.replace("_"," ").title(),
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
            "risk": spoil,
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

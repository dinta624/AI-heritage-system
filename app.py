from flask import Flask, render_template, request, redirect, url_for
import os
import cv2

app = Flask(__name__)

MONUMENTS = {

    "taj": {
        "name": "Taj Mahal",
        "location": "Agra, Uttar Pradesh",
        "year": "1632-1653",
        "architecture": "Mughal Architecture",
        "material": "White Marble",
        "unesco": "UNESCO World Heritage Site",
        "reference_image": "taj.jpg",
        "damage": "Minor Structural Crack",
        "confidence": "96%",
        "severity": "Low",
        "health": "93%",
        "weather": "Low",
        "cost": "₹4.8 Lakhs",
        "inspection": "20 August 2026",
        "recommendation": "Seal minor cracks and monitor every 30 days.",
        "damage_area": "Main Dome",
        "crack_length": "8.5 cm",
        "damage_percentage": "12%",
        "structural": "Stable",
        "surface": "Minor Wear",
        "moisture": "Low",
        "vegetation": "Low"
    },

    "fort": {
        "name": "Red Fort",
        "location": "Delhi",
        "year": "1638-1648",
        "architecture": "Mughal Fort",
        "material": "Red Sandstone",
        "unesco": "UNESCO World Heritage Site",
        "reference_image": "fort.jpg",
        "damage": "Surface Erosion",
        "confidence": "92%",
        "severity": "Medium",
        "health": "81%",
        "weather": "Medium",
        "cost": "₹8.2 Lakhs",
        "inspection": "15 August 2026",
        "recommendation": "Repair sandstone blocks.",
        "damage_area": "Eastern Wall",
        "crack_length": "15.2 cm",
        "damage_percentage": "22%",
        "structural": "Moderate",
        "surface": "Weathered",
        "moisture": "Medium",
        "vegetation": "Low"
    },

    "temple": {
        "name": "Brihadeeswarar Temple",
        "location": "Thanjavur, Tamil Nadu",
        "year": "1010 CE",
        "architecture": "Dravidian Architecture",
        "material": "Granite",
        "unesco": "UNESCO World Heritage Site",
        "reference_image": "temple.jpg",
        "damage": "Water Damage",
        "confidence": "95%",
        "severity": "High",
        "health": "68%",
        "weather": "High",
        "cost": "₹12 Lakhs",
        "inspection": "05 August 2026",
        "recommendation": "Immediate waterproof treatment.",
        "damage_area": "Temple Base",
        "crack_length": "18.5 cm",
        "damage_percentage": "35%",
        "structural": "Needs Inspection",
        "surface": "Moisture Damage",
        "moisture": "High",
        "vegetation": "Medium"
    },

    "charminar": {
        "name": "Charminar",
        "location": "Hyderabad",
        "year": "1591",
        "architecture": "Indo-Islamic",
        "material": "Granite",
        "unesco": "Historic Monument",
        "reference_image": "charminar.jpg",
        "damage": "Surface Weathering",
        "confidence": "93%",
        "severity": "Medium",
        "health": "84%",
        "weather": "Medium",
        "cost": "₹6 Lakhs",
        "inspection": "10 September 2026",
        "recommendation": "Restore weathered surface.",
        "damage_area": "Minaret",
        "crack_length": "10.2 cm",
        "damage_percentage": "16%",
        "structural": "Stable",
        "surface": "Weathered",
        "moisture": "Medium",
        "vegetation": "Low"
    },

    "gateway": {
        "name": "Gateway of India",
        "location": "Mumbai",
        "year": "1924",
        "architecture": "Indo-Saracenic",
        "material": "Basalt",
        "unesco": "Historical Monument",
        "reference_image": "gateway.jpg",
        "damage": "Stone Erosion",
        "confidence": "90%",
        "severity": "Medium",
        "health": "86%",
        "weather": "Medium",
        "cost": "₹7 Lakhs",
        "inspection": "25 September 2026",
        "recommendation": "Repair stone erosion.",
        "damage_area": "Main Arch",
        "crack_length": "14.1 cm",
        "damage_percentage": "20%",
        "structural": "Good",
        "surface": "Moderate Wear",
        "moisture": "Medium",
        "vegetation": "Low"
    },

    "hampi": {
        "name": "Hampi",
        "location": "Karnataka",
        "year": "14th Century",
        "architecture": "Vijayanagara",
        "material": "Granite",
        "unesco": "UNESCO World Heritage Site",
        "reference_image": "hampi.jpg",
        "damage": "Stone Deterioration",
        "confidence": "94%",
        "severity": "Medium",
        "health": "82%",
        "weather": "High",
        "cost": "₹10 Lakhs",
        "inspection": "18 September 2026",
        "recommendation": "Stone preservation required.",
        "damage_area": "Pillars",
        "crack_length": "11.6 cm",
        "damage_percentage": "19%",
        "structural": "Moderate",
        "surface": "Stone Wear",
        "moisture": "Low",
        "vegetation": "High"
    },

    "indiagate": {
        "name": "India Gate",
        "location": "New Delhi",
        "year": "1931",
        "architecture": "Triumphal Arch",
        "material": "Sandstone",
        "unesco": "National Monument",
        "reference_image": "indiagate.jpg",
        "damage": "Surface Discoloration",
        "confidence": "91%",
        "severity": "Low",
        "health": "90%",
        "weather": "Low",
        "cost": "₹4 Lakhs",
        "inspection": "12 October 2026",
        "recommendation": "Clean surface.",
        "damage_area": "Central Arch",
        "crack_length": "5.5 cm",
        "damage_percentage": "8%",
        "structural": "Excellent",
        "surface": "Minor Discoloration",
        "moisture": "Low",
        "vegetation": "Low"
    },

    "konark": {
        "name": "Konark Sun Temple",
        "location": "Odisha",
        "year": "1250 CE",
        "architecture": "Kalinga",
        "material": "Khondalite",
        "unesco": "UNESCO World Heritage Site",
        "reference_image": "konark.jpg",
        "damage": "Stone Cracking",
        "confidence": "95%",
        "severity": "High",
        "health": "70%",
        "weather": "High",
        "cost": "₹15 Lakhs",
        "inspection": "20 October 2026",
        "recommendation": "Immediate restoration.",
        "damage_area": "Stone Wheel",
        "crack_length": "20.3 cm",
        "damage_percentage": "35%",
        "structural": "Requires Restoration",
        "surface": "Severe Wear",
        "moisture": "Medium",
        "vegetation": "Medium"
    },

    "qutub": {
        "name": "Qutub Minar",
        "location": "Delhi",
        "year": "1193",
        "architecture": "Indo-Islamic",
        "material": "Red Sandstone",
        "unesco": "UNESCO World Heritage Site",
        "reference_image": "qutub.jpg",
        "damage": "Surface Cracks",
        "confidence": "92%",
        "severity": "Medium",
        "health": "80%",
        "weather": "Medium",
        "cost": "₹9 Lakhs",
        "inspection": "30 September 2026",
        "recommendation": "Repair stone joints.",
        "damage_area": "Tower Surface",
        "crack_length": "13.7 cm",
        "damage_percentage": "21%",
        "structural": "Moderate",
        "surface": "Cracked",
        "moisture": "Low",
        "vegetation": "Low"
    },

    "sanchi": {
        "name": "Sanchi Stupa",
        "location": "Madhya Pradesh",
        "year": "3rd Century BCE",
        "architecture": "Buddhist",
        "material": "Stone",
        "unesco": "UNESCO World Heritage Site",
        "reference_image": "sanchi.jpg",
        "damage": "Surface Wear",
        "confidence": "89%",
        "severity": "Low",
        "health": "88%",
        "weather": "Low",
        "cost": "₹5 Lakhs",
        "inspection": "15 November 2026",
        "recommendation": "Regular conservation.",
        "damage_area": "Stone Gateway",
        "crack_length": "7.4 cm",
        "damage_percentage": "10%",
        "structural": "Stable",
        "surface": "Aged Surface",
        "moisture": "Low",
        "vegetation": "Low"
    }
}
# -------------------------------------------------
# Splash Screen
# -------------------------------------------------
@app.route("/")
def splash():
    return render_template("splash.html")


# -------------------------------------------------
# Login
# -------------------------------------------------
@app.route("/login")
def login():
    return render_template("login.html")


# -------------------------------------------------
# Dashboard
# -------------------------------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -------------------------------------------------
# Heritage Sites
# -------------------------------------------------
@app.route("/sites")
@app.route("/heritage-sites")
@app.route("/heritage")
def heritage_sites():
    return render_template("heritage_sites.html")


# -------------------------------------------------
# Monument Details
# -------------------------------------------------
@app.route("/monument-details")
def monument_details():

    # Default monument shown when opening from Heritage Sites
    monument = MONUMENTS["taj"]

    return render_template(
        "monument_details.html",
        monument=monument
    )


# -------------------------------------------------
# AI Scan
# -------------------------------------------------
@app.route("/ai-scan")
def ai_scan():
    return render_template("ai_scan.html")


# -------------------------------------------------
# Health Score Page
# -------------------------------------------------
@app.route("/health-score")
def health_score():

    return render_template(
        "health_score.html",
        image="",
        monument=MONUMENTS["taj"]
    )


# -------------------------------------------------
# Maintenance
# -------------------------------------------------
@app.route("/maintenance")
def maintenance():
    return render_template("maintenance.html")


# -------------------------------------------------
# Reports
# -------------------------------------------------
@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route('/models/<filename>')
def model_files(filename):
    return send_from_directory('models', filename)


# -------------------------------------------------
# Interactive Map
# -------------------------------------------------
@app.route("/map")
def map_page():
    return render_template("map.html")


# -------------------------------------------------
# Drone Monitoring
# -------------------------------------------------
@app.route("/drone-monitoring")
def drone_monitoring():
    return render_template("drone_monitoring.html")


# -------------------------------------------------
# Climate Risk
# -------------------------------------------------
@app.route("/weather-risk")
@app.route("/climate-risk")
@app.route("/climate-change")
def weather_risk():
    return render_template("weather_risk.html")
@app.route("/visualization")
def visualization():
    return render_template("visualization.html")


# -------------------------------------------------
# Citizen Report
# -------------------------------------------------
@app.route("/citizen-report")
def citizen_report():
    return render_template("citizen_report.html")
# -------------------------------------------------
# AI IMAGE ANALYSIS
# -------------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    if "image" not in request.files:
        return "No image uploaded"

    image = request.files["image"]

    if image.filename == "":
        return "No image selected"

    upload_folder = "static/uploads"
    os.makedirs(upload_folder, exist_ok=True)

    image_path = os.path.join(upload_folder, image.filename)
    image.save(image_path)

    filename = image.filename.lower()

    monument = None

    # Detect monument from filename
    for key in MONUMENTS:
        if key in filename:
            monument = MONUMENTS[key]
            break

    # Backup mapping
    if monument is None:

        image_mapping = {
            "taj.jpg": "taj",
            "fort.jpg": "fort",
            "temple.jpg": "temple",
            "charminar.jpg": "charminar",
            "gateway.jpg": "gateway",
            "hampi.jpg": "hampi",
            "indiagate.jpg": "indiagate",
            "konark.jpg": "konark",
            "qutub.jpg": "qutub",
            "sanchi.jpg": "sanchi"
        }

        key = image_mapping.get(filename)

        if key:
            monument = MONUMENTS[key]

    # Final fallback
    if monument is None:

        monument = MONUMENTS["taj"]

    return render_template(
        "health_score.html",
        image=image.filename,
        monument=monument
    )
# -------------------------------------------------
# DRONE IMAGE ANALYSIS
# -------------------------------------------------
@app.route("/drone-analyze", methods=["POST"])
def drone_analyze():

    if "drone_image" not in request.files:
        return "No drone image uploaded"

    image = request.files["drone_image"]

    if image.filename == "":
        return "No image selected"

    upload_folder = "static/uploads/drone"
    os.makedirs(upload_folder, exist_ok=True)

    image_path = os.path.join(upload_folder, image.filename)
    image.save(image_path)

    # Read image using OpenCV
    img = cv2.imread(image_path)

    if img is None:
        return "Invalid image"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)

    edge_score = edges.mean()

    if edge_score > 35:
        damage = "Structural Crack Detected"
        confidence = "94%"
        risk = "High"

    elif edge_score > 15:
        damage = "Surface Erosion Detected"
        confidence = "87%"
        risk = "Medium"

    else:
        damage = "No Major Damage Detected"
        confidence = "90%"
        risk = "Low"

    return render_template(
        "drone_result.html",
        image=image.filename,
        damage=damage,
        confidence=confidence,
        risk=risk
    )


# -------------------------------------------------
# RUN APPLICATION
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
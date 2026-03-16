"""
Generate Shadow AI Detection Architecture diagram as .excalidraw JSON.

Usage: python execution/generate_architecture_diagram.py
Output: .tmp/shadow_ai_architecture.excalidraw
"""

import json
import os
import uuid

# ── Helpers ──────────────────────────────────────────────────────────────────

def rid():
    return uuid.uuid4().hex[:8]

def zone(id, x, y, w, h, bg, stroke, label, label_color=None):
    """Zone background + label text."""
    return [
        {
            "id": id,
            "type": "rectangle",
            "x": x, "y": y,
            "width": w, "height": h,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "dashed",
            "roughness": 0,
            "opacity": 30,
            "groupIds": [],
            "roundness": {"type": 3},
            "isDeleted": False,
            "boundElements": None,
            "link": None,
            "locked": False,
        },
        {
            "id": rid(),
            "type": "text",
            "x": x + 15, "y": y + 10,
            "width": 300, "height": 20,
            "text": label,
            "fontSize": 16,
            "fontFamily": 3,
            "textAlign": "left",
            "verticalAlign": "top",
            "strokeColor": label_color or stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "roughness": 0,
            "opacity": 80,
            "groupIds": [],
            "isDeleted": False,
            "boundElements": None,
            "link": None,
            "locked": False,
        },
    ]

def box(id, x, y, w, h, bg, stroke, text):
    """Rectangle shape with bound text."""
    text_id = f"{id}-text"
    return [
        {
            "id": id,
            "type": "rectangle",
            "x": x, "y": y,
            "width": w, "height": h,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "roundness": {"type": 3},
            "isDeleted": False,
            "boundElements": [{"id": text_id, "type": "text"}],
            "link": None,
            "locked": False,
        },
        {
            "id": text_id,
            "type": "text",
            "x": x + 10, "y": y + 10,
            "width": w - 20, "height": h - 20,
            "text": text,
            "fontSize": 14,
            "fontFamily": 3,
            "textAlign": "center",
            "verticalAlign": "middle",
            "strokeColor": "#1e1e1e",
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "isDeleted": False,
            "boundElements": None,
            "containerId": id,
            "link": None,
            "locked": False,
        },
    ]

def arrow(start_id, end_id, label=None, stroke="#495057", style="solid"):
    """Arrow connecting two shapes by ID."""
    a_id = rid()
    el = {
        "id": a_id,
        "type": "arrow",
        "x": 0, "y": 0,
        "width": 100, "height": 100,
        "strokeColor": stroke,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": style,
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "roundness": {"type": 2},
        "isDeleted": False,
        "points": [[0, 0], [100, 100]],
        "startBinding": {"elementId": start_id, "focus": 0, "gap": 4},
        "endBinding": {"elementId": end_id, "focus": 0, "gap": 4},
        "startArrowhead": None,
        "endArrowhead": "arrow",
        "link": None,
        "locked": False,
    }
    elements = [el]
    if label:
        lbl_id = rid()
        el["boundElements"] = [{"id": lbl_id, "type": "text"}]
        elements.append({
            "id": lbl_id,
            "type": "text",
            "x": 0, "y": 0,
            "width": 120, "height": 20,
            "text": label,
            "fontSize": 12,
            "fontFamily": 3,
            "textAlign": "center",
            "verticalAlign": "middle",
            "strokeColor": stroke,
            "backgroundColor": "#ffffff",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "isDeleted": False,
            "containerId": a_id,
            "boundElements": None,
            "link": None,
            "locked": False,
        })
    else:
        el["boundElements"] = None
    return elements

def title_text(x, y, text, size=24, color="#1e1e1e"):
    return {
        "id": rid(),
        "type": "text",
        "x": x, "y": y,
        "width": 600, "height": 30,
        "text": text,
        "fontSize": size,
        "fontFamily": 3,
        "textAlign": "left",
        "verticalAlign": "top",
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "isDeleted": False,
        "boundElements": None,
        "link": None,
        "locked": False,
    }


# ── Colors ───────────────────────────────────────────────────────────────────

# Sensors (teal/cyan)
SENSOR_BG = "#a5d8ff"
SENSOR_ST = "#1971c2"

# Local Agent (orange)
LOCAL_BG = "#ffe8cc"
LOCAL_ST = "#e8590c"

# Ingestion / Queue (yellow)
QUEUE_BG = "#fff3bf"
QUEUE_ST = "#fab005"

# Compute (purple)
COMPUTE_BG = "#d0bfff"
COMPUTE_ST = "#7048e8"

# Application (blue-purple)
APP_BG = "#eebefa"
APP_ST = "#9c36b5"

# Data (green)
DATA_BG = "#b2f2bb"
DATA_ST = "#2f9e44"

# Output (blue)
OUTPUT_BG = "#a5d8ff"
OUTPUT_ST = "#1971c2"

# Integration (red/pink)
INTEG_BG = "#ffc9c9"
INTEG_ST = "#e03131"

# Security (dark gray)
SEC_BG = "#dee2e6"
SEC_ST = "#495057"

# Zone
ZONE_BG = "#e9ecef"
ZONE_ST = "#868e96"


# ── Layout Constants ─────────────────────────────────────────────────────────

# Canvas dimensions
CX = 40           # left margin
CW = 1520         # total content width
BW = 230          # standard box width
BH = 80           # standard box height
ROW_GAP = 60      # gap between zone bottom and next zone top

# Row Y positions (zone tops)
Y_SENSOR = 80
Y_LOCAL = Y_SENSOR + 200 + ROW_GAP      # 340
Y_INGEST = Y_LOCAL + 200 + ROW_GAP      # 600
Y_COMPUTE = Y_INGEST + 180 + ROW_GAP    # 840
Y_APP = Y_COMPUTE + 200 + ROW_GAP       # 1100
Y_DATA = Y_APP + 200 + ROW_GAP          # 1360
Y_OUTPUT = Y_DATA + 200 + ROW_GAP       # 1620
Y_INTEG = Y_OUTPUT + 200 + ROW_GAP      # 1880

# Box Y offsets within zones (centered vertically)
def box_y(zone_y, zone_h=200):
    return zone_y + (zone_h - BH) // 2


# ── Build Elements ───────────────────────────────────────────────────────────

elements = []

# ── Title ────────────────────────────────────────────────────────────────────
elements.append(title_text(CX, 10, "Shadow AI Detection — System Architecture", 28))
elements.append(title_text(CX, 48, "GCP Jakarta (asia-southeast2) | Privacy-By-Design | Multi-Tenant", 14, "#868e96"))

# ── Security & Sovereignty wrapper (around GCP layers: Ingest→Data) ──────────
elements.extend(zone(
    "zone-security", CX - 30, Y_INGEST - 50,
    CW + 60, (Y_DATA + 200) - Y_INGEST + 100,
    SEC_BG, SEC_ST,
    "🔒 Security & Sovereignty — GCP asia-southeast2 (Jakarta) | VPC Service Controls | Cloud KMS | AES-256 | TLS 1.3",
    "#495057"
))

# ── Zone 1: Penta-Vector Sensor Layer ────────────────────────────────────────
elements.extend(zone("zone-sensor", CX, Y_SENSOR, CW, 200, ZONE_BG, SENSOR_ST,
                      "🔍 Penta-Vector Sensor Layer"))

# 5 sensor boxes spread evenly
sensor_gap = (CW - 5 * BW) // 6
sx = CX + sensor_gap
sy = box_y(Y_SENSOR)

sensors = [
    ("va", "Vector A\nCloud API Sensor\n(Agentless, OAuth)"),
    ("vb", "Vector B\nDNS Sensor\n(Go Agent, Real-time)"),
    ("vc", "Vector C\nBrowser Extension\n(Manifest V3, PII Scan)"),
    ("vd", "Vector D\nOS Agent\n(Go Binary, Socket Mon.)"),
    ("ve", "Vector E\nMCP Scanner\n(JSON-RPC, Config Watch)"),
]

for i, (sid, txt) in enumerate(sensors):
    elements.extend(box(sid, sx + i * (BW + sensor_gap), sy, BW, BH, SENSOR_BG, SENSOR_ST, txt))

# ── Zone 2: Local Agent Layer ────────────────────────────────────────────────
elements.extend(zone("zone-local", CX, Y_LOCAL, CW, 200, ZONE_BG, LOCAL_ST,
                      "💾 Local Agent Layer (Amendment #8)"))

ly = box_y(Y_LOCAL)
local_gap = (CW - 3 * 300) // 4
lx = CX + local_gap

elements.extend(box("buf", lx, ly, 300, BH, LOCAL_BG, LOCAL_ST,
                     "Event Buffer\nBoltDB + AES-256 + LZ4\n500MB / ~500K events"))
elements.extend(box("hm", lx + 300 + local_gap, ly, 300, BH, LOCAL_BG, LOCAL_ST,
                     "Health Monitor\nOnline → Degraded → Offline\n→ Backfill"))
elements.extend(box("la", lx + 2 * (300 + local_gap), ly, 300, BH, INTEG_BG, INTEG_ST,
                     "Local Critical Alert\nSMTP / Syslog / Webhook\n< 60s latency"))

# ── Zone 3: GCP Ingestion ───────────────────────────────────────────────────
elements.extend(zone("zone-ingest", CX, Y_INGEST, CW, 180, ZONE_BG, QUEUE_ST,
                      "📥 GCP Ingestion Layer"))

iy = box_y(Y_INGEST, 180)
ig = (CW - 2 * 350) // 3
ix = CX + ig

elements.extend(box("pubsub", ix, iy, 350, BH, QUEUE_BG, QUEUE_ST,
                     "Cloud Pub/Sub\n3 topics | per-firm ordering\n7-day retention"))
elements.extend(box("gcs", ix + 350 + ig, iy, 350, BH, "#ffec99", "#f08c00",
                     "Cloud Storage (GCS)\nDNS logs, PDFs, Signatures\nHot→Nearline→Archive"))

# ── Zone 4: GCP Compute ─────────────────────────────────────────────────────
elements.extend(zone("zone-compute", CX, Y_COMPUTE, CW, 200, ZONE_BG, COMPUTE_ST,
                      "⚙️ GCP Compute Layer (Cloud Dataflow / Apache Beam)"))

cy = box_y(Y_COMPUTE)
cw = 280
cg = (CW - 4 * cw) // 5
cx = CX + cg

compute_items = [
    ("dataflow", "Dataflow Pipeline\nIngestion + Dedup\nCross-vector correlation"),
    ("heuristic", "Heuristic Engine\nHeartbeat Density\nEntropy + CoT Pattern"),
    ("riskscore", "Risk Scorer\n6-Factor Composite\n(Scope/Sensitivity/Auth...)"),
    ("piitag", "PII Tag Processor\nClassification Enrichment\nGeoIP + Cross-border"),
]

for i, (cid, txt) in enumerate(compute_items):
    elements.extend(box(cid, cx + i * (cw + cg), cy, cw, BH, COMPUTE_BG, COMPUTE_ST, txt))

# ── Zone 5: Application Layer ───────────────────────────────────────────────
elements.extend(zone("zone-app", CX, Y_APP, CW, 200, ZONE_BG, APP_ST,
                      "🖥️ Application Layer"))

ay = box_y(Y_APP)
aw = 300
ag = (CW - 4 * aw) // 5
ax = CX + ag

app_items = [
    ("cf", "Cloud Functions\n10 serverless functions\nOAuth poll, alerts, reports"),
    ("cr", "Cloud Run\nNext.js + Tailwind + shadcn\nDashboard + API Backend"),
    ("nudge", "Nudge Engine\n7 nudge types\n(Amendment #7)"),
    ("prescreen", "Pre-Screen Engine\n6 parallel checks < 60s\n(Amendment #1)"),
]

for i, (aid, txt) in enumerate(app_items):
    elements.extend(box(aid, ax + i * (aw + ag), ay, aw, BH, APP_BG, APP_ST, txt))

# ── Zone 6: Data Layer ──────────────────────────────────────────────────────
elements.extend(zone("zone-data", CX, Y_DATA, CW, 200, ZONE_BG, DATA_ST,
                      "🗄️ Data Layer"))

dy = box_y(Y_DATA)
dw = 350
dg = (CW - 3 * dw) // 4
dx = CX + dg

data_items = [
    ("firestore", "Firestore (Hot Storage)\n35+ collections\nfirm_id namespace isolation"),
    ("bigquery", "BigQuery (Audit Vault)\n6 tables | 3-year retention\nSensor hits + HITL + flows"),
    ("sigdb", "AI Signature DB\n200+ tool domains\nMCP packages + pricing"),
]

for i, (did, txt) in enumerate(data_items):
    elements.extend(box(did, dx + i * (dw + dg), dy, dw, BH, DATA_BG, DATA_ST, txt))

# ── Zone 7: Output Layer ────────────────────────────────────────────────────
elements.extend(zone("zone-output", CX, Y_OUTPUT, CW, 200, ZONE_BG, OUTPUT_ST,
                      "📊 Output Layer"))

oy = box_y(Y_OUTPUT)
ow = 300
og = (CW - 4 * ow) // 5
ox = CX + og

output_items = [
    ("dash", "Admin Dashboard\nOverview | Discovery | HITL\nCosts | Data Flows | Reports"),
    ("ep", "Employee Portal\nCatalog | Request | My AI\nSSO-only access"),
    ("sandbox", "AI Sandbox\nEphemeral Cloud Run\nEnvoy proxy + synthetic data"),
    ("rpt", "Reports + Alerts\nOJK PDF | UU PDP RoPA\nWeekly Executive PDF"),
]

for i, (oid, txt) in enumerate(output_items):
    elements.extend(box(oid, ox + i * (ow + og), oy, ow, BH, OUTPUT_BG, OUTPUT_ST, txt))

# ── Zone 8: Integration Layer ───────────────────────────────────────────────
elements.extend(zone("zone-integ", CX, Y_INTEG, CW, 200, ZONE_BG, INTEG_ST,
                      "🔗 Integration Layer (Amendment #6)"))

igy = box_y(Y_INTEG)
igw = 300
igg = (CW - 4 * igw) // 5
igx = CX + igg

integ_items = [
    ("webhook", "Webhook API\n17 event types\nHMAC-SHA256 signed"),
    ("siem", "SIEM Connectors\nChronicle | Splunk | Elastic\nWazuh | Sentinel"),
    ("soar", "SOAR Playbooks\n6 templates\nPB-1 through PB-6"),
    ("ticket", "Ticketing\nJira | ServiceNow\nBidirectional sync"),
]

for i, (iid, txt) in enumerate(integ_items):
    elements.extend(box(iid, igx + i * (igw + igg), igy, igw, BH, INTEG_BG, INTEG_ST, txt))

# ── Arrows ───────────────────────────────────────────────────────────────────

# Sensors → Ingestion / Local Buffer
elements.extend(arrow("va", "pubsub", "events"))               # Cloud API → Pub/Sub
elements.extend(arrow("vb", "buf", "DNS logs"))                 # DNS → Buffer
elements.extend(arrow("vc", "pubsub", "DOM events"))            # Browser → Pub/Sub
elements.extend(arrow("vd", "buf", "socket data"))              # OS Agent → Buffer
elements.extend(arrow("ve", "buf", "MCP telemetry"))            # MCP → Buffer

# Local Agent internal
elements.extend(arrow("hm", "buf", "health checks"))            # Health Monitor → Buffer
elements.extend(arrow("buf", "pubsub", "Online: metadata only", QUEUE_ST))
elements.extend(arrow("buf", "la", "Offline: critical alerts", INTEG_ST, "dashed"))

# Ingestion → Compute
elements.extend(arrow("pubsub", "dataflow"))
elements.extend(arrow("gcs", "dataflow", "DNS log files"))

# Compute pipeline (left to right)
elements.extend(arrow("dataflow", "heuristic"))
elements.extend(arrow("heuristic", "riskscore"))
elements.extend(arrow("riskscore", "piitag"))

# Compute → Data
elements.extend(arrow("piitag", "firestore", "operational data"))
elements.extend(arrow("piitag", "bigquery", "audit records"))
elements.extend(arrow("sigdb", "cf", "signatures", DATA_ST, "dashed"))

# Data → Application
elements.extend(arrow("firestore", "cr"))
elements.extend(arrow("bigquery", "cr"))

# Application → Output
elements.extend(arrow("cr", "dash"))
elements.extend(arrow("cr", "ep"))
elements.extend(arrow("cr", "sandbox"))
elements.extend(arrow("cf", "rpt"))
elements.extend(arrow("nudge", "rpt", "nudge emails"))
elements.extend(arrow("prescreen", "ep", "screening results"))

# Output → Integration
elements.extend(arrow("dash", "webhook"))
elements.extend(arrow("rpt", "webhook"))
elements.extend(arrow("webhook", "siem"))
elements.extend(arrow("webhook", "soar"))
elements.extend(arrow("webhook", "ticket"))

# ── Side annotations ─────────────────────────────────────────────────────────
ann_x = CX + CW + 40

annotations = [
    (Y_SENSOR + 30, "CUSTOMER ENVIRONMENT\n(On-Premise / Workstations)", "#e8590c"),
    (Y_LOCAL + 30, "Zero-Loss Resilience\nWrite-Ahead Logging\nAES-256 at rest", "#e8590c"),
    (Y_INGEST + 20, "↓ Metadata + Tags ONLY ↓\nNever raw content\nNever prompts/responses", "#e03131"),
    (Y_COMPUTE + 30, "8-Stage Pipeline\n+ MCP Threat Analyzer\n+ Cost Enrichment\n+ Policy Check", "#7048e8"),
    (Y_APP + 30, "Better Auth (Session+MFA)\nRoles: Admin/Viewer/\nAuditor/Integration", "#9c36b5"),
    (Y_DATA + 30, "Data Sovereignty\nAll asia-southeast2\nUU PDP + POJK 30/2025", "#2f9e44"),
    (Y_OUTPUT + 30, "Multi-tenant\nfirm_id isolation\nSSO: Google + Entra ID", "#1971c2"),
    (Y_INTEG + 30, "17 webhook event types\n6 SOAR playbooks\nCEF syslog format", "#e03131"),
]

for y, txt, color in annotations:
    elements.append(title_text(ann_x, y, txt, 12, color))

# ── Privacy callout box ──────────────────────────────────────────────────────
priv_y = Y_INGEST - 45
elements.extend(zone("privacy-callout", ann_x - 10, priv_y, 340, 100,
                      "#ffc9c9", "#e03131",
                      "⚠️ PRIVACY BOUNDARY", "#e03131"))
elements.append(title_text(ann_x + 5, priv_y + 35,
    "Sensors transmit ONLY:\n• Classification tags\n• Structural metadata\n• Risk scores\nNEVER: prompts, responses, raw PII",
    11, "#e03131"))


# ── Assemble .excalidraw file ────────────────────────────────────────────────

scene = {
    "type": "excalidraw",
    "version": 2,
    "source": "shadow-ai-detector",
    "elements": elements,
    "appState": {
        "viewBackgroundColor": "#ffffff",
        "gridSize": None,
    },
    "files": {},
}

# Write output
os.makedirs(".tmp", exist_ok=True)
out_path = ".tmp/shadow_ai_architecture.excalidraw"
with open(out_path, "w") as f:
    json.dump(scene, f, indent=2)

print(f"✅ Diagram generated: {out_path}")
print(f"   Elements: {len(elements)}")
print(f"   Open in: excalidraw.com or VS Code Excalidraw extension")

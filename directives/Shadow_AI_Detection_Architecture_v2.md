# Shadow AI Detection — Complete System Architecture

**Version:** 3.0 + All 8 Amendments  
**Date:** March 16, 2026  
**Platform:** Google Cloud Platform (Jakarta Region — asia-southeast2)  
**Classification:** Confidential — Internal Use Only

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Master Architecture Blueprint](#2-master-architecture-blueprint)
3. [Penta-Vector Sensor Layer](#3-penta-vector-sensor-layer)
4. [Local Agent Layer](#4-local-agent-layer-amendment-8)
5. [GCP Ingestion Layer](#5-gcp-ingestion-layer)
6. [GCP Compute Layer](#6-gcp-compute-layer)
7. [Application Layer](#7-application-layer)
8. [Data Layer](#8-data-layer)
9. [Output Layer](#9-output-layer)
10. [Integration Layer](#10-integration-layer-amendment-6)
11. [Security and Sovereignty Layer](#11-security-and-sovereignty-layer)
12. [Data Flow Diagrams](#12-data-flow-diagrams)
13. [Database Schema Overview](#13-database-schema-overview)
14. [Deployment Topology](#14-deployment-topology)
15. [Amendment Feature Map](#15-amendment-feature-map)

---

## 1. Architecture Overview

The Shadow AI Detection platform operates on a Distributed Penta-Vector Sensor Model aggregated into a multi-tenant, serverless GCP backend. The architecture is designed around five core principles:

- **Data Sovereignty:** All compute and storage pinned to GCP Jakarta Region (asia-southeast2). Sensitive network traffic processed locally via on-premise agents. Only metadata leaves the company.
- **Local-First Detection:** PII scanning, MCP inspection, and heuristic analysis run on-device. Only classification tags and metadata are transmitted to the cloud.
- **Zero-Loss Resilience:** Local event buffers with write-ahead logging ensure no telemetry is lost during network outages (Amendment #8).
- **Privacy-By-Design:** The platform never captures prompt content, AI responses, or raw PII. Only structural classification tags flow to the cloud backend. This is enforced at the sensor layer, not by policy.
- **Multi-Tenant Isolation:** Firestore namespace logic with firm_id root collections and VPC Service Controls enforce strict tenant boundaries.

---

## 2. Master Architecture Blueprint

This section provides the definitive system diagram, structured as an Excalidraw-ready component and connection specification.

### 2.1 Layer Color Key

| Layer | Color (Hex) | Background (Hex) | Label |
|---|---|---|---|
| Penta-Vector Sensors | #1B4F72 (dark blue) | #D6EAF8 (light blue) | SENSOR |
| Local Agent | #7D6608 (dark yellow) | #FEF9E7 (light yellow) | LOCAL |
| GCP Ingestion | #1A5276 (navy) | #D4E6F1 (pale blue) | INGEST |
| GCP Compute | #4A235A (purple) | #F4ECF7 (light purple) | COMPUTE |
| Application | #196F3D (green) | #D5F5E3 (light green) | APP |
| Data | #784212 (brown) | #FDF2E9 (light brown) | DATA |
| Output | #1B4F72 (dark blue) | #EBF5FB (ice blue) | OUTPUT |
| Integration | #616A6B (gray) | #F2F3F4 (light gray) | INTEG |
| Security | #C0392B (red) | #FDEDEC (light red) | SEC |

### 2.2 Components (Excalidraw Rectangles)

Each component below maps to one Excalidraw rectangle. Group IDs indicate which frame/group the component belongs to.

#### Group: SENSORS (Frame label: "Penta-Vector Sensor Layer")

| ID | Label (Line 1) | Label (Line 2) | Width | Height |
|---|---|---|---|---|
| VA | Vector A | Cloud API Sensor (G-Workspace, M365, Slack) | 240 | 80 |
| VB | Vector B | DNS Sensor (Firewall log ingestion) | 240 | 80 |
| VC | Vector C | Browser Extension (MV3 + PII Scanner) | 240 | 80 |
| VD | Vector D | OS Agent (Process/Socket/PID + Heuristics) | 240 | 80 |
| VE | Vector E | MCP Scanner (Manifest + Config + Port Probe) | 240 | 80 |

#### Group: LOCAL (Frame label: "Local Agent Layer [Am.8]")

| ID | Label (Line 1) | Label (Line 2) | Width | Height |
|---|---|---|---|---|
| BUF | Event Buffer | BoltDB + AES-256 + LZ4 + Write-Ahead Log | 220 | 70 |
| HM | Health Monitor | Online / Degraded / Offline State Machine | 220 | 70 |
| LA | Local Critical Alert | SMTP + Syslog + Webhook (Offline-capable) | 220 | 70 |
| BS | Backfill Sync | Throttled Batch Replay + Resume-on-Failure | 220 | 70 |
| VCBUF | Browser Offline Buffer | IndexedDB (50 MB) for Vector C | 220 | 60 |

#### Group: INGEST (Frame label: "GCP Ingestion Layer")

| ID | Label (Line 1) | Label (Line 2) | Width | Height |
|---|---|---|---|---|
| PS | Cloud Pub/Sub | Decoupled event intake (3 topics) | 200 | 70 |
| GCS | Cloud Storage (GCS) | DNS logs + PDFs + Signature DB snapshots | 200 | 70 |

#### Group: COMPUTE (Frame label: "GCP Compute Layer")

| ID | Label (Line 1) | Label (Line 2) | Width | Height |
|---|---|---|---|---|
| DF | Cloud Dataflow | Apache Beam real-time pipeline | 200 | 60 |
| DD | De-Duplication | Cross-vector correlation engine | 200 | 60 |
| HE | Heuristic Engine | Heartbeat + Entropy + Chain-of-Thought | 200 | 60 |
| RS | Risk Scorer | 6-factor composite scoring | 200 | 60 |
| MTA | MCP Threat Analyzer | Mutation detection + Escalation chains | 200 | 60 |
| PII | PII Tag Processor | Classification enrichment + GeoIP | 200 | 60 |
| CE | Cost Enricher | Signature DB pricing lookup [Am.3] | 200 | 60 |
| PC | Policy Checker | Tier validation + Allowlist enforcement [Am.1] | 200 | 60 |

#### Group: APP (Frame label: "Application Layer")

| ID | Label (Line 1) | Label (Line 2) | Width | Height |
|---|---|---|---|---|
| CF | Cloud Functions | OAuth polling + Alert dispatch + PDF gen | 220 | 70 |
| CR | Cloud Run | Next.js Dashboard + API Backend | 220 | 70 |
| AUTH | Better Auth | SSO + RBAC + MFA (Admin/Viewer/Auditor) | 200 | 60 |
| NE | Nudge Engine [Am.7] | 7 nudge types + AUP distribution | 200 | 60 |
| PSE | Pre-Screening Engine [Am.1] | 6 parallel checks in 60 seconds | 200 | 60 |

#### Group: DATA (Frame label: "GCP Data Layer")

| ID | Label (Line 1) | Label (Line 2) | Width | Height |
|---|---|---|---|---|
| FS | Firestore | Multi-tenant operational data (35 collections) | 200 | 70 |
| BQ | BigQuery | Immutable audit warehouse (6 tables) | 200 | 70 |
| SDB | Signature DB | 200+ AI domains + pricing + MCP packages | 200 | 70 |

#### Group: OUTPUTS (Frame label: "Output Layer")

| ID | Label (Line 1) | Label (Line 2) | Width | Height |
|---|---|---|---|---|
| DASH | Admin Dashboard | Overview + Discovery + HITL + Costs + Flows + MCP | 240 | 70 |
| EP | Employee Portal [Am.1+7] | Catalog + My AI + Requests + Nudges | 240 | 70 |
| SAND | AI Sandbox [Am.5] | Cloud Run containers + Synthetic Data | 240 | 70 |
| ALERTS | Alert and Report Engine | Email + In-app + OJK PDF + Weekly + RoPA | 240 | 70 |

#### Group: INTEG (Frame label: "Integration Layer [Am.6]")

| ID | Label (Line 1) | Label (Line 2) | Width | Height |
|---|---|---|---|---|
| WH | Webhook API | 17 event types + HMAC-SHA256 | 200 | 60 |
| REST | REST API | OAuth 2.0 + Role-scoped + Pagination | 200 | 60 |
| SIEM | SIEM Connectors | Chronicle + Splunk + Elastic + Syslog/CEF | 200 | 60 |
| SOAR | SOAR Playbooks | 6 templates (XSOAR + Sentinel + JSON) | 200 | 60 |
| TICK | Ticketing | Jira + ServiceNow (Bidirectional sync) | 200 | 60 |

#### Group: SEC (Frame label: "Security and Sovereignty Layer" - dashed border around DATA + COMPUTE + APP)

| ID | Label (Line 1) | Label (Line 2) | Width | Height |
|---|---|---|---|---|
| VPC | VPC Service Controls | Sovereignty perimeter | 180 | 50 |
| KMS | Cloud KMS | AES-256 field-level encryption | 180 | 50 |
| JAK | Jakarta Region Pin | asia-southeast2 (UU PDP Art. 56) | 180 | 50 |

### 2.3 Connections (Excalidraw Arrows)

Each row is one arrow. "Style" indicates solid (data flow) or dashed (security/control relationship).

#### Sensor to Local/Ingestion

| From | To | Label | Style | Notes |
|---|---|---|---|---|
| VA | PS | OAuth data | solid | Vector A is agentless, goes directly to cloud |
| VB | BUF | DNS metadata | solid | Passes through local buffer first |
| VC | PS | DOM + PII tags | solid | Direct to cloud when online |
| VC | VCBUF | (offline) | dashed | IndexedDB buffer when browser-cloud fails |
| VD | BUF | Process telemetry | solid | Always writes to local buffer first |
| VE | BUF | MCP manifests | solid | Always writes to local buffer first |

#### Local Agent Internal

| From | To | Label | Style | Notes |
|---|---|---|---|---|
| HM | BUF | Controls mode | dashed | State machine governs buffer behavior |
| BUF | PS | Online/Degraded delivery | solid | Primary path when cloud is reachable |
| BUF | LA | Offline critical alert | solid | Only for critical-severity during OFFLINE |
| BS | PS | Backfill replay | solid | Throttled batch delivery on recovery |
| VCBUF | PS | Browser sync | solid | IndexedDB flush on reconnection |

#### Ingestion to Compute

| From | To | Label | Style | Notes |
|---|---|---|---|---|
| PS | DF | Event stream | solid | Main telemetry pipeline |
| GCS | DF | DNS log files | solid | Batch file ingestion |

#### Compute Pipeline (sequential)

| From | To | Label | Style | Notes |
|---|---|---|---|---|
| DF | DD | Parsed events | solid | Step 1 to 2 |
| DD | HE | De-duped events | solid | Step 2 to 3 |
| HE | RS | Heuristic-tagged | solid | Step 3 to 4 |
| RS | MTA | Risk-scored | solid | Step 4 to 5 |
| MTA | PII | MCP-analyzed | solid | Step 5 to 6 |
| PII | CE | PII-tagged | solid | Step 6 to 7 |
| CE | PC | Cost-enriched | solid | Step 7 to 8 |

#### Compute to Data

| From | To | Label | Style | Notes |
|---|---|---|---|---|
| PC | FS | Operational data | solid | Discovered apps, alerts, scores |
| PC | BQ | Audit data | solid | Immutable event log, flow events |

#### Data to Application

| From | To | Label | Style | Notes |
|---|---|---|---|---|
| FS | CR | Query | solid | Dashboard reads operational data |
| BQ | CR | Analytics query | solid | Reports, data flow visualization |
| FS | CF | Trigger data | solid | Alert and report generation source |
| SDB | CF | Signature lookup | solid | Tool matching, pricing |
| SDB | PSE | Pre-screen reference | solid | Amendment #1 request screening |

#### Application to Outputs

| From | To | Label | Style | Notes |
|---|---|---|---|---|
| CR | DASH | Serves UI | solid | Admin dashboard application |
| CR | EP | Serves UI | solid | Employee portal application |
| CR | SAND | Provisions | solid | Sandbox container management |
| CF | ALERTS | Generates | solid | Email alerts, PDF reports |
| NE | ALERTS | Nudge dispatch | solid | Employee nudge emails |
| PSE | EP | Pre-screen results | solid | Tool request status |
| AUTH | CR | Authenticates | dashed | Session + role enforcement |

#### Outputs to Integrations

| From | To | Label | Style | Notes |
|---|---|---|---|---|
| DASH | WH | Platform events | solid | All 17 event types |
| ALERTS | WH | Alert events | solid | Real-time alert webhook |
| DASH | REST | API responses | solid | Pull-based data access |
| WH | SIEM | Forward events | solid | Syslog/CEF/native connectors |
| WH | SOAR | Trigger playbooks | solid | 6 pre-built playbooks |
| WH | TICK | Create tickets | solid | Jira/ServiceNow auto-creation |
| REST | SIEM | Query data | solid | Pull-based SIEM enrichment |

#### Security (dashed, wraps around protected layers)

| From | To | Label | Style | Notes |
|---|---|---|---|---|
| VPC | DATA | Protects | dashed | Perimeter around Firestore/GCS/BQ |
| VPC | COMPUTE | Protects | dashed | Perimeter around Dataflow |
| KMS | FS | Encrypts | dashed | Field-level encryption |
| KMS | BUF | Encrypts | dashed | Local buffer encryption |
| JAK | DATA | Pins region | dashed | All resources in asia-southeast2 |
| JAK | COMPUTE | Pins region | dashed | All compute in asia-southeast2 |

### 2.4 Suggested Excalidraw Layout

```
LAYOUT GRID (left to right, 9 columns):

Col 1-2:  SENSORS group (5 boxes stacked vertically)
Col 2-3:  LOCAL group (5 boxes stacked vertically, overlapping Col 2)
Col 3-4:  INGEST group (2 boxes stacked)
Col 4-6:  COMPUTE group (8 boxes in 2 columns of 4)
Col 5-6:  APP group (5 boxes, positioned below COMPUTE)
Col 6-7:  DATA group (3 boxes stacked)
Col 7-8:  OUTPUTS group (4 boxes stacked)
Col 8-9:  INTEG group (5 boxes stacked)

SEC group: Dashed red border frame encompassing COMPUTE + APP + DATA

Flow direction: Left to Right (sensors -> local -> ingest -> compute -> data -> app -> outputs -> integrations)

Tip: In Excalidraw, create each group as a "Frame" first, then place
rectangles inside. Draw arrows between rectangle IDs. Use the color
key from Section 2.1 for fill colors.
```

---

## 3. Penta-Vector Sensor Layer

Five distinct sensors target different attack surfaces where Shadow AI enters the organization.

### Vector A: Cloud API Sensor (Agentless)

| Attribute | Value |
|---|---|
| Target | Corporate SaaS integrations (Google Workspace, M365, Slack) |
| Mechanism | Cloud Functions polling OAuth scopes and service-principal permissions |
| Deployment | Cloud-side only (no local agent required) |
| Output | Discovered OAuth-connected AI apps, permission scopes, install timestamps |
| Frequency | Every 15 minutes (configurable) |
| Offline Impact | None (runs entirely in cloud) |

### Vector B: Network DNS Sensor

| Attribute | Value |
|---|---|
| Target | Network-level traffic on corporate Wi-Fi |
| Mechanism | GCS ingestion of Firewall/DNS logs matched against AI Signature DB |
| Deployment | Lightweight Go agent on network perimeter or DNS forwarder |
| Output | AI domain hits, source IPs, query volumes, personal-account detection |
| Frequency | Real-time log streaming |
| Offline Impact | Logs buffered locally (Amendment #8). Signature matching continues against cached DB. |

### Vector C: Universal Browser Extension

| Attribute | Value |
|---|---|
| Target | Managed and unmanaged browser profiles |
| Mechanism | Cross-browser Manifest V3 extension monitoring DOM and network requests |
| Deployment | Chrome/Edge via Chrome Cloud Management or MDM |
| Output | AI tool DOM interactions, extension inventory, PII classification tags, employee in-browser warnings (Amendment #4) |
| Frequency | Real-time (event-driven) |
| Offline Impact | IndexedDB buffer (50 MB) stores events when browser-to-cloud connection fails (Amendment #8). PII scanner and employee warnings function fully offline. |

### Vector D: Endpoint OS Agent

| Attribute | Value |
|---|---|
| Target | Non-browser processes (CLI tools, Python scripts, Local LLMs) |
| Mechanism | Lightweight Go binary monitoring outbound socket calls + process-to-PID mapping |
| Deployment | Installed on workstations (Docker or native binary) |
| Output | Headless AI tool detection (AutoGPT, Aider, Claude Code), Heartbeat density, Entropy analysis, Chain-of-Thought patterning |
| Frequency | Every 60 seconds (process scan) + real-time (socket monitoring) |
| Offline Impact | All events written to local BoltDB buffer (Amendment #8). Heuristics run locally with cached thresholds. |

### Vector E: MCP Protocol Scanner (Amendment #2)

| Attribute | Value |
|---|---|
| Target | MCP client-server connections (local and remote) |
| Mechanism | Process scanning + localhost JSON-RPC port probing + config file watching + MCP manifest collection (tools/list, resources/list) |
| Deployment | Extension module within Vector D OS Agent (no separate install) |
| Output | MCP server inventory, tool descriptions (hashed for poisoning detection), credential audit, allowlist compliance, risk scores |
| Frequency | Every 60 seconds (process scan) + on-demand (config file change) |
| Offline Impact | All events written to local buffer. Allowlist checks run against locally-cached policy (Amendment #8). |

### Penta-Vector Coverage Matrix

| Attack Surface | A | B | C | D | E |
|---|---|---|---|---|---|
| SaaS OAuth AI apps | YES | - | - | - | - |
| Personal-account AI on corporate Wi-Fi | - | YES | - | - | - |
| AI browser extensions and sidebars | - | - | YES | - | - |
| Embedded SaaS AI features (Am.1 FR-17) | - | - | YES | - | - |
| CLI tools (AutoGPT, Aider, Claude Code) | - | - | - | YES | - |
| Local LLMs (Ollama, LM Studio) | - | - | - | YES | - |
| Autonomous AI agents (Heartbeat detection) | - | - | - | YES | - |
| Local MCP servers | - | - | - | - | YES |
| Remote MCP servers | - | YES | - | YES | YES |
| MCP tool poisoning | - | - | - | - | YES |
| MCP over-permissioned tokens | - | - | - | - | YES |

---

## 4. Local Agent Layer (Amendment #8)

Ensures zero data loss and continuous detection during network outages.

### 4.1 Local Event Buffer

| Attribute | Value |
|---|---|
| Engine | BoltDB (embedded key-value store within Go agent binary) |
| Encryption | AES-256 at rest (key derived from agent installation secret) |
| Compression | LZ4 (approximately 60% size reduction) |
| Capacity | 500 MB default (approximately 500K events, approximately 7 days for 500-employee org) |
| Strategy | Write-ahead: events persisted locally BEFORE cloud transmission attempted |
| Cleanup | FIFO for delivered events. Undelivered events are never purged, they compress in place. |

### 4.2 Connectivity Health Monitor (State Machine)

**Excalidraw Blueprint: 4 rectangles connected by arrows in vertical flow**

| State | Condition | Behavior | Color |
|---|---|---|---|
| ONLINE | Cloud responds under 5s, delivery succeeds | Normal real-time scan + transmit | Green (#27AE60) |
| DEGRADED | Latency over 5s OR over 10% drop rate in 5-min window | Batch mode: buffer accumulates, flushes every 60s | Yellow (#F39C12) |
| OFFLINE | 3 consecutive health check failures (40s intervals) | Full local buffering. No cloud transmission. Local critical alerts active. | Red (#E74C3C) |
| BACKFILL | 3 consecutive successful health checks after OFFLINE | Throttled batch replay: 100 events per batch, 500ms delay. Resume-on-failure. | Blue (#3498DB) |

**Transitions (arrows between states):**
- ONLINE to DEGRADED: Latency threshold exceeded
- DEGRADED to OFFLINE: 3 consecutive failures
- OFFLINE to BACKFILL: 3 consecutive successes
- BACKFILL to ONLINE: All buffered events delivered
- BACKFILL to OFFLINE: Connectivity drops again during backfill (resume later)

### 4.3 Backfill Sync Protocol (Numbered Steps)

1. Connectivity confirmed via 3 consecutive successful health checks (approximately 2 minutes of stable connectivity)
2. Agent reads undelivered events from local buffer in chronological order (oldest first)
3. Events transmitted in batches of 100 with configurable throttle delay (default 500ms between batches)
4. Each batch receives delivery confirmation from Pub/Sub. Confirmed events marked as delivered in local buffer.
5. If connectivity drops again during backfill, agent immediately re-enters OFFLINE mode. Remaining undelivered events stay in buffer. Backfill resumes on next recovery.
6. Dashboard shows: Backfill in Progress [X/Y] events synced
7. After all events synced: Backfill complete. [Y] events recovered from [duration] outage.

### 4.4 Local Critical Alert

| Attribute | Value |
|---|---|
| Triggers | Unauthorized MCP server (Vector E), Critical agentic AI detection (Vector D), PII exfiltration pattern (Amendment #4) |
| Channels | Local SMTP, Local Syslog, Local Webhook (all configurable in agent-config.yaml) |
| Latency | Under 60 seconds from detection |
| Deduplication | Matched with cloud alert by event_id after backfill completes |

### 4.5 Browser Extension Offline Buffer (Vector C)

| Attribute | Value |
|---|---|
| Storage | IndexedDB in employee browser |
| Capacity | 50 MB maximum |
| Trigger | Browser extension loses connection to cloud backend |
| Sync | Auto-flushes to Pub/Sub within 5 minutes of reconnection |
| Employee Impact | Transparent. PII warnings and in-browser nudges continue functioning fully offline. |

---

## 5. GCP Ingestion Layer

### 5.1 Cloud Pub/Sub

| Attribute | Value |
|---|---|
| Purpose | Decoupled, high-volume event intake from all sensors |
| Topics | shadow-ai-telemetry (main), shadow-ai-dns (DNS-specific), shadow-ai-mcp (MCP-specific) |
| Ordering | Per-firm_id message ordering for consistent processing |
| Retention | 7 days (for reprocessing on Dataflow pipeline updates) |

### 5.2 Cloud Storage (GCS)

| Attribute | Value |
|---|---|
| Purpose | Raw DNS log file ingestion, generated PDF reports, Signature DB snapshots, sandbox synthetic data |
| Lifecycle | Hot (0-30 days), Nearline (30-90 days), Archive (90+ days) |
| Region | asia-southeast2 (Jakarta), single-region bucket |

---

## 6. GCP Compute Layer

### 6.1 Cloud Dataflow Pipeline (Apache Beam)

The pipeline has 8 sequential processing stages. Each stage is one Dataflow transform.

**Excalidraw Blueprint: 8 rectangles connected left-to-right (or top-to-bottom) with arrows**

| Stage | Name | Function | Amendment |
|---|---|---|---|
| 1 | Ingestion | Parse sensor telemetry from all 5 vectors. Normalize event schema. | PRD v3.0 |
| 2 | De-Duplication | Cross-vector correlation. Merge when DNS + Browser flag same event. Prevent duplicate alerts. | PRD v3.0 |
| 3 | Heuristic Engine | Heartbeat density profiler (human vs agent speed). Entropy analysis (automated vs organic). Chain-of-Thought patterning (Completion + Research API alternation). | PRD v3.0 |
| 4 | Risk Scorer | 6-factor composite: Tool scope breadth (25%), Data source sensitivity (25%), Auth strength (20%), Server provenance (15%), HITL controls (10%), Data residency (5%). | PRD v3.0 |
| 5 | MCP Threat Analyzer | Tool description mutation detection. Privilege escalation chain correlation. Anomalous invocation pattern detection. | Amendment #2 |
| 6 | PII Tag Processor | Classification tag enrichment. GeoIP destination resolution. Cross-border transfer detection. UU PDP Art. 56 compliance flagging. | Amendment #4 |
| 7 | Cost Enricher | Signature DB pricing lookup. 3-tier cost estimation (Actual / Reported / Estimated). | Amendment #3 |
| 8 | Policy Checker | Tier compliance validation (Am.1). Allowlist and blocklist enforcement. Auto-approve pipeline for low-risk tools. | Amendment #1 |

**Pipeline Output Targets:**
- Firestore: operational data (discovered apps, alerts, triage status, scores)
- BigQuery: audit warehouse (immutable event log, data flow events, HITL decisions)
- Alert Engine: real-time alert triggers (email, webhook, nudge)

---

## 7. Application Layer

### 7.1 Cloud Functions (Serverless)

| Function | Purpose | Trigger | Amendment |
|---|---|---|---|
| oauth-poller | Poll G-Workspace, M365, Slack OAuth scopes (Vector A) | Cloud Scheduler (every 15 min) | PRD v3.0 |
| alert-dispatcher | Send email alerts + webhook events + nudge notifications | Pub/Sub (alert events) | PRD v3.0 |
| ojk-pdf-generator | Generate POJK 30/2025 Semester Risk Report PDF (Puppeteer) | HTTP (admin trigger) | PRD v3.0 |
| ropa-generator | Generate UU PDP RoPA export | HTTP (admin trigger) | PRD v3.0 |
| weekly-report | Compile and send weekly executive PDF | Cloud Scheduler (Monday 8AM WIB) | PRD v3.0 |
| pre-screener | 6-check tool pre-screening in under 60 seconds | HTTP (employee request) | Amendment #1 |
| cost-estimator | 3-tier cost calculation pipeline | Cloud Scheduler (weekly) | Amendment #3 |
| cross-border-alerter | PII + non-Indonesia destination alert | Pub/Sub (flow events) | Amendment #4 |
| sandbox-provisioner | Provision and destroy evaluation containers | HTTP (admin trigger) | Amendment #5 |
| nudge-sender | 7 nudge type email dispatch | Pub/Sub (detection events) | Amendment #7 |
| score-calculator | Monthly department compliance scorecard | Cloud Scheduler (1st of month) | Amendment #7 |

### 7.2 Cloud Run Services

| Service | Purpose | Tech | Amendment |
|---|---|---|---|
| dashboard-app | Admin dashboard + API backend | Next.js + Tailwind + shadcn/ui | PRD v3.0 |
| employee-portal | Employee-facing catalog, requests, My AI page | Next.js + SSO integration | Amendment #1 + #7 |
| sandbox-runtime | Isolated evaluation containers with Envoy proxy | Ephemeral Cloud Run + synthetic data | Amendment #5 |

### 7.3 Authentication (Better Auth)

| Attribute | Value |
|---|---|
| Method | Session-based with MFA support |
| Role: Admin | Full access to dashboard, triage, reports, settings |
| Role: Viewer | Read-only dashboard access |
| Role: Auditor | Read-only + compliance reports + HITL audit trail |
| Role: Integration | API + webhook events only (for SIEM/SOAR connectors) |
| SSO | Google Workspace SSO + Microsoft Entra ID SSO |
| Employee Access | SSO-only access to Employee Portal (no admin credentials required) |

---

## 8. Data Layer

### 8.1 Firestore (Hot Storage)

| Attribute | Value |
|---|---|
| Purpose | Multi-tenant operational data |
| Isolation | firm_id root collection namespace + Firestore Security Rules |
| Region | asia-southeast2 (Jakarta) |
| Total Collections | 36 |

#### Firestore Collections by Amendment

**PRD v3.0 Core (9 collections)**

| Collection | Purpose |
|---|---|
| organizations | Multi-tenant root entity: name, tier, compliance_mode, region |
| users | Admin accounts: email, role, MFA status |
| integrations | Sensor connection status, agent health, buffer utilization (+ Am.8 fields) |
| discovered_apps | Every AI tool found: risk, status, source vector, users affected, cost entry, catalog link |
| hitl_logs | HITL audit trail: decision, justification, evidence snapshot, review timestamp |
| alerts | Notification records: severity, channel, is_read, is_local_alert (Am.8) |
| audit_log | Immutable action history: triage decisions, exports, logins (3-year retention) |
| compliance_reports | Generated report metadata: type, period, status, generated_at |
| signature_db | AI tool domains, IP ranges, OAuth client IDs, extension IDs, MCP packages, pricing data |

**Amendment #1: Approved Catalog (4 collections)**

| Collection | Purpose |
|---|---|
| approved_catalog | Employee-facing approved tool registry with safety badges, tier levels, use cases |
| tool_requests | Self-service request pipeline: status, screening result, reviewer, resolution |
| policy_tiers | Data sensitivity tier definitions: required attributes per tier |
| policy_violations | Graduated enforcement records: tier violated, data sensitivity, action taken |

**Amendment #2: MCP Monitoring (5 collections)**

| Collection | Purpose |
|---|---|
| mcp_servers | Discovered MCP server inventory: type, transport, tools, risk score, allowlist status |
| mcp_tools | MCP tool descriptions with description_hash for poisoning detection |
| mcp_credentials | MCP server credentials (encrypted via Cloud KMS, masked in UI) |
| mcp_threats | MCP-specific threat detections: type, evidence, severity |
| mcp_allowlist | Admin-managed MCP policy: approved package names and remote URLs |

**Amendment #3: Cost Intelligence (4 collections)**

| Collection | Purpose |
|---|---|
| ai_cost_entries | Per-tool cost tracking: 3-tier confidence (actual/reported/estimated) |
| cost_thresholds | Configurable spend alert thresholds per tool, department, and org |
| expense_uploads | CSV import metadata: filename, row count, match count |
| expense_matches | Expense-discovery correlation: merchant, amount, matched app, confidence |

**Amendment #4: Data Flow Tracing (2 collections)**

| Collection | Purpose |
|---|---|
| detection_rules | Admin-configurable PII patterns: regex, keyword, entropy, sensitivity tier |
| employee_warnings | Warning interaction tracking: category detected, action taken, alternative suggested |

**Amendment #5: AI Sandbox (3 collections)**

| Collection | Purpose |
|---|---|
| sandbox_trials | Sandbox lifecycle: status, container ID, duration, risk score, decision |
| sandbox_participants | Trial invitations and structured feedback: rating, fit, notes |
| sandbox_reports | Evaluation report metadata and PDF URL reference |

**Amendment #6: Integrations (4 collections)**

| Collection | Purpose |
|---|---|
| webhook_endpoints | Customer webhook configs: URL, secret, event filters, health status |
| api_keys | Role-scoped REST API keys: scope, last used, active status |
| siem_connectors | Per-platform SIEM config: type, connection params, status |
| ticket_links | Bidirectional ticket sync state: external ID, URL, sync status |

**Amendment #7: Nudge Engine (5 collections - CORRECTION: was missing tool_suggestions in original)**

| Collection | Purpose |
|---|---|
| nudge_events | Every nudge interaction: type, channel, sent/opened/clicked/adopted |
| aup_versions | AI Acceptable Use Policy version history: content, published date |
| aup_acknowledgements | Immutable acknowledgement records: user, version, timestamp, IP |
| compliance_scores | Monthly department scores: 5-factor breakdown, trend vs prior |
| tool_suggestions | Employee-submitted tool recommendations via Suggest a Tool form |

### 8.2 BigQuery (Cold Storage / Warehouse)

| Attribute | Value |
|---|---|
| Purpose | Immutable audit vault + high-volume analytics |
| Region | asia-southeast2 (Jakarta) |
| Retention | 3 years (compliance requirement) |
| Total Tables | 6 |

| Table | Purpose | Volume | Amendment |
|---|---|---|---|
| sensor_hits | All sensor telemetry (raw processed events) | High | PRD v3.0 |
| hitl_decisions | Complete HITL audit trail with evidence snapshots | Medium | PRD v3.0 |
| data_flow_events | Classification tags per AI interaction (NO prompt content) | Very High | Amendment #4 |
| data_flow_aggregates | Pre-computed daily/weekly rollups for dashboard performance | Medium | Amendment #4 |
| sandbox_network_logs | Sandbox Envoy proxy traffic logs per trial | High (per trial) | Amendment #5 |
| webhook_deliveries | Webhook delivery tracking with status and response codes | High (30-day retention) | Amendment #6 |

### 8.3 AI Signature Database

| Attribute | Value |
|---|---|
| Entries | 200+ AI tool domains (expanding weekly) |
| Content | Domain patterns, IP ranges, OAuth client IDs, browser extension IDs, MCP package names, MCP server URLs, vendor metadata, privacy policy summaries, estimated per-user pricing (Am.3), vendor merchant category codes (Am.3) |
| Updates | Weekly automated pipeline + community submission for unknown tools |
| Caching | Locally cached on DNS sensor (Vector B) and OS agent (Vector D) for low-latency matching during offline mode |

---

## 9. Output Layer

### 9.1 Admin Dashboard Tab Structure

**Excalidraw Blueprint: Tab bar with 8 tabs, each expanding to a content area**

| Tab | Content | Amendments |
|---|---|---|
| Overview | Total tools, risk distribution, compliance status (OJK/UU PDP), financial impact card, enablement metrics, department leaderboard, agent health, HITL pending | Am.1, Am.3, Am.7, Am.8 |
| Discovery | Filterable table: Name, Vector (A/B/C/D/E), Risk, Status, Users, Residency, Cost, Last Seen. MCP Servers sub-view. Launch Sandbox action. Add to Catalog action. | Am.2, Am.5, Am.1 |
| HITL Audit | All human-in-the-loop decisions. Filterable by risk, decision type, date range. Evidence snapshot viewer. | PRD v3.0 |
| Costs | AI Spend Dashboard (monthly/quarterly/annual). Overlap and duplicate analysis. Zombie license detection. Expense correlation. | Amendment #3 |
| Data Flows | Sankey diagram: Users to Tools to Destinations. Color-coded by sensitivity tier. Cross-border transfer monitoring. | Amendment #4 |
| Catalog | Admin view of Approved Catalog. CRUD management. Request pipeline metrics. | Amendment #1 |
| Integrations | Per-sensor health (Online/Degraded/Offline). Buffer utilization. SIEM/SOAR connector status. Webhook endpoint health. | Am.6, Am.8 |
| Settings | Org profile, subscription, RBAC, policy tiers, MCP allowlist, AUP editor, webhook/API keys, SIEM config, nudge templates, detection rules. | All |
| Reports | OJK Semester Report generator, UU PDP RoPA export, weekly PDF, ISO 42001 docs (future). | PRD v3.0 |

### 9.2 Employee Portal Page Structure

| Page | Content | Amendments |
|---|---|---|
| Catalog | Grid/list of approved tools with safety badges, categories, tier indicators, search/filter | Amendment #1 |
| Request a Tool | URL submission, 60-second pre-screening, status tracker | Amendment #1 |
| My AI | Personal detected tools, compliance score, AUP status, tool requests, Suggest a Tool form | Amendment #7 |

### 9.3 AI Sandbox Environment

**Excalidraw Blueprint: One large frame containing 4 internal boxes**

| Component | Function | Amendment |
|---|---|---|
| Cloud Run Container | Isolated Linux environment per trial. Auto-provision, auto-destroy. | Amendment #5 |
| Envoy Network Proxy | All outbound traffic logged. Captures destinations, sizes, protocols. Blocks production APIs. | Amendment #5 |
| Synthetic Data Engine | Faker (id_ID) + custom KTP/NPWP generators. Pre-loaded documents, financial data, email corpus. | Amendment #5 |
| Penta-Vector Sensors | Vector C + D + E pre-installed. All telemetry tagged as sandbox_trial. | Amendment #5 |

---

## 10. Integration Layer (Amendment #6)

### 10.1 Webhook API Event Types (17 total)

| Event Type | Severity | Source | Amendment |
|---|---|---|---|
| discovery.new_tool | Info / Medium / High | Vectors A-E | PRD v3.0 |
| discovery.agentic_detected | High | Vector D Heuristics | PRD v3.0 |
| discovery.mcp_server_found | High | Vector E | Amendment #2 |
| triage.decision_made | Info | Admin Action | PRD v3.0 |
| alert.pii_cross_border | Critical | PII Tag Processor | Amendment #4 |
| alert.policy_violation | Medium / High | Policy Checker | Amendment #1 |
| alert.mcp_tool_poisoning | Critical | MCP Threat Analyzer | Amendment #2 |
| alert.mcp_overpermission | Medium | MCP Scanner | Amendment #2 |
| alert.spend_threshold | Medium | Cost Enricher | Amendment #3 |
| compliance.report_generated | Info | Report Engine | PRD v3.0 |
| hitl.review_required | High | HITL Engine | PRD v3.0 |
| hitl.decision_logged | Info | HITL Engine | PRD v3.0 |
| sandbox.trial_started | Info | Sandbox Provisioner | Amendment #5 |
| sandbox.trial_completed | Info | Sandbox Provisioner | Amendment #5 |
| catalog.tool_requested | Info | Employee Portal | Amendment #1 |
| catalog.tool_approved | Info | Admin Action | Amendment #1 |
| system.sensor_offline | High | Health Monitor | Amendment #8 |

### 10.2 SIEM Connectors

| Platform | Method | Priority |
|---|---|---|
| Syslog / CEF (universal) | RFC 5424 or ArcSight CEF over TLS | P1 |
| Google Security Operations (Chronicle) | GCP Pub/Sub topic subscription | P1 |
| Splunk | HTTP Event Collector (HEC) + pre-built Splunk app | P1 |
| Elastic Security | Elasticsearch API + Kibana dashboards | P2 |
| Wazuh | Syslog + custom decoder/rules (Indonesian mid-market focus) | P2 |
| Microsoft Sentinel | Azure Logic App connector | P2 |

### 10.3 SOAR Playbook Templates (6 total)

| ID | Name | Trigger to Response Chain | HITL Gate |
|---|---|---|---|
| PB-1 | High-Risk Tool Detected | Alert, Enrich via Signature DB, Ticket, Notify SOC, Escalate if over 5 users | Yes (ban needs approval) |
| PB-2 | PII Cross-Border Violation | Alert, Check Art. 56, Block network, Compliance incident, Notify DPO | Yes (block needs approval) |
| PB-3 | Unauthorized MCP Server | Alert, Check allowlist, Disable process via OS agent, Ticket, Notify admin | Yes (disable needs approval) |
| PB-4 | Shadow AI Spend Anomaly | Alert, Pull cost data, Identify owner, Procurement ticket, Notify finance | No (informational) |
| PB-5 | Sensor Offline | Alert, Identify host, Attempt restart, P1 ticket if fails | No (auto-remediation) |
| PB-6 | Employee Policy Violation | Alert, Check violation count, 1st: nudge, 2nd: admin, 3rd: HITL escalation | 3rd violation only |

### 10.4 Ticketing Integration

| System | Method | Sync | Priority |
|---|---|---|---|
| Jira (Atlassian) | REST API + webhook + pre-built issue templates | Bidirectional (status sync both ways) | P1 |
| ServiceNow | REST API + Integration Hub connector | Bidirectional | P2 |
| Freshservice | REST API connector | One-way (create only) | P2 |
| Generic (any) | Webhook payload to customer middleware (Zapier, n8n) | One-way | P1 (via webhook) |

---

## 11. Security and Sovereignty Layer

**Excalidraw Blueprint: Dashed red border frame encompassing the COMPUTE, APP, and DATA groups**

### 11.1 Region Pinning

| Attribute | Value |
|---|---|
| Region | asia-southeast2 (Jakarta, Indonesia) |
| Scope | ALL compute and storage resources (no exceptions) |
| Compliance | UU PDP Article 56 (cross-border data transfer) satisfied by architecture |
| Enforcement | Terraform resource constraints + GCP Organization Policy |

### 11.2 Encryption

| Scope | Method | Key Management |
|---|---|---|
| Data at rest (cloud) | AES-256 via Google Cloud KMS | Field-level encryption for PII metadata |
| Data at rest (local buffer) | AES-256 | Key derived from agent installation secret |
| Data in transit | TLS 1.3 | All API communications and sensor telemetry |

### 11.3 Network Isolation

| Control | Purpose |
|---|---|
| VPC Service Controls | Security perimeter around Firestore, GCS, BigQuery, and Dataflow. Prevents unauthorized data exfiltration. |
| Firestore Security Rules | firm_id namespace isolation. Cross-tenant data access blocked at database level. |
| Agent Network Proxy (Sandbox) | Envoy proxy in sandbox environment blocks access to production internal APIs. |

### 11.4 Privacy-By-Design Enforcement Points

| Layer | What Is Captured | What Is NEVER Captured |
|---|---|---|
| Vector B (DNS Sensor) | Domain names, query volumes, source IPs | DNS response content, full packet data |
| Vector C (Browser Extension) | DOM element metadata, PII classification tags | Prompt text, AI response content, page screenshots |
| Vector D (OS Agent) | Process names, socket destinations, PID mappings | File contents, clipboard text, keystrokes |
| Vector E (MCP Scanner) | Tool descriptions, scopes, credential metadata (masked) | Actual credentials, prompt payloads, MCP response data |
| Amendment #4 (PII Scanner) | Classification tags (e.g., PII_KTP_DETECTED) | Actual KTP numbers, financial data, or any raw PII |

---

## 12. Data Flow Diagrams

### 12.1 Flow A: Discovery to Triage to Governance

**Excalidraw Blueprint: Vertical flow with 5 stages**

| Stage | Component | Action | Output |
|---|---|---|---|
| 1 | Penta-Vector Sensors | Detect AI tool usage | Raw telemetry event |
| 2 | Cloud Dataflow Pipeline | Process through 8 stages | Risk-scored, enriched event in Firestore/BigQuery |
| 3 | Alert Engine | Evaluate severity thresholds | Email alert + in-app notification + nudge (Am.7) + webhook (Am.6) |
| 4 | Admin Dashboard (Triage) | Admin reviews discovery | Three actions: Approve (+ Add to Catalog), Ban, or Launch Sandbox (Am.5) |
| 5 | Governance Action | Decision logged in audit trail | HITL record (if high-risk) + ticket (Am.6) + employee notification |

### 12.2 Flow B: Employee Self-Service Request (Amendment #1)

**Excalidraw Blueprint: Decision tree with 3 branches**

| Stage | Component | Action |
|---|---|---|
| 1 | Employee Portal | Employee submits tool URL |
| 2 | Pre-Screening Engine | 6 parallel checks in under 60 seconds. Outputs risk score (Low/Medium/High). |
| 3a (Low Risk) | Auto-Approve Pipeline | Auto-approved for Tier 1. Added to catalog. IT notified (informational). |
| 3b (Medium Risk) | IT Triage Queue | Pre-populated assessment. 48-hour SLA. Option to Launch Sandbox (Am.5). |
| 3c (High Risk) | HITL Review | Compliance flags highlighted. 5-day SLA. Sandbox required before approval. |
| 4 (Denied) | Employee Notification | Denial reason + Suggested Alternative from Approved Catalog. |

### 12.3 Flow C: OJK Compliance Report Generation

**Excalidraw Blueprint: 4 data sources feeding into 1 generator, outputting 4-section report**

**Data Sources (4 inputs):**
- Firestore: discovered_apps + integrations (discovery data)
- hitl_logs: HITL audit trail with evidence snapshots
- BigQuery: data_flow_events (Amendment #4 classification tags + destinations)
- Firestore: ai_cost_entries (Amendment #3 cost data per vendor)

**Generator:** OJK PDF Generator (Cloud Function + Puppeteer)

**Output: POJK 30/2025 Semester Risk Report (4 sections)**

| Section | Title | Content Sources |
|---|---|---|
| 1 | Operational and Cyber Risk | System availability, Shadow AI incident log, AI vendor dependency list with certifications, cost exposure per vendor (Am.3) |
| 2 | Legal and Compliance Risk | RoPA status per tool, data residency confirmation, DPA verification status, cross-border flow evidence (Am.4) |
| 3 | Strategic and Reputation Risk | AI Ethical Score, High-Risk AI Inventory, HITL Oversight Documentation (from hitl_logs), HITL response time verification |
| 4 | Action Plan | Mitigation recommendations, policy review log, cost optimization actions (Am.3) |

---

## 13. Database Schema Overview

### 13.1 Entity Relationships

**Excalidraw Blueprint: Central ORGANIZATIONS entity with radiating connections**

**ORGANIZATIONS connects to:**
- USERS (one to many)
- INTEGRATIONS (one to many)
- DISCOVERED_APPS (one to many)
- APPROVED_CATALOG (one to many) [Am.1]
- TOOL_REQUESTS (one to many) [Am.1]
- POLICY_TIERS (one to many) [Am.1]
- MCP_SERVERS (one to many) [Am.2]
- MCP_ALLOWLIST (one to many) [Am.2]
- AI_COST_ENTRIES (one to many via discovered_apps) [Am.3]
- COST_THRESHOLDS (one to many) [Am.3]
- SANDBOX_TRIALS (one to many) [Am.5]
- WEBHOOK_ENDPOINTS (one to many) [Am.6]
- SIEM_CONNECTORS (one to many) [Am.6]
- API_KEYS (one to many) [Am.6]
- AUP_VERSIONS (one to many) [Am.7]
- COMPLIANCE_SCORES (one to many) [Am.7]

**DISCOVERED_APPS connects to:**
- ALERTS (one to many)
- HITL_LOGS (one to many)
- AI_COST_ENTRIES (one to one) [Am.3]
- DATA_FLOW_EVENTS (one to many) [Am.4]
- TICKET_LINKS (one to many) [Am.6]
- SANDBOX_TRIALS (one to many) [Am.5]
- APPROVED_CATALOG (optional link when converted) [Am.1]

**MCP_SERVERS connects to:**
- MCP_TOOLS (one to many)
- MCP_CREDENTIALS (one to many)
- MCP_THREATS (one to many)

**SANDBOX_TRIALS connects to:**
- SANDBOX_PARTICIPANTS (one to many)
- SANDBOX_NETWORK_LOGS (one to many, BigQuery)
- SANDBOX_REPORTS (one to one)

**USERS connects to:**
- NUDGE_EVENTS (one to many) [Am.7]
- AUP_ACKNOWLEDGEMENTS (one to many) [Am.7]
- EMPLOYEE_WARNINGS (one to many) [Am.4]
- TOOL_SUGGESTIONS (one to many) [Am.7]

---

## 14. Deployment Topology

**Excalidraw Blueprint: Two large frames (Customer Environment and GCP Jakarta) with arrow between them labeled "Metadata + Classification Tags Only (never raw content)"**

### 14.1 Customer Environment Components

| Component | Location | Contains |
|---|---|---|
| Workstation (per employee) | Employee desk | OS Agent (Vector D) + MCP Extension (Vector E) + Local Event Buffer (Am.8) + Chrome Extension (Vector C) with PII Scanner (Am.4) and IndexedDB Buffer (Am.8) |
| Network Perimeter | Server room / cloud gateway | DNS Sensor (Vector B) + Local Event Buffer (Am.8) + Cached Signature DB |
| Corporate SaaS | Cloud (external) | Google Workspace, Microsoft 365, Slack (accessed by Vector A from GCP side, no local agent) |

### 14.2 GCP Jakarta Region Components

| Component | GCP Service | Purpose |
|---|---|---|
| Event Intake | Cloud Pub/Sub | Receives all sensor telemetry |
| File Intake | Cloud Storage (GCS) | DNS log files, PDF reports, synthetic data |
| Processing Pipeline | Cloud Dataflow | 8-stage real-time analysis |
| Operational Database | Firestore | 35 collections, multi-tenant |
| Audit Warehouse | BigQuery | 6 tables, 3-year immutable retention |
| Serverless Logic | Cloud Functions | 11 functions (see Section 7.1) |
| Applications | Cloud Run | 3 services: dashboard, employee portal, sandbox |
| Security Perimeter | VPC Service Controls + Cloud KMS | Sovereignty enforcement |

### 14.3 Data Transmission Boundary

| What Crosses the Boundary | What NEVER Crosses the Boundary |
|---|---|
| AI tool identification metadata (tool name, domain, risk score) | Raw network traffic or DNS response content |
| User count and department association | Employee prompt text or AI response content |
| PII classification tags (e.g., PII_KTP_DETECTED) | Actual KTP numbers, bank accounts, or financial data |
| MCP server tool descriptions and scope lists | MCP prompt payloads or response data |
| Timestamp, source vector, and event type | File contents, clipboard text, or screenshots |
| Heuristic scores (Heartbeat density, Entropy) | Raw process output or application data |

---

## 15. Amendment Feature Map

| # | Amendment | Arch Layer | Priority | Sprints | Weeks |
|---|---|---|---|---|---|
| 8 | Offline/Degraded Mode | Local Agent | MVP (Q2) | +2.5w to Sprints 2-4 | 2.5 |
| 1 | Approved AI Catalog and Self-Service Request Portal | Application + Output | P1 (Q3) | Sprints 6-9 | 8 |
| 2 | MCP Server Monitoring (Vector E) | Sensor + Compute | P1 (Q3) | Sprints 10-13 | 8 |
| 7 | Employee Education and Policy Nudge Engine | Application + Output | P1 (Q3-Q4) | Sprints 29-31 | 6 |
| 3 | AI Cost Intelligence Module | Compute + Output | P1 (Q3-Q4) | Sprints 14-17 | 9 |
| 4 | Prompt-Level Data Flow Tracing | Sensor + Compute + Output | P1 (Q3-Q4) | Sprints 18-21 | 10 |
| 5 | Enterprise AI Sandbox | Application + Output | P2 (Q4) | Sprints 22-25 | 9 |
| 6 | SIEM/SOAR Integration and Webhook API | Integration | P2 (Q4) | Sprints 26-28 | 8 |

**Totals:** 77 functional requirements, 37 user stories, 31 sprints, approximately 70.5 weeks of development.

---

## Appendix: Excalidraw Conversion Quick Reference

### Recommended Excalidraw Settings

| Setting | Value |
|---|---|
| Canvas background | White (#FFFFFF) |
| Default font | Hand-drawn (Virgil) for labels, or Normal for technical text |
| Arrow style | Rounded, with arrowhead on target end |
| Frame style | Use Excalidraw Frames for each layer group |
| Stroke width | 1px for component borders, 2px for group frames |

### Step-by-Step Conversion Process

1. Create 9 Excalidraw Frames using the Layer Color Key (Section 2.1). Arrange left-to-right per the layout grid in Section 2.4.
2. Inside each Frame, add rectangles from the Components table (Section 2.2). Use the fill color from the Layer Color Key.
3. Add text labels to each rectangle: Line 1 (bold) = component name, Line 2 (regular) = description.
4. Draw arrows between rectangles using the Connections table (Section 2.3). Solid arrows for data flow, dashed arrows for security/control relationships.
5. Add the Security layer as a dashed red border Frame encompassing the COMPUTE, APP, and DATA groups.
6. For the Dataflow Pipeline detail (Section 6.1), create a separate Excalidraw page with 8 connected boxes in a vertical column.
7. For the State Machine (Section 4.2), create 4 colored rectangles (green, yellow, red, blue) with labeled arrows between them showing transition conditions.
8. For the ER Diagram (Section 13.1), use the entity relationship listings to create boxes with connection lines. Central entity is ORGANIZATIONS.

---

**Document Status:** Final (Corrected)  
**Classification:** Confidential — Internal Use Only  
**Corrections Applied:** Added missing sandbox-provisioner Cloud Function, added missing ORGANIZATIONS to MCP_SERVERS relationship, added Vector C IndexedDB offline buffer, added REST API integration connection, replaced Mermaid/ASCII diagrams with Excalidraw-ready component specifications, added explicit data transmission boundary table, corrected Amendment #7 collection count to 5, corrected Firestore total from 35 to 36.

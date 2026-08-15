from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
from typing import List, Dict, Any

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/finance")
async def get_finance_data():
    await asyncio.sleep(0.5)
    return {
        "kpis": [
            {"label": "Total Revenue", "value": "$2,845,000", "delta": "↓ 8% vs last month", "trend": "down"},
            {"label": "Net Profit", "value": "$845,000", "delta": "↓ 2% vs last month", "trend": "down"},
            {"label": "Operating Expenses", "value": "$1,200,000", "delta": "↑ 4% vs last month", "trend": "up"},
            {"label": "Cash Flow", "value": "$4.2M", "delta": "Healthy", "trend": "up"},
            {"label": "Accounts Receivable", "value": "$1,420,000", "delta": "↑ 14% this week", "trend": "up"},
            {"label": "Accounts Payable", "value": "$680,000", "delta": "↓ 3% this week", "trend": "down"},
            {"label": "Gross Margin", "value": "42.8%", "delta": "↓ 1.2pp vs Q2", "trend": "down"},
            {"label": "Burn Rate", "value": "$312K/mo", "delta": "Stable", "trend": "flat"}
        ],
        "insight": {
            "title": "AI detected 3 important anomalies",
            "description": "Revenue is down 8% compared to projected forecasts. Outstanding receivables have increased by 14% this week. 2 invoices are overdue beyond 60 days."
        },
        "invoices": [
            {"id": "INV-10291", "customer": "Acme Corp", "amount": "$14,500.00", "status": "Paid", "date": "Oct 12, 2026"},
            {"id": "INV-10292", "customer": "Global Tech", "amount": "$8,200.00", "status": "Pending", "date": "Oct 14, 2026"},
            {"id": "INV-10293", "customer": "Stark Industries", "amount": "$142,000.00", "status": "Overdue", "date": "Sep 01, 2026"},
            {"id": "INV-10294", "customer": "Wayne Enterprises", "amount": "$67,800.00", "status": "Paid", "date": "Oct 10, 2026"},
            {"id": "INV-10295", "customer": "Oscorp Industries", "amount": "$23,400.00", "status": "Pending", "date": "Oct 16, 2026"},
            {"id": "INV-10296", "customer": "LexCorp", "amount": "$198,000.00", "status": "Overdue", "date": "Aug 22, 2026"},
            {"id": "INV-10297", "customer": "Cyberdyne Systems", "amount": "$45,600.00", "status": "Paid", "date": "Oct 08, 2026"},
            {"id": "INV-10298", "customer": "Umbrella Corporation", "amount": "$31,200.00", "status": "Pending", "date": "Oct 18, 2026"},
            {"id": "INV-10299", "customer": "Weyland-Yutani", "amount": "$89,000.00", "status": "Paid", "date": "Oct 05, 2026"},
            {"id": "INV-10300", "customer": "Soylent Corp", "amount": "$12,750.00", "status": "Draft", "date": "Oct 20, 2026"}
        ]
    }

@router.get("/inventory")
async def get_inventory_data():
    await asyncio.sleep(0.5)
    return {
        "kpis": [
            {"label": "Total Inventory Value", "value": "$4,285,100", "delta": "Stable", "trend": "flat"},
            {"label": "Low Stock Alerts", "value": "12", "delta": "Action Required", "trend": "down"},
            {"label": "Active SKUs", "value": "8,492", "delta": "+14 this week", "trend": "up"},
            {"label": "Dead Stock", "value": "248 SKUs", "delta": "$124K value", "trend": "down"},
            {"label": "Avg Days on Hand", "value": "34.2", "delta": "↓ 2.1 days", "trend": "up"},
            {"label": "Stockout Rate", "value": "2.4%", "delta": "↑ 0.6% this week", "trend": "down"}
        ],
        "insight": {
            "title": "AI Inventory Risk: 12 products at risk",
            "description": "5 predicted stockouts within the next 7 days based on current sales velocity. 3 products are significantly overstocked. 4 seasonal items need replenishment before holiday demand surge."
        },
        "products": [
            {"sku": "ABC-100", "name": "Wireless Noise-Canceling Headphones", "stock": 120, "velocity": "840/mo", "status": "Stockout Risk"},
            {"sku": "DEF-200", "name": "Ergonomic Office Chair", "stock": 450, "velocity": "120/mo", "status": "Healthy"},
            {"sku": "GHI-300", "name": "USB-C Hub Multiport Adapter", "stock": 4200, "velocity": "300/mo", "status": "Overstocked"},
            {"sku": "JKL-401", "name": "Mechanical Keyboard (Cherry MX)", "stock": 85, "velocity": "620/mo", "status": "Stockout Risk"},
            {"sku": "MNO-502", "name": "4K Ultra Monitor 32\"", "stock": 310, "velocity": "180/mo", "status": "Healthy"},
            {"sku": "PQR-603", "name": "Wireless Charging Pad", "stock": 1850, "velocity": "210/mo", "status": "Overstocked"},
            {"sku": "STU-704", "name": "Laptop Stand Adjustable", "stock": 42, "velocity": "380/mo", "status": "Stockout Risk"},
            {"sku": "VWX-805", "name": "Bluetooth Earbuds Pro", "stock": 670, "velocity": "540/mo", "status": "Low Stock"},
            {"sku": "YZA-906", "name": "Smart Desk Lamp", "stock": 920, "velocity": "150/mo", "status": "Healthy"},
            {"sku": "BCD-107", "name": "Webcam 1080p HD", "stock": 55, "velocity": "290/mo", "status": "Stockout Risk"},
            {"sku": "EFG-208", "name": "Cable Management Kit", "stock": 3400, "velocity": "80/mo", "status": "Overstocked"},
            {"sku": "HIJ-309", "name": "Portable SSD 2TB", "stock": 240, "velocity": "310/mo", "status": "Low Stock"}
        ]
    }

@router.get("/procurement")
async def get_procurement_data():
    await asyncio.sleep(0.5)
    return {
        "kpis": [
            {"label": "Active POs", "value": "42", "delta": "$842k committed", "trend": "up"},
            {"label": "Pending Approvals", "value": "7", "delta": "Awaiting Manager", "trend": "warning"},
            {"label": "Supplier Performance", "value": "94%", "delta": "On-time delivery", "trend": "up"},
            {"label": "Cost Savings YTD", "value": "$284K", "delta": "↑ 12% vs target", "trend": "up"},
            {"label": "Avg Lead Time", "value": "6.2 days", "delta": "↓ 0.8 days", "trend": "up"},
            {"label": "Active Suppliers", "value": "38", "delta": "4 under review", "trend": "flat"}
        ],
        "insight": {
            "title": "Purchase Recommendations Available",
            "description": "The Procurement Agent has prepared 4 purchase orders based on projected inventory stockouts. 2 supplier contracts are up for renewal next month."
        },
        "orders": [
            {"po": "PO-10482", "supplier": "ABC Trading Co.", "amount": "$85,000.00", "status": "Pending Approval", "author": "Procurement Agent", "is_ai": True},
            {"po": "PO-10481", "supplier": "Global Logistics", "amount": "$12,400.00", "status": "Approved", "author": "Sarah Jenkins", "is_ai": False},
            {"po": "PO-10480", "supplier": "TechSupply Inc", "amount": "$420,000.00", "status": "Fulfilled", "author": "Procurement Agent", "is_ai": True},
            {"po": "PO-10479", "supplier": "MegaParts Ltd", "amount": "$67,200.00", "status": "Pending Approval", "author": "Procurement Agent", "is_ai": True},
            {"po": "PO-10478", "supplier": "Pacific Components", "amount": "$143,000.00", "status": "In Transit", "author": "James Chen", "is_ai": False},
            {"po": "PO-10477", "supplier": "Nordic Electronics", "amount": "$38,900.00", "status": "Approved", "author": "Procurement Agent", "is_ai": True},
            {"po": "PO-10476", "supplier": "QuickShip Direct", "amount": "$9,800.00", "status": "Fulfilled", "author": "Maria Garcia", "is_ai": False},
            {"po": "PO-10475", "supplier": "Delta Manufacturing", "amount": "$256,000.00", "status": "In Transit", "author": "Procurement Agent", "is_ai": True}
        ]
    }

@router.get("/sales")
async def get_sales_data():
    await asyncio.sleep(0.5)
    return {
        "kpis": [
            {"label": "Pipeline Value", "value": "$8.2M", "delta": "↑ 12% vs last quarter", "trend": "up"},
            {"label": "Win Rate", "value": "34.2%", "delta": "Stable", "trend": "flat"},
            {"label": "Active Opportunities", "value": "124", "delta": "+18 this month", "trend": "up"},
            {"label": "Avg Deal Size", "value": "$66.1K", "delta": "↑ 8% vs Q2", "trend": "up"},
            {"label": "Sales Cycle", "value": "42 days", "delta": "↓ 5 days", "trend": "up"},
            {"label": "Churn Risk", "value": "3 accounts", "delta": "$420K at risk", "trend": "down"},
            {"label": "Monthly Recurring Revenue", "value": "$1.8M", "delta": "↑ 6%", "trend": "up"},
            {"label": "Customer Acquisition Cost", "value": "$2,400", "delta": "↓ 11%", "trend": "up"}
        ],
        "insight": {
            "title": "Opportunity Detection",
            "description": "Sales Agent identified 4 high-probability upsell opportunities based on recent customer usage patterns. 2 accounts at churn risk need immediate attention."
        },
        "opportunities": [
            {"name": "Enterprise License Expansion", "account": "Acme Corp", "value": "$250,000", "stage": "Negotiation", "probability": "80%"},
            {"name": "New Implementation", "account": "Global Tech", "value": "$1.2M", "stage": "Discovery", "probability": "20%"},
            {"name": "Q4 Renewal", "account": "Stark Industries", "value": "$85,000", "stage": "Closed Won", "probability": "100%"},
            {"name": "Platform Migration", "account": "Wayne Enterprises", "value": "$340,000", "stage": "Proposal", "probability": "55%"},
            {"name": "Data Analytics Add-on", "account": "Oscorp Industries", "value": "$120,000", "stage": "Qualification", "probability": "35%"},
            {"name": "Multi-region Deployment", "account": "Cyberdyne Systems", "value": "$890,000", "stage": "Negotiation", "probability": "72%"},
            {"name": "Support Tier Upgrade", "account": "Umbrella Corporation", "value": "$45,000", "stage": "Proposal", "probability": "60%"},
            {"name": "Full Stack License", "account": "Weyland-Yutani", "value": "$2.1M", "stage": "Discovery", "probability": "15%"},
            {"name": "API Integration Package", "account": "LexCorp", "value": "$180,000", "stage": "Closed Lost", "probability": "0%"},
            {"name": "Annual Contract Renewal", "account": "Soylent Corp", "value": "$72,000", "stage": "Closed Won", "probability": "100%"}
        ]
    }

@router.get("/knowledge")
async def get_knowledge_data():
    await asyncio.sleep(0.5)
    return {
        "kpis": [
            {"label": "Total Documents", "value": "1,284", "delta": "12 updated today", "trend": "up"},
            {"label": "Index Status", "value": "98%", "delta": "Healthy", "trend": "active"},
            {"label": "Agent Queries (30d)", "value": "48.2k", "delta": "High utilization", "trend": "up"},
            {"label": "Avg Retrieval Time", "value": "120ms", "delta": "↓ 15ms", "trend": "up"},
            {"label": "Unindexed Files", "value": "24", "delta": "Processing", "trend": "warning"}
        ],
        "documents": [
            {"name": "2026 Procurement Policy.pdf", "type": "Policy", "owner": "Operations Team", "updated": "2 hours ago", "access": "Global"},
            {"name": "Q3 Financial Projections.xlsx", "type": "Data", "owner": "Finance Team", "updated": "Yesterday", "access": "Restricted"},
            {"name": "Supplier Onboarding SOP.docx", "type": "SOP", "owner": "Procurement Team", "updated": "Oct 12, 2026", "access": "Global"},
            {"name": "Employee Handbook v4.2.pdf", "type": "Policy", "owner": "HR Team", "updated": "Sep 28, 2026", "access": "Global"},
            {"name": "Product Catalog 2026-Q4.pdf", "type": "Data", "owner": "Sales Team", "updated": "Oct 15, 2026", "access": "Global"},
            {"name": "IT Security Guidelines.pdf", "type": "Policy", "owner": "IT Security", "updated": "Oct 01, 2026", "access": "Restricted"},
            {"name": "Vendor Risk Assessment.xlsx", "type": "Report", "owner": "Compliance Team", "updated": "Oct 14, 2026", "access": "Restricted"},
            {"name": "Customer Onboarding Playbook.pptx", "type": "SOP", "owner": "Customer Success", "updated": "Oct 10, 2026", "access": "Global"},
            {"name": "Warehouse Operations Manual.pdf", "type": "SOP", "owner": "Logistics Team", "updated": "Sep 20, 2026", "access": "Global"},
            {"name": "API Integration Documentation.md", "type": "Technical", "owner": "Engineering", "updated": "3 hours ago", "access": "Internal"}
        ]
    }

@router.get("/audit")
async def get_audit_data():
    await asyncio.sleep(0.5)
    return {
        "logs": [
            {"time": "10:42 AM", "actor": "Procurement Agent", "is_ai": True, "action": "Created Purchase Order (PO-10482)", "system": "SAP S/4HANA", "risk": "Medium", "status": "Verified"},
            {"time": "10:38 AM", "actor": "Finance Manager", "is_ai": False, "action": "Approved Purchase Order (PO-10482)", "system": "System Platform", "risk": "Low", "status": "Success"},
            {"time": "09:12 AM", "actor": "Finance Agent", "is_ai": True, "action": "Sync Bank Feeds", "system": "Stripe / Plaid", "risk": "Low", "status": "Success"},
            {"time": "09:05 AM", "actor": "Inventory Agent", "is_ai": True, "action": "Updated stock levels for 48 SKUs", "system": "SAP S/4HANA", "risk": "Low", "status": "Success"},
            {"time": "08:45 AM", "actor": "Sales Agent", "is_ai": True, "action": "Synced CRM pipeline data", "system": "Salesforce", "risk": "Low", "status": "Success"},
            {"time": "08:30 AM", "actor": "John Smith", "is_ai": False, "action": "Modified supplier payment terms", "system": "SAP S/4HANA", "risk": "Medium", "status": "Verified"},
            {"time": "08:15 AM", "actor": "Procurement Agent", "is_ai": True, "action": "Sent RFQ to 3 suppliers", "system": "Email / Slack", "risk": "Low", "status": "Success"},
            {"time": "07:55 AM", "actor": "HR Agent", "is_ai": True, "action": "Generated payroll summary", "system": "BambooHR", "risk": "Low", "status": "Success"},
            {"time": "07:30 AM", "actor": "System Scheduler", "is_ai": True, "action": "Executed daily data backup", "system": "AWS S3", "risk": "Low", "status": "Success"},
            {"time": "Yesterday 11:42 PM", "actor": "Unknown IP (91.108.x.x)", "is_ai": False, "action": "Failed Authentication Attempt (3x)", "system": "System API", "risk": "High", "status": "Blocked"},
            {"time": "Yesterday 6:30 PM", "actor": "Finance Agent", "is_ai": True, "action": "Generated monthly expense report", "system": "QuickBooks", "risk": "Low", "status": "Success"},
            {"time": "Yesterday 4:15 PM", "actor": "Maria Garcia", "is_ai": False, "action": "Bulk updated pricing for 120 products", "system": "Shopify", "risk": "Medium", "status": "Verified"},
            {"time": "Yesterday 2:00 PM", "actor": "Inventory Agent", "is_ai": True, "action": "Flagged 5 products with stockout risk", "system": "Internal Analytics", "risk": "Medium", "status": "Action Required"},
            {"time": "Yesterday 10:00 AM", "actor": "Admin", "is_ai": False, "action": "Updated API rate limits", "system": "System Platform", "risk": "Low", "status": "Success"}
        ]
    }

@router.get("/security")
async def get_security_data():
    await asyncio.sleep(0.5)
    return {
        "kpis": [
            {"label": "Active Users", "value": "124", "delta": "Across 4 departments", "trend": "flat"},
            {"label": "Agent Roles", "value": "8", "delta": "Strict isolation", "trend": "active"},
            {"label": "Failed Logins (24h)", "value": "3", "delta": "Review recommended", "trend": "warning"},
            {"label": "API Keys Active", "value": "12", "delta": "2 expiring soon", "trend": "warning"},
            {"label": "Data Encryption", "value": "AES-256", "delta": "Compliant", "trend": "active"},
            {"label": "Last Security Scan", "value": "2h ago", "delta": "No issues found", "trend": "active"}
        ],
        "permissions": [
            {"agent": "Finance Agent", "read": "Allowed", "create": "Allowed", "update": "Allowed", "delete": "Denied", "limit": "$1,000"},
            {"agent": "Inventory Agent", "read": "Allowed", "create": "Allowed", "update": "Allowed", "delete": "Denied", "limit": "$0 (Requires Review)"},
            {"agent": "Procurement Agent", "read": "Allowed", "create": "Allowed", "update": "Denied", "delete": "Denied", "limit": "$5,000"},
            {"agent": "Sales Agent", "read": "Allowed", "create": "Allowed", "update": "Allowed", "delete": "Denied", "limit": "N/A"},
            {"agent": "HR Agent", "read": "Allowed", "create": "Denied", "update": "Denied", "delete": "Denied", "limit": "N/A"},
            {"agent": "Operations Agent", "read": "Allowed", "create": "Allowed", "update": "Allowed", "delete": "Denied", "limit": "$2,500"},
            {"agent": "Analytics Agent", "read": "Allowed", "create": "Denied", "update": "Denied", "delete": "Denied", "limit": "N/A"},
            {"agent": "Compliance Agent", "read": "Allowed", "create": "Allowed", "update": "Denied", "delete": "Denied", "limit": "N/A"}
        ]
    }

@router.get("/activity")
async def get_activity_data():
    await asyncio.sleep(0.5)
    return {
        "activities": [
            {
                "agent": "Inventory Agent",
                "time": "10:42 AM",
                "type": "warning",
                "title": "Detected stockout risk for Product ABC-100",
                "description": "Stockout expected in 4 days. A purchase recommendation has been created for 500 units from Supplier ABC Trading.",
                "action": "Review Recommendation"
            },
            {
                "agent": "Finance Agent",
                "time": "10:38 AM",
                "type": "danger",
                "title": "Detected 7 unusual invoices",
                "description": "Potential duplicate invoice flagged: INV-10291 for $14,500.00. 2 invoices exceed normal thresholds.",
                "action": "Investigate Invoices"
            },
            {
                "agent": "Procurement Agent",
                "time": "10:32 AM",
                "type": "verified",
                "title": "Purchase order created (PO-10482)",
                "description": "Amount: $85,000.00. Approved by Finance Manager via Slack integration.",
                "action": "View PO"
            },
            {
                "agent": "Sales Agent",
                "time": "10:15 AM",
                "type": "warning",
                "title": "Churn risk detected: LexCorp account",
                "description": "Usage dropped 45% in the last 30 days. No support tickets filed. Recommend proactive outreach.",
                "action": "View Account"
            },
            {
                "agent": "HR Agent",
                "time": "09:48 AM",
                "type": "verified",
                "title": "Payroll processed for October",
                "description": "124 employees processed. Total disbursement: $842,000. 3 adjustments flagged for review.",
                "action": "View Payroll"
            },
            {
                "agent": "Operations Agent",
                "time": "09:30 AM",
                "type": "verified",
                "title": "Warehouse capacity optimization complete",
                "description": "Reorganized Zone B storage. Estimated 18% improvement in picking efficiency.",
                "action": "View Report"
            },
            {
                "agent": "Compliance Agent",
                "time": "09:12 AM",
                "type": "danger",
                "title": "GDPR data retention policy violation",
                "description": "42 customer records exceed 36-month retention limit. Automated deletion scheduled pending approval.",
                "action": "Review Records"
            },
            {
                "agent": "Finance Agent",
                "time": "08:45 AM",
                "type": "verified",
                "title": "Bank feed reconciliation complete",
                "description": "148 transactions matched. 3 require manual review. Net discrepancy: $0.42.",
                "action": "View Reconciliation"
            },
            {
                "agent": "Inventory Agent",
                "time": "08:20 AM",
                "type": "warning",
                "title": "Seasonal demand surge predicted",
                "description": "Holiday season analysis predicts 2.3x demand increase for 18 SKUs. Pre-orders recommended.",
                "action": "View Analysis"
            },
            {
                "agent": "Analytics Agent",
                "time": "08:00 AM",
                "type": "verified",
                "title": "Daily business intelligence digest generated",
                "description": "12 KPIs updated. 3 anomalies detected. Executive summary available for download.",
                "action": "View Digest"
            }
        ]
    }

class CommandRequest(BaseModel):
    query: str

@router.post("/command")
async def run_command(req: CommandRequest):
    await asyncio.sleep(1.5)
    
    query_lower = req.query.lower()
    
    # --- INVENTORY AGENT ---
    if any(kw in query_lower for kw in ["inventory", "product", "stock", "sku", "warehouse"]):
        return {
            "agent_name": "Inventory Agent",
            "execution_steps": [
                "Connecting to SAP S/4HANA...",
                "Retrieved real-time inventory data for 8,492 SKUs",
                "Analyzed 90-day sales velocity trends",
                "Checked open purchase orders pipeline",
                "Cross-referenced supplier lead times",
                "Ran predictive stockout model",
                "Identified 5 products at critical risk"
            ],
            "summary": "5 products face imminent stockout within 7 days based on current sales velocity. The most critical is ABC-100 (Wireless Headphones) with only 4.3 days of stock remaining at current run rate. 3 products are significantly overstocked, tying up approximately $124K in capital.",
            "findings": [
                {"label": "Products at Risk", "value": "5 SKUs"},
                {"label": "Most Critical", "value": "ABC-100"},
                {"label": "Days to Stockout", "value": "4.3 days"},
                {"label": "Overstocked Items", "value": "3 SKUs"},
                {"label": "Capital Tied Up", "value": "$124,000"},
                {"label": "Dead Stock", "value": "248 SKUs"}
            ],
            "evidence": "Sales velocity for ABC-100 spiked 45% over the last weekend due to a viral social media campaign. Current stock of 120 units at 28 units/day consumption will deplete in approximately 4.3 days. Supplier ABC Trading has a 4-day lead time.",
            "sources": ["SAP S/4HANA (Inventory)", "Shopify (Sales)", "Internal Analytics Engine"],
            "recommendation": "Immediately place an expedited purchase order for ABC-100 (500 units) from ABC Trading Co. Also recommend pre-ordering JKL-401 and STU-704 which will stockout within 6-7 days.",
            "actions": [
                {
                    "title": "Emergency PO: ABC-100 (500 units)",
                    "details": [
                        "Product: ABC-100 — Wireless Noise-Canceling Headphones",
                        "Quantity: 500 units @ ₹1,200/unit",
                        "Supplier: ABC Trading Co. (Lead time: 4 days)",
                        "Total Cost: ₹600,000",
                        "Risk Level: Medium — expedited shipping recommended"
                    ],
                    "action_type": "approval"
                },
                {
                    "title": "Preventive PO: JKL-401 (300 units)",
                    "details": [
                        "Product: JKL-401 — Mechanical Keyboard (Cherry MX)",
                        "Quantity: 300 units @ ₹3,400/unit",
                        "Supplier: TechSupply Inc (Lead time: 2 days)",
                        "Total Cost: ₹1,020,000"
                    ],
                    "action_type": "approval"
                }
            ],
            "table": {
                "columns": ["SKU", "Product", "Stock", "Daily Velocity", "Days Left", "Status"],
                "rows": [
                    ["ABC-100", "Wireless Headphones", "120", "28/day", "4.3", "🔴 Critical"],
                    ["JKL-401", "Mechanical Keyboard", "85", "21/day", "4.0", "🔴 Critical"],
                    ["STU-704", "Laptop Stand", "42", "13/day", "3.2", "🔴 Critical"],
                    ["BCD-107", "Webcam 1080p HD", "55", "10/day", "5.5", "🟠 Warning"],
                    ["VWX-805", "Bluetooth Earbuds", "670", "18/day", "37.2", "🟡 Low Stock"],
                    ["HIJ-309", "Portable SSD 2TB", "240", "10/day", "24.0", "🟡 Low Stock"],
                    ["DEF-200", "Ergonomic Office Chair", "450", "4/day", "112.5", "🟢 Healthy"],
                    ["MNO-502", "4K Ultra Monitor", "310", "6/day", "51.7", "🟢 Healthy"],
                    ["GHI-300", "USB-C Hub Adapter", "4,200", "10/day", "420.0", "🔵 Overstocked"],
                    ["PQR-603", "Wireless Charging Pad", "1,850", "7/day", "264.3", "🔵 Overstocked"]
                ]
            }
        }

    # --- REVENUE / FINANCE / INVOICE ---
    if any(kw in query_lower for kw in ["revenue", "finance", "invoice", "cash", "profit", "expense", "overdue", "payment"]):
        if "overdue" in query_lower:
            return {
                "agent_name": "Finance Agent",
                "execution_steps": [
                    "Connecting to QuickBooks & SAP...",
                    "Queried accounts receivable ledger",
                    "Filtered invoices past due date",
                    "Calculated aging buckets (30/60/90+ days)",
                    "Cross-referenced payment history",
                    "Assessed collection risk per account",
                    "Generated prioritized collection plan"
                ],
                "summary": "There are 8 overdue invoices totaling $487,200. 2 invoices are critically overdue (90+ days) representing $340,000 in outstanding receivables. Stark Industries alone accounts for 29% of total overdue value.",
                "findings": [
                    {"label": "Total Overdue", "value": "$487,200"},
                    {"label": "Overdue Invoices", "value": "8"},
                    {"label": "Critical (90+ days)", "value": "2 invoices"},
                    {"label": "Highest Risk", "value": "Stark Industries"},
                    {"label": "Avg Days Overdue", "value": "34 days"},
                    {"label": "Collection Rate", "value": "72%"}
                ],
                "evidence": "Stark Industries (INV-10293, $142,000) has been overdue for 42 days with no response to 3 follow-up emails. LexCorp (INV-10296, $198,000) is 51 days overdue. Both accounts have historically paid within 45 days.",
                "sources": ["QuickBooks (AR Ledger)", "SAP S/4HANA (Customer Master)", "Email Tracker", "CRM History"],
                "recommendation": "Escalate collection for Stark Industries and LexCorp immediately. Consider offering 2% early payment discount for invoices in the 30-day bucket to accelerate collections.",
                "actions": [
                    {
                        "title": "Escalate: Stark Industries Collection",
                        "details": [
                            "Invoice: INV-10293 — $142,000.00",
                            "Days Overdue: 42 days",
                            "Action: Send formal demand letter + schedule call",
                            "Escalation: Finance Director notification"
                        ],
                        "action_type": "approval"
                    },
                    {
                        "title": "Escalate: LexCorp Collection",
                        "details": [
                            "Invoice: INV-10296 — $198,000.00",
                            "Days Overdue: 51 days",
                            "Action: Initiate legal review process",
                            "Risk: Potential write-off if unresolved in 30 days"
                        ],
                        "action_type": "approval"
                    }
                ],
                "table": {
                    "columns": ["Invoice", "Customer", "Amount", "Due Date", "Days Overdue", "Status", "Risk"],
                    "rows": [
                        ["INV-10296", "LexCorp", "$198,000", "Aug 22", "51 days", "No Response", "🔴 Critical"],
                        ["INV-10293", "Stark Industries", "$142,000", "Sep 01", "42 days", "Partial Contact", "🔴 Critical"],
                        ["INV-10292", "Global Tech", "$8,200", "Oct 14", "8 days", "Payment Promised", "🟡 Medium"],
                        ["INV-10295", "Oscorp Industries", "$23,400", "Oct 16", "6 days", "Under Review", "🟡 Medium"],
                        ["INV-10298", "Umbrella Corp", "$31,200", "Oct 18", "4 days", "Contacted", "🟢 Low"],
                        ["INV-10301", "Initech", "$18,400", "Oct 12", "10 days", "Dispute Filed", "🟠 High"],
                        ["INV-10302", "Massive Dynamic", "$42,000", "Oct 08", "14 days", "Contacted", "🟡 Medium"],
                        ["INV-10303", "Hooli", "$24,000", "Oct 10", "12 days", "Payment Scheduled", "🟢 Low"]
                    ]
                }
            }
        
        return {
            "agent_name": "Finance Agent",
            "execution_steps": [
                "Connecting to QuickBooks & Stripe...",
                "Retrieved P&L statement data",
                "Analyzed revenue trends (12-month rolling)",
                "Compared actuals vs forecast",
                "Identified variance drivers",
                "Cross-referenced with market data",
                "Generated executive insights"
            ],
            "summary": "Revenue declined 8% ($247K) month-over-month, primarily driven by a 23% drop in the Enterprise segment. However, SMB revenue grew 12%. Operating expenses increased 4% due to hiring. Net margin compressed from 31.2% to 29.7%.",
            "findings": [
                {"label": "Monthly Revenue", "value": "$2,845,000"},
                {"label": "MoM Change", "value": "↓ 8% ($247K)"},
                {"label": "Enterprise Revenue", "value": "↓ 23%"},
                {"label": "SMB Revenue", "value": "↑ 12%"},
                {"label": "Net Margin", "value": "29.7%"},
                {"label": "Cash Runway", "value": "14.2 months"}
            ],
            "evidence": "Enterprise revenue dropped due to 2 large contract renewals being delayed (Stark Industries $142K, LexCorp $198K). Both are in active negotiation. SMB growth is attributed to the new self-serve onboarding launched in September (+84 new accounts).",
            "sources": ["QuickBooks (P&L)", "Stripe (Payments)", "Salesforce (Pipeline)", "Internal Forecasting Model"],
            "recommendation": "Prioritize closing the 2 delayed enterprise renewals which represent $340K in potential recovery. Continue investing in SMB self-serve channel which shows strong unit economics (LTV/CAC ratio of 4.2x).",
            "actions": [
                {
                    "title": "Revenue Recovery Plan",
                    "details": [
                        "Priority 1: Close Stark Industries renewal ($142K)",
                        "Priority 2: Close LexCorp renewal ($198K)",
                        "Priority 3: Accelerate 4 pipeline deals in negotiation ($680K total)",
                        "Timeline: Execute within 30 days"
                    ],
                    "action_type": "approval"
                }
            ],
            "table": {
                "columns": ["Segment", "This Month", "Last Month", "Change", "YTD", "vs Forecast"],
                "rows": [
                    ["Enterprise", "$1,420,000", "$1,844,000", "↓ 23%", "$16.8M", "↓ 12%"],
                    ["Mid-Market", "$780,000", "$756,000", "↑ 3%", "$8.9M", "On Track"],
                    ["SMB", "$485,000", "$433,000", "↑ 12%", "$4.2M", "↑ 8%"],
                    ["Services", "$160,000", "$159,000", "↑ 0.6%", "$1.8M", "On Track"],
                    ["Total", "$2,845,000", "$3,092,000", "↓ 8%", "$31.7M", "↓ 4%"]
                ]
            }
        }

    # --- SUPPLIER / PROCUREMENT ---
    if any(kw in query_lower for kw in ["supplier", "purchase", "procurement", "vendor", "compare"]):
        return {
            "agent_name": "Procurement Agent",
            "execution_steps": [
                "Connecting to Supplier Database...",
                "Queried approved vendor list",
                "Retrieved pricing & lead time data",
                "Analyzed quality scores (12-month)",
                "Checked compliance certifications",
                "Evaluated total cost of ownership",
                "Ranked suppliers by composite score"
            ],
            "summary": "Comprehensive supplier analysis complete. ABC Trading offers the best balance of price and reliability. TechSupply Inc has the fastest delivery but at 17% premium. Global Logistics has the lowest price but poor quality record and high risk score.",
            "findings": [
                {"label": "Suppliers Evaluated", "value": "6"},
                {"label": "Best Overall", "value": "ABC Trading"},
                {"label": "Fastest Delivery", "value": "TechSupply Inc"},
                {"label": "Lowest Price", "value": "Global Logistics"},
                {"label": "Avg Lead Time", "value": "5.8 days"},
                {"label": "Price Range", "value": "₹1,050 — ₹1,400"}
            ],
            "evidence": "ABC Trading has maintained a 98% quality score across 24 orders in the past 12 months with an average lead time of 4 days. TechSupply is faster (2 days) but 17% more expensive. Global Logistics had 3 quality incidents in the last quarter.",
            "sources": ["Supplier Portal", "SAP S/4HANA (Purchase History)", "Quality Management System", "Compliance Database"],
            "recommendation": "Select ABC Trading Co. as primary supplier for routine orders. Use TechSupply Inc for emergency/expedited orders where speed is critical. Avoid Global Logistics until quality issues are resolved.",
            "actions": [],
            "table": {
                "columns": ["Supplier", "Unit Price", "Lead Time", "Quality Score", "On-Time %", "Risk", "MOQ", "Recommendation"],
                "rows": [
                    ["ABC Trading Co.", "₹1,200", "4 days", "98%", "96%", "Low", "100", "✅ Primary Supplier"],
                    ["TechSupply Inc", "₹1,400", "2 days", "99%", "98%", "Low", "50", "⚡ Expedited Orders"],
                    ["Nordic Electronics", "₹1,180", "6 days", "95%", "91%", "Medium", "200", "🔄 Alternative"],
                    ["Pacific Components", "₹1,100", "8 days", "93%", "88%", "Medium", "500", "📋 Bulk Orders"],
                    ["Global Logistics", "₹1,050", "12 days", "82%", "74%", "High", "100", "⚠️ Not Recommended"],
                    ["Delta Manufacturing", "₹1,350", "3 days", "97%", "95%", "Low", "75", "✅ Secondary Supplier"]
                ]
            }
        }

    # --- SALES ---
    if any(kw in query_lower for kw in ["sales", "pipeline", "deal", "opportunity", "churn", "customer", "account", "renewal"]):
        return {
            "agent_name": "Sales Agent",
            "execution_steps": [
                "Connecting to Salesforce CRM...",
                "Retrieved pipeline data for Q4",
                "Analyzed win/loss patterns (6 months)",
                "Identified high-probability opportunities",
                "Detected churn risk signals",
                "Generated upsell recommendations",
                "Compiled executive sales brief"
            ],
            "summary": "Q4 pipeline stands at $8.2M across 124 active opportunities. Win rate is 34.2% (stable). 4 high-value deals ($2.68M combined) are in advanced stages. 3 accounts showing churn risk signals — LexCorp, Umbrella Corp, and Initech — representing $420K in ARR at risk.",
            "findings": [
                {"label": "Pipeline Value", "value": "$8.2M"},
                {"label": "Win Rate", "value": "34.2%"},
                {"label": "Weighted Pipeline", "value": "$2.8M"},
                {"label": "Avg Deal Size", "value": "$66.1K"},
                {"label": "Deals Closing This Month", "value": "18"},
                {"label": "Churn Risk", "value": "3 accounts ($420K)"}
            ],
            "evidence": "Acme Corp enterprise expansion ($250K) is at 80% probability — champion confirmed budget approval. Cyberdyne multi-region deal ($890K) moved to negotiation after successful POC. LexCorp usage dropped 45% — no support engagement in 60 days, strong churn indicator.",
            "sources": ["Salesforce (CRM)", "Stripe (Usage Data)", "Intercom (Support)", "Internal Analytics"],
            "recommendation": "Focus this week on: (1) Close Acme Corp expansion — schedule contract signing. (2) Advance Cyberdyne negotiation — prepare custom pricing. (3) Initiate churn intervention for LexCorp — executive outreach call.",
            "actions": [
                {
                    "title": "Churn Intervention: LexCorp",
                    "details": [
                        "Account: LexCorp — $180K ARR",
                        "Signal: Usage ↓ 45%, No support tickets in 60 days",
                        "Action: Schedule executive QBR + offer extended pilot of new features",
                        "Owner: VP Sales (escalated)"
                    ],
                    "action_type": "approval"
                },
                {
                    "title": "Close Acceleration: Acme Corp",
                    "details": [
                        "Deal: Enterprise License Expansion — $250,000",
                        "Stage: Negotiation (80% probability)",
                        "Action: Send final contract + schedule signing ceremony",
                        "Expected Close: This week"
                    ],
                    "action_type": "approval"
                }
            ],
            "table": {
                "columns": ["Account", "Deal", "Value", "Stage", "Probability", "Close Date", "Signal"],
                "rows": [
                    ["Acme Corp", "Enterprise Expansion", "$250K", "Negotiation", "80%", "Oct 25", "🟢 Strong"],
                    ["Cyberdyne", "Multi-region Deploy", "$890K", "Negotiation", "72%", "Nov 15", "🟢 Strong"],
                    ["Wayne Enterprises", "Platform Migration", "$340K", "Proposal", "55%", "Nov 30", "🟡 Moderate"],
                    ["Global Tech", "New Implementation", "$1.2M", "Discovery", "20%", "Q1 2027", "🟡 Early"],
                    ["Weyland-Yutani", "Full Stack License", "$2.1M", "Discovery", "15%", "Q1 2027", "🟡 Early"],
                    ["Oscorp Industries", "Analytics Add-on", "$120K", "Qualification", "35%", "Dec 15", "🟡 Moderate"],
                    ["Umbrella Corp", "Support Upgrade", "$45K", "Proposal", "60%", "Nov 10", "🟠 Churn Risk"],
                    ["LexCorp", "API Integration", "$180K", "At Risk", "10%", "—", "🔴 Churn Risk"]
                ]
            }
        }

    # --- HR / PEOPLE / PAYROLL ---
    if any(kw in query_lower for kw in ["hr", "employee", "payroll", "hire", "people", "headcount", "attrition"]):
        return {
            "agent_name": "HR Agent",
            "execution_steps": [
                "Connecting to BambooHR...",
                "Retrieved workforce data",
                "Analyzed headcount trends",
                "Processed attrition metrics",
                "Reviewed open requisitions",
                "Generated workforce insights"
            ],
            "summary": "Current headcount is 124 across 4 departments. Engineering is the largest team (52). October attrition rate is 2.4% (within healthy range). 8 open requisitions in pipeline. Average time-to-hire is 34 days.",
            "findings": [
                {"label": "Total Headcount", "value": "124"},
                {"label": "New Hires (Q4)", "value": "12"},
                {"label": "Attrition Rate", "value": "2.4%"},
                {"label": "Open Positions", "value": "8"},
                {"label": "Avg Tenure", "value": "2.8 years"},
                {"label": "Payroll (Monthly)", "value": "$842,000"}
            ],
            "evidence": "Engineering team grew 15% this quarter (7 new hires). Sales team has the highest attrition at 4.2%, primarily in SDR roles. 2 senior engineering candidates are in final interview stage.",
            "sources": ["BambooHR (HRIS)", "Greenhouse (ATS)", "Payroll System", "Internal Analytics"],
            "recommendation": "Focus recruiting efforts on filling the 3 open Sales Development positions to support Q1 pipeline growth. Consider retention bonuses for the 2 senior engineers flagged as flight risks.",
            "actions": [
                {
                    "title": "Retention Plan: Senior Engineers",
                    "details": [
                        "2 senior engineers flagged as flight risk",
                        "Proposed: 15% equity refresh + title promotion",
                        "Combined cost: $48,000/year",
                        "Replacement cost if lost: ~$280,000"
                    ],
                    "action_type": "approval"
                }
            ],
            "table": {
                "columns": ["Department", "Headcount", "New Hires (Q4)", "Open Roles", "Attrition", "Avg Tenure"],
                "rows": [
                    ["Engineering", "52", "7", "2", "1.9%", "3.1 years"],
                    ["Sales", "34", "3", "3", "4.2%", "1.8 years"],
                    ["Operations", "22", "1", "2", "2.3%", "3.4 years"],
                    ["G&A", "16", "1", "1", "1.2%", "4.1 years"]
                ]
            }
        }

    # --- OPERATIONS / LOGISTICS ---
    if any(kw in query_lower for kw in ["operation", "logistics", "warehouse", "shipping", "delivery", "fulfillment"]):
        return {
            "agent_name": "Operations Agent",
            "execution_steps": [
                "Connecting to WMS...",
                "Retrieved operational metrics",
                "Analyzed fulfillment rates",
                "Checked shipping performance",
                "Evaluated warehouse utilization",
                "Generated operational summary"
            ],
            "summary": "Operations are running at 94.2% efficiency. Average order fulfillment time is 1.8 days. Warehouse utilization is at 78% — approaching optimal threshold. 3 shipping delays reported this week due to carrier issues.",
            "findings": [
                {"label": "Fulfillment Rate", "value": "94.2%"},
                {"label": "Avg Fulfillment Time", "value": "1.8 days"},
                {"label": "Warehouse Utilization", "value": "78%"},
                {"label": "Orders Today", "value": "342"},
                {"label": "Shipping Delays", "value": "3 this week"},
                {"label": "Returns Rate", "value": "2.1%"}
            ],
            "evidence": "Zone B reorganization improved picking efficiency by 18%. Carrier XYZ Express has caused 3 delivery delays this week — SLA breach on 2 priority orders. Consider switching to FedEx for priority shipments.",
            "sources": ["WMS (Warehouse)", "ShipStation", "Carrier APIs", "Internal Metrics"],
            "recommendation": "Switch priority shipments from XYZ Express to FedEx for the remainder of Q4. Begin planning warehouse expansion for Zone C to accommodate projected holiday demand increase.",
            "actions": [
                {
                    "title": "Switch Priority Carrier",
                    "details": [
                        "Current: XYZ Express (3 SLA breaches this week)",
                        "Proposed: FedEx Priority (99.2% on-time record)",
                        "Cost Impact: +$1,200/month",
                        "Benefit: Eliminate delivery delays for priority orders"
                    ],
                    "action_type": "approval"
                }
            ],
            "table": {
                "columns": ["Metric", "Today", "This Week", "This Month", "Trend"],
                "rows": [
                    ["Orders Processed", "342", "2,180", "8,420", "↑ 6%"],
                    ["On-Time Delivery", "96.8%", "94.2%", "95.1%", "↓ 1.2%"],
                    ["Pick Accuracy", "99.4%", "99.2%", "99.3%", "Stable"],
                    ["Returns Processed", "7", "48", "176", "↓ 8%"],
                    ["Avg Ship Time", "1.2 days", "1.8 days", "1.6 days", "↑ 0.2 days"]
                ]
            }
        }

    # --- ATTENTION / TODAY / SUMMARY ---
    if any(kw in query_lower for kw in ["attention", "today", "summary", "brief", "morning", "status", "what"]):
        return {
            "agent_name": "Agent Orchestrator",
            "execution_steps": [
                "Polling all connected agents...",
                "Finance Agent: 3 alerts",
                "Inventory Agent: 5 critical items",
                "Sales Agent: 2 churn risks",
                "Procurement Agent: 2 pending approvals",
                "HR Agent: payroll complete",
                "Operations Agent: 3 shipping delays",
                "Compliance Agent: 1 policy violation",
                "Consolidated executive briefing generated"
            ],
            "summary": "Good morning! Here is your executive briefing. There are 7 items requiring your immediate attention across Finance, Inventory, Sales, and Compliance. Revenue is trending 8% below forecast. 5 products face stockout risk. 2 enterprise accounts show churn signals.",
            "findings": [
                {"label": "Critical Alerts", "value": "7"},
                {"label": "Revenue vs Forecast", "value": "↓ 8%"},
                {"label": "Stockout Risks", "value": "5 products"},
                {"label": "Pending Approvals", "value": "4"},
                {"label": "Churn Risk", "value": "2 accounts"},
                {"label": "Compliance Issues", "value": "1"}
            ],
            "evidence": "Finance: Revenue down 8% — 2 large renewals delayed ($340K). Inventory: 5 products will stockout within 7 days. Sales: LexCorp usage dropped 45%. Compliance: 42 customer records exceed GDPR retention limit.",
            "sources": ["All Connected Systems", "Finance Agent", "Inventory Agent", "Sales Agent", "Compliance Agent"],
            "recommendation": "Prioritize: (1) Approve emergency PO for ABC-100. (2) Escalate Stark Industries collection. (3) Schedule LexCorp churn intervention call. (4) Review GDPR compliance records.",
            "actions": [
                {
                    "title": "Morning Action Plan",
                    "details": [
                        "🔴 Approve emergency PO for ABC-100 (stockout in 4 days)",
                        "🔴 Escalate Stark Industries collection ($142K overdue 42 days)",
                        "🟠 Schedule LexCorp executive call (churn risk: $180K ARR)",
                        "🟠 Review GDPR data retention violations (42 records)",
                        "🟡 Approve pending POs: PO-10482, PO-10479",
                        "🟡 Review payroll adjustments (3 flagged)",
                        "🟢 Review warehouse optimization report"
                    ],
                    "action_type": "approval"
                }
            ],
            "table": {
                "columns": ["Priority", "Area", "Issue", "Impact", "Action Required"],
                "rows": [
                    ["🔴 P0", "Inventory", "ABC-100 stockout in 4 days", "$84K revenue at risk", "Approve emergency PO"],
                    ["🔴 P0", "Finance", "Stark Industries $142K overdue", "Cash flow impact", "Escalate collection"],
                    ["🟠 P1", "Sales", "LexCorp churn risk", "$180K ARR at risk", "Executive outreach"],
                    ["🟠 P1", "Compliance", "GDPR retention violation", "Regulatory risk", "Review & approve deletion"],
                    ["🟡 P2", "Procurement", "2 POs pending approval", "$152K committed", "Review & approve"],
                    ["🟡 P2", "HR", "3 payroll adjustments", "Employee satisfaction", "Review & approve"],
                    ["🟢 P3", "Operations", "3 shipping delays", "Customer experience", "Monitor carrier switch"]
                ]
            }
        }

    # --- REPORT / ANALYTICS ---
    if any(kw in query_lower for kw in ["report", "analytics", "dashboard", "metric", "kpi", "performance"]):
        return {
            "agent_name": "Analytics Agent",
            "execution_steps": [
                "Aggregating data from all systems...",
                "Processed 48 KPIs across 6 departments",
                "Computed month-over-month deltas",
                "Identified 3 anomalies",
                "Generated trend analysis",
                "Compiled business performance report"
            ],
            "summary": "Business performance report for October 2026. Overall health score: 7.2/10. Revenue is the primary concern at 8% below forecast. Operational efficiency and customer satisfaction remain strong. 3 KPIs require attention.",
            "findings": [
                {"label": "Health Score", "value": "7.2 / 10"},
                {"label": "Revenue", "value": "↓ 8%"},
                {"label": "Efficiency", "value": "94.2%"},
                {"label": "Customer NPS", "value": "72"},
                {"label": "Employee Satisfaction", "value": "8.1/10"},
                {"label": "System Uptime", "value": "99.97%"}
            ],
            "evidence": "Revenue decline is concentrated in Enterprise segment. All other segments are on track or above forecast. Operational metrics are strong — warehouse efficiency improved 18% after Zone B reorganization.",
            "sources": ["All Connected Systems", "Internal Analytics Engine", "Business Intelligence Platform"],
            "recommendation": "Focus on revenue recovery in Enterprise segment. All other business areas are performing well. Consider quarterly business review with executive team to realign targets.",
            "actions": [],
            "table": {
                "columns": ["Department", "Health", "Key Metric", "Status", "Trend", "Action"],
                "rows": [
                    ["Finance", "6.8/10", "Revenue: $2.85M", "↓ Below Target", "Declining", "Revenue recovery plan"],
                    ["Sales", "7.5/10", "Pipeline: $8.2M", "On Track", "Growing", "Close pending deals"],
                    ["Inventory", "6.2/10", "5 stockout risks", "⚠ Needs Action", "Worsening", "Emergency POs"],
                    ["Procurement", "8.1/10", "94% on-time delivery", "Healthy", "Stable", "Continue monitoring"],
                    ["Operations", "8.5/10", "94.2% efficiency", "Healthy", "Improving", "Expand Zone C"],
                    ["HR", "7.8/10", "2.4% attrition", "Healthy", "Stable", "Fill open roles"]
                ]
            }
        }

    # --- STRATEGY / PLANNING ---
    if any(kw in query_lower for kw in ["strategy", "plan", "forecast", "budget", "goal", "target", "q4", "quarter"]):
        return {
            "agent_name": "Agent Orchestrator",
            "execution_steps": [
                "Analyzing Q4 targets vs actuals...",
                "Retrieved strategic plan data",
                "Evaluated progress across 12 OKRs",
                "Identified gaps and risks",
                "Generated strategic recommendations"
            ],
            "summary": "Q4 strategic review: 7 of 12 OKRs are on track. Revenue target of $9.2M requires acceleration — currently pacing at $8.5M. Key risks: Enterprise renewal delays and inventory supply chain. Key opportunity: SMB self-serve channel exceeding expectations (+18% above target).",
            "findings": [
                {"label": "OKRs On Track", "value": "7 of 12"},
                {"label": "Revenue Pacing", "value": "$8.5M / $9.2M"},
                {"label": "Gap to Target", "value": "$700K"},
                {"label": "Top Risk", "value": "Enterprise Renewals"},
                {"label": "Top Opportunity", "value": "SMB Channel"},
                {"label": "Budget Utilization", "value": "82%"}
            ],
            "evidence": "2 enterprise renewals worth $340K are delayed but recoverable. SMB self-serve launched in September is growing 18% above projections. New product features in pipeline should unlock $420K in upsell potential.",
            "sources": ["Strategic Plan", "OKR Tracker", "Financial Model", "CRM Pipeline"],
            "recommendation": "To close the $700K revenue gap: (1) Accelerate enterprise renewal closures ($340K). (2) Launch targeted upsell campaign for existing SMB accounts ($200K potential). (3) Fast-track Q4 product release to unlock feature-gated upgrades ($160K).",
            "actions": [
                {
                    "title": "Q4 Revenue Acceleration Plan",
                    "details": [
                        "Close 2 delayed enterprise renewals: $340K",
                        "SMB upsell campaign (200 accounts): $200K target",
                        "Product-led growth from Q4 release: $160K target",
                        "Total recovery potential: $700K",
                        "Timeline: Execute by Dec 15, 2026"
                    ],
                    "action_type": "approval"
                }
            ],
            "table": {
                "columns": ["OKR", "Target", "Current", "Status", "Owner"],
                "rows": [
                    ["Q4 Revenue", "$9.2M", "$8.5M (pacing)", "🟠 At Risk", "VP Sales"],
                    ["New Customers", "40", "28", "🟡 Behind", "Marketing"],
                    ["NPS Score", "> 70", "72", "🟢 On Track", "Customer Success"],
                    ["System Uptime", "99.9%", "99.97%", "🟢 Exceeding", "Engineering"],
                    ["Employee Retention", "> 95%", "97.6%", "🟢 On Track", "HR"],
                    ["Warehouse Efficiency", "> 90%", "94.2%", "🟢 Exceeding", "Operations"],
                    ["Cost Savings", "$250K", "$284K", "🟢 Exceeding", "Procurement"],
                    ["SMB Revenue", "$1.5M", "$1.77M", "🟢 Exceeding", "Growth Team"]
                ]
            }
        }

    # --- DEFAULT FALLBACK ---
    return {
        "agent_name": "Agent Orchestrator",
        "execution_steps": [
            "Analyzing request intent...",
            "Routing to relevant agents...",
            "Aggregating cross-functional data...",
            "Generating analysis...",
            "Compiling recommendations"
        ],
        "summary": f"I've analyzed your request: '{req.query}'. Based on cross-functional data from all connected systems, here is a comprehensive analysis. The AI Orchestrator routed this to the most relevant agents for processing.",
        "findings": [
            {"label": "Systems Queried", "value": "6"},
            {"label": "Data Points Analyzed", "value": "2,840"},
            {"label": "Anomalies Detected", "value": "3"},
            {"label": "Confidence", "value": "High (92%)"}
        ],
        "evidence": "Analysis based on real-time data from SAP S/4HANA, QuickBooks, Salesforce, Shopify, BambooHR, and internal analytics. All data sources synced within the last 15 minutes.",
        "sources": ["SAP S/4HANA", "QuickBooks", "Salesforce", "Shopify", "BambooHR", "Internal Analytics"],
        "recommendation": "Based on the analysis, I recommend reviewing the detailed findings above and taking action on any flagged items. You can ask follow-up questions to dive deeper into any specific area.",
        "actions": [
            {
                "title": "Deep Dive Analysis",
                "details": [
                    "Run detailed analysis on flagged anomalies",
                    "Generate downloadable report (PDF)",
                    "Schedule automated monitoring"
                ],
                "action_type": "approval"
            }
        ],
        "table": None
    }

@router.get("/home")
async def get_home_data():
    await asyncio.sleep(0.5)
    return {
        "insights": [
            {"title": "Revenue Anomaly", "desc": "Revenue dropped 8% vs forecast. Enterprise segment is the primary driver."},
            {"title": "Inventory Risk", "desc": "5 products at critical stockout risk within 7 days."},
            {"title": "Churn Alert", "desc": "LexCorp usage down 45%. Immediate outreach recommended."},
            {"title": "Cost Savings", "desc": "Procurement Agent saved $284K YTD — 12% above target."},
            {"title": "Compliance", "desc": "GDPR: 42 records exceed retention limit. Action required."}
        ],
        "approvals": [
            {"title": "Emergency PO: ABC-100", "amount": "₹600,000", "risk": "High"},
            {"title": "PO-10482: ABC Trading", "amount": "₹850,000", "risk": "Medium"},
            {"title": "PO-10479: MegaParts", "amount": "₹672,000", "risk": "Medium"},
            {"title": "Carrier Switch: FedEx", "amount": "+₹14,400/yr", "risk": "Low"}
        ],
        "activity": [
            {"agent": "Inventory Agent", "action": "Flagged 5 stockout risks", "time": "2m ago"},
            {"agent": "Finance Agent", "action": "Synced bank feeds — 148 transactions", "time": "15m ago"},
            {"agent": "Sales Agent", "action": "Detected churn risk: LexCorp", "time": "32m ago"},
            {"agent": "Procurement Agent", "action": "Created PO-10482 ($85K)", "time": "48m ago"},
            {"agent": "HR Agent", "action": "Processed October payroll", "time": "1h ago"},
            {"agent": "Operations Agent", "action": "Completed Zone B optimization", "time": "1.5h ago"},
            {"agent": "Compliance Agent", "action": "GDPR retention scan complete", "time": "2h ago"},
            {"agent": "Analytics Agent", "action": "Generated daily BI digest", "time": "3h ago"}
        ]
    }

"use client";

export default function OperationsPage() {
  return (
    <main className="main">
      <div className="topbar">
        <div className="breadcrumb">Operations</div>
      </div>
      <div className="content">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <div>
            <h1 className="display" style={{ fontSize: '24px' }}>Operations Control</h1>
            <p className="text-dim text-sm" style={{ marginTop: '4px' }}>Manage logistics and operational workflows.</p>
          </div>
          <button className="btn btn-primary" style={{ background: 'var(--ai-core)' }}>Ask Operations Agent</button>
        </div>

        <div className="kpi-grid" style={{ marginBottom: '32px' }}>
          <div className="kpi-card">
            <div className="kpi-label">Active Shipments</div>
            <div className="kpi-val">1,204</div>
            <div className="kpi-delta flat">Stable</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Delayed Shipments</div>
            <div className="kpi-val">14</div>
            <div className="kpi-delta warning">Attention Needed</div>
          </div>
        </div>
      </div>
    </main>
  );
}

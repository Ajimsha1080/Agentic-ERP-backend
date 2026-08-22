export default function AnalyticsPage() {
  return (
    <main className="main">
      <div className="topbar">
        <div>
          <span className="crumb">Analytics</span>
          <span className="crumb-sub">Platform metrics and AI ROI</span>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: '12px' }}>
          <button className="panel-action" style={{ background: 'var(--surface-2)' }}>Last 30 Days ▾</button>
          <button className="panel-action">Export Report</button>
        </div>
      </div>

      <div className="content" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div className="kpi-row" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px' }}>
          {[
            { label: 'Total Tokens Used', value: '42.8M', delta: '+12% vs last month', color: 'var(--accent)' },
            { label: 'Hours Saved', value: '1,240', delta: '+8% vs last month', color: 'var(--verified)' },
            { label: 'Actions Executed', value: '84,902', delta: '+22% vs last month', color: 'var(--executing)' },
            { label: 'Human Interventions', value: '42', delta: '-15% vs last month', color: 'var(--pending)' }
          ].map(kpi => (
            <div key={kpi.label} className="panel" style={{ padding: '24px' }}>
              <div style={{ fontSize: '12px', color: 'var(--text-dim)', marginBottom: '8px' }}>{kpi.label}</div>
              <div style={{ fontSize: '28px', fontFamily: "'Space Grotesk', sans-serif", fontWeight: 500, marginBottom: '8px' }}>{kpi.value}</div>
              <div style={{ fontSize: '11px', color: kpi.color }}>{kpi.delta}</div>
            </div>
          ))}
        </div>

        <div className="panel" style={{ flex: 1, minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
          <div className="panel-head">
            <h2 className="panel-title">Token Usage over time</h2>
          </div>
          <div style={{ flex: 1, padding: '24px', display: 'flex', alignItems: 'flex-end', position: 'relative' }}>
            {/* Mock Chart Area */}
            <svg viewBox="0 0 1000 300" width="100%" height="100%" preserveAspectRatio="none" style={{ overflow: 'visible' }}>
              <defs>
                <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.4" />
                  <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
                </linearGradient>
              </defs>
              {/* Grid Lines */}
              {[0, 75, 150, 225, 300].map(y => (
                <line key={y} x1="0" y1={y} x2="1000" y2={y} stroke="var(--border-soft)" strokeWidth="1" />
              ))}
              <path d="M0,250 L100,220 L200,240 L300,150 L400,180 L500,90 L600,120 L700,50 L800,80 L900,20 L1000,40 L1000,300 L0,300 Z" fill="url(#chartGradient)" />
              <path d="M0,250 L100,220 L200,240 L300,150 L400,180 L500,90 L600,120 L700,50 L800,80 L900,20 L1000,40" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
        </div>
      </div>
    </main>
  );
}

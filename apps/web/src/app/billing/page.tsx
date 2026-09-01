export default function BillingPage() {
  return (
    <main className="main">
      <div className="topbar">
        <div>
          <span className="crumb">Billing</span>
          <span className="crumb-sub">Manage subscription and API usage</span>
        </div>
      </div>

      <div className="content" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="panel" style={{ padding: '32px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
              <div>
                <h2 style={{ fontSize: '18px', fontWeight: 600, margin: 0 }}>Enterprise Plan</h2>
                <div style={{ fontSize: '13px', color: 'var(--text-dim)', marginTop: '4px' }}>Active Enterprise Tier</div>
              </div>
              <button className="panel-action" style={{ background: 'var(--surface-2)' }}>Manage Plan</button>
            </div>
            
            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '8px' }}>
                <span style={{ color: 'var(--text-dim)' }}>API Tokens Used (Current Billing Cycle)</span>
                <span style={{ fontWeight: 500 }}>0.0M / 50M</span>
              </div>
              <div style={{ width: '100%', height: '8px', background: 'var(--surface-2)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: '0%', height: '100%', background: 'var(--accent)' }}></div>
              </div>
            </div>
            
            <div style={{ fontSize: '12px', color: 'var(--text-faint)' }}>
              Real-time API token usage resets at the beginning of each billing cycle.
            </div>
          </div>

          <div className="panel" style={{ padding: '32px' }}>
            <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '20px' }}>Payment Method</h3>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '16px', border: '1px solid var(--border-soft)', borderRadius: '8px' }}>
              <div style={{ fontSize: '13px', color: 'var(--text-dim)' }}>
                No active credit card saved. Payment details will be configured upon connector activation.
              </div>
              <button className="panel-action" style={{ marginLeft: 'auto' }}>+ Add Method</button>
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-head">
            <h2 className="panel-title">Invoice History</h2>
          </div>
          <div style={{ padding: '32px', color: 'var(--text-dim)', fontSize: '13px', textAlign: 'center' }}>
            No prior billing invoice history found.
          </div>
        </div>
      </div>
    </main>
  );
}

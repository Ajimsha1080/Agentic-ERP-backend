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
                <h2 style={{ fontSize: '18px', fontWeight: 600, margin: 0 }}>Scale Plan</h2>
                <div style={{ fontSize: '13px', color: 'var(--text-dim)', marginTop: '4px' }}>$499 / month + usage</div>
              </div>
              <button className="panel-action" style={{ background: 'var(--surface-2)' }}>Upgrade Plan</button>
            </div>
            
            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '8px' }}>
                <span style={{ color: 'var(--text-dim)' }}>API Tokens Used (Current Billing Cycle)</span>
                <span style={{ fontWeight: 500 }}>42.8M / 50M</span>
              </div>
              <div style={{ width: '100%', height: '8px', background: 'var(--surface-2)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: '85%', height: '100%', background: 'var(--accent)' }}></div>
              </div>
            </div>
            
            <div style={{ fontSize: '12px', color: 'var(--text-faint)' }}>
              Billing cycle resets in 12 days. Overage billed at $0.002 / 1k tokens.
            </div>
          </div>

          <div className="panel" style={{ padding: '32px' }}>
            <h3 style={{ fontSize: '15px', fontWeight: 600, marginBottom: '20px' }}>Payment Method</h3>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '16px', border: '1px solid var(--border-soft)', borderRadius: '8px' }}>
              <div style={{ width: '48px', height: '32px', background: '#fff', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#000', fontWeight: 700, fontSize: '12px' }}>
                VISA
              </div>
              <div>
                <div style={{ fontSize: '14px', fontWeight: 500 }}>Visa ending in 4242</div>
                <div style={{ fontSize: '12px', color: 'var(--text-dim)' }}>Expires 12/28</div>
              </div>
              <button className="panel-action" style={{ marginLeft: 'auto' }}>Edit</button>
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-head">
            <h2 className="panel-title">Invoice History</h2>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {[
              { id: 'INV-2026-07', date: 'Jul 1, 2026', amount: '$542.10', status: 'Paid' },
              { id: 'INV-2026-06', date: 'Jun 1, 2026', amount: '$499.00', status: 'Paid' },
              { id: 'INV-2026-05', date: 'May 1, 2026', amount: '$499.00', status: 'Paid' },
            ].map(inv => (
              <div key={inv.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 24px', borderBottom: '1px solid var(--border-soft)' }}>
                <div>
                  <div style={{ fontSize: '14px', fontWeight: 500 }}>{inv.date}</div>
                  <div style={{ fontSize: '12px', color: 'var(--text-dim)', marginTop: '4px' }}>{inv.id}</div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div style={{ fontSize: '14px', fontWeight: 500 }}>{inv.amount}</div>
                  <span style={{ fontSize: '11px', color: 'var(--verified)', background: 'rgba(47,217,168,0.1)', padding: '4px 8px', borderRadius: '4px' }}>{inv.status}</span>
                  <button className="panel-action" style={{ padding: '6px' }}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: '16px', height: '16px' }}>
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <polyline points="7 10 12 15 17 10" />
                      <line x1="12" y1="15" x2="12" y2="3" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}

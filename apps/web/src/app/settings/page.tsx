"use client";

import { useState } from "react";

export default function SettingsPage() {
  const [strictMode, setStrictMode] = useState(false);
  const [autoSummarize, setAutoSummarize] = useState(true);

  return (
    <main className="main">
      <div className="topbar">
        <div>
          <span className="crumb">Settings</span>
          <span className="crumb-sub">Manage workspace preferences</span>
        </div>
        <button className="panel-action" style={{ marginLeft: 'auto', background: 'var(--accent)', color: '#fff', borderColor: 'var(--accent)' }}>
          Save Changes
        </button>
      </div>

      <div className="content" style={{ display: 'flex', gap: '32px' }}>
        <div style={{ width: '240px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <button className="nav-item active" style={{ background: 'var(--surface-2)', color: 'var(--text)' }}>General</button>
          <button className="nav-item" style={{ background: 'transparent' }}>Organization</button>
          <button className="nav-item" style={{ background: 'transparent' }}>Team Members</button>
          <button className="nav-item" style={{ background: 'transparent' }}>API Keys</button>
          <button className="nav-item" style={{ background: 'transparent' }}>Notifications</button>
        </div>

        <div className="panel" style={{ flex: 1, padding: '32px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '24px' }}>General Settings</h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-dim)', marginBottom: '8px' }}>Workspace Name</label>
              <input 
                type="text" 
                defaultValue="Northbeam Foods" 
                style={{ width: '100%', maxWidth: '400px', background: 'var(--bg)', border: '1px solid var(--border)', padding: '10px 12px', borderRadius: '6px', color: 'var(--text)', fontSize: '14px', outline: 'none' }} 
              />
            </div>
            
            <div>
              <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-dim)', marginBottom: '8px' }}>Support Email</label>
              <input 
                type="email" 
                defaultValue="hello@northbeam.com" 
                style={{ width: '100%', maxWidth: '400px', background: 'var(--bg)', border: '1px solid var(--border)', padding: '10px 12px', borderRadius: '6px', color: 'var(--text)', fontSize: '14px', outline: 'none' }} 
              />
            </div>

            <div style={{ borderTop: '1px solid var(--border-soft)', paddingTop: '24px', marginTop: '8px' }}>
              <h3 style={{ fontSize: '15px', fontWeight: 500, marginBottom: '16px' }}>AI Agent Preferences</h3>
              
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', maxWidth: '400px', marginBottom: '16px' }}>
                <div>
                  <div style={{ fontSize: '14px', fontWeight: 500 }}>Strict Approval Mode</div>
                  <div style={{ fontSize: '12px', color: 'var(--text-dim)' }}>Require human approval for all actions.</div>
                </div>
                <div onClick={() => setStrictMode(!strictMode)} style={{ width: '40px', height: '24px', borderRadius: '12px', background: strictMode ? 'var(--accent)' : 'var(--surface-2)', position: 'relative', cursor: 'pointer', transition: 'background 0.3s' }}>
                  <div style={{ width: '18px', height: '18px', borderRadius: '9px', background: '#fff', position: 'absolute', top: '3px', left: strictMode ? '19px' : '3px', transition: 'left 0.3s' }}></div>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', maxWidth: '400px' }}>
                <div>
                  <div style={{ fontSize: '14px', fontWeight: 500 }}>Auto-Summarize Workflows</div>
                  <div style={{ fontSize: '12px', color: 'var(--text-dim)' }}>Generate end-of-day summary reports.</div>
                </div>
                <div onClick={() => setAutoSummarize(!autoSummarize)} style={{ width: '40px', height: '24px', borderRadius: '12px', background: autoSummarize ? 'var(--accent)' : 'var(--surface-2)', position: 'relative', cursor: 'pointer', transition: 'background 0.3s' }}>
                  <div style={{ width: '18px', height: '18px', borderRadius: '9px', background: '#fff', position: 'absolute', top: '3px', left: autoSummarize ? '19px' : '3px', transition: 'left 0.3s' }}></div>
                </div>
              </div>
            </div>
            
            <div style={{ borderTop: '1px solid var(--border-soft)', paddingTop: '24px', marginTop: '8px' }}>
              <button className="panel-action" style={{ color: 'var(--danger)', borderColor: 'var(--danger)', background: 'rgba(240,85,91,0.1)' }}>
                Delete Workspace
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

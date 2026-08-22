"use client";

import { useState, useEffect } from "react";

import Link from "next/link";

export default function AgentsPage() {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    const fetchAgents = () => {
      fetch("http://localhost:8000/api/v1/agents")
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
        .then(data => {
          if (isMounted) {
            if (Array.isArray(data)) setAgents(data);
            else if (data && data.items) setAgents(data.items);
            else setAgents([]);
          }
        })
        .catch(err => {
          console.warn("API connecting...", err);
          if (isMounted) setAgents([]);
        })
        .finally(() => {
          if (isMounted) setLoading(false);
        });
    };

    fetchAgents();
    return () => { isMounted = false; };
  }, []);

  return (
    <main className="main">
      <div className="topbar">
        <div className="breadcrumb">Agents</div>
      </div>
      <div className="content">
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h1 className="display" style={{ fontSize: '24px' }}>AI Workforce</h1>
            <p className="text-dim text-sm" style={{ marginTop: '4px' }}>Manage and configure your specialized autonomous agents.</p>
          </div>
          <button className="btn btn-primary">+ Deploy Agent</button>
        </div>

        {loading ? (
          <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
            <div className="skeleton" style={{ height: '200px', borderRadius: '12px' }}></div>
            <div className="skeleton" style={{ height: '200px', borderRadius: '12px' }}></div>
            <div className="skeleton" style={{ height: '200px', borderRadius: '12px' }}></div>
          </div>
        ) : (
          <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
            {agents.map((agent: any, i: number) => (
              <div key={i} className="kpi-card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                    <div style={{ width: '40px', height: '40px', borderRadius: '10px', background: 'var(--surface-2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--ai-core)', border: '1px solid var(--border)' }}>
                      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zM4 11a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-7z"/>
                      </svg>
                    </div>
                    <div>
                      <h3 className="font-semibold text-base">{agent.name || agent.role}</h3>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '4px' }}>
                        <span className={`badge ${agent.status === 'Active' || agent.status === 'idle' ? 'active' : 'warning'}`}>
                          {agent.status || 'Active'}
                        </span>
                      </div>
                    </div>
                  </div>
                  <button style={{ color: 'var(--text-faint)' }}>•••</button>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', borderTop: '1px solid var(--border-soft)', borderBottom: '1px solid var(--border-soft)', padding: '16px 0' }}>
                  <div>
                    <div className="text-xs text-faint font-semibold uppercase mb-1" style={{ marginBottom: '4px' }}>Tasks Completed</div>
                    <div className="font-semibold text-base">{agent.actions ?? 0}</div>
                  </div>
                  <div>
                    <div className="text-xs text-faint font-semibold uppercase mb-1" style={{ marginBottom: '4px' }}>Success Rate</div>
                    <div className="font-semibold text-base">{agent.successRate || '100%'}</div>
                  </div>
                  <div>
                    <div className="text-xs text-faint font-semibold uppercase mb-1" style={{ marginBottom: '4px' }}>Role</div>
                    <div className="font-semibold text-base">{agent.role}</div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '8px' }}>
                  <Link href={`/agents/${agent.id || i + 1}`} className="btn btn-secondary" style={{ flex: 1, textAlign: 'center', textDecoration: 'none' }}>Configure</Link>
                  <button className="btn btn-secondary" style={{ flex: 1 }}>{agent.status === 'Paused' ? 'Resume' : 'Pause'}</button>
                </div>
              </div>
            ))}
          </div>
        )}

      </div>
    </main>
  );
}

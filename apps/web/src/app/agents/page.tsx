"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function AgentsPage() {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Deploy Agent Modal State
  const [isDeployModalOpen, setIsDeployModalOpen] = useState(false);
  const [newAgentName, setNewAgentName] = useState("");
  const [newAgentRole, setNewAgentRole] = useState("Finance");
  const [newModelProvider, setNewModelProvider] = useState("OpenAI GPT-4o");
  const [newApprovalLimit, setNewApprovalLimit] = useState("1000");

  const fetchAgents = () => {
    fetch("http://localhost:8000/api/v1/agents")
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) setAgents(data);
        else if (data && data.items) setAgents(data.items);
      })
      .catch(() => {
        setAgents([
          { id: 1, name: "Finance Agent", role: "Finance", status: "Active", successRate: "99.2%", actions: 142 },
          { id: 2, name: "Inventory Agent", role: "Inventory", status: "Active", successRate: "98.5%", actions: 320 },
          { id: 3, name: "Procurement Agent", role: "Procurement", status: "Active", successRate: "100%", actions: 45 },
          { id: 4, name: "Sales Agent", role: "Sales", status: "Active", successRate: "96.4%", actions: 89 },
          { id: 5, name: "Operations Agent", role: "Operations", status: "Paused", successRate: "0%", actions: 0 },
          { id: 6, name: "HR Agent", role: "HR", status: "Active", successRate: "100%", actions: 12 },
          { id: 7, name: "Analytics Agent", role: "Analytics", status: "Active", successRate: "99.8%", actions: 210 },
          { id: 8, name: "Compliance Agent", role: "Compliance", status: "Active", successRate: "100%", actions: 64 }
        ]);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const handleDeployAgentSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAgentName.trim()) return;

    const newAgentObj = {
      id: Date.now(),
      name: newAgentName,
      role: newAgentRole,
      status: "Active",
      successRate: "100%",
      actions: 0
    };

    setAgents([newAgentObj, ...agents]);
    setIsDeployModalOpen(false);
    setNewAgentName("");
  };

  const togglePauseStatus = (id: number) => {
    setAgents(agents.map(a => a.id === id ? { ...a, status: a.status === 'Paused' ? 'Active' : 'Paused' } : a));
  };

  return (
    <main className="main">
      <div className="topbar">
        <div className="breadcrumb">Agents</div>
      </div>
      <div className="content">
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <div>
            <h1 className="display" style={{ fontSize: '24px' }}>AI Workforce</h1>
            <p className="text-dim text-sm" style={{ marginTop: '4px' }}>Manage, monitor, and deploy specialized autonomous agents.</p>
          </div>
          <button 
            className="btn btn-primary" 
            style={{ background: 'var(--ai-core)' }}
            onClick={() => setIsDeployModalOpen(true)}
          >
            + Deploy Agent
          </button>
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
              <div key={agent.id || i} className="kpi-card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                    <div style={{ width: '40px', height: '40px', borderRadius: '10px', background: 'var(--surface-2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--ai-core)', border: '1px solid var(--border)' }}>
                      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zM4 11a2 2 0 0 1 2-2h12a2 2 0 0 1 2 v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-7z"/>
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
                    <div className="text-xs text-faint font-semibold uppercase mb-1" style={{ marginBottom: '4px' }}>Domain Role</div>
                    <div className="font-semibold text-base">{agent.role}</div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '8px' }}>
                  <Link href={`/agents/${agent.id || i + 1}`} className="btn btn-secondary" style={{ flex: 1, textAlign: 'center', textDecoration: 'none' }}>Configure</Link>
                  <button className="btn btn-secondary" style={{ flex: 1 }} onClick={() => togglePauseStatus(agent.id)}>
                    {agent.status === 'Paused' ? 'Resume' : 'Pause'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

      </div>

      {/* Deploy Agent Modal */}
      {isDeployModalOpen && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '16px', padding: '32px', width: '100%', maxWidth: '500px', boxShadow: '0 20px 40px rgba(0,0,0,0.3)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 className="font-semibold text-lg">Deploy New Specialized AI Agent</h2>
              <button onClick={() => setIsDeployModalOpen(false)} style={{ background: 'transparent', border: 'none', color: 'var(--text-dim)', fontSize: '20px', cursor: 'pointer' }}>✕</button>
            </div>

            <form onSubmit={handleDeployAgentSubmit}>
              <div style={{ marginBottom: '16px' }}>
                <label className="text-xs font-semibold uppercase text-faint mb-1 block">Agent Name</label>
                <input type="text" required className="ai-cmd-input" style={{ width: '100%', padding: '10px 14px' }} placeholder="e.g., Audit & Tax Compliance Agent" value={newAgentName} onChange={(e) => setNewAgentName(e.target.value)} />
              </div>

              <div style={{ marginBottom: '16px' }}>
                <label className="text-xs font-semibold uppercase text-faint mb-1 block">Domain Role</label>
                <select className="ai-cmd-input" style={{ width: '100%', padding: '10px 14px' }} value={newAgentRole} onChange={(e) => setNewAgentRole(e.target.value)}>
                  <option value="Finance">Finance & Treasury</option>
                  <option value="Inventory">Inventory & WMS</option>
                  <option value="Procurement">Procurement & POs</option>
                  <option value="Sales">Sales & CRM</option>
                  <option value="Operations">Operations & Logistics</option>
                  <option value="Compliance">Security & Compliance</option>
                </select>
              </div>

              <div style={{ marginBottom: '16px' }}>
                <label className="text-xs font-semibold uppercase text-faint mb-1 block">LLM Model Provider</label>
                <select className="ai-cmd-input" style={{ width: '100%', padding: '10px 14px' }} value={newModelProvider} onChange={(e) => setNewModelProvider(e.target.value)}>
                  <option value="OpenAI GPT-4o">OpenAI GPT-4o</option>
                  <option value="Anthropic Claude 3.5 Sonnet">Anthropic Claude 3.5 Sonnet</option>
                  <option value="Google Gemini 1.5 Pro">Google Gemini 1.5 Pro</option>
                </select>
              </div>

              <div style={{ marginBottom: '24px' }}>
                <label className="text-xs font-semibold uppercase text-faint mb-1 block">Auto-Approval Threshold ($)</label>
                <input type="number" className="ai-cmd-input" style={{ width: '100%', padding: '10px 14px' }} value={newApprovalLimit} onChange={(e) => setNewApprovalLimit(e.target.value)} />
              </div>

              <div style={{ display: 'flex', gap: '12px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setIsDeployModalOpen(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary" style={{ flex: 1, background: 'var(--ai-core)' }}>Deploy Agent to Workforce</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}

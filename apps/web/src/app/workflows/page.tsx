"use client";

import { useState } from "react";

export default function WorkflowsPage() {
  // Clean Real-Time State (Workflows built dynamically by user)
  const [workflows, setWorkflows] = useState<any[]>([]);

  const [isBuilderOpen, setIsBuilderOpen] = useState(false);
  const [newWfName, setNewWfName] = useState("");
  const [newWfDesc, setNewWfDesc] = useState("");
  const [selectedAgentNodes, setSelectedAgentNodes] = useState<string[]>(["Inventory Agent"]);

  const toggleWorkflow = (id: number) => {
    setWorkflows(workflows.map(wf => wf.id === id ? { ...wf, active: !wf.active } : wf));
  };

  const toggleAgentNode = (agent: string) => {
    if (selectedAgentNodes.includes(agent)) {
      setSelectedAgentNodes(selectedAgentNodes.filter(a => a !== agent));
    } else {
      setSelectedAgentNodes([...selectedAgentNodes, agent]);
    }
  };

  const handleCreateWorkflow = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newWfName.trim()) return;
    setWorkflows([
      {
        id: Date.now(),
        name: newWfName,
        description: newWfDesc || 'Custom agentic multi-node workflow pipeline.',
        active: true,
        agents: selectedAgentNodes.length ? selectedAgentNodes : ['Agent Orchestrator']
      },
      ...workflows
    ]);
    setIsBuilderOpen(false);
    setNewWfName("");
    setNewWfDesc("");
  };

  return (
    <main className="main">
      <div className="topbar">
        <div>
          <span className="crumb">Workflows</span>
          <span className="crumb-sub">Manage & Orchestrate Multi-Agent Pipelines</span>
        </div>
        <button 
          className="btn btn-primary" 
          style={{ marginLeft: 'auto', background: 'var(--ai-core)' }}
          onClick={() => setIsBuilderOpen(true)}
        >
          + Build New Workflow Pipeline
        </button>
      </div>

      <div className="content">
        
        {/* Workflows Grid / Empty State */}
        {workflows.length === 0 ? (
          <div className="panel" style={{ padding: '60px 24px', textAlign: 'center', color: 'var(--text-dim)', borderRadius: '16px' }}>
            <div style={{ fontSize: '42px', marginBottom: '16px' }}>⚡</div>
            <h3 className="font-semibold text-base mb-1" style={{ color: 'var(--text)' }}>No Custom Multi-Agent Workflows Configured</h3>
            <p className="text-sm text-dim mb-4" style={{ maxWidth: '460px', margin: '0 auto 16px auto' }}>
              Construct multi-node workflow pipelines connecting your domain agents (e.g. Finance Agent $\rightarrow$ Inventory Agent $\rightarrow$ Procurement Agent).
            </p>
            <button 
              className="btn btn-primary" 
              style={{ background: 'var(--ai-core)' }}
              onClick={() => setIsBuilderOpen(true)}
            >
              + Build New Workflow Pipeline
            </button>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '24px' }}>
            {workflows.map((wf) => (
              <div key={wf.id} className="panel" style={{ padding: '24px', borderRadius: '16px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <h3 style={{ fontSize: '16px', fontWeight: 600, margin: 0, color: 'var(--text)' }}>{wf.name}</h3>
                    <p style={{ fontSize: '12px', color: 'var(--text-dim)', marginTop: '4px' }}>{wf.description}</p>
                  </div>
                  <button 
                    onClick={() => toggleWorkflow(wf.id)}
                    style={{ 
                      background: wf.active ? 'var(--verified-soft)' : 'var(--surface-2)', 
                      color: wf.active ? 'var(--verified)' : 'var(--text-dim)',
                      border: 'none',
                      padding: '4px 10px',
                      borderRadius: '12px',
                      fontSize: '11px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    {wf.active ? '🟢 Active' : '⚪ Paused'}
                  </button>
                </div>

                <div style={{ background: 'var(--bg)', borderRadius: '10px', padding: '12px', border: '1px solid var(--border-soft)' }}>
                  <div className="text-xs font-semibold text-faint uppercase mb-2">Connected Agent Nodes</div>
                  <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    {wf.agents.map((ag: string) => (
                      <span key={ag} className="badge" style={{ background: 'var(--surface-2)', color: 'var(--ai-core)', fontSize: '11px' }}>
                        {ag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Workflow Builder Modal */}
      {isBuilderOpen && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '16px', padding: '32px', width: '100%', maxWidth: '520px', boxShadow: '0 20px 40px rgba(0,0,0,0.3)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 className="font-semibold text-lg">Build Agentic Workflow Pipeline</h2>
              <button onClick={() => setIsBuilderOpen(false)} style={{ background: 'transparent', border: 'none', color: 'var(--text-dim)', fontSize: '20px', cursor: 'pointer' }}>✕</button>
            </div>

            <form onSubmit={handleCreateWorkflow}>
              <div style={{ marginBottom: '16px' }}>
                <label className="text-xs font-semibold uppercase text-faint mb-1 block">Workflow Name</label>
                <input type="text" required className="ai-cmd-input" style={{ width: '100%', padding: '10px 14px' }} placeholder="e.g., Automated Stockout Replenishment" value={newWfName} onChange={(e) => setNewWfName(e.target.value)} />
              </div>

              <div style={{ marginBottom: '16px' }}>
                <label className="text-xs font-semibold uppercase text-faint mb-1 block">Description</label>
                <input type="text" className="ai-cmd-input" style={{ width: '100%', padding: '10px 14px' }} placeholder="Describe pipeline trigger and action..." value={newWfDesc} onChange={(e) => setNewWfDesc(e.target.value)} />
              </div>

              <div style={{ marginBottom: '24px' }}>
                <label className="text-xs font-semibold uppercase text-faint mb-2 block">Select Agent Nodes</label>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                  {["Finance Agent", "Inventory Agent", "Procurement Agent", "Sales Agent", "Operations Agent", "Compliance Agent"].map((ag) => (
                    <div 
                      key={ag}
                      onClick={() => toggleAgentNode(ag)}
                      style={{ 
                        padding: '10px', 
                        borderRadius: '8px', 
                        border: `1px solid ${selectedAgentNodes.includes(ag) ? 'var(--ai-core)' : 'var(--border)'}`,
                        background: selectedAgentNodes.includes(ag) ? 'var(--surface-2)' : 'var(--bg)',
                        cursor: 'pointer',
                        fontSize: '12px'
                      }}
                    >
                      {selectedAgentNodes.includes(ag) ? '✓ ' : ''}{ag}
                    </div>
                  ))}
                </div>
              </div>

              <div style={{ display: 'flex', gap: '12px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setIsBuilderOpen(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary" style={{ flex: 1, background: 'var(--ai-core)' }}>Deploy Workflow Pipeline</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}

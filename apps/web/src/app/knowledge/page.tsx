"use client";

import { useState, useEffect } from "react";

export default function KnowledgePage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/dashboard/knowledge")
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  return (
    <main className="main">
      <div className="topbar">
        <div className="breadcrumb">Knowledge Base</div>
        <div className="search-bar">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input type="text" placeholder="Search policies, SOPs..." />
          <span className="cmd-k">⌘K</span>
        </div>
      </div>
      <div className="content">
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <div>
            <h1 className="display" style={{ fontSize: '24px' }}>Company Knowledge</h1>
            <p className="text-dim text-sm" style={{ marginTop: '4px' }}>The central nervous system for your AI agents. All uploaded documents are indexed for RAG.</p>
          </div>
          <button className="btn btn-primary">Upload Document</button>
        </div>

        {!data ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div className="skeleton" style={{ height: '120px', borderRadius: '8px' }}></div>
            <div className="skeleton" style={{ height: '400px', borderRadius: '8px' }}></div>
          </div>
        ) : (
          <>
            <div className="kpi-grid" style={{ marginBottom: '32px' }}>
              {(data?.kpis || []).map((kpi: any, i: number) => (
                <div key={i} className="kpi-card">
                  <div className="kpi-label">{kpi.label}</div>
                  <div className="kpi-val">{kpi.value}</div>
                  <div className={`kpi-delta ${kpi.trend}`}>{kpi.delta}</div>
                </div>
              ))}
            </div>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Document Name</th>
                    <th>Type</th>
                    <th>Owner</th>
                    <th>Last Updated</th>
                    <th>Agent Access</th>
                  </tr>
                </thead>
                <tbody>
                  {(data?.documents || []).map((doc: any, i: number) => (
                    <tr key={i}>
                      <td className="font-medium">{doc.name}</td>
                      <td>{doc.type}</td>
                      <td>{doc.owner}</td>
                      <td className="text-faint">{doc.updated}</td>
                      <td>
                        <span className={`badge ${doc.access === 'Global' ? 'active' : 'warning'}`}>
                          {doc.access}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

      </div>
    </main>
  );
}

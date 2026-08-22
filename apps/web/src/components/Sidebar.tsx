"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();
  
  // For a truly massive enterprise nav, we might normally want collapsible sections. 
  // We'll keep them open for now but logically grouped.
  
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M12 3L4 7v10l8 4 8-4V7l-8-4z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
          </svg>
        </div>
        <div>
          <div className="brand-name">Agentic ERP</div>
        </div>
      </div>

      <nav>
        <div className="nav-group">
          <div className="nav-label">AI Workspace</div>
          <Link href="/" className={`nav-item ${pathname === "/" ? "active" : ""}`}>
            Overview
          </Link>
          <Link href="/agents" className={`nav-item ${pathname === "/agents" ? "active" : ""}`}>
            Agents
            <span className="nav-badge">8 Active</span>
          </Link>
          <Link href="/activity" className={`nav-item ${pathname === "/activity" ? "active" : ""}`}>
            Agent Activity
          </Link>
          <Link href="/approvals" className={`nav-item ${pathname === "/approvals" ? "active" : ""}`}>
            Approvals
          </Link>
        </div>

        <div className="nav-group">
          <div className="nav-label">Business</div>
          <Link href="/finance" className={`nav-item ${pathname === "/finance" ? "active" : ""}`}>Finance</Link>
          <Link href="/sales" className={`nav-item ${pathname === "/sales" ? "active" : ""}`}>Sales</Link>
          <Link href="/inventory" className={`nav-item ${pathname === "/inventory" ? "active" : ""}`}>Inventory</Link>
          <Link href="/procurement" className={`nav-item ${pathname === "/procurement" ? "active" : ""}`}>Procurement</Link>
          <Link href="/operations" className={`nav-item ${pathname === "/operations" ? "active" : ""}`}>Operations</Link>
        </div>

        <div className="nav-group">
          <div className="nav-label">Data & Integration</div>
          <Link href="/connectors" className={`nav-item ${pathname === "/connectors" ? "active" : ""}`}>Integrations Hub</Link>
          <Link href="/knowledge" className={`nav-item ${pathname === "/knowledge" ? "active" : ""}`}>Knowledge Base</Link>
        </div>

        <div className="nav-group">
          <div className="nav-label">Administration</div>
          <Link href="/security" className={`nav-item ${pathname === "/security" ? "active" : ""}`}>Security</Link>
          <Link href="/audit" className={`nav-item ${pathname === "/audit" ? "active" : ""}`}>Audit Logs</Link>
          <Link href="/settings" className={`nav-item ${pathname === "/settings" ? "active" : ""}`}>Settings</Link>
        </div>
      </nav>
    </aside>
  );
}

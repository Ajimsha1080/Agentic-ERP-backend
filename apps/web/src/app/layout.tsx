import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "../components/Sidebar";
import CommandPalette from "../components/CommandPalette";

export const metadata: Metadata = {
  title: "Agentic ERP Platform",
  description: "Enterprise-grade AI-Native Business Operating Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <Sidebar />
          {children}
        </div>
        <CommandPalette />
      </body>
    </html>
  );
}

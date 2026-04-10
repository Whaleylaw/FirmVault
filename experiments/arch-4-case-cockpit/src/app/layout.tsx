import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";

// TODO: auth — the cockpit is intentionally unauthenticated for the
// MVP bake-off. Before it goes anywhere near real client data,
// add at minimum a single-user password gate or an OIDC proxy.

export const metadata: Metadata = {
  title: "Case Cockpit — FirmVault",
  description: "Case-centric paralegal runtime for the FirmVault Track A bake-off.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <header className="border-b border-cockpit-edge bg-cockpit-panel">
          <div className="mx-auto max-w-7xl px-6 py-4 flex items-center justify-between">
            <Link href="/" className="text-lg font-semibold text-cockpit-accent">
              Case Cockpit
            </Link>
            <nav className="text-sm text-slate-400 flex gap-4">
              <span>arch-4</span>
              <span>track A bake-off</span>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-7xl px-6 py-8">{children}</main>
        <footer className="mx-auto max-w-7xl px-6 py-6 text-xs text-slate-500">
          Reads the firmvault repo via simple-git. Writes vault commits,
          optionally opens PRs via <code>gh</code>. See <code>docs/smoke-test.md</code>.
        </footer>
      </body>
    </html>
  );
}

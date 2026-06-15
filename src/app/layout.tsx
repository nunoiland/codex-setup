import type { Metadata } from "next";
import Link from "next/link";

import { productConfig } from "@/config/product";

import "./globals.css";

export const metadata: Metadata = {
  title: productConfig.name,
  description: productConfig.description,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen">
          <header className="border-b border-[var(--border)] bg-white/90 backdrop-blur">
            <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
              <div>
                <p className="text-sm font-semibold tracking-wide text-slate-900">
                  {productConfig.name}
                </p>
                <p className="text-xs text-slate-500">{productConfig.tagline}</p>
              </div>
              <nav className="flex items-center gap-5 text-sm text-slate-600">
                <Link href="/">Landing</Link>
                <Link href="/app">App</Link>
                <Link href="/admin">Admin</Link>
                <Link href="/health">Health</Link>
              </nav>
            </div>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}

import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RED BLEE",
  description: "RED BLEE - Multi-model AI comparison and benchmarking dashboard.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

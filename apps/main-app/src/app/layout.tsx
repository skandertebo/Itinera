import "@/styles/globals.css";

import { type Metadata } from "next";
import { Geist } from "next/font/google";
import { NavTop } from "./_components/NavTop";
import { Providers } from "./providers";

import { TRPCReactProvider } from "@/trpc/react";

const geist = Geist({
  subsets: ["latin"],
  variable: "--font-geist-sans",
});

export const metadata: Metadata = {
  title: "Itinera - AI-Powered Hotel Recommendations",
  description: "Find your perfect hotel with AI-powered recommendations",
  icons: [{ rel: "icon", url: "/favicon.ico" }],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${geist.variable}`}>
      <body>
        <TRPCReactProvider>
          <Providers>
            <div className="min-h-screen bg-gray-50">
              <NavTop />
              <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
                {children}
              </main>
            </div>
          </Providers>
        </TRPCReactProvider>
      </body>
    </html>
  );
}

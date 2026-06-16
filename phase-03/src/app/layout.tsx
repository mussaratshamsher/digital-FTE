import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Toaster } from "@/components/ui/sonner";
import { ThemeProvider } from "@/components/theme-provider";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Digital FTE | AI CRM Digital Factory & Automated Workflows",
  description: "Digital FTE - The ultimate AI CRM Digital Factory. Transform your business with automated lead qualification, project management, and humanoid robotics workflow solutions.",
  keywords: [
    "Digital FTE",
    "AI CRM",
    "Business Automation",
    "Digital Factory",
    "Workflow Optimization",
    "Lead Qualification",
    "Project Logistics",
    "Customer Support AI",
    "Agentic Workflows",
    "Humanoid Robotics"
  ],
  authors: [{ name: "Mussarat Shamsher" }],
  metadataBase: new URL("https://mussarat-digital-fte.vercel.app"),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "Digital FTE | AI CRM Digital Factory",
    description: "Automate your business operations with Digital FTE. The next generation of AI-powered CRM and workflow management.",
    url: "https://mussarat-digital-fte.vercel.app",
    siteName: "Digital FTE",
    images: [
      {
        url: "/fte.jpg",
        width: 1200,
        height: 630,
        alt: "Digital FTE Preview",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Digital FTE | AI CRM Digital Factory",
    description: "Automate your business operations with Digital FTE.",
    images: ["/fte.jpg"],
  },
  icons: {
    icon: "/fte.jpg",
  },
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
      suppressHydrationWarning
    >
      <body className={`${geistSans.variable} ${geistMono.variable} min-h-full flex flex-col`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}

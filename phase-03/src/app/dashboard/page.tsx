import { Metadata } from "next";
import DashboardClient from "./DashboardClient";

export const metadata: Metadata = {
  title: "Dashboard | Digital FTE Command Center",
  description: "Manage your Digital FTE autonomous workforce. Monitor agent activity, optimize neural workflows, and track business intelligence in real-time.",
};

export default function DashboardPage() {
  return <DashboardClient />;
}

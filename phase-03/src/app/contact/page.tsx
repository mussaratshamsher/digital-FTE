import { Metadata } from "next";
import ContactClient from "./ContactClient";

export const metadata: Metadata = {
  title: "Contact Digital FTE | AI Business Automation Support",
  description: "Get in touch with the Digital FTE team. Learn how our AI CRM Digital Factory can transform your business workflows with autonomous agents.",
  keywords: ["Contact Digital FTE", "AI Support", "Business Automation Inquiry", "Digital Factory Consultation"],
};

export default function ContactPage() {
  return <ContactClient />;
}

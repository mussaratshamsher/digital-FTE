To connect WhatsApp, Gmail, and a Web Form to orchestrator while staying within "Forever Free" tiers, here is
  the architecture and the step-by-step guide.

  ---

  1. The "Forever Free" Connectivity Strategy

  A. WhatsApp (The Bridge)
   * Choice: Evolution API or WPPConnect (Self-hosted).
   * Why: Official Meta APIs have 1,000 free conversations/month, but after that, they charge. Self-hosted bridges act
     like "WhatsApp Web" on a server. They are 100% free as long as your server is running.
   * Hosting: Use Oracle Cloud "Always Free" (4 ARM CPUs, 24GB RAM). This is the most powerful free server on the
     planet and will never expire.

  B. Gmail (The Inbox)
   * Choice: Google Cloud Gmail API.
   * Why: Using IMAP/SMTP is getting harder due to security. The Gmail API allows you to "watch" your inbox. Google
     Cloud's free tier for API calls is extremely generous (virtually unlimited for personal use).
   * Setup: Enable Gmail API in Google Cloud Console, create an OAuth2 credential, and the AI will poll for new
     messages.

  C. Web Form (The Frontend)
   * Choice: Next.js (your phase-03 code) hosted on Vercel.
   * Why: Vercel’s free tier is permanent and includes SSL, global CDN, and easy deployments.

  ---

  2. How the Orchestrator Handles it Autonomously

  Your Orchestrator (currently in phase-02/app/agents/stage1_agents/orchestrator.py) will be upgraded with a "Channel &
  Sensitivity Layer".

  Workflow Logic:
   1. Ingestion: A background service listens to Gmail, WhatsApp, and the Web Form.
   2. Classification: The Orchestrator analyzes the message:
       * Simple Task: (e.g., "What are your prices?") -> AI replies directly via the same channel.
       * Sensitive/Personal: (e.g., "I want to discuss a private contract" or "Refund request") -> AI stops.
   3. Human-in-the-Loop:
       * The AI sends YOU a WhatsApp message: "Review needed: Customer [Name] asked about [Topic]. Suggested reply:
         [Text]. Reply 'Yes' to send or type your edit."
       * Once you reply on WhatsApp, the AI sends the final response to the customer.

  ---

  3. Step-by-Step Implementation Guide

  Phase 1: Infrastructure (The "Never-End" Server)
   1. Sign up for Oracle Cloud Always Free.
   2. Spin up an Ubuntu ARM Instance.
   3. Install Docker and run Evolution API. Scan the QR code with your phone. Now your AI can send/receive WhatsApp
      messages for free.

  Phase 2: Gmail Integration
   1. Go to Google Cloud Console (https://console.cloud.google.com/).
   2. Create a project -> Enable Gmail API.
   3. Configure OAuth Screen and download credentials.json.
   4. We will add a Python script to your tools/ folder that uses these credentials to read and send emails.

  Phase 3: Upgrading the Orchestrator
  We will modify orchestrator.py to include a is_sensitive check in the JSON output:

   1 {
   2     "intent": "...",
   3     "is_sensitive": true,
   4     "review_reason": "Personal financial data mentioned",
   5     "plan": [...]
   6 }

  Phase 4: The "Notification" Tool
  We will update communication_tools.py to:
   1. Connect to your Evolution API (WhatsApp).
   2. Send a message to your specific phone number whenever is_sensitive is true.

  ---

  Would you like me to start by:
   1. Creating the Gmail API integration tool? (Requires you to get the credentials.json later, but I can write the
      code now).
   2. Setting up the WhatsApp Evolution API connector?
   3. Modifying the Orchestrator to handle "Sensitive" vs "Autonomous" logic?

  Note: Since we are aiming for "Forever Free," I recommend we use Groq (which you already have) for the AI logic, as
  their current free tier is very high-performance. If you want a 100% offline/local "Forever Free" model, we can use
  Ollama on your Oracle server, though it will be slower.

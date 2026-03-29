import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.config import settings

def send_email(to: str, subject: str, html_body: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = settings.EMAIL_FROM
    msg["To"]      = to
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAIL_FROM, to, msg.as_string())

# ── Template helpers ───────────────────────────────────────
def send_lead_confirmation(name: str, email: str):
    send_email(
        to=email,
        subject="Thanks for reaching out — LevelUp Agency",
        html_body=f"""
        <div style="font-family:sans-serif;max-width:520px;margin:auto;padding:32px;background:#f9f9f9;border-radius:8px">
          <h2 style="color:#070708">Hey {name}, we got your request! 👋</h2>
          <p style="color:#555;line-height:1.7">
            Thanks for reaching out to <strong>LevelUp Agency</strong>. 
            We'll review your details and send over a free audit of your social media 
            presence within <strong>24 hours</strong>.
          </p>
          <a href="https://levelup.agency" 
             style="display:inline-block;margin-top:24px;padding:12px 28px;background:#b8ff57;color:#070708;font-weight:700;border-radius:4px;text-decoration:none">
            Visit Our Website
          </a>
          <p style="color:#aaa;font-size:12px;margin-top:32px">LevelUp Agency · hello@levelup.agency</p>
        </div>
        """
    )

def send_admin_lead_alert(name: str, email: str, message: str):
    send_email(
        to=settings.ADMIN_EMAIL,
        subject=f"🔥 New Lead: {name}",
        html_body=f"""
        <div style="font-family:sans-serif;max-width:520px;margin:auto;padding:32px;background:#111;color:#f5f5f5;border-radius:8px">
          <h2 style="color:#b8ff57">New Lead Received</h2>
          <p><strong>Name:</strong> {name}</p>
          <p><strong>Email:</strong> {email}</p>
          <p><strong>Message:</strong><br>{message}</p>
        </div>
        """
    )

def send_welcome_email(name: str, email: str):
    send_email(
        to=email,
        subject="Welcome to LevelUp 🚀",
        html_body=f"""
        <div style="font-family:sans-serif;max-width:520px;margin:auto;padding:32px;background:#f9f9f9;border-radius:8px">
          <h2 style="color:#070708">Welcome, {name}!</h2>
          <p style="color:#555;line-height:1.7">
            Your LevelUp account is ready. Log in to access your dashboard and track your campaigns.
          </p>
          <p style="color:#aaa;font-size:12px;margin-top:32px">LevelUp Agency · hello@levelup.agency</p>
        </div>
        """
    )

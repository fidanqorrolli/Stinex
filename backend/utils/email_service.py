"""
Email service for sending notifications about contact form submissions.
This is a basic implementation - in production, you would use a proper email service.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("EMAIL_HOST", "localhost")
        self.smtp_port = int(os.getenv("EMAIL_PORT", "587"))
        self.smtp_user = os.getenv("EMAIL_USER", "")
        self.smtp_password = os.getenv("EMAIL_PASS", "")
        self.from_email = os.getenv("FROM_EMAIL", "info@stinex.de")
        self.admin_email = os.getenv("ADMIN_EMAIL", "admin@stinex.de")
        
    def send_contact_notification(self, contact_data: dict) -> bool:
        """
        Send email notification when a new contact form is submitted.
        
        Args:
            contact_data: Dictionary containing contact form data
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.admin_email
            msg['Subject'] = f"Neue Kontaktanfrage von {contact_data.get('name', 'Unbekannt')}"
            
            # Email body
            body = self._create_contact_email_body(contact_data)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email (only if SMTP is configured)
            if self.smtp_user and self.smtp_password:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
                    
                logger.info(f"Contact notification email sent for {contact_data.get('name')}")
                return True
            else:
                logger.info("SMTP not configured, skipping email notification")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send contact notification email: {str(e)}")
            return False
    
    def send_confirmation_email(self, contact_data: dict) -> bool:
        """
        Send confirmation email to the customer who submitted the contact form.
        
        Args:
            contact_data: Dictionary containing contact form data
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = contact_data.get('email')
            msg['Subject'] = "Ihre Anfrage bei Stinex - Bestätigung"
            
            # Email body
            body = self._create_confirmation_email_body(contact_data)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email (only if SMTP is configured)
            if self.smtp_user and self.smtp_password:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
                    
                logger.info(f"Confirmation email sent to {contact_data.get('email')}")
                return True
            else:
                logger.info("SMTP not configured, skipping confirmation email")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {str(e)}")
            return False
    
    def _create_contact_email_body(self, contact_data: dict) -> str:
        """Create HTML email body for contact notification."""
        service = contact_data.get('service', 'Nicht angegeben')
        phone = contact_data.get('phone', 'Nicht angegeben')
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2563eb;">Neue Kontaktanfrage - Stinex</h2>
                
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1e40af;">Kontaktdaten:</h3>
                    <p><strong>Name:</strong> {contact_data.get('name', 'Nicht angegeben')}</p>
                    <p><strong>E-Mail:</strong> {contact_data.get('email', 'Nicht angegeben')}</p>
                    <p><strong>Telefon:</strong> {phone}</p>
                    <p><strong>Gewünschte Leistung:</strong> {service}</p>
                </div>
                
                <div style="background-color: #fff; border-left: 4px solid #2563eb; padding: 20px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1e40af;">Nachricht:</h3>
                    <p style="white-space: pre-wrap;">{contact_data.get('message', 'Keine Nachricht')}</p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
                    <p style="color: #64748b; font-size: 14px;">
                        Diese Anfrage wurde am {datetime.now().strftime('%d.%m.%Y um %H:%M')} über die Stinex-Website eingereicht.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_confirmation_email_body(self, contact_data: dict) -> str:
        """Create HTML email body for customer confirmation."""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2563eb;">Vielen Dank für Ihre Anfrage!</h2>
                
                <p>Liebe/r {contact_data.get('name', 'Kunde/Kundin')},</p>
                
                <p>vielen Dank für Ihr Interesse an den Reinigungsdienstleistungen von Stinex. 
                Wir haben Ihre Anfrage erhalten und werden uns innerhalb von 24 Stunden bei Ihnen melden.</p>
                
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1e40af;">Ihre Anfrage im Überblick:</h3>
                    <p><strong>Gewünschte Leistung:</strong> {contact_data.get('service', 'Nicht angegeben')}</p>
                    <p><strong>Eingereicht am:</strong> {datetime.now().strftime('%d.%m.%Y um %H:%M')}</p>
                </div>
                
                <p>Bei dringenden Fragen erreichen Sie uns unter:</p>
                <ul>
                    <li><strong>Telefon:</strong> +49 123 456 789</li>
                    <li><strong>E-Mail:</strong> info@stinex.de</li>
                    <li><strong>Notfall-Hotline:</strong> +49 123 456 000</li>
                </ul>
                
                <p>Mit freundlichen Grüßen,<br>
                Ihr Stinex-Team</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; color: #64748b; font-size: 14px;">
                    <p>Stinex Reinigungsservice<br>
                    Musterstraße 123<br>
                    20095 Hamburg<br>
                    www.stinex.de</p>
                </div>
            </div>
        </body>
        </html>
        """

# Global email service instance
email_service = EmailService()
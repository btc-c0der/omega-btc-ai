#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌌 AIXBT Divine Monitor Coverage Report Notifier
-------------------------------------------

This module handles notifications for coverage report updates.
"""

import os
import json
import logging
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
from coverage_report_utils import load_config, format_coverage_value

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('coverage_report_notifier')

class CoverageReportNotifier:
    """Handler for coverage report notifications."""
    
    def __init__(self):
        """Initialize the notifier."""
        self.config = load_config()
        if not self.config:
            raise ValueError('Failed to load configuration')
        
        self.notifications = self.config['report']['notifications']
    
    def prepare_notification_content(
        self,
        coverage_data: Dict[str, Any],
        history_data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Prepare notification content."""
        totals = coverage_data.get('totals', {})
        coverage = totals.get('percent_covered', 0)
        
        history = history_data.get('history', {})
        entries = history.get('entries', [])
        previous_coverage = entries[1].get('coverage', coverage) if entries and len(entries) > 1 else coverage
        
        change = coverage - previous_coverage
        trend = '📈' if change > 0 else '📉' if change < 0 else '➡️'
        
        title = f'🌌 AIXBT Divine Monitor Coverage Update'
        
        message = f"""
Coverage Report Update

Current Coverage: {format_coverage_value(coverage)}
Previous Coverage: {format_coverage_value(previous_coverage)}
Change: {trend} {format_coverage_value(abs(change))}

Lines Covered: {totals.get('covered_lines', 0)}/{totals.get('num_statements', 0)}
Branches Covered: {totals.get('covered_branches', 0)}/{totals.get('num_branches', 0)}
Functions Covered: {totals.get('covered_functions', 0)}/{totals.get('num_functions', 0)}

Divine Metrics:
- Harmony: {format_coverage_value(history.get('summary', {}).get('divine_alignment', 0) * 100)}
- Balance: {format_coverage_value(history.get('summary', {}).get('sacred_balance', 0) * 100)}
- Resonance: {format_coverage_value(history.get('summary', {}).get('divine_resonance', 0) * 100)}

View the full report: {self.config['report']['template']['output_dir']}/coverage_report.html
"""
        
        return {
            'title': title,
            'message': message
        }
    
    def send_slack_notification(
        self,
        content: Dict[str, str]
    ) -> bool:
        """Send notification to Slack."""
        if not self.notifications['slack']['enabled']:
            return True
        
        webhook_url = self.notifications['slack']['webhook_url']
        if not webhook_url:
            logger.error('Slack webhook URL not configured')
            return False
        
        try:
            payload = {
                'text': f"*{content['title']}*\n\n{content['message']}"
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                logger.info('Slack notification sent successfully')
                return True
            else:
                logger.error(f'Failed to send Slack notification: {response.text}')
                return False
        except Exception as e:
            logger.error(f'Error sending Slack notification: {e}')
            return False
    
    def send_email_notification(
        self,
        content: Dict[str, str]
    ) -> bool:
        """Send notification via email."""
        if not self.notifications['email']['enabled']:
            return True
        
        recipients = self.notifications['email']['recipients']
        if not recipients:
            logger.error('Email recipients not configured')
            return False
        
        try:
            msg = MIMEMultipart()
            msg['Subject'] = content['title']
            msg['From'] = os.getenv('SMTP_FROM', 'aixbt-monitor@example.com')
            msg['To'] = ', '.join(recipients)
            
            msg.attach(MIMEText(content['message'], 'plain'))
            
            smtp_host = os.getenv('SMTP_HOST', 'localhost')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_user = os.getenv('SMTP_USER')
            smtp_pass = os.getenv('SMTP_PASS')
            
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                if smtp_user and smtp_pass:
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                
                server.send_message(msg)
            
            logger.info('Email notification sent successfully')
            return True
        except Exception as e:
            logger.error(f'Error sending email notification: {e}')
            return False
    
    def send_notifications(
        self,
        coverage_data: Dict[str, Any],
        history_data: Dict[str, Any]
    ) -> bool:
        """Send all configured notifications."""
        try:
            content = self.prepare_notification_content(coverage_data, history_data)
            
            success = True
            
            if self.notifications['slack']['enabled']:
                success &= self.send_slack_notification(content)
            
            if self.notifications['email']['enabled']:
                success &= self.send_email_notification(content)
            
            return success
        except Exception as e:
            logger.error(f'Error sending notifications: {e}')
            return False

def main():
    """Main function to send coverage report notifications."""
    try:
        # Load coverage data
        with open('coverage.json', 'r') as f:
            coverage_data = json.load(f)
        
        # Load history data
        with open('coverage_history.json', 'r') as f:
            history_data = json.load(f)
        
        # Initialize notifier
        notifier = CoverageReportNotifier()
        
        # Send notifications
        if notifier.send_notifications(coverage_data, history_data):
            logger.info('Coverage report notifications sent successfully')
        else:
            logger.error('Failed to send coverage report notifications')
    except FileNotFoundError as e:
        logger.error(f'Required file not found: {e}')
    except json.JSONDecodeError as e:
        logger.error(f'Invalid JSON in data file: {e}')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')

if __name__ == '__main__':
    main() 
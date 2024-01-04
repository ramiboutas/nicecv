from utils.telegram import report_to_admin


def send_email_message(m):
    try:
        m.send(fail_silently=False)
    except Exception as e:
        report_to_admin(f"Failed to send email to {m.to}: \n\n {e}")

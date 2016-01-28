import dns.resolver
import socket
import smtplib

def verify_email(email_address, email_domain):
    # fetching MX record for target domain
    records = dns.resolver.query(email_domain, 'MX')
    mx_record = records[0].exchange
    mx_record = str(mx_record)

    # get local server hostname
    host = socket.gethostname()

    # SMTP lib setup
    server = smtplib.SMTP()
    server.set_debuglevel(1) # set to 1 for full output

    # SMTP conversation
    server.connect(mx_record)
    server.helo(host)
    server.mail('yarden.arane@gmail.com')
    code, message = server.rcpt(str(email_address))
    server.quit()

    return code


print verify_email('423045@gmail.com', 'gmail.com')

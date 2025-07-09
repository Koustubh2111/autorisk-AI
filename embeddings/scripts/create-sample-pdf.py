from fpdf import FPDF
import os

policy_text = """
Bank Security Policy

1. All failed login attempts must be logged and reviewed within 24 hours.
2. Privileged account reviews shall occur monthly.
3. Access to sensitive data must be granted based on role and business need.
4. All data transfers outside the organization must be encrypted.
5. Security incidents must be reported to the CISO within 1 hour.
6. Multifactor authentication is mandatory for all remote access.
7. Passwords must be changed every 90 days and follow complexity rules.
8. All audit logs must be retained for at least 3 years.
9. Employees must complete annual security awareness training.
10. Vulnerability scans must be performed quarterly and remediation tracked.
"""

output_path = os.path.join(os.path.dirname(__file__), "../data/sample_policy.pdf")

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Bank Security Policy Document", ln=True, align="C")
        self.ln(10)

    def chapter_body(self, text):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)
        self.ln()

pdf = PDF()
pdf.add_page()
pdf.chapter_body(policy_text)
pdf.output(output_path)

print(f"PDF created at: {output_path}")

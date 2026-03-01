from fpdf import FPDF
import os

OUTPUT_DIR = "generate_docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def sanitize_text(text: str) -> str:
    replacements = {
        "–": "-", "—": "-", "•": "-",
        "“": '"', "”": '"', "‘": "'", "’": "'",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode("latin-1", "ignore").decode("latin-1")


class ProfessionalPDF(FPDF):

    # ---------- HEADER ----------
    def header(self):
        self.set_fill_color(11, 42, 74)  # Navy
        self.rect(0, 0, 210, 20, "F")

        self.set_font("Arial", "B", 14)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "Requirement Analysis Report", 0, 1, "C")
        self.ln(5)

        self.set_text_color(0, 0, 0)

    # ---------- FOOTER ----------
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    # ---------- SECTION TITLE ----------
    def section_title(self, title):
        self.set_fill_color(230, 168, 0)  # Gold
        self.set_font("Arial", "B", 13)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, "L", True)
        self.ln(3)
        self.set_text_color(0, 0, 0)

    # ---------- BULLET LIST ----------
    def bullet(self, text):
        self.set_font("Arial", "", 11)
        self.cell(5)
        self.multi_cell(0, 7, f"- {text}")
        self.ln(1)


def generate_requirements_pdf(document_id, text, analysis):
    structured = analysis.get("structured_data", analysis)

    pdf = ProfessionalPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---------- COVER PAGE ----------
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, "Architectural Requirement Analysis", 0, 1, "C")

    pdf.set_font("Arial", "", 14)
    pdf.cell(0, 10, f"Document ID: {document_id}", 0, 1, "C")

    pdf.ln(20)
    pdf.set_font("Arial", "I", 12)
    pdf.multi_cell(0, 8,
        "This report provides a structured analysis of client requirements, "
        "identified gaps, risks, and strategic recommendations for project planning."
    )

    # ---------- EXECUTIVE SUMMARY ----------
    pdf.add_page()
    pdf.section_title("Executive Summary")

    exec_sum = structured.get("executive_summary", {})
    for key, val in exec_sum.items():
        pdf.set_font("Arial", "B", 11)
        pdf.cell(60, 8, key.replace("_", " ").title() + ":")
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, str(val))
        pdf.ln(2)

    # ---------- REQUIREMENT BREAKDOWN ----------
    pdf.section_title("Requirement Breakdown")
    breakdown = structured.get("requirement_breakdown", {})

    for section, items in breakdown.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, section.replace("_", " ").title(), 0, 1)
        for item in items:
            pdf.bullet(item)
        pdf.ln(3)

    # ---------- MISSING REQUIREMENTS ----------
    pdf.add_page()
    pdf.section_title("Missing Requirements")

    missing = structured.get("missing_requirements", {})
    for section, items in missing.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, section.replace("_", " ").title(), 0, 1)
        for item in items:
            pdf.bullet(item)
        pdf.ln(3)

    # ---------- RISK MATRIX ----------
    pdf.add_page()
    pdf.section_title("Risk Matrix")

    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(200, 200, 200)

    headers = ["Category", "Description", "Impact", "Probability"]
    widths = [35, 85, 35, 35]
    

    for i, h in enumerate(headers):
        pdf.cell(widths[i], 10, h, 1, 0, "C", True)
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    def get_row_height(texts, widths):
        """Calculate max height needed for a row."""
        max_lines = 0
        for text, w in zip(texts, widths):
            lines = pdf.multi_cell(w, 6, text, border=0, split_only=True)
            max_lines = max(max_lines, len(lines))
        return max_lines * 6


    for r in structured.get("risk_matrix", []):
        row_texts = [
        r["risk_category"],
        r["risk_description"],
        r["impact_level"],
        r["probability_estimate"]
        ]
        
        # Calculate dynamic row height
        row_height = get_row_height(row_texts, widths)

        x_start = pdf.get_x()
        y_start = pdf.get_y()
        for i, text in enumerate(row_texts):
            x_current = pdf.get_x()
            y_current = pdf.get_y()

            pdf.rect(x_current, y_current, widths[i], row_height)
            pdf.multi_cell(widths[i], 6, text)

            pdf.set_xy(x_current + widths[i], y_current)

        
        pdf.ln(row_height)



        # pdf.multi_cell(widths[0], 8, r["risk_category"], border=1, align="C")
        # x = pdf.get_x()
        # y = pdf.get_y() - 8

        # pdf.set_xy(x + widths[0], y)
        # pdf.multi_cell(widths[1], 8, r["risk_description"], border=1)

        # pdf.set_xy(x + widths[0] + widths[1], y)
        # pdf.multi_cell(widths[2], 8, r["impact_level"], border=1, align="C")

        # pdf.set_xy(x + widths[0] + widths[1] + widths[2], y)
        # pdf.multi_cell(widths[3], 8, r["probability_estimate"], border=1, align="C")

    # ---------- REFINED TEXT ----------
    pdf.add_page()
    pdf.section_title("Refined Requirements")
    refined_text = analysis.get("refine_text", text)


    safe_text = sanitize_text(refined_text)
    pdf.set_font("Arial", "", 11)

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 7, line)

    file_path = f"{OUTPUT_DIR}/document_{document_id}_premium.pdf"
    pdf.output(file_path)
    return file_path









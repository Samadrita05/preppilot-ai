from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.colors import HexColor
from io import BytesIO
from database.models import Answer

# ================= COLORS =================
PRIMARY = HexColor("#2563eb")
GRAY = HexColor("#6b7280")
BOX = HexColor("#f1f5f9")

# ================= STYLES =================
QUESTION_STYLE = ParagraphStyle(
    "QuestionStyle",
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=16,
    spaceAfter=6,
)

NORMAL_STYLE = ParagraphStyle(
    "NormalStyle",
    fontName="Helvetica",
    fontSize=11,
    leading=15,
    spaceAfter=6,
)

VERDICT_TITLE_STYLE = ParagraphStyle(
    "VerdictTitle",
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=16,
    spaceAfter=6,
)

VERDICT_TEXT_STYLE = ParagraphStyle(
    "VerdictText",
    fontName="Helvetica",
    fontSize=11,
    leading=15,
    spaceAfter=4,
)

# ================= HELPERS =================
def draw_box(pdf, x, y, w, h):
    pdf.saveState()
    pdf.setFillColor(BOX)
    pdf.roundRect(x, y - h, w, h, 12, fill=1, stroke=0)
    pdf.restoreState()

def draw_paragraph(pdf, text, x, y, max_width, style):
    p = Paragraph(text, style)
    _, h = p.wrap(max_width, 800)
    p.drawOn(pdf, x, y - h)
    return y - h - 6

# ================= MAIN =================
def generate_interview_pdf(interview, questions, overall_verdict, db):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    # ================= HEADER =================
    pdf.setFont("Helvetica-Bold", 22)
    pdf.setFillColor(PRIMARY)
    pdf.drawCentredString(width / 2, y, "PrepPilot AI – Interview Report")
    y -= 30

    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(GRAY)
    pdf.drawCentredString(
        width / 2,
        y,
        f"Role: {interview.role} | Difficulty: {interview.difficulty} | "
        f"Completed On: {interview.created_at.strftime('%d %B %Y, %I:%M %p')}",
    )
    y -= 40

    # ================= QUESTIONS =================
    for idx, q in enumerate(questions, start=1):
        if y < 240:
            pdf.showPage()
            y = height - 50

        answer = (
            db.query(Answer)
            .filter(Answer.question_id == q.id)
            .order_by(Answer.id.desc())
            .first()
        )

        content_start = y - 20
        temp_y = content_start

        temp_y = draw_paragraph(pdf, f"Q{idx}. {q.content}", 55, temp_y, width - 110, QUESTION_STYLE)
        temp_y = draw_paragraph(pdf, f"<b>Your Answer:</b> {answer.user_answer if answer else 'Not answered'}", 55, temp_y, width - 110, NORMAL_STYLE)
        temp_y = draw_paragraph(pdf, f"<b>Score:</b> {answer.score}/10" if answer and answer.score is not None else "<b>Score:</b> N/A", 55, temp_y, width - 110, NORMAL_STYLE)
        temp_y = draw_paragraph(pdf, f"<b>Feedback:</b> {answer.feedback}" if answer and answer.feedback else "<b>Feedback:</b> No feedback", 55, temp_y, width - 110, NORMAL_STYLE)

        box_height = (y - temp_y) + 25
        draw_box(pdf, 40, y, width - 80, box_height)

        temp_y = content_start
        temp_y = draw_paragraph(pdf, f"Q{idx}. {q.content}", 55, temp_y, width - 110, QUESTION_STYLE)
        temp_y = draw_paragraph(pdf, f"<b>Your Answer:</b> {answer.user_answer if answer else 'Not answered'}", 55, temp_y, width - 110, NORMAL_STYLE)
        temp_y = draw_paragraph(pdf, f"<b>Score:</b> {answer.score}/10" if answer and answer.score is not None else "<b>Score:</b> N/A", 55, temp_y, width - 110, NORMAL_STYLE)
        draw_paragraph(pdf, f"<b>Feedback:</b> {answer.feedback}" if answer and answer.feedback else "<b>Feedback:</b> No feedback", 55, temp_y, width - 110, NORMAL_STYLE)

        y -= box_height + 25

    # ================= OVERALL VERDICT =================
    pdf.showPage()
    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColor(PRIMARY)
    pdf.drawString(50, y, "Overall AI Verdict")
    y -= 25

    text = (overall_verdict or "").replace("**", "").strip()

    sections = []
    def split_section(label, src):
        if label in src:
            before, after = src.split(label, 1)
            return before.strip(), after
        return src.strip(), ""

    overall, rest = split_section("Strengths:", text)
    strengths, rest = split_section("Weaknesses:", rest)
    weaknesses, final = split_section("Final Verdict:", rest)

    sections.append(("Overall Performance", overall))
    sections.append(("Strengths", strengths))
    sections.append(("Weaknesses", weaknesses))
    sections.append(("Final Verdict", final))

    content_start = y
    temp_y = content_start

    for title, body in sections:
        temp_y = draw_paragraph(pdf, title, 65, temp_y, width - 130, VERDICT_TITLE_STYLE)
        for line in body.split("\n"):
            if line.strip():
                temp_y = draw_paragraph(pdf, f"- {line.strip()}", 75, temp_y, width - 150, VERDICT_TEXT_STYLE)

    box_height = (y - temp_y) + 25
    draw_box(pdf, 50, y, width - 100, box_height)

    temp_y = content_start
    for title, body in sections:
        temp_y = draw_paragraph(pdf, title, 65, temp_y, width - 130, VERDICT_TITLE_STYLE)
        for line in body.split("\n"):
            if line.strip():
                temp_y = draw_paragraph(pdf, f"- {line.strip()}", 75, temp_y, width - 150, VERDICT_TEXT_STYLE)

    pdf.save()
    buffer.seek(0)
    return buffer

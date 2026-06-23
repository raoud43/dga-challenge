import io
from docx import Document

def extract_text_and_tables_from_docx(file_bytes: bytes) -> str:
    """
    Reads the docx file directly from memory, extracts text, and converts tables
    into Markdown format so that the DeepSeek model can understand them accurately.
    """
    # Open the file in memory using io.BytesIO
    doc = Document(io.BytesIO(file_bytes))
    content = []

    # 1. Extract regular text from paragraphs
    content.append("=== Text Document Content ===")
    for para in doc.paragraphs:
        if para.text.strip():
            content.append(para.text.strip())

    # 2. Extract tables and convert them to Markdown
    if doc.tables:
        content.append("\n=== Attached Tables in the Document (Markdown Format) ===")
        for i, table in enumerate(doc.tables):
            content.append(f"\n[Table No. {i+1}]")
            
            for row_idx, row in enumerate(table.rows):
                # Clean the text inside each cell
                row_data = [cell.text.strip().replace("\n", " ") for cell in row.cells]
                
                # Build the Markdown row
                markdown_row = "| " + " | ".join(row_data) + " |"
                content.append(markdown_row)
                
                # Add a separator line after the first header row
                if row_idx == 0:
                    separator = "|" + "|".join(["---"] * len(row.cells)) + "|"
                    content.append(separator)

    return "\n".join(content)
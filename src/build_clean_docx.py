import re
import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_border(cell, **kwargs):
    """
    Set cell borders for academic 3-line table style:
    kwargs: top, bottom, left, right
    values: dict(sz=12, val='single', color='000000')
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'<w:tcBorders {}/>'.format(nsdecls('w')))
    for border_name in ['top', 'left', 'bottom', 'right']:
        if border_name in kwargs:
            b_el = parse_xml(f'<w:{border_name} {nsdecls("w")} w:val="{kwargs[border_name].get("val", "single")}" w:sz="{kwargs[border_name].get("sz", 4)}" w:space="0" w:color="{kwargs[border_name].get("color", "000000")}"/>')
            tcBorders.append(b_el)
        else:
            b_el = parse_xml(f'<w:{border_name} {nsdecls("w")} w:val="none"/>')
            tcBorders.append(b_el)
    tcPr.append(tcBorders)

def build_professional_docx():
    doc = docx.Document()
    
    # Page setup - Standard A4 with professional 2.5 cm margins
    for sec in doc.sections:
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        sec.top_margin = Inches(0.98) # 2.5 cm
        sec.bottom_margin = Inches(0.98)
        sec.left_margin = Inches(0.98)
        sec.right_margin = Inches(0.98)
        
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(0, 0, 0)
    
    # 1. Judul Utama
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(8)
    p_title.paragraph_format.line_spacing = 1.15
    r_t = p_title.add_run("Kerangka Benchmark Simulasi Non-Sirkular untuk Pemeringkatan Risiko Kepatuhan Pajak Pedagang Daring melalui Integrasi Data Transaksi Gerbang Pembayaran, Logistik, dan Indikator Regional Berbasis Data BPS")
    r_t.bold = True
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(14)
    
    # Judul Inggris
    p_etitle = doc.add_paragraph()
    p_etitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_etitle.paragraph_format.space_after = Pt(14)
    r_et = p_etitle.add_run("(A Non-Circular Synthetic Simulation Benchmark for E-Commerce Merchant Tax Compliance Risk Ranking Integrating Digital Payment Gateway, Logistics, and BPS Regional Indicators)")
    r_et.italic = True
    r_et.font.name = 'Times New Roman'
    r_et.font.size = Pt(11)
    
    # Penulis
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(3)
    r1 = p_auth.add_run("Izam Rosiawan")
    r1.bold = True
    r1.font.size = Pt(11)
    r1_sup = p_auth.add_run("1*")
    r1_sup.font.superscript = True
    p_auth.add_run(", ")
    r2 = p_auth.add_run("Sulthan")
    r2.bold = True
    r2.font.size = Pt(11)
    r2_sup = p_auth.add_run("2")
    r2_sup.font.superscript = True
    
    # Afiliasi
    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_after = Pt(2)
    p_aff.paragraph_format.line_spacing = 1.05
    r_aff1 = p_aff.add_run("1Program Studi Sains Data, Fakultas Informatika, Telkom University Kampus Surabaya, Indonesia\n")
    r_aff1.font.size = Pt(9.5)
    r_aff2 = p_aff.add_run("2Direktorat Kampus Surabaya, Telkom University Kampus Surabaya, Indonesia\n")
    r_aff2.font.size = Pt(9.5)
    r_aff3 = p_aff.add_run("*Korespondensi: izamrosiawan@student.telkomuniversity.ac.id")
    r_aff3.font.size = Pt(9.0)
    r_aff3.italic = True
    p_aff.paragraph_format.space_after = Pt(12)
    
    # Garis Pembatas Abstrak
    p_line1 = doc.add_paragraph()
    p_line1.paragraph_format.space_after = Pt(6)
    p_border1 = parse_xml(r'<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:bottom w:val="single" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>')
    p_line1._p.get_or_add_pPr().append(p_border1)
    
    # Baca paper.md
    with open("paper.md", "r", encoding="utf-8") as f:
        md_content = f.read()

    # Abstrak Indo
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.space_after = Pt(4)
    p_abs.paragraph_format.line_spacing = 1.0
    r_h_id = p_abs.add_run("ABSTRAK — ")
    r_h_id.bold = True
    r_h_id.font.size = Pt(9.5)
    
    m_abs_id = re.search(r'### ABSTRAK\s*\n(.*?)\n\s*\*\*Kata Kunci:\*\*\s*(.*?)\n', md_content, re.DOTALL)
    abs_id_txt = m_abs_id.group(1).strip() if m_abs_id else ""
    kw_id_txt = m_abs_id.group(2).strip() if m_abs_id else ""
    
    r_body_id = p_abs.add_run(abs_id_txt)
    r_body_id.font.size = Pt(9.5)
    
    p_kw_id = doc.add_paragraph()
    p_kw_id.paragraph_format.space_after = Pt(10)
    r_kwt_id = p_kw_id.add_run("Kata Kunci: ")
    r_kwt_id.bold = True
    r_kwt_id.font.size = Pt(9.5)
    r_kw_body_id = p_kw_id.add_run(kw_id_txt)
    r_kw_body_id.italic = True
    r_kw_body_id.font.size = Pt(9.5)
    
    # Abstrak Inggris
    p_eabs = doc.add_paragraph()
    p_eabs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_eabs.paragraph_format.space_after = Pt(4)
    p_eabs.paragraph_format.line_spacing = 1.0
    r_h_en = p_eabs.add_run("ABSTRACT — ")
    r_h_en.bold = True
    r_h_en.font.size = Pt(9.5)
    
    m_abs_en = re.search(r'### ABSTRACT\s*\n\*(.*?)\*\n\s*\*\*Keywords:\*\*\s*(.*?)\n', md_content, re.DOTALL)
    abs_en_txt = m_abs_en.group(1).strip() if m_abs_en else ""
    kw_en_txt = m_abs_en.group(2).strip() if m_abs_en else ""
    
    r_body_en = p_eabs.add_run(abs_en_txt)
    r_body_en.italic = True
    r_body_en.font.size = Pt(9.5)
    
    p_kw_en = doc.add_paragraph()
    p_kw_en.paragraph_format.space_after = Pt(8)
    r_kwt_en = p_kw_en.add_run("Keywords: ")
    r_kwt_en.bold = True
    r_kwt_en.font.size = Pt(9.5)
    r_kw_body_en = p_kw_en.add_run(kw_en_txt)
    r_kw_body_en.italic = True
    r_kw_body_en.font.size = Pt(9.5)
    
    # Garis Pembatas Bawah Abstrak
    p_line2 = doc.add_paragraph()
    p_line2.paragraph_format.space_after = Pt(14)
    p_border2 = parse_xml(r'<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:bottom w:val="single" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>')
    p_line2._p.get_or_add_pPr().append(p_border2)

    # Parsing Body
    body_start = md_content.find("## 1. PENDAHULUAN")
    body_text = md_content[body_start:]
    lines = body_text.split("\n")
    
    table_lines = []
    
    def render_academic_table(tbl_lines):
        if len(tbl_lines) < 2:
            return
        rows_data = []
        for l in tbl_lines:
            if re.match(r'^\s*\|?\s*:?---', l):
                continue
            cells = [c.strip() for c in l.strip().strip('|').split('|')]
            if any(cells):
                rows_data.append(cells)
        if not rows_data:
            return
        
        cols = max(len(r) for r in rows_data)
        tbl = doc.add_table(rows=len(rows_data), cols=cols)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = True
        
        # 3-Line Academic Table (APA / IEEE format)
        for i, row in enumerate(rows_data):
            for j, cell_text in enumerate(row):
                if j >= cols:
                    continue
                cell = tbl.cell(i, j)
                cell.text = cell_text
                
                # Format text
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.0
                    for r in p.runs:
                        r.font.name = 'Times New Roman'
                        r.font.size = Pt(8.5)
                        if i == 0:
                            r.bold = True
                
                # Borders
                if i == 0:
                    set_cell_border(cell, top={'sz': 12, 'val': 'single'}, bottom={'sz': 6, 'val': 'single'})
                    shd = parse_xml(r'<w:shd {} w:fill="F5F5F5"/>'.format(nsdecls('w')))
                    cell._tc.get_or_add_tcPr().append(shd)
                elif i == len(rows_data) - 1:
                    set_cell_border(cell, bottom={'sz': 12, 'val': 'single'})
                else:
                    set_cell_border(cell)
                    
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(6)

    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        
        # Table collector
        if line.startswith("|") and line.endswith("|"):
            table_lines.append(line)
            idx += 1
            continue
        elif table_lines:
            render_academic_table(table_lines)
            table_lines = []
            
        if not line:
            idx += 1
            continue
            
        # Section 1
        if line.startswith("## "):
            h_text = line[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.bold = True
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
        # Section 2
        elif line.startswith("### "):
            h_text = line[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.bold = True
            r.italic = True
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)
        # Gambar
        elif line.startswith("!["):
            m_img = re.search(r'!\[(.*?)\]\((.*?)\)', line)
            if m_img:
                img_path = m_img.group(2).lstrip('/')
                if os.path.exists(img_path):
                    p_img = doc.add_paragraph()
                    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_img.paragraph_format.space_before = Pt(8)
                    p_img.paragraph_format.space_after = Pt(2)
                    r_img = p_img.add_run()
                    r_img.add_picture(img_path, width=Inches(5.6))
        # Caption Gambar
        elif line.startswith("*Gambar ") or line.startswith("Gambar "):
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            clean_cap = line.strip('*')
            r_cap = p_cap.add_run(clean_cap)
            r_cap.font.size = Pt(9.0)
            r_cap.italic = True
        # Caption Tabel
        elif line.startswith("**Tabel ") or line.startswith("Tabel "):
            p_tcap = doc.add_paragraph()
            p_tcap.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_tcap.paragraph_format.space_before = Pt(8)
            p_tcap.paragraph_format.space_after = Pt(2)
            clean_tcap = line.strip('*')
            r_tcap = p_tcap.add_run(clean_tcap)
            r_tcap.bold = True
            r_tcap.font.size = Pt(9.5)
        # Reference items
        elif line.startswith("* "):
            p_ref = doc.add_paragraph()
            p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_ref.paragraph_format.left_indent = Inches(0.3)
            p_ref.paragraph_format.first_line_indent = Inches(-0.3)
            p_ref.paragraph_format.space_after = Pt(4)
            p_ref.paragraph_format.line_spacing = 1.05
            r_ref = p_ref.add_run(line[2:].strip())
            r_ref.font.size = Pt(9.5)
        # Lists (a., b., c., etc.)
        elif re.match(r'^[a-d]\.\s', line) or re.match(r'^\d\.\s', line):
            p_li = doc.add_paragraph()
            p_li.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_li.paragraph_format.left_indent = Inches(0.25)
            p_li.paragraph_format.space_after = Pt(3)
            p_li.paragraph_format.line_spacing = 1.15
            clean_li = line.replace("$$", "").replace("$", "")
            r_li = p_li.add_run(clean_li)
            r_li.font.size = Pt(10.5)
        # Diagram box (Verbatim)
        elif line.startswith("```"):
            code_lines = []
            idx += 1
            while idx < len(lines) and not lines[idx].strip().startswith("```"):
                code_lines.append(lines[idx])
                idx += 1
            p_code = doc.add_paragraph()
            p_code.paragraph_format.left_indent = Inches(0.25)
            p_code.paragraph_format.space_before = Pt(4)
            p_code.paragraph_format.space_after = Pt(6)
            r_code = p_code.add_run("\n".join(code_lines))
            r_code.font.name = 'Consolas'
            r_code.font.size = Pt(8.0)
        # Paragraf Biasa
        else:
            p_p = doc.add_paragraph()
            p_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_p.paragraph_format.first_line_indent = Inches(0.35)
            p_p.paragraph_format.space_after = Pt(5)
            p_p.paragraph_format.line_spacing = 1.15
            clean_p = line.replace("$$", "").replace("$", "")
            r_p = p_p.add_run(clean_p)
            r_p.font.size = Pt(10.5)
            
        idx += 1
        
    if table_lines:
        render_academic_table(table_lines)
        
    out_file = "tax_compliance_manuscript_clean.docx"
    doc.save(out_file)
    print(f"Professional clean DOCX created at: {out_file}")

if __name__ == "__main__":
    build_professional_docx()

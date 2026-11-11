from io import BytesIO
import csv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def csv_bytes(rows):
    out=BytesIO(); text=__import__('io').StringIO(); w=csv.DictWriter(text,fieldnames=list(rows[0].keys()) if rows else ["timestamp","visitors"]); w.writeheader(); w.writerows(rows); return text.getvalue().encode('utf-8')

def pdf_summary(site_name, summary, source_label):
    out=BytesIO(); doc=SimpleDocTemplate(out,pagesize=A4); styles=getSampleStyleSheet(); story=[Paragraph("TrafficIQ — Traffic Analysis Report",styles['Title']),Spacer(1,12),Paragraph(f"Site: {site_name}",styles['Normal']),Paragraph(f"Data source: {source_label}",styles['Normal']),Spacer(1,16)]
    if not summary.get('available'): story.append(Paragraph(summary.get('reason','No results available.'),styles['BodyText']))
    else:
        rows=[["Metric","Calculated value"],["Observations",str(summary['observations'])],["Total visitors",str(summary['total_visitors'])],["Average visitors per observation",f"{summary['average_visitors']:.3f}"],["Peak traffic",str(summary['peak_traffic'])],["Lowest traffic",str(summary['lowest_traffic'])],["Growth (%)",str(summary['growth_percent']) if summary['growth_percent'] is not None else "N/A"]]
        table=Table(rows,hAlign='LEFT'); table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#26364a')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.4,colors.grey),('PADDING',(0,0),(-1,-1),7)])); story.append(table)
    story += [Spacer(1,18),Paragraph("Interpretation and limitations",styles['Heading2']),Paragraph("This report contains calculations derived from observations stored in TrafficIQ. Forecasts and anomaly indicators are estimates and should be interpreted with the stated model assumptions. No infrastructure resource estimate is implied.",styles['BodyText'])]
    doc.build(story); return out.getvalue()

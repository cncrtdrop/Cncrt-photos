"""Remise en forme complète de Inventaire.xlsx (CNCRT DROP).

Usage : python3 inventaire.py source.xlsx destination.xlsx
À lancer après CHAQUE modification de l'Excel (ajout de ligne, vente, nouvelle marque...) :
- normalise les marques et les statuts,
- trie les lignes par réf (001, 002, ... 130bis ..., puis H001... = ventes historiques),
- applique la même mise en forme à toutes les lignes (€, dates, centrage, liens),
- remet les formules (Marge, Jours en ligne),
- reconstruit le Tableau de bord avec TOUTES les marques présentes et le détail par mois.
"""
import sys, re, datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

DARK = "2B2B2B"; PINK = "E8578C"; GREY = "808080"
EUR = '#,##0.00 €'; DATE = 'DD/MM/YYYY'
HEAD = ['Réf', 'Article', 'Marque', 'Catégorie', 'Taille', 'État', "Prix d'achat", 'Prix affiché',
        'Prix de vente', 'Marge', 'Statut', 'Mis en ligne le', 'Jours en ligne', 'Vendu le', 'Vues',
        'Favoris', 'Republications', 'Dernière action', 'Lien Vinted', 'Dossier photos', 'Notes']
WIDTH = [8, 46, 18, 26, 12, 16, 11, 11, 11, 10, 13, 13, 11, 12, 8, 9, 13, 26, 14, 40, 40]
STATUTS = ['En ligne', 'Pas en ligne', 'À republier', 'Réservé', 'Vendu', 'Retiré']
N = 2000  # lignes couvertes par les formules

BRANDS = {
    'helas': 'Hélas', 'hélas': 'Hélas', 'adidas': 'Adidas', 'guess': 'Guess', 'boss': 'Hugo Boss',
    'hugo boss': 'Hugo Boss', "levi's": "Levi's", 'levis': "Levi's", "levi’s": "Levi's",
    'quicksilver': 'Quiksilver', 'quiksilver': 'Quiksilver', 'stussy': 'Stüssy', 'stüssy': 'Stüssy',
    'wrung': 'Wrüng', 'wrüng': 'Wrüng', 'majenta': 'Magenta', 'magenta': 'Magenta', 'th': 'Tommy Hilfiger',
    'tommy hilfiger': 'Tommy Hilfiger', 'blench': 'Bench', 'bench': 'Bench',
    'baptiste million': 'Batiste Million', 'batiste million': 'Batiste Million',
    'cuir et peaux paris': 'Cuirs et Peaux', 'cuirs et peaux': 'Cuirs et Peaux', 'dgk': 'DGK', 'lsa': 'LSA',
    'nba': 'NBA', 'reebok nba': 'Reebok', 'nike patta': 'Nike x Patta', 'nike x patta': 'Nike x Patta',
    'patta umbro': 'Patta x Umbro', 'patta x umbro': 'Patta x Umbro', 'pasdemer': 'Pas de Mer',
    'pas de mer': 'Pas de Mer', 'wearaloud': 'Wear A Loud', 'wear a loud': 'Wear A Loud',
    'ecko unltd.': 'Ecko Unltd', 'ecko unltd': 'Ecko Unltd', 'élément': 'Element', 'element': 'Element',
    'ünküt': 'Ünkut', 'unkut': 'Ünkut', 'ünkut': 'Ünkut', 'diamond supply co': 'Diamond Supply Co.',
    'diamond supply co.': 'Diamond Supply Co.', 'marlboro classic': 'Marlboro Classics',
    'marlboro classics': 'Marlboro Classics', 'motorhead': 'Motörhead', 'motörhead': 'Motörhead',
    'none': 'Sans marque', '': 'Sans marque', 'sans marque': 'Sans marque', 'new era': 'New Era',
    'le coq sportif': 'Le Coq Sportif', 'petrol industries': 'Petrol Industries', 'columbia': 'Columbia',
    'united colors of benetton': 'Benetton', 'fila': 'Fila', 'fleurs de bagne': 'Fleurs de Bagne', 'nike x patta ': 'Nike x Patta', 'benetton': 'Benetton', 'wanabee': 'Wanabee',
}


def norm_brand(b):
    k = str(b or '').strip()
    return BRANDS.get(k.lower(), k[:1].upper() + k[1:] if k else 'Sans marque')


def norm_status(s):
    s = str(s or '').strip()
    for x in STATUTS:
        if s.lower() == x.lower():
            return x
    if s.lower() in ('a republier', 'à republier'):
        return 'À republier'
    return s or 'Pas en ligne'


def ref_key(r):
    r = str(r)
    m = re.match(r'^([A-Za-z]*)(\d+)(.*)$', r)
    if not m:
        return (2, 0, r)
    return (1 if m.group(1) else 0, int(m.group(2)), m.group(3))


def to_date(v):
    if isinstance(v, datetime.datetime):
        return v.replace(hour=0, minute=0, second=0, microsecond=0)
    if isinstance(v, datetime.date):
        return datetime.datetime(v.year, v.month, v.day)
    if isinstance(v, str):
        for f in ('%Y-%m-%d', '%d/%m/%Y'):
            try:
                return datetime.datetime.strptime(v.strip()[:10], f)
            except ValueError:
                pass
    return v


def to_num(v):
    if v in (None, ''):
        return None
    if isinstance(v, (int, float)):
        return v
    try:
        return float(str(v).replace('€', '').replace(',', '.').strip())
    except ValueError:
        return v


def read_rows(ws):
    rows = []
    for row in ws.iter_rows(min_row=2, max_col=21):
        v = [c.value for c in row]
        if v[0] in (None, '') and v[1] in (None, ''):
            continue
        link = row[18].hyperlink.target if row[18].hyperlink else (
            v[18] if isinstance(v[18], str) and v[18].startswith('http') else None)
        v[18] = link
        rows.append(v)
    return rows


def clean(v):
    v = list(v) + [None] * (21 - len(v))
    v[0] = str(v[0]).strip()
    v[2] = norm_brand(v[2])
    for i in (6, 7, 8):
        v[i] = to_num(v[i])
    v[10] = norm_status(v[10])
    for i in (11, 13):
        v[i] = to_date(v[i])
    for i in (14, 15, 16):
        v[i] = to_num(v[i])
    if isinstance(v[19], str):
        v[19] = v[19].replace('/', '\\')
    return v


thin = Side(style='thin', color='D9D9D9')
BORDER = Border(bottom=thin)


def write_inventaire(wb, rows):
    ws = wb.create_sheet('Inventaire')
    for c, h in enumerate(HEAD, 1):
        x = ws.cell(1, c, h)
        x.font = Font(bold=True, color='FFFFFF'); x.fill = PatternFill('solid', fgColor=DARK)
        x.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 32
    for i, w in enumerate(WIDTH, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    center = Alignment(horizontal='center', vertical='center')
    left = Alignment(horizontal='left', vertical='center')
    for r, v in enumerate(rows, 2):
        vals = v[:]
        vals[9] = f'=IF(AND(G{r}<>"",I{r}<>""),I{r}-G{r},"")'
        vals[12] = f'=IF(AND(K{r}="En ligne",L{r}<>""),TODAY()-L{r},"")'
        link = vals[18]
        vals[18] = "Voir l'annonce" if link else None
        for c, val in enumerate(vals, 1):
            x = ws.cell(r, c, val)
            x.font = Font(name='Calibri', size=11)
            x.border = BORDER
            x.alignment = left if c in (2, 3, 4, 18, 20, 21) else center
            if c in (7, 8, 9, 10):
                x.number_format = EUR
            elif c in (12, 14):
                x.number_format = DATE
            elif c == 1:
                x.number_format = '@'
        if link:
            x = ws.cell(r, 19)
            x.hyperlink = link
            x.font = Font(name='Calibri', size=11, color='0563C1', underline='single')
    last = max(2, len(rows) + 1)
    ws.freeze_panes = 'C2'
    ws.auto_filter.ref = f'A1:U{last}'
    dv = DataValidation(type='list', formula1='"' + ','.join(STATUTS) + '"', allow_blank=True)
    ws.add_data_validation(dv); dv.add(f'K2:K{N}')
    for val, col in (('En ligne', 'D9EAD3'), ('Vendu', 'E7E6E6'), ('Pas en ligne', 'FFF2CC'),
                     ('À republier', 'FCE5CD'), ('Réservé', 'CFE2F3'), ('Retiré', 'F4CCCC')):
        ws.conditional_formatting.add(f'K2:K{N}', CellIsRule(operator='equal', formula=[f'"{val}"'],
                                                              fill=PatternFill('solid', fgColor=col)))
    ws.conditional_formatting.add(f'J2:J{N}', CellIsRule(operator='lessThan', formula=['0'],
                                                          font=Font(color='C00000')))
    return ws


def write_dashboard(wb, rows):
    d = wb.create_sheet('Tableau de bord', 0)
    for col, w in zip('ABCDEFGHI', (3, 42, 13, 13, 14, 13, 12, 12, 12)):
        d.column_dimensions[col].width = w
    d['B2'] = 'CNCRT DROP — Tableau de bord'; d['B2'].font = Font(bold=True, size=18, color=DARK)
    d['B3'] = ("Calculé à partir de l'onglet Inventaire (toutes les lignes). Marges : uniquement les "
               "articles dont le prix d'achat est connu.")
    d['B3'].font = Font(italic=True, color=GREY)
    I = lambda c: f'Inventaire!{c}2:{c}{N}'
    kpi = [
        ('Articles au total', f'=COUNTA({I("A")})', None),
        ('En ligne sur Vinted', f'=COUNTIF({I("K")},"En ligne")', None),
        ('À republier (en stock)', f'=COUNTIF({I("K")},"À republier")', None),
        ('Pas encore en ligne', f'=COUNTIF({I("K")},"Pas en ligne")', None),
        ('Vendus', f'=COUNTIF({I("K")},"Vendu")', None),
        ("Chiffre d'affaires total", f'=SUMIF({I("K")},"Vendu",{I("I")})', EUR),
        ("Chiffre d'affaires des 30 derniers jours",
         f'=SUMIFS({I("I")},{I("K")},"Vendu",{I("N")},">="&(TODAY()-30))', EUR),
        ('Marge totale (prix d\'achat connu)', f'=SUM({I("J")})', EUR),
        ('Marge moyenne par vente', f'=IFERROR(AVERAGE({I("J")}),0)', EUR),
        ("Ventes sans prix d'achat (marge inconnue)",
         f'=COUNTIFS({I("K")},"Vendu",{I("G")},"")', None),
        ('Délai moyen de vente (jours)',
         f'=IFERROR(SUMPRODUCT(({I("K")}="Vendu")*ISNUMBER({I("L")})*ISNUMBER({I("N")})*({I("N")}-{I("L")}))'
         f'/SUMPRODUCT(({I("K")}="Vendu")*ISNUMBER({I("L")})*ISNUMBER({I("N")})),"")', '0.0'),
        ('Coût du stock non vendu', f'=SUMIF({I("K")},"<>Vendu",{I("G")})', EUR),
        ('Valeur affichée du stock en ligne', f'=SUMIF({I("K")},"En ligne",{I("H")})', EUR),
        ('Annonces en ligne depuis 21 j ou plus', f'=COUNTIFS({I("K")},"En ligne",{I("M")},">=21")', None),
        ('Annonces avec 5 favoris ou plus', f'=COUNTIFS({I("K")},"En ligne",{I("P")},">=5")', None),
    ]
    r = 5
    for lab, f, fmt in kpi:
        a, b = d.cell(r, 2, lab), d.cell(r, 3, f)
        a.font = Font(size=11, color=DARK); a.border = BORDER
        b.font = Font(bold=True, size=12, color=PINK if fmt == EUR else DARK)
        b.alignment = Alignment(horizontal='right'); b.border = BORDER
        if fmt:
            b.number_format = fmt
        r += 1

    def header(row, labels):
        for i, h in enumerate(labels):
            x = d.cell(row, 2 + i, h)
            x.font = Font(bold=True, color='FFFFFF'); x.fill = PatternFill('solid', fgColor=DARK)
            x.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        d.row_dimensions[row].height = 30

    # Par mois
    r += 1
    d.cell(r, 2, 'Ventes par mois').font = Font(bold=True, size=13, color=DARK); r += 1
    header(r, ['Mois', 'Ventes', "Chiffre d'affaires", 'Marge']); r += 1
    dates = [v[13] for v in rows if v[10] == 'Vendu' and isinstance(v[13], datetime.datetime)]
    today = datetime.datetime.now()
    start = min(dates) if dates else today
    y, m = start.year, start.month
    months = []
    while (y, m) <= (today.year, today.month):
        months.append((y, m)); m += 1
        if m == 13:
            y, m = y + 1, 1
    noms = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
    sold_months = {(x.year, x.month) for x in dates}
    months = [ym for ym in months if ym in sold_months or ym >= (today.year, today.month)]
    for (y, m) in reversed(months):
        d1 = f'DATE({y},{m},1)'; d2 = f'DATE({y + (m == 12)},{m % 12 + 1},1)'
        cond = f'{I("K")},"Vendu",{I("N")},">="&{d1},{I("N")},"<"&{d2}'
        vals = [f'{noms[m - 1]} {y}', f'=COUNTIFS({cond})', f'=SUMIFS({I("I")},{cond})', f'=SUMIFS({I("J")},{cond})']
        for i, val in enumerate(vals):
            x = d.cell(r, 2 + i, val); x.border = BORDER
            x.alignment = Alignment(horizontal='left' if i == 0 else 'center')
            if i >= 2:
                x.number_format = EUR
        r += 1
    x = d.cell(r, 2, 'Vente sans date connue'); x.font = Font(italic=True, color=GREY)
    d.cell(r, 3, f'=COUNTIFS({I("K")},"Vendu",{I("N")},"")').alignment = Alignment(horizontal='center')
    r += 2

    # Par marque
    d.cell(r, 2, 'Par marque (toutes les marques, classées par chiffre d\'affaires)').font = Font(bold=True, size=13, color=DARK)
    r += 1
    header(r, ['Marque', 'Articles', 'Vendus', "Chiffre d'affaires", 'Marge totale', 'Marge moy.', 'En ligne', 'Taux de vente'])
    r += 1
    stats = {}
    for v in rows:
        s = stats.setdefault(v[2], [0, 0.0])
        if v[10] == 'Vendu':
            s[0] += 1; s[1] += float(v[8] or 0)
    for b in sorted(stats, key=lambda b: (-stats[b][1], -stats[b][0], b.lower())):
        B = f'$B{r}'
        vals = [b, f'=COUNTIF({I("C")},{B})', f'=COUNTIFS({I("C")},{B},{I("K")},"Vendu")',
                f'=SUMIFS({I("I")},{I("C")},{B},{I("K")},"Vendu")', f'=SUMIFS({I("J")},{I("C")},{B})',
                f'=IFERROR(AVERAGEIFS({I("J")},{I("C")},{B}),"")', f'=COUNTIFS({I("C")},{B},{I("K")},"En ligne")',
                f'=IFERROR(D{r}/C{r},"")']
        for i, val in enumerate(vals):
            x = d.cell(r, 2 + i, val); x.border = BORDER
            x.alignment = Alignment(horizontal='left' if i == 0 else 'center')
            if i in (3, 4, 5):
                x.number_format = EUR
            if i == 7:
                x.number_format = '0%'
        r += 1
    d.freeze_panes = 'A5'
    return d


def write_copy(wb, src_ws, title, date_cols=(), widths=None):
    ws = wb.create_sheet(title)
    for row in src_ws.iter_rows(values_only=True):
        if all(c in (None, '') for c in row):
            continue
        ws.append(list(row))
    for c in ws[1]:
        c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor=DARK)
        c.alignment = Alignment(horizontal='center', vertical='center')
    for col in date_cols:
        for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
            for c in row:
                c.value = to_date(c.value)
                c.number_format = DATE
                c.alignment = Alignment(horizontal='center')
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = 'A2'
    return ws


def rebuild_from_rows(rows, src_wb, dst):
    rows = sorted((clean(v) for v in rows), key=lambda v: ref_key(v[0]))
    wb = openpyxl.Workbook(); wb.remove(wb.active)
    write_inventaire(wb, rows)
    write_dashboard(wb, rows)
    if 'Règles' in src_wb.sheetnames:
        write_copy(wb, src_wb['Règles'], 'Règles', widths=(45, 90))
    if 'Journal' in src_wb.sheetnames:
        write_copy(wb, src_wb['Journal'], 'Journal', date_cols=(1,), widths=(12, 8, 20, 100))
    wb.active = 0
    wb.save(dst)
    return rows


def rebuild(src, dst):
    swb = openpyxl.load_workbook(src)
    return rebuild_from_rows(read_rows(swb['Inventaire']), swb, dst)


if __name__ == '__main__':
    rebuild(sys.argv[1], sys.argv[2])

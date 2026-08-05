# -*- coding: utf-8 -*-
import json, re, base64, os, html as _html
import markdown

REPO=os.path.dirname(os.path.abspath(__file__))
NB=REPO+'/notebook/MA336_Project_Notebook.ipynb'
FIGDIR=REPO+'/figures'
OUT=REPO+'/report/report.html'

def b64(path):
    return base64.b64encode(open(path,'rb').read()).decode()
def font_face(family,path,weight='400',style='normal'):
    return (f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};"
            f"font-display:swap;src:url(data:font/ttf;base64,{b64(path)}) format('truetype');}}")

FONTS=""
FONTS+=font_face('Lora','/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf','400 700','normal')
FONTS+=font_face('Lora','/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf','400 700','italic')
FONTS+=font_face('LatoDoc','/usr/share/fonts/truetype/lato/Lato-Regular.ttf','400','normal')
FONTS+=font_face('LatoDoc','/usr/share/fonts/truetype/lato/Lato-Italic.ttf','400','italic')
FONTS+=font_face('LatoDoc','/usr/share/fonts/truetype/lato/Lato-Bold.ttf','700','normal')
FONTS+=font_face('LatoDoc','/usr/share/fonts/truetype/lato/Lato-Light.ttf','300','normal')

GRAIN_SVG=("<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'>"
           "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/>"
           "<feColorMatrix type='saturate' values='0'/></filter>"
           "<rect width='100%' height='100%' filter='url(%23n)'/></svg>")
GRAIN=base64.b64encode(GRAIN_SVG.encode()).decode()

CAP={
 'fig01_attitude-correlation-heatmap.png':"The six attitudinal scales are only loosely correlated, so no single item captures the space.",
 'fig02_pca-scree-plot.png':"Two principal components retain roughly three-quarters of the attitudinal variance.",
 'fig03_pca-biplot.png':"The two retained components read as left–right (PC1) and authoritarian–libertarian (PC2).",
 'fig04_silhouette-analysis.png':"Silhouette scores across candidate k; k=3 is adopted on substantive grounds.",
 'fig05_kmeans-clusters-k3-scatter.png':"K-means on the two-component space separates the electorate into three attitudinal clusters.",
 'fig06_autoencoder-vs-pca-embedding.png':"A tanh autoencoder recovers essentially the same three-part structure as PCA.",
 'fig10_linear-autoencoder-embedding.png':"A from-scratch linear-bottleneck autoencoder reproduces the PCA geometry.",
 'fig07_hierarchical-dendrogram.png':"Ward-linkage hierarchical clustering independently returns three groups.",
 'fig11_education-by-cluster.png':"Formal education tracks the divide: the authoritarian-left cluster is the least qualified.",
 'fig08_decision-tree-confusion-roc.png':"A supervised decision tree separates Reform voters with moderate accuracy (AUC ≈ 0.73).",
 'fig09_decision-tree-diagram.png':"The top of the tuned decision tree, showing its principal splits.",
}

md=markdown.Markdown(extensions=['extra','sane_lists','smarty'])
def render(src):
    md.reset(); return md.convert(src)

def render_outputs(cell):
    """Reinstate a code cell's stored TABLE and computed-output blocks (code stays hidden)."""
    parts=[]
    for o in cell.get('outputs',[]):
        ot=o.get('output_type')
        if ot in ('execute_result','display_data'):
            data=o.get('data',{})
            if 'text/html' in data:                       # a dataframe table
                tbl="".join(data['text/html'])
                tbl=re.sub(r'border="\d+"','',tbl)
                tbl=re.sub(r'>(-?\d+\.\d+)<', lambda mm: '>'+format(round(float(mm.group(1)),2),'g')+'<', tbl); parts.append(f'<div class="tablewrap">{tbl}</div>')
            # png handled separately (we inject our own styled figures)
        elif ot=='stream' and o.get('name')=='stdout':
            txt="".join(o.get('text',[])).rstrip()
            if txt:
                parts.append(f'<pre class="dataout">{_html.escape(txt)}</pre>')
    return "\n".join(parts)

nb=json.load(open(NB))
cells=nb['cells']

# cover pieces from cell 0
c0="".join(cells[0]['source']); parts=c0.split('---',1)
title=re.search(r'#\s+(.*)',parts[0]).group(1).strip()
sub=re.search(r'\*(.+?)\*',parts[0],re.S).group(1).strip()
rest0=parts[1] if len(parts)>1 else ''

SKIP_CELLS={1,5,6}     # 1 = licence (moved to appendix); 5/6 = Setup heading + import code
fignum=0
body=[]
for i,c in enumerate(cells):
    if i in SKIP_CELLS: continue
    if i==0:
        body.append(render(rest0)); continue
    if c['cell_type']=='markdown':
        body.append(render("".join(c['source'])))
    else:
        s="".join(c['source']); m=re.search(r"savefig\('([^']+)'",s)
        if m:                                             # inject our styled figure first
            fn=m.group(1); fignum+=1; p=os.path.join(FIGDIR,fn)
            if os.path.exists(p):
                body.append(f'<figure><img alt="{CAP.get(fn,"")}" src="data:image/png;base64,{b64(p)}">'
                            f'<figcaption><b>Figure {fignum}.</b> {CAP.get(fn,"")}</figcaption></figure>')
        outs=render_outputs(c)                            # then reinstate tables / computed output
        if outs: body.append(outs)
BODY="\n".join(body)
APPENDIX=render("".join(cells[1]['source']))              # licence -> appendix at end

CSS='''
:root{--canvas:#F6F5F1;--ink:#242628;--muted:#5A6165;--rule:#DDD6CB;--grid:#E2DED2;
--slate:#3E5B76;--ochre:#7A5230;--mauve:#7E6578;--band:#EFEBE1;--out:#EEEAE0;}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;background:var(--canvas)}
body{margin:0;color:var(--ink);background:var(--canvas);
font-family:'Public Sans','LatoDoc',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
font-size:18px;line-height:1.66;font-weight:400;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased;}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.035;
background-image:url("data:image/svg+xml;base64,%GRAIN%");background-size:180px 180px;}
.wrap{position:relative;z-index:1;max-width:920px;margin:0 auto;padding:0 22px 110px}
.cover{padding:76px 0 34px;border-bottom:1px solid var(--rule);margin-bottom:44px}
.eyebrow{font-weight:700;font-size:13px;letter-spacing:.19em;text-transform:uppercase;color:var(--ochre);margin:0 0 20px}
h1.title{font-family:Lora,Georgia,serif;font-weight:600;font-size:47px;line-height:1.12;letter-spacing:-.012em;margin:0 0 20px}
.standfirst{font-family:Lora,Georgia,serif;font-style:italic;font-weight:400;font-size:21px;line-height:1.5;color:#3d4247;margin:0 0 30px;max-width:60ch}
.meta{display:flex;flex-wrap:wrap;gap:6px 26px;font-size:14px;color:var(--muted);padding-top:20px;border-top:1px solid var(--rule)}
.meta b{color:var(--ink);font-weight:700}
.keyfinding{background:var(--band);border-left:3px solid var(--ochre);padding:24px 28px;border-radius:3px;margin:38px 0 8px}
.keyfinding .lab{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ochre);font-weight:700;margin:0 0 10px}
.keyfinding p{margin:0;font-size:18.5px;line-height:1.55}
.keyfinding b{color:var(--slate);font-weight:700}
h2{font-family:Lora,Georgia,serif;font-weight:600;font-size:29px;line-height:1.2;letter-spacing:-.01em;margin:52px 0 14px;padding-top:8px}
h3{font-family:Lora,Georgia,serif;font-weight:600;font-size:22px;margin:34px 0 10px;color:#33373b}
p{margin:0 0 20px}
a{color:var(--ochre);text-decoration:underline;text-underline-offset:2px;text-decoration-thickness:1px}
strong,b{font-weight:700}em,i{font-style:italic}
hr{border:0;border-top:1px solid var(--rule);margin:40px 0}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;background:#ECE8DE;padding:1px 5px;border-radius:3px}
ul,ol{margin:0 0 20px;padding-left:1.3em}li{margin:6px 0}
figure{margin:40px 0}
figure img{width:100%;display:block;background:var(--canvas);border:1px solid var(--rule);border-radius:4px}
figcaption{font-size:14px;color:var(--muted);margin-top:11px;line-height:1.5}figcaption b{color:var(--ink);font-weight:700}
/* reinstated tables + computed output */
.tablewrap{overflow-x:auto;margin:24px 0}
table{border-collapse:collapse;font-size:14.5px;margin:0}
table.dataframe{width:100%}
th,td{text-align:right;padding:8px 13px;border-bottom:1px solid var(--rule);vertical-align:top;white-space:nowrap}
th:first-child,td:first-child{text-align:left}
thead th,table.dataframe thead th{border-bottom:2px solid var(--ink);font-size:12px;letter-spacing:.03em;text-transform:uppercase;color:var(--muted);font-weight:700}
table.dataframe tbody th{font-weight:700;text-align:left;color:var(--ink)}
tbody tr:last-child td{border-bottom:2px solid var(--ink)}
.dataout{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;line-height:1.5;
color:#33373b;background:var(--out);border:1px solid var(--rule);border-radius:4px;
padding:14px 16px;margin:22px 0;overflow-x:auto;white-space:pre}
.appendix{margin-top:72px;padding-top:8px;border-top:2px solid var(--ink)}
.appendix h2{font-size:22px}.appendix p,.appendix li{font-size:14.5px;color:var(--muted)}
@media (max-width:640px){body{font-size:17px}h1.title{font-size:36px}.wrap{padding:0 20px 80px}}
'''.replace('%GRAIN%',GRAIN)

HTML=f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="author" content="Bradley Quinlan">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>{FONTS}{CSS}</style></head>
<body><div class="wrap">
<header class="cover">
<p class="eyebrow">Cross-Pressure Study &middot; 2026</p>
<h1 class="title">One Coalition, Two Electorates</h1>
<p class="standfirst">{sub}</p>
<div class="meta"><span><b>Bradley Quinlan</b></span><span>University of Essex</span><span>MA336</span><span>British Social Attitudes 2014 &amp; 2024</span></div>
<div class="keyfinding"><p class="lab">Headline finding</p>
<p>Clustered on political attitudes alone, Reform’s 2024 voters divide almost in half—<b>55.0%</b> in a conventional right-authoritarian group and <b>41.0%</b> in an authoritarian-left group that is pro-redistribution and disproportionately benefit-reliant, sitting inside a party that campaigned on roughly £90bn of tax cuts. Projected onto 2014 UKIP identifiers the left-behind cluster is larger still, so the pattern predates Reform by a decade.</p></div>
</header>
<main>{BODY}</main>
<section class="appendix">{APPENDIX}</section>
</div></body></html>'''
open(OUT,'w').write(HTML)
print("wrote",OUT,f"({len(HTML)/1e6:.2f} MB); figures={fignum}; tables reinstated")

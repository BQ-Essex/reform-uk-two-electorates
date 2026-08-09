# -*- coding: utf-8 -*-
import json, re, base64, os, html as _html
import markdown
from report_style import b64, FONTS, CSS

REPO=os.path.dirname(os.path.abspath(__file__))
NB=REPO+'/notebook/MA336_Project_Notebook.ipynb'
FIGDIR=REPO+'/figures'
OUT=REPO+'/report/report.html'

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
                tbl=re.sub(r'>(-?\d+\.\d+)<', lambda mm: '>'+format(round(float(mm.group(1)),2),'g')+'<', tbl)
                # Column headers are pandas column names -- often long snake_case
                # identifiers (reform_vote_share_2024GE_BSA) with no space for a
                # renderer to wrap at, which ran the widest tables off the page
                # edge in print. <wbr> after each underscore gives the renderer a
                # clean place to break -- invisible, no visual change on screen,
                # where headers have room to sit on one line anyway.
                tbl=re.sub(r'(<th[^>]*>)([^<]*)(</th>)',
                           lambda mm: mm.group(1)+mm.group(2).replace('_','_<wbr>')+mm.group(3), tbl)
                parts.append(f'<div class="tablewrap">{tbl}</div>')
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
<div class="meta"><span><b>Bradley Quinlan</b></span><span>University of Essex</span><span>Artificial Intelligence and Machine Learning with Applications</span><span>British Social Attitudes 2014 &amp; 2024</span></div>
<div class="keyfinding"><p class="lab">Headline finding</p>
<p>Clustered on political attitudes alone, Reform’s 2024 voters divide almost in half—<b>55.0%</b> in a conventional right-authoritarian group and <b>41.0%</b> in an authoritarian-left group that is pro-redistribution, on lower household incomes and markedly the least credentialled of the three, sitting inside a party that campaigned on tax cuts it costed at nearly £90bn a year. Projected onto 2014 UKIP identifiers the left-behind cluster is larger still, so the pattern predates Reform by a decade.</p></div>
</header>
<main>{BODY}</main>
<section class="appendix">{APPENDIX}</section>
</div></body></html>'''
open(OUT,'w').write(HTML)
print("wrote",OUT,f"({len(HTML)/1e6:.2f} MB); figures={fignum}; tables reinstated")

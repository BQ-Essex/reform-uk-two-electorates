# -*- coding: utf-8 -*-
"""Shared house style for the two HTML builders.

build_report.py and build_summary.py previously would have carried their own
copies of this CSS. They did not diverge by accident once -- SUMMARY.html was
hand-maintained and drifted from report.html three times. One definition,
imported twice, removes that failure mode structurally.
"""
import base64, os

REPO=os.path.dirname(os.path.abspath(__file__))
FONTDIR=REPO+'/fonts'

def b64(path):
    return base64.b64encode(open(path,'rb').read()).decode()
def font_face(family,path,weight='400',style='normal'):
    return (f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};"
            f"font-display:swap;src:url(data:font/ttf;base64,{b64(path)}) format('truetype');}}")

FONTDIR=REPO+'/fonts'
FONTS=""
FONTS+=font_face('Lora',FONTDIR+'/Lora-Variable.ttf','400 700','normal')
FONTS+=font_face('Lora',FONTDIR+'/Lora-Italic-Variable.ttf','400 700','italic')
FONTS+=font_face('LatoDoc',FONTDIR+'/Lato-Regular.ttf','400','normal')
FONTS+=font_face('LatoDoc',FONTDIR+'/Lato-Italic.ttf','400','italic')
FONTS+=font_face('LatoDoc',FONTDIR+'/Lato-Bold.ttf','700','normal')
FONTS+=font_face('LatoDoc',FONTDIR+'/Lato-Light.ttf','300','normal')

GRAIN_SVG=("<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'>"
           "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/>"
           "<feColorMatrix type='saturate' values='0'/></filter>"
           "<rect width='100%' height='100%' filter='url(%23n)'/></svg>")
GRAIN=base64.b64encode(GRAIN_SVG.encode()).decode()

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
table:not(.dataframe) th,table:not(.dataframe) td{text-align:left;white-space:normal}
table:not(.dataframe) th:first-child,table:not(.dataframe) td:first-child{white-space:nowrap;width:1%;padding-right:26px}
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


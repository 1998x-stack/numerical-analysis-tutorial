#!/usr/bin/env python3
"""Static site QA. Browser screenshots/interaction checks are a separate manual gate."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Scan(HTMLParser):
    def __init__(self):
        super().__init__();self.refs=[];self.ids=set();self.h1=0;self.fig=0;self.math=0;self.svgdepth=0;self.svgmath=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if "id" in d:self.ids.add(d["id"])
        for k in ("src","href"):
            if k in d:self.refs.append((k,d[k]))
        if tag=="h1":self.h1+=1
        if tag=="figcaption":self.fig+=1
        if tag=="svg":self.svgdepth+=1
        if tag=="math":
            self.math+=1;self.svgmath|=self.svgdepth>0
    def handle_endtag(self,tag):
        if tag=="svg":self.svgdepth=max(0,self.svgdepth-1)
def run():
    manifest=json.loads((ROOT/"courses.json").read_text(encoding="utf-8"))
    chapters=manifest["chapters"];errs=[]
    if len(chapters)!=28 or len({c["num"] for c in chapters})!=28:errs.append("manifest must contain 28 unique chapters")
    pages=[ROOT/"index.html"]+[ROOT/c["file"] for c in chapters]
    for page in pages:
        if not page.exists():errs.append(f"missing {page}");continue
        s=Scan();s.feed(page.read_text(encoding="utf-8"))
        is_new=page.name in {f"{i:02}.html" for i in range(1,6)}
        if (page.name=="index.html" or is_new) and s.h1!=1:errs.append(f"{page}: must have exactly 1 h1, got {s.h1}")
        if is_new and (s.fig<2 or s.math<2 or "references" not in s.ids):errs.append(f"{page}: need figures, MathML and sources")
        if s.svgmath:errs.append(f"{page}: nested SVG MathML")
        for attr,ref in s.refs:
            if ref.startswith(("http://","https://","mailto:","data:","javascript:")):continue
            path=ref.split("#",1)[0].split("?",1)[0]
            if path and not (page.parent/path).exists():errs.append(f"{page}: broken {attr}={ref}")
            if ref.startswith("#") and ref[1:] and ref[1:] not in s.ids:errs.append(f"{page}: broken anchor {ref}")
    svgfiles=list((ROOT/"assets/svg").glob("*.svg"))
    if len(svgfiles)<11:errs.append(f"expected 11 SVG diagrams, found {len(svgfiles)}")
    for p in svgfiles:
        try:
            r=ET.parse(p).getroot();children={c.tag.rsplit("}",1)[-1] for c in r}
            if not r.get("viewBox") or not {"title","desc"}.issubset(children):errs.append(f"{p}: accessibility metadata missing")
        except ET.ParseError as exc:errs.append(f"{p}: {exc}")
    if errs:
        print("\n".join("ERROR: "+x for x in errs));sys.exit(1)
    print(f"OK: {len(pages)} canonical HTML pages; {len(svgfiles)} standalone SVGs; relative links and anchors")
if __name__=="__main__":run()

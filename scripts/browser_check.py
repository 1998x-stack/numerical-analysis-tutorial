#!/usr/bin/env python3
"""Playwright browser audit: actual rendering, responsive widths, MathML, images, interactions.
Setup: pip install playwright && python -m playwright install chromium
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"qa"/"screenshots"
PAGES=["index.html"]+[f"chapters/{n:02d}.html" for n in range(1,11)]
SIZES=[(1440,900),(768,1024),(390,844),(360,800)]

def run():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    failures=[]
    checks=0
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for path in PAGES:
            for width,height in SIZES:
                page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
                errors=[]
                page.on("pageerror",lambda exc:errors.append(str(exc)))
                page.goto((ROOT/path).as_uri(),wait_until="load")
                page.wait_for_timeout(100)
                info=page.evaluate("""() => ({
                    width: document.documentElement.scrollWidth,
                    viewport: window.innerWidth,
                    images: [...document.querySelectorAll('figure img')].map(x=>({ok:x.complete && x.naturalWidth>0,src:x.getAttribute('src')})),
                    maths: [...document.querySelectorAll('math')].map(x=>({ns:x.namespaceURI,ok:x.getBoundingClientRect().height>0 && x.getBoundingClientRect().width>0})),
                    fractionCount: document.querySelectorAll('math mfrac').length
                })""")
                if info["width"]>info["viewport"]+1:
                    failures.append(f"{path} at {width}px: horizontal document overflow {info['width']}")
                if any(not x["ok"] for x in info["images"]):
                    failures.append(f"{path} at {width}px: broken image")
                if path!="index.html" and (len(info["maths"])<2 or info["fractionCount"]<1):
                    failures.append(f"{path} at {width}px: missing MathML/fraction")
                for obj in info["maths"]:
                    if obj["ns"]!="http://www.w3.org/1998/Math/MathML" or not obj["ok"]:
                        failures.append(f"{path} at {width}px: MathML namespace or geometry wrong")
                if errors:failures.extend(f"{path} at {width}px: JavaScript {x}" for x in errors)
                if width in (1440,390):
                    page.screenshot(path=str(OUTPUT/(path.replace("/","-")+"-"+str(width)+".png")),full_page=True)
                if width==390:
                    if path=="index.html":
                        field=page.locator("#chapter-filter")
                        field.fill("Newton")
                        count=page.locator(".lesson:visible").count()
                        if not 0<count<28:failures.append("home: search control does not filter")
                    else:
                        area=page.locator("[data-lab]")
                        if area.count()!=1:failures.append(f"{path}: expected one working demo")
                        else:
                            inp=area.locator("[data-input]")
                            out=area.locator("[data-output]")
                            initial=out.inner_text()
                            inp.select_option(index=1)
                            new=out.inner_text()
                            if initial==new:failures.append(f"{path}: demo did not update")
                checks+=1
                page.close()
        browser.close()
    if failures:
        for x in failures:print("FAIL:",x)
        sys.exit(1)
    print(f"OK: {checks} browser viewports; SVG images, MathML, demo changes and search; screenshots in qa/screenshots")
if __name__=="__main__":run()

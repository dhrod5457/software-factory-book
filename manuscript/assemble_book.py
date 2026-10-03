#!/usr/bin/env python3
"""Synchronize canonical drafts, preserving the book's publication figures/cases.

The chapter drafts are authoritative. The existing book supplies front matter,
Part headings, consolidated references and the publication-only insertions.
No network access or publication is performed.
"""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
path = ROOT / 'book.md'
old = path.read_text()
figure = re.compile(r'(?ms)^<!-- FIGURE (F\d+):[^\n]*-->\n\n\*\*Figure .*?\n\n```mermaid\n.*?^```\n\n\*[^\n]+\*')
case = re.compile(r'(?m)^<!-- CASE (C\d+):[^\n]*-->\n\n(?:>[^\n]*\n?)+')
heads=list(re.finditer(r'(?m)^#{1,4} (.+)$',old))
inserts=[]
for kind,pattern in [('figure',figure),('case',case)]:
 for m in pattern.finditer(old):
  prev=[h for h in heads if h.start()<m.start()]
  anchor=prev[-1].group(1)
  chapter=next((int(h.group(1).split('장.')[0]) for h in reversed(prev) if re.match(r'\d+장\.',h.group(1))),None)
  inserts.append((chapter,anchor,kind,m[1],m[0].rstrip()))
assert sum(x[2]=='figure' for x in inserts)==21
front=old[:old.index('# 들어가며')]
parts={}
for m in re.finditer(r'(?m)^# Part [^\n]+',old):
 after=old[m.end():];n=re.search(r'^## (\d+)장\.',after,re.M)
 parts[int(n[1])]=m[0]
chapters=[];attached=[]
for n in range(1,25):
 text=(REPO/f'chapters/{n:02d}/draft.md').read_text().split('\n## 참고 자료')[0].strip()
 # Publication headings sit below their Part; retain the draft's complete structure.
 text=re.sub(r'(?m)^(#{1,5}) ',r'\1# ',text)
 for ch,anchor,kind,ident,block in inserts:
  if ch!=n:continue
  if f'<!-- CASE {ident}:' in text:attached.append(ident);continue
  target=re.search(r'(?m)^#{2,5} '+re.escape(anchor)+r'$',text)
  if not target:raise RuntimeError(f'Insertion anchor missing: {ident}: {anchor}')
  # Both figures and case boxes attach immediately to their original section.
  text=text[:target.end()]+'\n\n'+block+'\n'+text[target.end():]
  attached.append(ident)
 chapters.append((parts[n]+'\n\n' if n in parts else '')+text)
refs=old[old.index('# References'):].rstrip()
# The RC2 drafts may cite sources absent from the older consolidated list.
for draft in sorted((REPO/'chapters').glob('*/draft.md')):
 text=draft.read_text();section=text.split('\n## 참고 자료\n')
 if len(section)<2:continue
 for item in re.split(r'(?m)(?=^- )',section[1]):
  urls=re.findall(r'https?://\S+',item)
  if urls and all(u not in refs for u in urls):refs+='\n\n'+item.strip()
result=front+(ROOT/'preface.md').read_text().strip()+'\n\n---\n\n'+'\n\n---\n\n'.join(chapters)+'\n\n---\n\n'+(REPO/'chapters/epilogue/draft.md').read_text().strip()+'\n\n---\n\n'+(ROOT/'glossary.md').read_text().strip()+'\n\n---\n\n'+refs+'\n'
assert len(figure.findall(result))==21
assert len(case.findall(result))==len(case.findall(old))
result = '\n'.join(line.rstrip() for line in result.splitlines()) + '\n'
path.write_text(result)
print(f'Synchronized 24 chapters, epilogue, preface, glossary; preserved {len(attached)} publication insertions.')

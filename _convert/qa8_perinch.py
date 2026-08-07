import glob, re, os
n=0; files=0
for f in glob.glob("src/content/**/*.json", recursive=True):
    t=open(f,encoding="utf-8").read(); o=t
    t=re.sub(r"\s*[+·,;]?\s*\$8\s*/\s*inch(?:\s+after(?:\s+12\?\"?)?)?","",t)
    t=re.sub(r"\s*[+·,;]?\s*\$8\s*per\s*inch(?:\s+after(?:\s+12\?\"?)?)?","",t)
    t=re.sub(r"\$8\s*[–—-]\s*\$15\s*per\s*inch","quoted per inch",t)
    if t!=o:
        open(f,"w",encoding="utf-8").write(t); files+=1; n+=1
print(f"per-inch swept from {files} files")

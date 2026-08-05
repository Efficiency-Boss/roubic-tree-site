"""Fix founder attribution: Thomas Roubic founded the business in 1982 and worked
it until semi-retiring in 2017; Aaron (his son) joined 2009 and took over 2017.
So any "Aaron / {{owner_name}} has worked X since 1982 / since the early 1990s"
heritage claim is factually wrong — it should be Thomas. Present-day claims
("Aaron personally walks every estimate") are correct and left untouched.
Also fixes the auburn-township schema founder = owner_name -> Thomas Roubic.
"""
import glob, os, re

# founding-era clause: <name> [Roubic] has [been] [personally] worked/working <...> since <1982|early 1990s>
CLAUSE = re.compile(
    r'(\{\{global\.owner_name\}\}|Aaron)(\s+Roubic)?'
    r'(\s+has\s+(?:been\s+)?(?:personally\s+)?work\w*\b[^.]*?'
    r'since\s+(?:1982|the\s+early\s+1990s))'
)


def name_repl(m):
    # template -> full "Thomas Roubic"; literal "Aaron" -> "Thomas" (matches first-name style)
    if m.group(1).startswith("{{"):
        return "Thomas Roubic" + m.group(3)
    return "Thomas" + m.group(3)


changed = []
for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    t = open(f, encoding="utf-8").read()
    o = t
    t, n = CLAUSE.subn(name_repl, t)
    # schema founder = owner_name -> Thomas Roubic (auburn only, but safe globally)
    t2 = t.replace(
        '\\"founder\\": { \\"@type\\": \\"Person\\", \\"name\\": \\"{{global.owner_name}}\\" }',
        '\\"founder\\": { \\"@type\\": \\"Person\\", \\"name\\": \\"Thomas Roubic\\" }')
    if t2 != t:
        n += 1
    t = t2
    if t != o:
        open(f, "w", encoding="utf-8").write(t)
        changed.append((os.path.basename(f)[:-5], n))

print(f"files changed: {len(changed)}")
for name, n in changed:
    print(f"  {n}x  {name}")

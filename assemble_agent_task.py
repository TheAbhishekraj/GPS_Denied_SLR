import os

src = r"E:\GPS_Denied_SLR\AGENT_TASK_CHUNK2.md"
dst = r"E:\GPS_Denied_SLR\AGENT_TASK.md"

with open(src, "r", encoding="utf-8") as f:
    text = f.read()

idx1 = text.find("# AGENT_TASK.md — GPS_Denied_SLR End-to-End Completion Brief")

# Find the end of Chunk 1: look for Set-Content
p7 = text.find("## PHASE 7", idx1)
sc1 = text.find("Set-Content", p7)
# Look backward from sc1 for '@
end_chunk1 = text.rfind("'@", p7, sc1)

# Find Chunk 2
idx2 = text.find("## PHASE 8 — PRISMA & Figures")
sc2 = text.find("Add-Content", idx2)
end_chunk2 = text.rfind("'@", idx2, sc2)

print(f"chunk1: {idx1} to {end_chunk1}, chunk2: {idx2} to {end_chunk2}")

if idx1 != -1 and end_chunk1 != -1 and idx2 != -1 and end_chunk2 != -1:
    chunk1 = text[idx1:end_chunk1].strip()
    chunk2 = text[idx2:end_chunk2].strip()
    full = chunk1 + "\n\n---\n\n" + chunk2
    with open(dst, "w", encoding="utf-8") as out:
        out.write(full)
    print(f"Written {dst}: {len(full)} chars, {full.count(chr(10))+1} lines")
    if os.path.exists(src):
        os.remove(src)

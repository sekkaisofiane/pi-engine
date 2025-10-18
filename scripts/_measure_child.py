import json, psutil, time, subprocess, os, sys
def run_and_measure(cmd):
    p = psutil.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    peak = 0
    while True:
        if p.poll() is not None: break
        try:
            mem = p.memory_info().rss
            for c in p.children(recursive=True):
                mem += c.memory_info().rss
            if mem>peak: peak=mem
        except psutil.Error: pass
        time.sleep(0.1)
    out, err = p.communicate()
    return {"rc":p.returncode,"stdout":out.decode(errors="ignore"),"stderr":err.decode(errors="ignore"),
            "peak_ram_mb": round(peak/1048576,1)}
print(json.dumps(run_and_measure(sys.argv[1:])))

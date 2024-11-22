import psutil
from pprint import pprint
from os import getpid


bad_statuses = ["zombie", "dead", "ghost", "stopped", "suspended"]
bad_procs = []

for p in psutil.process_iter():
    if p.status() in bad_statuses:
        bad_procs.append(p)
    if p.name().startswith("python") and p.pid != getpid():
        bad_procs.append(p)

for p in bad_procs:
    print(p.pid, p.name(), p.status())
    if (query := input("kill? y/n/a: ")) == "y":
        p.kill()
    elif query == "a":
        for p in bedrock:
            pprint(p.name())
            p.kill()
        break
    else:
        break

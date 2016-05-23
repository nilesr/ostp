#!/usr/bin/env python3
import os, pyotp, subprocess, time
def clean():
    subprocess.call(["iptables","-t","nat","-F"])
    subprocess.call(["iptables","-t","nat","-A","POSTROUTING","-j","MASQUERADE"])
def fixport(s):
    while s[0] == "0":
        s = s[1:]
    return s
computers = {
        2: "Hazel-Alder",
        3: "Archbishop",
        # No idea what 4 is
        5: "ethan",
        6: "Smokewood",
        7: "Quaking-Aspen",
        8: "Spice-Birch",
        9: "Silver-Birch",
        10: "macmini",
        11: "Leichhardt-Pine",
        }
d = []
for i in range(10):
    d.append(["10.8.0." + str(i+2)]) # 10.8.0.2-11
for i in range(len(d)):
    filename = "/opt/ostp/" + d[i][0] + ".key"
    if not os.path.isfile(filename):
        print(filename + "does not exist, creating")
        f = open(filename, "w")
        f.write(pyotp.random_base32())
        f.close()
    f = open(filename,"r")
    d[i].append(pyotp.TOTP(f.read()))
    f.close()
    id = int(d[i][0].split(".")[-1])
    name = d[i][0]
    if id in computers:
        name = computers[id]
    filename = "/opt/ostp/" + d[i][0] + ".url"
    f = open(filename, "w")
    f.write(d[i][1].provisioning_uri(name) + '&issuer=ostp')
    f.close()
    #print(d[i][1].now())
clean()
subprocess.call(["sysctl", "net.ipv4.ip_forward=1"])
while True:
    for i in d:
        port = fixport(str(i[1].now())[:4])
        subprocess.call(["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "tcp", "--dport", port, "-j","DNAT","--to-destination", i[0] + ":22"])
    time.sleep(30)
    #for i in d:
    #    subprocess.call(["iptables", "-t", "nat", "-D", "PREROUTING", "-p", "tcp", "--dport", port, "-j","DNAT","--to-destination", i[0] + ":22"])
    clean()

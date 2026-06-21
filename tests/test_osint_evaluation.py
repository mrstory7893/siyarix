#!/usr/bin/env python3
"""OSINT-focused NLP/planner evaluation — 160 commands, basic to advanced."""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from siyarix import RegistryPlanner

AVAILABLE_TOOLS = [
    "nmap", "masscan", "rustscan", "naabu",
    "gobuster", "ffuf", "dirb", "dirsearch",
    "whatweb", "wappalyzer", "builtwith",
    "nuclei", "nikto", "wapiti", "skipfish",
    "hydra", "medusa", "ncrack", "patator",
    "subfinder", "amass", "sublist3r", "assetfinder",
    "curl", "wget", "httpie",
    "dig", "nslookup", "host",
    "aircrack-ng", "hashcat", "john",
    "sqlmap", "jSQL", "sqlninja",
    "whois", "openssl", "eyewitness",
    "tracert", "traceroute", "responder",
    "impacket", "impacket-secretsdump", "impacket-GetUserSPNs", "impacket-GetNPUsers",
    "bloodhound-python", "searchsploit",
    "shodan", "censys",
    "theHarvester", "gau", "waybackurls",
    "httpx", "katana", "gospider",
    "uncover", "subjack",
    "trufflehog", "gitleaks",
    "sherlock", "holehe", "maigret",
    "dnsx", "massdns", "puredns",
    "arjun", "paramspider",
    "cloud_enum", "scoutsuite", "prowler",
    "interactsh", "testssl.sh", "ssllabs-scan",
    "bluetoothctl", "crackmapexec", "netexec", "enum4linux",
    "wpscan",
]

def check_plan(planner, goal, expected_tools, min_steps=1, max_steps=None):
    """Check that the planner returns a valid plan for the given goal."""
    plan = planner.decompose_goal(goal)
    actual_tools = [s.tool for s in plan.steps]
    step_count = len(plan.steps)

    if step_count < min_steps:
        return False, f"step_count {step_count} < min_steps {min_steps}"
    if max_steps and step_count > max_steps:
        return False, f"step_count {step_count} > max_steps {max_steps}"
    for et in expected_tools:
        if et not in actual_tools:
            return False, f"expected tool {et!r} not in {actual_tools}"
    return True, f"OK steps={step_count} tools={actual_tools}"


# ==============================================================================
# OSINT COMMANDS — 160 total, organized by category
# ==============================================================================
OSINT_COMMANDS = [
    # ------------------------------------------------------------------
    # 1. WHOIS & Domain Registration (12)
    # ------------------------------------------------------------------
    ("whois lookup for example.com", ["whois"], 1, 2),
    ("domain whois on example.com", ["whois"], 1, 2),
    ("whois registration for example.com", ["whois"], 1, 2),
    ("reverse whois for example.com", ["whois"], 1, 2),
    ("asn lookup for 8.8.8.8", ["whois"], 1, 2),
    ("asn recon on AS15169", ["whois"], 1, 2),
    ("ip whois for 8.8.8.8", ["whois"], 1, 2),
    ("domain registration check example.com", ["whois"], 1, 2),
    ("whois domain ownership for example.com", ["whois"], 1, 2),
    ("rdap lookup for 8.8.8.8", ["whois"], 1, 2),
    ("registrar information for example.com", ["whois"], 1, 2),
    ("domain registration info for example.com", ["whois"], 1, 2),

    # ------------------------------------------------------------------
    # 2. DNS Reconnaissance (18)
    # ------------------------------------------------------------------
    ("dns enumeration on example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
    ("dns record check for example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
    ("mx record lookup for example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
    ("dns resolution for example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
    ("nameserver lookup for example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
    ("dns zone transfer on example.com", ["dig"], 1, 2),
    ("axfr query for example.com", ["dig"], 1, 2),
    ("dns a record check for example.com", ["dig"], 1, 3),
    ("dns txt record enumeration for example.com", ["dig"], 1, 3),
    ("dns cname lookup for example.com", ["dig"], 1, 3),
    ("reverse dns lookup on 8.8.8.8", ["dig"], 1, 2),
    ("dns ptr record for 8.8.8.8", ["dig"], 1, 2),
    ("dns soa record for example.com", ["dig"], 1, 2),
    ("aaaa record check for example.com", ["dig"], 1, 2),
    ("dnssec check for example.com", ["dig"], 1, 2),
    ("spf record lookup for example.com", ["dig"], 1, 3),
    ("dmarc record check for example.com", ["dig"], 1, 3),
    ("dns cache snooping on 8.8.8.8", ["dig"], 1, 2),

    # ------------------------------------------------------------------
    # 3. Subdomain Enumeration (12)
    # ------------------------------------------------------------------
    ("subdomain enumeration on example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),
    ("subdomain discovery for example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),
    ("amass subdomain brute on example.com", ["amass"], 1, 2),
    ("amass intel on example.com", ["amass"], 1, 2),
    ("amass enum for example.com", ["amass"], 1, 2),
    ("subfinder passive enum on example.com", ["subfinder"], 1, 2),
    ("sublist3r subdomain search for example.com", ["sublist3r"], 1, 2),
    ("assetfinder subdomain discovery for example.com", ["assetfinder"], 1, 2),
    ("passive subdomain enum on example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),
    ("dns brute force subdomain on example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),
    ("subdomain takeover check on example.com", ["subjack"], 1, 2),
    ("check subdomain takeover on example.com", ["subjack"], 1, 2),

    # ------------------------------------------------------------------
    # 4. Certificate Transparency (8)
    # ------------------------------------------------------------------
    ("certificate transparency search for example.com", ["curl"], 1, 2),
    ("crtsh lookup for example.com", ["curl"], 1, 2),
    ("crt.sh search for example.com", ["curl"], 1, 2),
    ("certificate log inspection for example.com", ["openssl"], 1, 2),
    ("crtsh certificate search for example.com", ["curl"], 1, 2),
    ("certificate transparency logs for example.com", ["curl"], 1, 2),
    ("crt.sh domain search for example.com", ["curl"], 1, 2),
    ("ssl certificate transparency for example.com", ["openssl", "nmap"], 2, 4),

    # ------------------------------------------------------------------
    # 5. Email OSINT (10)
    # ------------------------------------------------------------------
    ("theHarvester email osint on example.com", ["theHarvester"], 1, 2),
    ("the harvester harvest on example.com", ["theHarvester"], 1, 2),
    ("email osint harvesting for example.com", ["theHarvester"], 1, 2),
    ("email recon on example.com", ["theHarvester", "dig", "nmap"], 3, 5),
    ("email harvest on example.com", ["theHarvester", "dig", "nmap"], 3, 5),
    ("smtp enum on mail.example.com", ["theHarvester", "dig", "nmap"], 3, 5),
    ("mail server discovery for example.com", ["theHarvester", "dig", "nmap"], 3, 5),
    ("holehe email check for user@example.com", ["holehe"], 1, 2),
    ("holehe email check for user@example.com", ["holehe"], 1, 2),
    ("theHarvester email search on example.com", ["theHarvester"], 1, 2),

    # ------------------------------------------------------------------
    # 6. Username & Social Media OSINT (10)
    # ------------------------------------------------------------------
    ("sherlock username search for johndoe", ["sherlock"], 1, 2),
    ("maigret user search for johndoe", ["maigret"], 1, 2),
    ("social media lookup for johndoe", ["sherlock"], 1, 2),
    ("social media lookup for johndoe across platforms", ["sherlock"], 1, 2),
    ("social network search for johndoe on social media", ["sherlock"], 1, 2),
    ("find all accounts for johndoe across networks", ["sherlock"], 1, 2),
    ("digital footprint search for johndoe online", ["whois", "dig", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("osint username reconnaissance for johndoe on social medias", ["sherlock"], 1, 2),
    ("identity osint on johndoe across all platforms", ["sherlock"], 1, 3),

    # ------------------------------------------------------------------
    # 7. URL Discovery & Wayback Machine (10)
    # ------------------------------------------------------------------
    ("wayback machine urls for example.com", ["waybackurls"], 1, 2),
    ("gau url discovery for example.com", ["gau"], 1, 2),
    ("get all urls for example.com", ["gau"], 1, 2),
    ("waybackurls discovery on example.com", ["waybackurls"], 1, 2),
    ("gau wayback url discovery for example.com", ["gau"], 1, 2),
    ("wayback machine endpoints for example.com", ["waybackurls"], 1, 2),
    ("historic urls for example.com from archive", ["gau"], 1, 2),
    ("url enumeration on example.com from wayback", ["waybackurls"], 1, 2),
    ("fetch all wayback urls for example.com", ["waybackurls"], 1, 2),
    ("waybackurls discovery on example.com", ["waybackurls"], 1, 2),

    # ------------------------------------------------------------------
    # 8. Web Probing & Crawling (12)
    # ------------------------------------------------------------------
    ("httpx probe on https://example.com", ["httpx"], 1, 2),
    ("http probe on example.com", ["httpx"], 1, 2),
    ("web crawl with katana on https://example.com", ["katana"], 1, 2),
    ("spider with gospider on https://example.com", ["gospider"], 1, 2),
    ("httpx live host probing for example.com", ["httpx"], 1, 2),
    ("katana crawl example.com for endpoints", ["katana"], 1, 2),
    ("gospider web spider on https://example.com", ["gospider"], 1, 2),
    ("probe all subdomains for example.com with httpx", ["httpx"], 1, 2),
    ("crawl and spider example.com", ["katana"], 1, 2),
    ("httpx tech detection on https://example.com", ["httpx"], 1, 2),
    ("katana url discovery on example.com", ["katana"], 1, 2),
    ("gospider content discovery on https://example.com", ["gospider"], 1, 2),

    # ------------------------------------------------------------------
    # 9. Parameter Discovery (8)
    # ------------------------------------------------------------------
    ("arjun parameter discovery on https://example.com", ["arjun"], 1, 2),
    ("paramspider mining on example.com", ["paramspider"], 1, 2),
    ("discover http parameter on https://example.com", ["arjun"], 1, 2),
    ("param mining on example.com", ["arjun"], 1, 2),
    ("arjun find hidden params on https://example.com", ["arjun"], 1, 2),
    ("parameter discovery scan on example.com", ["arjun"], 1, 2),
    ("url parameter enumeration on https://example.com", ["arjun"], 1, 2),
    ("get params from url on https://example.com", ["arjun"], 1, 2),

    # ------------------------------------------------------------------
    # 10. Cloud & Infrastructure OSINT (10)
    # ------------------------------------------------------------------
    ("cloud_enum storage scan for example", ["cloud_enum"], 1, 2),
    ("scoutsuite cloud audit for aws", ["scoutsuite"], 1, 2),
    ("prowler aws security audit", ["prowler"], 1, 2),
    ("cloud_enum storage scan for example", ["cloud_enum"], 1, 2),
    ("aws bucket discovery on example", ["curl", "whatweb", "dig", "openssl"], 3, 5),
    ("azure cloud storage check for example", ["curl", "whatweb", "dig", "openssl"], 3, 5),
    ("gcp bucket enumeration on example", ["curl", "whatweb", "dig", "openssl"], 3, 5),
    ("cloud_enum multi cloud scan for example", ["cloud_enum"], 1, 2),
    ("s3 bucket osint for example", ["curl", "whatweb", "dig", "openssl"], 3, 5),
    ("cloud_enum discovery on example", ["cloud_enum"], 1, 2),

    # ------------------------------------------------------------------
    # 11. Shodan / Censys / Uncover (10)
    # ------------------------------------------------------------------
    ("shodan search for example.com on internet", ["shodan"], 1, 2),
    ("shodan internet device search for example.com", ["shodan"], 1, 2),
    ("censys search for example.com certificates", ["censys"], 1, 2),
    ("censys ip lookup for 8.8.8.8", ["censys"], 1, 2),
    ("shodan port scan history for 8.8.8.8", ["shodan"], 1, 2),
    ("shodan honeypot check for 8.8.8.8", ["shodan"], 1, 2),
    ("uncover search for example.com", ["uncover"], 1, 2),
    ("shodan and censys search on example.com", ["shodan"], 1, 2),
    ("shodan internet search for example.com", ["shodan"], 1, 2),
    ("attack surface discovery with shodan for example.com", ["shodan"], 1, 2),

    # ------------------------------------------------------------------
    # 12. Secret Scanning (8)
    # ------------------------------------------------------------------
    ("trufflehog secret scan on git repo", ["trufflehog"], 1, 2),
    ("gitleaks scan on repository", ["gitleaks"], 1, 2),
    ("git secret scanning on repo", ["trufflehog"], 1, 2),
    ("find leaked secrets in repo", ["trufflehog"], 1, 2),
    ("trufflehog git history scan for credentials", ["trufflehog"], 1, 2),
    ("gitleaks git secrets detection", ["gitleaks"], 1, 2),
    ("scan for api keys in repository", ["trufflehog"], 1, 2),
    ("credential leak detection in git repo", ["trufflehog"], 1, 2),

    # ------------------------------------------------------------------
    # 13. DNS Toolkit (8)
    # ------------------------------------------------------------------
    ("dnsx query on example.com", ["dnsx"], 1, 2),
    ("massdns on example.com with resolvers", ["massdns"], 1, 2),
    ("puredns resolve for example.com", ["puredns"], 1, 2),
    ("dns probe with dnsx on example.com", ["dnsx"], 1, 2),
    ("massdns brute force subdomains on example.com", ["massdns"], 1, 2),
    ("puredns wildcard filter for example.com", ["puredns"], 1, 2),
    ("dnsx a record query for example.com", ["dnsx"], 1, 2),
    ("bulk dns resolution with dnsx for example.com", ["dnsx"], 1, 2),

    # ------------------------------------------------------------------
    # 14. SSL/TLS OSINT (8)
    # ------------------------------------------------------------------
    ("ssl labs scan for example.com", ["ssllabs-scan"], 1, 2),
    ("testssl full check on example.com", ["testssl.sh"], 1, 2),
    ("ssl certificate info for https://example.com", ["openssl", "nmap"], 2, 4),
    ("ssl certificate chain validation for example.com", ["openssl", "nmap"], 2, 4),
    ("tls cipher suite check on example.com", ["openssl", "nmap"], 2, 4),
    ("ssl tls security assessment on example.com", ["openssl", "nmap"], 2, 4),
    ("testssl audit on example.com", ["testssl.sh"], 1, 2),
    ("ssllabs certificate analysis for example.com", ["ssllabs-scan"], 1, 2),

    # ------------------------------------------------------------------
    # 15. Passive Recon (8)
    # ------------------------------------------------------------------
    ("passive recon on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("passive reconnaissance on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("passive scan on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("passive intel gathering on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("stealth osint on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("quiet passive recon on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("passive information gathering on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("non intrusive recon on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),

    # ------------------------------------------------------------------
    # 16. Full OSINT Recon (8)
    # ------------------------------------------------------------------
    ("osint recon on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("full osint recon on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("open source intelligence on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("osint intelligence gathering on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("complete osint assessment on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("deep osint reconnaissance on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("thorough osint investigation on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("recon-ng style osint on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),

    # ------------------------------------------------------------------
    # 17. External Attack Surface (6)
    # ------------------------------------------------------------------
    ("external recon on example.com", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 7),
    ("external attack surface on example.com", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 7),
    ("external attack surface recon on example.com", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 7),
    ("internet scan for example.com assets", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 7),
    ("external perimeter recon on example.com", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 7),
    ("edge discovery for example.com", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 7),

    # ------------------------------------------------------------------
    # 18. Multi-Tool / Compound OSINT (14)
    # ------------------------------------------------------------------
    ("gau then httpx on example.com", ["gau", "httpx"], 2, 3),
    ("subfinder then httpx on example.com", ["subfinder", "httpx"], 2, 3),
    ("waybackurls then httpx on example.com", ["waybackurls", "httpx"], 2, 3),
    ("theHarvester and then holehe on example.com", ["theHarvester", "holehe"], 2, 3),
    ("amass subdomains and then httpx probe on example.com", ["amass", "httpx"], 2, 3),
    ("gau and then katana on example.com", ["gau", "katana"], 2, 3),
    ("subfinder and then gospider on example.com", ["subfinder", "gospider"], 2, 3),
    ("dnsx then httpx on example.com", ["dnsx", "httpx"], 2, 3),
    ("massdns then puredns on example.com", ["massdns", "puredns"], 2, 3),
    ("arjun then paramspider on https://example.com", ["arjun", "paramspider"], 2, 3),
    ("uncover then httpx on example.com", ["uncover", "httpx"], 2, 3),
    ("theHarvester then sherlock for johndoe", ["theHarvester", "sherlock"], 2, 3),
    ("gau and then waybackurls on example.com", ["gau", "waybackurls"], 2, 3),
    ("crtsh and then httpx on example.com", ["curl", "httpx"], 2, 3),

    # ------------------------------------------------------------------
    # 19. Advanced / Specialized OSINT (10)
    # ------------------------------------------------------------------
    ("interactsh oob testing client", ["interactsh"], 1, 2),
    ("oob collaboration test with interactsh", ["interactsh"], 1, 2),
    ("certificate transparency log monitoring for example.com", ["curl"], 1, 2),
    ("google dorking for example.com", ["curl"], 1, 2),
    ("dork search for exposed configs on example.com", ["curl"], 1, 2),
    ("ssllabs api scan for example.com", ["ssllabs-scan"], 1, 2),
    ("ssllabs api scan on example.com", ["ssllabs-scan"], 1, 2),
    ("web technology fingerprint on example.com", ["whatweb"], 1, 2),
    ("tech stack detection on example.com", ["whatweb"], 1, 2),
    ("cdn detection for cdn.example.com", ["curl"], 1, 2),

    # ------------------------------------------------------------------
    # 20. Complex / Professional OSINT Workflows (12)
    # ------------------------------------------------------------------
    ("full external osint assessment on example.com", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 7),
    ("comprehensive passive recon on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("multi vector external recon on example.com", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 7),
    ("initial access osint on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("pre engagement osint on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 4, 6),
    ("attack surface mapping for example.com", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 7),
    ("osint profiling on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("adversary recon on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("full scope osint engagement on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("reconnaissance lifecycle on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("tier 1 osint collection on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
    ("zero touch osint automation on example.com", ["whois", "dig", "curl", "subfinder", "amass", "whatweb"], 5, 8),
]


def main():
    planner = RegistryPlanner()
    planner.build_index(AVAILABLE_TOOLS)

    passed = 0
    failed = 0
    failures = []

    print(f"\n{'='*60}")
    print(f"  OSINT EVALUATION: {len(OSINT_COMMANDS)} Commands")
    print(f"{'='*60}\n")

    for idx, (cmd, expected_tools, min_steps, max_steps) in enumerate(OSINT_COMMANDS):
        ok, msg = check_plan(planner, cmd, expected_tools, min_steps, max_steps)
        if ok:
            passed += 1
        else:
            failed += 1
            failures.append((cmd, msg))
        status = "PASS" if ok else "FAIL"
        print(f"  [{status:4s}] ({idx+1:3d}) {cmd:55s} → {msg}")

    print(f"\n{'='*60}")
    print(f"  RESULTS: {passed} passed, {failed} failed out of {len(OSINT_COMMANDS)}")
    print(f"  SCORE: {passed/len(OSINT_COMMANDS)*100:.1f}%")
    print(f"{'='*60}\n")

    if failures:
        print("FAILED COMMANDS:")
        for cmd, msg in failures:
            print(f"  - {cmd}")
            print(f"    Reason: {msg}")
        print()

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

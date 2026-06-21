"""Evaluation: 150+ reconnaissance commands from basic to advanced."""

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
]


def check_plan(goal: str, expected_tools: list[str], min_steps: int = 1,
               max_steps: int | None = None) -> bool:
    p = RegistryPlanner()
    p.build_index(AVAILABLE_TOOLS)
    plan = p.decompose_goal(goal)
    actual_tools = [s.tool for s in plan.steps]
    step_count = len(plan.steps)
    if step_count < min_steps:
        return False
    if max_steps and step_count > max_steps:
        return False
    for et in expected_tools:
        if et not in actual_tools:
            return False
    return True


def run_tests():
    passed = 0
    failed = 0
    failures = []

    # Format: (command, [expected tools], min_steps, max_steps)

    tests = [
        # ============ SECTION 1: BASIC RECON (20) ============
        ("check headers of https://example.com", ["curl"], 1, 2),
        ("scan ports on 10.0.0.1", ["nmap"], 1, 2),
        ("dns enumeration on example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
        ("whois lookup for example.com", ["whois"], 1, 2),
        ("find tech stack on example.com", ["whatweb"], 1, 2),
        ("check http://example.com security headers", ["curl"], 1, 2),
        ("wordpress scan on https://example.com", ["wpscan"], 1, 2),
        ("cms detection on https://example.com", ["whatweb"], 1, 2),
        ("enumerate directories on https://example.com", ["gobuster"], 1, 2),
        ("fuzz endpoints on https://example.com", ["ffuf"], 1, 2),
        ("ping sweep on 10.0.0.0/24", ["nmap"], 1, 2),
        ("find live hosts on 192.168.1.0/24", ["nmap"], 1, 2),
        ("tcp scan on 10.0.0.1", ["nmap"], 3, 6),
        ("udp scan on 10.0.0.1", ["nmap"], 1, 2),
        ("service version scan on 10.0.0.1", ["nmap"], 1, 2),
        ("ssl check on https://example.com", ["openssl", "nmap"], 2, 4),
        ("tls cipher scan on example.com", ["openssl", "nmap"], 2, 4),
        ("certificate info for https://example.com", ["openssl"], 1, 2),
        ("mx record lookup for example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
        ("dns resolution for example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),

        # ============ SECTION 2: WEB RECON (20) ============
        ("cors check on https://example.com", ["curl"], 1, 3),
        ("cookie analysis on https://example.com", ["curl"], 1, 2),
        ("redirect chain for https://example.com", ["curl"], 1, 2),
        ("waf detection on https://example.com", ["nmap"], 1, 2),
        ("cdn detection for https://example.com", ["curl"], 1, 2),
        ("api endpoint check on https://example.com", ["curl"], 1, 2),
        ("graphql introspection on https://example.com", ["curl"], 1, 2),
        ("swagger discovery on https://example.com", ["curl"], 1, 2),
        ("websocket upgrade check on https://example.com", ["curl"], 1, 2),
        ("check for exposed .git on https://example.com", ["curl"], 1, 2),
        ("check oauth endpoints on https://example.com", ["nmap"], 1, 2),
        ("exposed panel scan on https://example.com", ["nuclei"], 1, 2),
        ("ssrf check on https://example.com", ["nuclei"], 1, 2),
        ("idor scan on https://example.com/api", ["nuclei"], 1, 2),
        ("lfi scan on https://example.com/page", ["nuclei"], 1, 2),
        ("rfi scan on https://example.com/page", ["nuclei"], 1, 2),
        ("clickjacking test on https://example.com", ["curl"], 1, 2),
        ("deserialization check on https://example.com", ["nuclei"], 1, 2),
        ("open redirect scan on https://example.com", ["nuclei"], 1, 2),
        ("broken access control check on https://example.com", ["nuclei"], 1, 2),

        # ============ SECTION 3: DNS RECON (15) ============
        ("full dns recon on example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
        ("dns zone transfer on example.com", ["dig"], 1, 2),
        ("axfr query for example.com", ["dig"], 1, 2),
        ("nameserver lookup for example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
        ("subdomain enumeration on example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),
        ("amass subdomain brute on example.com", ["amass"], 1, 2),
        ("dns record check for example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
        ("subdomain discovery for example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),
        ("dnsrecon on example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),
        ("dns resolution check on example.com", ["dig", "subfinder", "amass", "whois"], 3, 5),
        ("reverse dns lookup on 8.8.8.8", ["dig"], 1, 2),
        ("dns probe with dnsx on example.com", ["dnsx"], 1, 2),
        ("massdns on example.com with resolvers", ["massdns"], 1, 2),
        ("puredns resolve for example.com", ["puredns"], 1, 2),
        ("passive subdomain enum on example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),

        # ============ SECTION 4: NETWORK RECON (15) ============
        ("full port scan on 10.0.0.1", ["nmap"], 3, 6),
        ("stealth scan on 10.0.0.1", ["nmap"], 1, 2),
        ("host discovery on 192.168.1.0/24", ["nmap"], 1, 2),
        ("snmp enumeration on 10.0.0.1", ["nmap"], 1, 2),
        ("smtp server enum on mail.example.com", ["nmap"], 1, 2),
        ("imap enumeration on 10.0.0.1", ["nmap"], 1, 2),
        ("traceroute to example.com", ["tracert"], 1, 2),
        ("tracert to 8.8.8.8", ["tracert"], 1, 2),
        ("masscan full sweep on 10.0.0.0/16", ["masscan"], 1, 2),
        ("fast port scan on 10.0.0.1 top 1000", ["nmap"], 3, 6),
        ("aggressive scan on 10.0.0.1 all ports", ["nmap"], 1, 2),
        ("ipmi recon on 10.0.0.1", ["nmap"], 1, 2),
        ("live host discovery on 10.0.0.0/24", ["nmap"], 1, 2),
        ("check open ports on 10.0.0.1", ["nmap"], 3, 6),
        ("up hosts scan on 172.16.0.0/24", ["nmap"], 1, 2),

        # ============ SECTION 5: SSL/TLS RECON (10) ============
        ("full ssl audit on https://example.com", ["openssl", "nmap"], 2, 4),
        ("tls cipher suite check on example.com", ["openssl", "nmap"], 2, 4),
        ("heartbleed check on https://example.com", ["nmap"], 1, 2),
        ("ssl certificate chain validation for example.com", ["openssl", "nmap"], 2, 4),
        ("ssl labs scan for example.com", ["ssllabs-scan"], 1, 2),
        ("testssl full check on example.com", ["testssl.sh"], 1, 2),
        ("certificate transparency search for example.com", ["curl"], 1, 2),
        ("crtsh lookup for example.com", ["curl"], 1, 2),
        ("crt.sh certificate search for example.com", ["curl"], 1, 2),
        ("ssl cipher enum on example.com:443", ["openssl", "nmap"], 2, 4),

        # ============ SECTION 6: OSINT & EXTERNAL RECON (20) ============
        ("full osint recon on example.com", ["whois", "dig", "subfinder", "amass", "whatweb", "curl"], 4, 8),
        ("open source recon on example.com", ["whois", "dig", "subfinder", "amass", "whatweb", "curl"], 4, 8),
        ("theHarvester email osint on example.com", ["theHarvester"], 1, 2),
        ("shodan internet search for example.com", ["shodan"], 1, 2),
        ("censys search for example.com", ["censys"], 1, 2),
        ("the harvester recon for example.com", ["theHarvester"], 1, 2),
        ("external attack surface recon on example.com", ["shodan", "curl", "whatweb", "subfinder", "whois", "dig"], 4, 8),
        ("passive reconnaissance on example.com", ["whatweb", "subfinder", "dig", "whois", "openssl"], 3, 6),
        ("passive scan on 10.0.0.1", ["whatweb", "subfinder", "dig", "whois", "openssl"], 3, 6),
        ("google dorking for example.com", ["curl"], 1, 3),
        ("uncover search for example.com", ["uncover"], 1, 2),
        ("wayback machine urls for example.com", ["waybackurls"], 1, 2),
        ("gau url discovery for example.com", ["gau"], 1, 2),
        ("sherlock username search for johndoe", ["sherlock"], 1, 2),
        ("holehe email check for user@example.com", ["holehe"], 1, 2),
        ("maigret user search for johndoe", ["maigret"], 1, 2),
        ("whois domain registration lookup for example.com", ["whois"], 1, 2),
        ("reverse whois search for example.com", ["whois"], 1, 2),
        ("asn ownership recon on AS12345", ["whois"], 1, 2),
        ("email osint harvesting for example.com", ["theHarvester"], 1, 2),

        # ============ SECTION 7: ACTIVE DIRECTORY RECON (15) ============
        ("active directory assessment on 10.0.0.1", ["nmap"], 2, 5),
        ("ad recon on domain controller 10.0.0.5", ["nmap"], 2, 5),
        ("ldap enum on 10.0.0.1", ["nmap"], 1, 2),
        ("kerberos user enum on 10.0.0.1", ["nmap"], 1, 2),
        ("smb share enum on 10.0.0.1", ["nmap"], 1, 5),
        ("smb enum on windows server 10.0.0.1", ["nmap"], 1, 5),
        ("netbios scan on 10.0.0.1", ["nmap"], 1, 5),
        ("responder capture on eth0", ["responder"], 1, 2),
        ("impacket enumeration on dc.example.com", ["impacket"], 1, 2),
        ("enum4linux recon on 10.0.0.1", ["nmap"], 1, 5),
        ("ldap domain dump on dc.example.com", ["nmap"], 1, 2),
        ("samba recon on 10.0.0.1", ["nmap"], 1, 5),
        ("crackmapexec smb enum on 10.0.0.1", ["nmap"], 1, 5),
        ("netexec ad recon on 10.0.0.1", ["nmap"], 1, 5),
        ("adcs enumeration on dc.example.com", ["nmap"], 1, 3),

        # ============ SECTION 8: CLOUD RECON (15) ============
        ("cloud audit on https://example.com", ["curl", "whatweb", "dig", "openssl"], 3, 5),
        ("aws metadata check on http://169.254.169.254", ["curl", "whatweb", "dig", "openssl"], 3, 5),
        ("azure metadata check on 169.254.169.254", ["curl", "whatweb", "dig", "openssl"], 3, 5),
        ("gcp metadata check on metadata.google.internal", ["curl", "whatweb", "dig", "openssl"], 3, 5),
        ("cloudfront detection for example.com", ["curl"], 1, 2),
        ("s3 bucket enumeration for example", ["curl", "whatweb", "dig", "openssl"], 3, 5),
        ("cloud storage audit on example", ["whatweb"], 1, 3),
        ("scoutsuite cloud audit for aws", ["scoutsuite"], 1, 2),
        ("prowler aws security audit", ["prowler"], 1, 2),
        ("cdn detection for cdn.example.com", ["curl"], 1, 2),
        ("azure blob check on https://test.blob.core.windows.net", ["curl", "whatweb", "dig", "openssl"], 3, 5),
        ("gcp bucket scan on storage.googleapis.com", ["curl", "whatweb", "dig", "openssl"], 3, 5),
        ("docker discovery on 10.0.0.1:2375", ["nmap"], 1, 2),
        ("kubernetes discovery on k8s.example.com", ["nmap"], 1, 2),
        ("jenkins discovery on jenkins.example.com", ["nmap"], 1, 2),

        # ============ SECTION 9: ADVANCED WEB RECON (15) ============
        ("http probe with httpx on https://example.com", ["httpx"], 1, 2),
        ("web crawl with katana on https://example.com", ["katana"], 1, 2),
        ("spider with gospider on https://example.com", ["gospider"], 1, 2),
        ("subdomain takeover check on example.com", ["subjack"], 1, 2),
        ("arjun parameter discovery on https://example.com", ["arjun"], 1, 2),
        ("paramspider mining on example.com", ["paramspider"], 1, 2),
        ("directory busting on https://example.com", ["gobuster"], 1, 2),
        ("fuzz with ffuf on https://example.com/FUZZ", ["ffuf"], 1, 2),
        ("screenshot web on https://example.com", ["eyewitness"], 1, 2),
        ("trufflehog secret scan on repo", ["trufflehog"], 1, 2),
        ("gitleaks scan on repo", ["gitleaks"], 1, 2),
        ("web app scan on https://example.com", ["curl", "whatweb", "nuclei", "ffuf", "wpscan", "nikto"], 4, 7),
        ("cms detection on https://example.com", ["whatweb"], 1, 2),
        ("nikto vulnerability scan on https://example.com", ["nikto"], 1, 2),
        ("exposed panels scan on https://example.com", ["nuclei"], 1, 2),

        # ============ SECTION 10: DATABASE & MIDDLEWARE RECON (12) ============
        ("redis enumeration on 10.0.0.1:6379", ["nmap"], 1, 2),
        ("mongodb enum on 10.0.0.1:27017", ["nmap"], 1, 2),
        ("mysql scan on 10.0.0.1:3306", ["nmap"], 1, 2),
        ("mssql discovery on 10.0.0.1:1433", ["nmap"], 1, 2),
        ("elasticsearch discovery on 10.0.0.1:9200", ["nmap"], 1, 2),
        ("memcached discovery on 10.0.0.1:11211", ["nmap"], 1, 2),
        ("kafka discovery on 10.0.0.1:9092", ["nmap"], 1, 2),
        ("activemq discovery on 10.0.0.1:61616", ["nmap"], 1, 2),
        ("cassandra scan on 10.0.0.1:9042", ["nmap"], 1, 2),
        ("postgresql enum on 10.0.0.1:5432", ["nmap"], 1, 2),
        ("rabbitmq discovery on 10.0.0.1:5672", ["nmap"], 1, 2),
        ("graphql endpoint check on https://example.com/graphql", ["curl"], 1, 2),

        # ============ SECTION 11: MULTI-STEP & COMPOUND RECON (15) ============
        # Multi-intent with "then" splits correctly
        ("enumerate subdomains then scan ports on example.com", ["subfinder", "nmap"], 2, 7),
        ("whois lookup then ssl check on example.com", ["whois", "openssl"], 2, 5),
        # Single intent with "and" picks best template
        ("find tech stack and check headers on https://example.com", ["whatweb"], 1, 3),
        ("dns recon and port scan on example.com", ["dig", "subfinder", "amass", "whois"], 3, 6),
        ("subdomain enum and web screenshot on example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),
        ("check ports and tech stack on example.com", ["whatweb"], 1, 2),
        ("full recon on example.com", ["nmap", "whatweb", "curl", "nuclei", "gobuster", "dig", "subfinder", "whois"], 5, 10),
        ("comprehensive recon on example.com", ["nmap", "whatweb", "curl", "nuclei", "gobuster", "dig", "subfinder", "whois"], 5, 10),
        ("thorough recon on example.com", ["nmap", "whatweb", "curl", "nuclei", "gobuster", "dig", "subfinder", "whois"], 5, 10),
        ("full recon and vuln scan on example.com", ["nuclei", "nikto", "wpscan", "sqlmap"], 3, 5),
        ("passive recon and dns enum on example.com", ["nmap", "whatweb", "gobuster", "subfinder", "amass", "nuclei"], 4, 7),
        ("network scan and service detection on 10.0.0.1", ["nmap"], 3, 6),
        ("web audit and directory enum on https://example.com", ["curl", "whatweb", "nuclei", "ffuf", "wpscan", "nikto"], 4, 8),
        ("smb enum and ldap check on 10.0.0.1", ["nmap"], 2, 6),
        ("cloud audit and cdn check on https://example.com", ["curl", "whatweb", "dig", "openssl"], 3, 5),

        # ============ SECTION 12: SPECIALIZED / EDGE CASE RECON (12) ============
        ("quick check on https://example.com", ["curl"], 1, 2),
        ("stealth network scan on 10.0.0.1", ["nmap"], 3, 6),
        ("interactsh oob testing client", ["interactsh"], 1, 2),
        ("httpx probe on https://example.com", ["httpx"], 1, 2),
        ("dnsx query on example.com", ["dnsx"], 1, 2),
        ("waybackurls discovery on example.com", ["waybackurls"], 1, 2),
        ("gau wayback url discovery for example.com", ["gau"], 1, 2),
        ("broken access control scan on https://example.com", ["nuclei"], 1, 2),
        ("zone transfer test on example.com", ["dig"], 1, 2),
        ("oauth endpoint enum on https://example.com", ["nmap"], 1, 2),
        ("smtp user enum on mail.example.com", ["nmap"], 1, 2),
        ("snmpwalk on 10.0.0.1 community public", ["nmap"], 1, 2),

        # ============ SECTION 13: CVE & VULN-SPECIFIC RECON (12) ============
        ("log4j check on https://example.com", ["nuclei"], 1, 2),
        ("heartbleed test on https://example.com", ["nmap"], 1, 2),
        ("shellshock scan on https://example.com", ["nuclei"], 1, 2),
        ("spring4shell check on https://example.com", ["nuclei"], 1, 2),
        ("struts vulnerability scan on https://example.com", ["nuclei"], 1, 5),
        ("searchsploit apache 2.4.49", ["searchsploit"], 1, 2),
        ("exploit search for wordpress 5.8", ["searchsploit"], 1, 2),
        ("cve scan on https://example.com", ["nuclei"], 1, 5),
        ("vuln scan on https://example.com", ["nuclei"], 1, 5),
        ("check cve-2021-44228 on https://example.com", ["nuclei"], 1, 2),
        ("check cve-2014-0160 on https://example.com", ["nmap"], 1, 2),
        ("check cve-2017-5638 on https://example.com", ["nuclei"], 1, 2),

        # ============ SECTION 14: PARAMETERIZED RECON (8) ============
        ("port scan on 10.0.0.1 ports 80,443,8080", ["nmap"], 3, 6),
        ("dns enumeration on example.com with verbose output", ["dig", "subfinder", "amass", "whois"], 3, 5),
        ("whois lookup on example.com with json output", ["whois"], 1, 2),
        ("fast port scan on 10.0.0.1 with nmap", ["nmap"], 3, 6),
        ("stealth tcp scan on 10.0.0.1", ["nmap"], 3, 6),
        ("nmap aggressive scan on 10.0.0.1 all ports", ["nmap"], 1, 2),
        ("detailed ssl audit on https://example.com with cipher enum", ["openssl", "nmap"], 2, 4),
        ("full port scan with service version on 10.0.0.1", ["nmap"], 3, 6),

        # ============ SECTION 15: SEARCH ENGINE & CERTIFICATE RECON (6) ============
        ("searchsploit search for kernel exploits", ["searchsploit"], 1, 2),
        ("exploit search for remote code execution", ["searchsploit"], 1, 2),
        ("certificate transparency log inspection for example.com", ["curl"], 1, 2),
        ("crtsh domain search for example.com", ["curl"], 1, 2),
        ("ssl certificate info for https://example.com", ["openssl", "nmap"], 2, 4),
        ("certificate chain validation for example.com", ["openssl"], 1, 2),
    ]

    total = len(tests)

    for i, (cmd, expected, min_steps, max_steps) in enumerate(tests, 1):
        try:
            result = check_plan(cmd, expected, min_steps, max_steps)
            if result:
                passed += 1
            else:
                failed += 1
                failures.append(cmd)
        except Exception as e:
            failed += 1
            failures.append(f"{cmd} (ERROR: {e})")

    print(f"\n{'='*60}")
    print(f"RECON EVALUATION RESULTS: {passed} passed, {failed} failed out of {total}")
    print(f"{'='*60}")

    if failures:
        print(f"\nFAILED COMMANDS ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")

        print(f"\nDebug: checking actual plans...")
        p = RegistryPlanner()
        p.build_index(AVAILABLE_TOOLS)
        for cmd in failures[:15]:
            try:
                plan = p.decompose_goal(cmd)
                tools = [s.tool for s in plan.steps]
                print(f"  {cmd:60s} -> steps={len(tools):2d}, tools={tools}")
            except Exception as e:
                print(f"  {cmd:60s} -> ERROR: {e}")

    return passed, failed, total


if __name__ == "__main__":
    import sys
    passed, failed, total = run_tests()
    sys.exit(0 if failed == 0 else 1)

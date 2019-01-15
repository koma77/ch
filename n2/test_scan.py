from __future__ import print_function
import sys, json
import urllib
import scan


images = """
[
  {
   "Organisation":"coreos",
   "Repository":"hyperkube",
   "Tag":"v1.10.4_coreos.0"
  }
]
"""


pkg = """
  {
      "AddedBy": "64024fc848dcf4ed52afda037ce3bed83b62c2d08b07f4423b78f15f315dae7a.b76bd06f-d229-4fef-be46-d3b5f083e5dc", 
      "Name": "ipset", 
      "NamespaceName": "debian:9", 
      "Version": "6.30-2", 
      "VersionFormat": "dpkg"
  }
"""

vuln = """
  {
      "Link": "https://security-tracker.debian.org/tracker/CVE-2011-3374", 
      "Name": "CVE-2011-3374", 
      "NamespaceName": "debian:9", 
      "PackageName": "apt", 
      "Severity": "Negligible"
  }
"""

image_sha = "sha256:ced8ba1345b8fef845ab256b7b4d0634423363721afe8f306c1a4bc4a75d9a0c"

def err(txt):
    print(txt)
    exit(1)

in_json = json.loads(images)

repo_json = scan.get_repo_info(in_json[0]["Organisation"],in_json[0]["Repository"])

if in_json[0]["Tag"] in repo_json["tags"]:
    print("get_repo_info: OK")
else:
    err("get_repo_info: ERR")

secscan_json = scan.get_secscan(in_json[0]["Organisation"],in_json[0]["Repository"], image_sha)

pkg_json = json.loads(pkg)

if pkg_json in secscan_json["data"]["Layer"]["Features"]:
    print("get_sec_scan: OK")
else:
    err("get_secscan: ERR")


vuln_json = json.loads(vuln)

img_info_json = scan.img_info(in_json)

if vuln_json in img_info_json[0]["Vulnerabilities"]:
    print("main: OK")
else:
    err("main: ERR") 


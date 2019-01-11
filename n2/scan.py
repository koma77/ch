'''
program expects json on stdin:

[
  {
   "Organisation":"coreos",
   "Repository":"hyperkube",
   "Tag":"v1.10.4_coreos.0"
  },
  {
   "Organisation":"coreos",
   "Repository":"dnsmasq",
   "Tag":"v0.5.0"
  }
]
'''

from __future__ import print_function
import sys, json
import urllib

# https://quay.io/api/v1/repository/coreos/hyperkube?includeTags=true
REPO_INFO="https://quay.io/api/v1/repository/{}/{}?includeTags=true"
# https://quay.io/api/v1/repository/coreos/dnsmasq/manifest/sha256%3A910710beddb9cf3a01fe36450b4188b160a03608786c11e0c39b81f570f55377/security?vulnerabilities=true
SECSCAN="https://quay.io/api/v1/repository/{}/{}/manifest/{}/security?vulnerabilities=true"

def err(txt):
    print(txt, file=sys.stderr)

def call_api(url):
    try:
        r = urllib.urlopen(url)
        if r.getcode() == 200:
            return json.loads(r.read())
    except IOError, e:
        err(e)

def get_repo_info(org, repo):
    res = call_api(REPO_INFO.format(org, repo))
    if res:
        return res

def get_secscan(org, repo, img_sha):
    res = call_api(SECSCAN.format(org, repo, img_sha))
    if res:
        return res

def get_vulns(scan):
    if scan["status"].upper() == "SCANNED":
        res = []
        for f in scan["data"]["Layer"]["Features"]:
            if "Vulnerabilities" in f:
                for v in f["Vulnerabilities"]:
                    v.update(PackageName = f["Name"])
                    if "Description" in v:
                        del v["Description"]
                    res.append(v)
    else:
        return []
    return res

try:
  images = json.load(sys.stdin)
except ValueError, e:
  err(e) 
  sys.exit(1)

#json.dumps(images)
#print(json.dumps(images, indent=4, sort_keys=True))

res = []

for img in images:
    org, repo, tag = img["Organisation"], img["Repository"], img["Tag"]
    #print "{}/{}:{}".format(org, repo, tag)
    repo_info = get_repo_info(org, repo)
    if repo_info:
        if tag in repo_info["tags"]:
            img_info = repo_info["tags"][tag]
            img_sha = img_info["manifest_digest"]
            if img_sha:
                img.update(Manifest = img_info["manifest_digest"])
                scan = get_secscan(org, repo, img_sha)
                vulns = get_vulns(scan)
                img.update( Vulnerabilities = vulns)
            res.append(img)
        else:
            err("Could not find specified tag: {}/{}:{}".format(org, repo, tag))
    else:
        err("Could not get repo info: {}/{}".format(org, repo))

print(json.dumps(res, indent=4, sort_keys=True))


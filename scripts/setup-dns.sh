#!/usr/bin/env bash
# Point climb29ers.com at the Vercel project once the domain exists in Cloudflare.
#
# Usage:
#   export CF_API_TOKEN=...      # Cloudflare token with Zone:Read + DNS:Edit
#   ./scripts/setup-dns.sh
#
# Records are created DNS-only (proxied=false): Vercel terminates TLS itself, and
# Cloudflare's proxy in front of it causes redirect loops and cert-issuance failures.
set -euo pipefail

DOMAIN="climb29ers.com"
A_IPS=("216.150.1.1" "216.150.16.1")
WWW_CNAME="c3b3a2f17a1209ac.vercel-dns-016.com"

: "${CF_API_TOKEN:?set CF_API_TOKEN first}"
api() { curl -sS -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" "$@"; }

ZONE_ID=$(api "https://api.cloudflare.com/client/v4/zones?name=$DOMAIN" |
  python3 -c "import json,sys; r=json.load(sys.stdin)['result']; print(r[0]['id'] if r else '')")
[ -n "$ZONE_ID" ] || { echo "No Cloudflare zone for $DOMAIN — is it registered on this account?" >&2; exit 1; }
echo "zone: $ZONE_ID"

upsert() {  # type name content
  local type=$1 name=$2 content=$3
  local id
  id=$(api "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?type=$type&name=$name" |
    python3 -c "import json,sys; r=json.load(sys.stdin)['result']; print(r[0]['id'] if r else '')")
  local body
  body=$(python3 -c "import json,sys; print(json.dumps({'type':sys.argv[1],'name':sys.argv[2],'content':sys.argv[3],'ttl':1,'proxied':False}))" "$type" "$name" "$content")
  if [ -n "$id" ]; then
    api -X PUT -d "$body" "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$id" >/dev/null
    echo "updated $type $name -> $content"
  else
    api -X POST -d "$body" "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" >/dev/null
    echo "created $type $name -> $content"
  fi
}

upsert A "$DOMAIN" "${A_IPS[0]}"
upsert CNAME "www.$DOMAIN" "$WWW_CNAME"

echo
echo "Done. Vercel issues the certificate once DNS propagates (usually a minute or two):"
echo "  curl -sI https://$DOMAIN | head -1"

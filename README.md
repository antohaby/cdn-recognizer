# CDN Finder for url

This service can recognize what CDNS are using in given URL.
This was made as test work and will be improved.

## HowTo

* docker-compose up -d
* POST http://localhost:8080/recognize/cdns
Headers:
`
Content-Type : application/json
`
Body:
`
{
  "url": "http://www.funnygames.at"
}
`

*Response:*
`
{
    "www.funnygames.at": "Cloudflare",
    "cdnjs.cloudflare.com": "Cloudflare",
    "s7.addthis.com": null,
    "assets.funnygames.at": "OptimiCDN"
}
`
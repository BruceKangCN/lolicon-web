# Lolicon Web

a web API simplifies original lolicon API, using API from [Lolicon API](https://api.lolicon.app/#/setu)

## Application configurations

configurations can be set in `/etc/lolicon/config.toml`, the following settings will be used by app:

- `api_url`: str - Lolicon API URL
- `size`: str - which key to use for getting image URL in object `urls` in response from Lolicon API

the following fields in `params` section are supported and can be used to set POST parameters for Lolicon API:

- `r18`
- `num`
- `size`
- `proxy`
- `uid`
- `tag`
- `dateAfter`
- `dateBefore`

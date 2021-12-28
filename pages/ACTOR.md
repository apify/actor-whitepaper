# .actor/actor.json

File `.actor/actor.json

```json
{
    "formatVersion": 2,
    "name": "google-search-scraper",
    "title": "Google Search Scraper",
    "description": "The 200-char description",
    "version": "0.0",
    "buildTag": "latest",
    "env": {
        "MYSQL_USER": "my_username",
        "MYSQL_PASSWORD": "@mySecretPassword"
    }
}
```

Notes compared to the previous version
- Removed `template` property as its not needed for anything, it only stored the original template
- Added `title`
    - We're pushing towards having human readable names shown for actors everywhere 
      so we should probably let users define it here, even if they run this code outside of Apify.
    - TODO: But shall the text from here overwrite changes done manually by copywriter? Probably not, so what's the purpose of having these here?
- No `username` in `name` as actor can be deployed to any account.
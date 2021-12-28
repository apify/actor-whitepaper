# `.ACTOR/actor.json`

This JSON file is the main definition of the actor.

```json
{
  "formatVersion": 2,
  "name": "bob/google-search-scraper",
  "title": "Google Search Scraper",
  "version": "0.0",
  "buildTag": "latest",
  "env": {
    "MYSQL_USER": "my_username",
    "MYSQL_PASSWORD": "@mySecretPassword"
  },
  "datasetSchema": "./schemas/DATASET_SCHEMA.json",
  "keyValueStoreSchema": "./schemas/KEY_VALUE_STORE_SCHEMA.json",
  "requestQueueSchema": "./schemas/REQUEST_QUEUE_SCHEMA.json",

  "inputSchema": "./schemas/DATASET_SCHEMA.json",
  "outputSchema": "./schemas/KEY_VALUE_STORE_SCHEMA.json",
  
  "description": "The 200-char description"
}
```


This replaces the legacy `apify.json` file. Change notes compared to the previous version:

- Removed `template` property as it's not needed for anything, it only stored the original template
- We're pushing towards having human-readable names shown for actors everywhere,
      so it makes sense to define `title` directly in the source code.
- For `description`, it might be preferable to keep text
      with overwritten changes done manually by a copywriter. `apify push` has options
      `--keep-description` and `--keep-title` 
- Username can be present in `name` to establish a strong link between the source code
  and the actor on Apify. This is consistent with `version` and `buildTag`,
  which is also user-specific.
  We want developers of the actors be the ones to own and be in charge of them,
  take care of them being running them by default.
  The username can be `@me`, and
 `apify push` can have option `--target=eva/my-actor:0.0` that will deploy the actor under a different
  user account
- `datasetSchema` and `keyValueStoreSchema` link to the schema objects required
  by the actor

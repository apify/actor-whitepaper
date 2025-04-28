# Key-value store schema file specification [work in progress]

This JSON file should contain schema for files stored in the key-value store,
defining their name, format, or content type.

**BEWARE: This is currently not implemented yet and subject to change.**

## Basic properties

Key-value store schema has two main use cases described in the following examples:

1. Some Actors such as [Instagram scraper](https://apify.com/jaroslavhejlek/instagram-scraper)
store multiple types of files into the key-value store. Let's say the scraper stores images and user pictures.
So for each of these, we would define a prefix group called collection and allow the user to list images from a single collection in both the
UI and API.

```jsonc
{
   "collections": {
      "screenshots": {
            "name": "Post images",
            "keyPrefix": "images-",
            "contentTypes": ["image/jpeg", "image/png"]
       }
   }
}
```

2. Some Actor stores a specific record, and we want to ensure the content type to be HTML and embed it into the run view.
A good example is [monitoring](https://apify.com/apify/monitoring#check-frequency) Actor that generates HTML report that we would
like to embed to run view for the user once the monitoring is finished.

```jsonc
{
    "collections": {
        "monitoringReport": {
            "name": "Monitoring report",
            "description": "HTML page containing monitoring results",
            "key": "REPORT",
            "contentTypes": ["text/html"]
        }
    }
}
```

3. Some Actors store a record that has a specific structure. The structure can be specified using [JSON schema](https://json-schema.org/draft-07).
Contrary to dataset schema, the record in key-value store represents output that is a single item, instead of a sequence of items. But both approaches use JSON schema to describe the structure.

```jsonc
{
    "collections": {
        "monitoringReportData": {
            "name": "Monitoring report data",
            "description": "JSON containing the report data",
            "key": "report-data.json",
            "contentTypes": ["application/json"],
            "jsonSchema": {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "properties": {
                    "summary": { "type": "string" },
                    "totalResults": { "type": "number" }
                }
            } // alternatively "jsonSchema": "./report-schema.json" can be used
        }
    }
}
```

## Structure

```jsonc
{
    "actorKeyValueStoreSchemaVersion": 1,
    "name": "My Instagram backup",
    "description": "Backup of my Instagram account",
    
    "collections": {
        "postImages": {
            "name": "Post images",
            "description": "Contains all Instagram post images",
            "keyPrefix": "post-image-",
            "contentTypes": ["image/jpeg", "image/png"]
        },

        "profilePicture": {
            "name": "Profile picture",
            "key": "profile-picture",
            "contentTypes": ["image/*"] // Be able to enable all images or text types etc.
        }
    }
}
```

## API implications

Enable user to list keys for specific collection:

```
https://api.apify.com/v2/key-value-stores/storeId/keys?collection=postImages&exclusiveStartKey=xxx
```

In addition to this user will be able to list by prefix directly:

```
https://api.apify.com/v2/key-value-stores/storeId/keys?prefix=post-images-
```

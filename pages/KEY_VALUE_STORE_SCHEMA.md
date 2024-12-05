# Key-value store schema file specification [work in progress]

This JSON file should contain schema for files stored in the key-value store,
defining their name, format, or content type.

**BEWARE: This is currently not implemented yet and subject to change.**

## Basic properties

Key-value store schema has two main use cases described in the following examples:

1. Some Actors such as [Instagram scraper](https://apify.com/jaroslavhejlek/instagram-scraper)
store multiple types of files into the key-value store. Let's say the scraper stores images and user pictures.
So for each of these, we would define a prefix group and allow the user to list images from a single group in both the
UI and API.

```jsonc
{
   "collections": {
      "screenshots": {
            "name": "Post images",
            "keyPrefixes": ["images-"],
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

For more information on how to create a key-value store with a schema, see [DATASET_SCHEMA.json](./DATASET_SCHEMA.md)
as the implementation and API will be the same.

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

Enable user to list keys for specific record group:

```
https://api.apify.com/v2/key-value-stores/storeId/keys?recordGroup=postImages&exclusiveStartKey=xxx
```

In addition to this user will be able to list by prefix directly:

```
https://api.apify.com/v2/key-value-stores/storeId/keys?prefix=post-images-
```

## TODO(@jancurn)
- Finalize this text, keep `collections` for now
- What is kv-store schema is used by Actor to define structure of key-value store it operates on,
  but the developer defines a non-compatible record group for "INPUT" prefix?
  Maybe the default kv-stores should be created with a default record group to cover the "INPUT" prefixes
  and give them JSON types. Then, we'd never need to worry about existing records.
  But it's a breaking change for some Actors... maybe we can only do this for V2 Actors with Actor file...
  ... it's getting quite complicated.
- What if there's a conflict between record groups?
  Shall we consider the first one matching as if the file is valid for schema?

... just add a note that these conflicting situations are unspecified behavior

# Key-value Store Schema File

## Basic properties

Key-value store schema has two main use cases described in the following examples:

1. Some actors such as [Instagram scraper](https://apify.com/jaroslavhejlek/instagram-scraper)
store multiple types of files into the key-value store. Let's say the scraper stores images and user pictures.
So for each of these, we would define a prefix group and allow the user to list images from a single group in both the
UI and API.

```json
{
   "recordGroups": {
      "screenshots": {
            "name": "Post images",
            "keyPrefix": "images-",
            "contentTypes": ["image/jpeg", "image/png"]
       }
   }
}
```

2. Some actor stores a specific record, and we want to ensure the content type to be HTML and embed it into the run view.
A good example is [monitoring](https://apify.com/apify/monitoring#check-frequency) actor that generates HTML report that we would
like to embed to run view for the user once the monitoring is finished.

```json
{
    "recordGroups": {
        "report": {
            "name": "Monitoring report",
            "description": "HTML page containing monitoring results",
            "key": "REPORT",
            "contentTypes": ["text/html"],
        },
    }
}
```

For more information on how to create a key-value store with a schema, see [DATASET_SCHEMA.json](./DATASET_SCHEMA.md)
as the implementation and API will be the same.

## Structure

```json
{
    "formatVersion": 2,
    "name": "My Instagram backup",
    "description": "Backup of my Instagram account",
    
    "recordGroups": {
        "postImages": {
            "name": "Post images",
            "description": "Contains all Instagram post images",
            "keyPrefix": "post-image-",
            "contentTypes": ["image/jpeg", "image/png"]
        }

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

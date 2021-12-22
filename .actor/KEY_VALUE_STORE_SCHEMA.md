# Key-value store schema

## Use cases

Key-value store schema has 2 main usecases described here at following examples. 

1. Some actor such as [Instagram scraper](https://apify.com/jaroslavhejlek/instagram-scraper)
store multiple types of files into the key-value store. Let's say the scraper stores images and user pictures.
So for each of these we would define a prefix group and allow user to list images from a single group in both
UI and API.

```
{
    "prefixGroups": {
        "images": {
            "name": "Post images",
            "prefix": "images-",
            "contentTypes": ["image/jpeg", "image/png"]
        },
        "userPictures": {
            "name": "User pictures",
            "prefix": "user-pictures-",
            "contentTypes": ["image/jpeg", "image/png"]
        }
    }
}
```

2. Some actor stores certain record and we want to ensure the content type to be for example HTML and embed it into the run view.
The good example is [monitoring](https://apify.com/apify/monitoring#check-frequency) actor that generates HTML report that we would
like to embed to run view for user once the monitoring finished.

```
    "records": {
        "report": {
            "name": "Monitoring report",
            "description": "HTML page containing monitoring results",
            "contentTypes": ["text/html"]
        }
    }
```

## Structure

```js
{
    formatVersion,
    name,
    description,
    
    prefixGroups,
    records,
}
```

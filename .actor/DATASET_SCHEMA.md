# Dataset schema

## Basic properties

Dataset schema describes:
- Content of the dataset, i.e. schema of objects that are allowed to be added
- Different views on how we can look at the data, AKA transformations
- Visualization of the view using predefined components (grid, table, ...) which improves the run view interface at Apify Console
  and also provides better interface for dasets shared by Apify users

<img src="https://user-images.githubusercontent.com/594801/147474979-a224008c-8cba-43a6-8d2e-c24f6b0d5b37.png" width="500">

Basic properties:
- It's immutable
    - If you want to change the structure then you need to create a new dataset
- It's weak
    - You can always push there additional properties but schema will enasure that all the listed once are there with a correct type
    - This is to make actors more compatible, i.e. some actor expects dataset to contain certain fields but does not care about the additional ones

There are two ways how to create a dataset with schema:
- User can start the actor that has dataset schema linked from its
[OUTPUT_SCHEMA.json](./OUTPUT_SCHEMA.md)
- Or user can do it pragmatically via API by
  - either passing schema as payload to [create dataset](https://docs.apify.com/api#/reference/datasets/dataset-collection/create-dataset) API endpoint
  - or using the SDK:

```js
const dataset = await Apify.openDataset('my-new-dataset', { schema });
```

This also esnures that you are opening dataset that is compatible with the actor as otherwise you get an error:

```
Uncaught Error: Dataset schema is not compatible with a given schema
```

## Structure

```js
{
    "formatVersion": 2,
    "name": "Eshop products",
    "description": "Dataset containing the whole product catalog including prices and stock availability.",
    "fields": {
        "title": "String",	
        "priceUsd": "Number",	
        "manufacturer": "Object",
        "manufacturer.title": "String",	
        "manufacturer.url": "Number",
        "productVariants": "Array",
        "productVariants.color": "String",	
        ...
    },
    "views": {
        "overview": {
            "name": "Products overview",
            "description": "Displays only basic fields such as title and price",
            "transformation": {
                // Comma separated arrays such as "fields" and "pick" will be written as arrays
                "fields": [
                    "title",
                    "price",
                    "picture"
                ]
            },
            "visualisation": {
                "component": "grid",
                "options": { "width": 6 },
                "properties": {
                    "title": "$title",
                    // We will need some templating here
                    "description": "${price} USD",
                    "pictureUrl": "$picture"
                }
            }
        }
        "productVariants": {
            "name": "Product variants",
            "description": "Each product expanded into item per variant",
            "transformation": {
                "fields": [
                    "title",
                    "price",
                    "productVariants"
                ],
                "unwind": "productVariants"

            },
            "visualisation": {
                // Simply renders all the available fields
                "component": "table"
            }
        }
    },
}
```

### Views's transformation

Transformation is a combination of a 
[GET dataset items](https://docs.apify.com/api#/reference/datasets/item-collection/get-items)
API endpoint parameters. This makes view usable in both UI and API
where the users can use it to preset the parameters easily, for example:

```
https://api.apify.com/v2/datasets/[ID]/items?format=[FORMAT]&view=searchResults
```

instead of this complicated URL in the case of [Google Search Scraper](https://apify.com/apify/google-search-scraper#how-to-get-one-search-result-per-row):

```
https://api.apify.com/v2/datasets/[ID]/items?format=[FORMAT]&fields=searchQuery,organicResults&unwind=organicResults
```

### View's visualisation

It's a triplet of `component`, `options` and `properties` (according to the ReactJS language) that maps dataset fields to template property names.

```
visualization: {
    component: 'grid',
    options: {
    	columns: 6,
    },
    properties: {
        image: '$image.href',
        title: '$title',
        url: '$field1.field2.url,
    }
}
```

## TODOs

- Do we need `description` and `name` here? Shouldn't we assign it a name when the schema is referenced in the `OUTPUT_SCHEMA.json`?
- Should one of the views be default?
- Perhaps the visualization's `properties` should be called `itemProperties` as it's not property of the whole component but one item

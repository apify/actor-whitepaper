# Dataset Schema File

TODO (@mtrunkat): Mara will finish the specs in this file to be accurate, Jan will polish the text then

Actor results can be saved to append-only object storage
called [Dataset](https://sdk.apify.com/docs/api/dataset),
which can be assigned a schema that ensures only objects with certain properties and types
are added to the dataset. 

The Dataset schema can be programmatically assigned to dataset on creation or when its empty dataset,
using the API.

**Dataset schema describes:**

- Content of the dataset, i.e., the schema of objects that are allowed to be added
- Different views on how we can look at the data, aka transformations
- Visualization of the View using predefined components (grid, table, ...), which improves the run view interface at Apify Console
  and also provides a better interface for datasets shared by Apify users

<img src="https://user-images.githubusercontent.com/594801/147474979-a224008c-8cba-43a6-8d2e-c24f6b0d5b37.png" width="500">

## Basic properties

- It's immutable
    - If you want to change the structure, then you need to create a new dataset
- It's weak
    - You can always push their additional properties, but schema will ensure that all the listed once are there with a correct type
    - This is to make actors more compatible, i.e., some actor expects dataset to contain certain fields but does not care about the additional ones

There are two ways how to create a dataset with schema:
- User can start the actor that has dataset schema linked from its
[OUTPUT_SCHEMA.json](./OUTPUT_SCHEMA.md)
- Or user can do it pragmatically via API (for empty dataset) by
  - either passing schema as payload to [create dataset](https://docs.apify.com/api#/reference/datasets/dataset-collection/create-dataset) API endpoint
  - or using the SDK:

```js
const dataset = await Apify.openDataset('my-new-dataset', { schema });
```

This also ensures that you are opening a dataset that is compatible with the actor as otherwise, you get an error:

```
Uncaught Error: Dataset schema is not compatible with the provided schema
```

## Structure

```jsonc
{
    "actorSpecification": 1,
    "title": "Eshop products", // optional
    "description": "Dataset containing the whole product catalog including prices and stock availability.", // optional
    "fields": { // not supported yer
        "title": "string",  
        "priceUsd": "number", 
        "manufacturer": {
            "title": "string", 
            "url": "number",
        },
        "productVariants": [{
            "color": "?string"
        }],
        
        ...
    },
    "views": {
        "overview": {
            "title": "Products overview", // optional
            "description": "Displays only basic fields such as title and price", // optional
            "transformation": {
                "flatten":[
                    "author"
                    "latestTweets",
                ],
                "fields": [
                    "author.name",
                    "latestTweets.0.tweet",
                    "someOtherField",
                    "anotherField",
                    "nonFlatenedObjectOrArray"
                ]
            },
            "display": {
                "component": "table",
                "properties": {
                    "author.name": {
                      "label": "Author"
                    },
                    "latestTweets.0.tweet": {
                      "label": "Latest tweet"
                    },
                    "nonFlatenedObjectOrArray":{
                      "label": "Meta"
                    }
                }
            }
        },
        "productVariants": {
            "title": "Product variants",
            "description": "Each product expanded into item per variant",
            "transformation": {
                "fields": [
                    "title",
                    "price",
                    "productVariants"
                ]
            },
            "display": {
                // Simply renders all the available fields. 
                // This component is used by default when no display is specified.
                "component": "table"
            }
        }
    },
}
```

## Fields


TODO(@mtrunkat): Please finish this part, we'll have to start with JSON schema before adding any other
. see https://github.com/apify/actor-specs/pull/7/files#r794764956 

One big TODO: What schema definition are we going to support? The most powerful and standardized but
slow to write is [JSON Schema](https://json-schema.org/). We could start with
the [Easy JSON Schema](https://github.com/easy-json-schema/easy-json-schema) and add support for JSON
Schema later, but in this case, we will need another property saying what schema is used.

NOTE JC: In any case, we need to support field types and required/optional.
Let's start with Easy JSON schema to keep things simple, we can extend in the future.

Here is a comparison of JSON Schema and Easy JSON Schema:

```jsonc
{
  "id": "string",
  "*name": "string",
  "*email": "string",
  "arr": [{
    "site": "string",
    "url": "string"
  }]
}
```

```jsonc
{
  "type": "object",
  "required": [
    "name",
    "email"
  ],
  "properties": {
    "id": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "email": {
      "type": "string"
    },
    "arr": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [],
        "properties": {
          "site": {
            "type": "string"
          },
          "url": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

## Views

Dataset view enables the user to explore certain data ways. For example the
[Google Search Scraper](https://apify.com/apify/google-search-scraper) enables the user to View 
the results in multiple ways:
- One item = one page with two embed arrays of organic results and ads
- One item = one organic results
- One item = one search result

The first View in the list is considered to be a default one.

### Views' transformation

Transformation is a combination of a 
[GET dataset items](https://docs.apify.com/api#/reference/datasets/item-collection/get-items)
API endpoint parameters. This makes View usable in both UI and API
where the users can use it to preset the parameters easily, for example:

```
https://api.apify.com/v2/datasets/[ID]/items?format=[FORMAT]&view=searchResults
```

instead of this complicated URL in the case of [Google Search Scraper](https://apify.com/apify/google-search-scraper#how-to-get-one-search-result-per-row):

```
https://api.apify.com/v2/datasets/[ID]/items?format=[FORMAT]&fields=searchQuery,organicResults&unwind=organicResults
```

And here is the description from the dataset schema:

```jsonc
  "transformation": {
      "fields": [
          "searchQuery",
          "organicResults"
      ],
      "unwind": "organicResults",
      "flatten": ["searchQuery"]
  },
```
**Nested objects**
In order to be able to properly and consistently display nested object data in Excel, CSV, Table UI etc. it is necessary to flatten or unwind the original object. 

Unwind deconstructs the nested children into parent object. eg: with transformation.unwind:[”foo”] the object ```{”foo”:{”bar”:”hello”}}``` is turned into ```{’bar”:”hello”}``` ( Please be aware that in case of the object key conflict, the existing key/value will be replaced by the new key/value )

Flatten transforms the nested object into flat structure. eg: with transformation.flatten:[”foo”] the object ```{”foo”:{”bar”:”hello”}}``` is turned into ```{’foo.bar”:”hello”}``` 

### Display of a view

It's a triplet of `component`, `options`, and `properties` (according to the ReactJS language) that maps dataset fields to template property names.

```
display: {
    component: "grid",
    options: {
      columns: 6,
    },
    properties: {
        "title":{
          position:"header"
        },
        "image.href":{
          position:"image"
        },
        "field1.field2.url":{
          position:"link"
        }
    }
}
```


## Dataset schema structure definitions

### DatasetSchema object definition

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| actorSpecification | integer | true | Specifies the version of dataset schema structure document. Currently only version 1 is available. |
| fields | JSONSchema compatible object | true | Schema of one dataset object. Use JsonSchema Draft 2020-12 or other compatible format. |
| views | DatasetView object | true | An object with description of an API and UI views |

### DatasetView object definition

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| title | string | true | The title is visible in UI in Output tab as well as in the API. |
| description | string | false | Description is only available in API response. Usage of this field is optional. |
| transformation | ViewTransformation object | true | The definition of data transformation which is applied when dataset data are loaded from Dataset API. |
| display | ViewDisplay object | true | The definition of Output tab UI visualisation. |

### ViewTransformation object definition

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| fields | string[] | true | Selects fields that is going to be presented on Output. An order of  the fields in matches the order of columns in visualisation UI. In case the fields value is missing it will be presented as “undefined” in UI. |
| unwind | string | false | Deconstructs the nested children into parent object. eg: with unwind:[”foo”] the object {”foo”:{”bar”:”hello”}} is turned into {’bar”:”hello”} |
| flatten | string[] | false | Transforms the nested object into flat structure. eg: with flatten:[”foo”] the object {”foo”:{”bar”:”hello”}} is turned into {’foo.bar”:”hello”} |
| omit | string | false | Removes the specified fields from the output. Nested fields names can used there as well. |
| limit | integer | false | Maximum number of results returned. Default is all results. |
| desc | boolean | false | By default results are sorted Ascending based on the write event into dataset. desc:true param will return the newest writes to dataset first. |

### ViewDisplay object definition

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| component | string | true | Only component “table” is available. |
| properties | Object with keys matching the Output object’s properties. Each one is configured using ViewDisplayProperty object. | false | In case properties are not set the table will be rendered automatically with fields formatted as Strings, Arrays or Objects. |

### ViewDisplayProperty object definition

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| label | string | false | In case the data are visualised as in Table view. Label will be visible table column’s header. |
| format | enum(text, number, date, boolean, image, array, object) | false | Describes how Output data values are formatted in order to be rendered in Output tab UI. |

## TODOs

- JSON schema specification (full or simple) above

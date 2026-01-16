# Dataset schema file specification 1.0

Dataset storage enables you to sequentially store and retrieve data records, in various formats.
Each Actor run is assigned its own dataset, which is created when the first item is stored to it.
Datasets usually contain results from web scraping, crawling or data processing jobs.
The data can be visualized as a table where each object is a row and its attributes are the columns.
The data can be exported in JSON, CSV, XML, RSS, Excel, or HTML formats.

The specification is also at https://docs.apify.com/platform/actors/development/actor-definition/output-schema 

Dataset can be assigned a schema which describes:

- Content of the dataset, i.e., the schema of objects that are allowed to be added
- Different views on how we can look at the data, aka transformations
- Visualization of the View using predefined components (grid, table, ...), which improves the run view interface at Apify Console
  and also provides a better interface for datasets shared by Apify users

<img src="https://user-images.githubusercontent.com/594801/147474979-a224008c-8cba-43a6-8d2e-c24f6b0d5b37.png" width="500">

<!-- ASTRO: <Picture src={illuDatasetSchema} alt="Dataset schema" formats={['avif', 'webp']} /> -->

## Basic properties

- Storage schema is immutable. I.e., if you want to change the structure, then you need to create a new dataset.
- Storage is append-only. I.e. you can only append new items to the dataset, but you cannot modify or delete items that are already present.

There are two ways how to create a dataset with schema:
1. User can start the Actor that has dataset schema linked from its
[OUTPUT_SCHEMA.json](./OUTPUT_SCHEMA.md)
2. Or user can do it pragmatically via API (for empty dataset) by
    - either by passing the schema as payload to [create dataset](https://docs.apify.com/api#/reference/datasets/dataset-collection/create-dataset) API endpoint.
    - or using the SDK:

    ```js
    const dataset = await Apify.openDataset('my-new-dataset', { schema });
    ```

By opening an **existing** dataset with `schema` parameter, the system ensures that you are opening a dataset that is compatible with the Actor as otherwise, you get an error:

```
Uncaught Error: Dataset schema is not compatible with the provided schema
```

### Extension: multiple datasets, dataset alias

By default, the Actor run is assigned a single dataset. If needed it's possible to specify more datasets (see [actor.json](./ACTOR_FILE.md)) that can be used to store the results.

The first of those specified datasets is treated as the "default" one when needed.

Those datasets can then be accessed using their `alias` (specified in the schema).

```js
const dataset = await Apify.openDataset({ alias: 'firstDatasetAlias' });
```

The difference between Dataset `alias` and `name` is that `alias` is local in the context of Actor run, whereas the `name` is global (eg. exists in user's workspace).

## Structure

```jsonc
{
    "actorDatasetSchemaVersion": 1,
    "title": "E-shop products",
    "description": "Dataset containing the whole product catalog including prices and stock availability.",

    // A JSON schema object describing the dataset fields, with our extensions: the "title", "description", and "example" properties.
    // "example" is used to generate code and API examples for the Actor output.
    // For details, see https://docs.apify.com/platform/actors/development/actor-definition/dataset-schema
    "fields": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The name of the results",
            },
            "imageUrl": {
                "type": "string",
                "description": "Function executed for each request",
            },
            "priceUsd": {
                "type": "integer",
                "description": "Price of the item",
            },
            "manufacturer": {
                "type": "object",
                "properties": {
                    "title": { ... }, 
                    "url": { ... },
                }
            },
            ...
        },
        "required": ["title"],
    },
  
    // Define the ways how to present the Dataset to users
    "views": {
        "overview": {
            "title": "Products overview",
            "description": "Displays only basic fields such as title and price",
            "transformation": {
                "flatten": ["stockInfo"],
                "fields": [
                    "title",
                    "imageUrl",
                    "variants"
                ]
            },
            "display": {
                "component": "table",
                "properties": {
                    "title": {
                      "label": "Title"
                    },                           
                    "imageUrl": {
                        "label": "Image",
                        "format": "image" // optional, in this case the format is overridden to show "image" instead of image link "text". "image" format only works with .jpeg, .png or other image format urls.
                    },
                    "stockInfo.availability": {
                        "label": "Availability"
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
                ],
                "unwind": "productVariants"
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

## DatasetSchema object definition

| Property           | Type                         | Required | Description                                                                                        |
| ------------------ | ---------------------------- | -------- | -------------------------------------------------------------------------------------------------- |
| actorSpecification | integer                      | true     | Specifies the version of dataset schema <br/>structure document. <br/>Currently only version 1 is available. |
| fields             | JSON schema | true     | JSON schema object with more formats in the future.             |
| views              | [DatasetView]          | true     | An array of objects with a description of an API <br/>and UI views.                                                  |

### JSON schema

Items of a dataset can be described by a JSON schema definition, passed into the `fields` property.
The Actor system then ensures that each records added to the dataset complies with the provided schema.

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


### DatasetView object definition

| Property       | Type                      | Required | Description                                                                                           |
| -------------- | ------------------------- | -------- | ----------------------------------------------------------------------------------------------------- |
| title          | string                    | true     | The title is visible in UI in the Output tab <br/>as well as in the API.                                       |
| description    | string                    | false    | The description is only available in the API response. <br/>The usage of this field is optional.                       |
| transformation | ViewTransformation object | true     | The definition of data transformation <br/>is applied when dataset data are loaded from <br/>Dataset API. |
| display        | ViewDisplay object        | true     | The definition of Output tab UI visualization.                                                        |

### ViewTransformation object definition

| Property | Type     | Required | Description                                                                                                                                                                                                         |
| -------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| fields   | string[] | true     | Selects fields that are going to be presented in the output. <br/>The order of fields matches the order of columns <br/>in visualization UI. In case the fields value <br/>is missing, it will be presented as “undefined” in the UI. |
| unwind   | string   | false    | Deconstructs nested children into parent object, <br/>e.g.: with unwind:[”foo”], the object `{”foo”:{”bar”:”hello”}}`  <br/> is turned into `{’bar”:”hello”}`.                                                                     |
| flatten  | string[] | false    | Transforms nested object into flat structure. <br/>eg: with flatten:[”foo”] the object `{”foo”:{”bar”:”hello”}}` <br/> is turned into `{’foo.bar”:”hello”}`.                                                                    |
| omit     | string   | false    | Removes the specified fields from the output. <br/>Nested fields names can be used there as well.                                                                                                                           |
| limit    | integer  | false    | The maximum number of results returned. <br/>Default is all results.                                                                                                                                                         |
| desc     | boolean  | false    | By default, results are sorted in ascending based <br/>on the write event into the dataset. desc:true param <br/>will return the newest writes to the dataset first.                                                                      |

### ViewDisplay object definition

| Property   | Type                                                                                                               | Required | Description                                                                                                                  |
| ---------- | ------------------------------------------------------------------------------------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| component  | string                                                                                                             | true     | Only component “table” is available.                                                                                         |
| properties |  Object | false    | Object with keys matching the `transformation.fields` <br/> and ViewDisplayProperty as values. In case properties are not set <br/>the table will be rendered automatically with fields formatted as Strings, <br/>Arrays or Objects. |

### ViewDisplayProperty object definition

| Property | Type                                                    | Required | Description                                                                                    |
| -------- | ------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------- |
| label    | string                                                  | false    | In case the data are visualized as in Table view. <br/>The label will be visible table column’s header. |
| format   | enum(text, number, date, link, <br/>boolean, image, array, object) | false    | Describes how output data values are formatted <br/>in order to be rendered in the output tab UI.       |

# Dataset Schema File

Dataset storage enables you to sequentially save and retrieve data. Each Actor run is assigned its own dataset, which is created when the first item is stored to it. Datasets usually contain results from web scraping, crawling or data processing jobs. The data can be visualized as a table where each object is a row and its attributes are the columns. The data can be exported in JSON, CSV, XML, RSS, Excel or HTML formats.

Dataset can be assigned a schema which describes:

- Content of the dataset, i.e., the schema of objects that are allowed to be added
- Different views on how we can look at the data, aka transformations
- Visualization of the View using predefined components (grid, table, ...), which improves the run view interface at Apify Console
  and also provides a better interface for datasets shared by Apify users

<img src="https://user-images.githubusercontent.com/594801/147474979-a224008c-8cba-43a6-8d2e-c24f6b0d5b37.png" width="500">

## Basic properties

- Storage is immutable. I.e., if you want to change the structure, then you need to create a new dataset.
- Its schema is weak. I.e., you can always push their additional properties, but schema will ensure that all the listed once are there with a correct type. This is to make Actors more compatible, i.e., some Actor expects dataset to contain certain fields but does not care about the additional ones.

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

## Structure

```jsonc
{
    "actorSpecification": 1,
    "title": "Eshop products",
    "description": "Dataset containing the whole product catalog including prices and stock availability.",

    // Not supported yet
    "fields": {
        "title": "string",  
        "imageUrl": "string",  
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
                        "format": "image" // optional, in this case the format is overriden to show "image" instead of image link "text". "image" format only works with .jpeg, .png or other image format urls.
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

Items of a dataset can be described by a JSON schema definition. Apify platform then ensures that each object accomplies with the provided schema. In the first version only the standard JSON schema will be supported, i.e.:


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

with simplifed version comming in the near future:

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

# Dataset schema

## Basic properties

Dataset schema describes:
- Content of the dataset
- Different views on how we can look at the data, aka transformations
- Visualization in the UI. This is also good when sharing the data

Basic properties:
- It's immutable
    - If you want to change the structure then you need to create a new dataset
- It's weak
    - You can always push there additional properties but schema will enasure that all the listed once are there with a correct type
    - This is to make actors more compatible, i.e. some actor expects dataset to contain certain fields but does not care about the additional ones

There are two ways how to create a dataset with schema. First you can start actor that has dataset schema linked from its
[OUTPUT_SCHEMA.json](./OUTPUT_SCHEMA.md). Second you can do it pragmatically via API (`datasetSchema` base64 encoded parameter) or using the SDK:

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
	formatVersion,
	name,
	description,
	fields: {},
	views: {
		myView: {
			name,
			description,
			transformation,
			visualisation,
		}
	},
}
```

### Views's transformation

Transformation is basically a combination of a GET dataset items API endpoint parameters.
So the users could use it to preset the parameters easily, for example:

```
https://api.apify.com/v2/datasets/[ID]/items?format=[FORMAT]&view=searchResults
```

instead of this complicated URL in the case of [Google Search Scraper](https://apify.com/apify/google-search-scraper#how-to-get-one-search-result-per-row):

```
https://api.apify.com/v2/datasets/[ID]/items?format=[FORMAT]&fields=searchQuery,organicResults&unwind=organicResults
```

### View's visualisation

It's a pair of `template` and `properties` (according to the ReactJS language) that maps dataset fields to template property names.

```
visualization: {
    template: 'grid',
    properties: {
        image: '$image.href',
        title: '$title',
        url: '$field1.field2.url,
    }
}
```

### TODOs

- Should one of the views be default?


# Sandbox for various ideas

Here you can find random ideas and notes, in no particular order, relevance, or promise they will be implemented.

## TODOs


- Add ideas for the permission system
  - Note from Marek regarding permissision:
  - Just a note on this, I was thinking about how this could be done systematically, so dropping the notes here:
  - By default, the Actor should have following permissions that the user would accept when running the Actor for the first time:
      - Write to all the default + named storages linked in the output schema
      - Proxy - simply because we want all the traffic to run thru the proxy so we don't want actors scraping directly
  - In `actor.json` the Actor could request additional permissions, basically anything from [permissions](https://docs.apify.com/access-rights/list-of-permissions#actor-task), for example, `DATASET.READ` to be able to read all the datasets or `SCHEDULER.WRITE` to manage schedules
  There is one tricky part:
    - If an Actor needs to `.call()` other actors then basically the user must give him full permissions. Otherwise, the Actor would have to list all the other actors it's going to call and the user would have to accept all the permissions needed in recursive calls.
  Extra question:
    - What to do if the new version of the Actor requires more permissions? We should probably require the author to increase a major version and keep users on the old build + email them to accept the updated permissions.

- We should make env vars independent of Apify, i.e. start them with `ACTOR_`, rather then `APIFY_`

- To storages, add info about atomic rename, e.g. `setName` function, and link to other operations...

- Maybe add `Actor.getThisRun()` function to return run object of the current Actor. Not sure about use case...

- Figure the push/build workflow, see https://github.com/apify/actor-specs/pull/7/files#r997020215 
   / https://github.com/apify/actor-specs/pull/7#pullrequestreview-1144097598 
   how should that work with

- Would be nice to have an API that would send a message to a run and the run would get it as `.on('message', (msg) => { ... })`. Would save people from implementing their own servers in actors.
  It would make it easier to orchestrate actors. Currently it's a bit painful to create a "master" Actor and then "workers" to process some workloads. But it could probably be achieved with a queue. if it were distributed and generic.
   Explain why is this better than live-view HTTP API


- NOTE: BTW we have a new API v3 doc with ideas for changes in API https://www.notion.so/apify/API-v3-6fcd240d9621427f9650b741ec6fa06b ?

- For DATASET schema, In future versions let's consider referencing schema using URL, for now let's keep it simple



### Pipe result of an Actor to another (aka chaining)

Actor can start other actors and
pass them its own dataset or key-value store.
For example, the main Actor can produce files
and the spawned others can consume them, from the same storages.

In the future, we could let datasets be cleaned up from the beginning,
effectively creating a pipe, with custom rolling window.
Webhooks can be attached to storage operations,
and so launch other actors to consume newly added items or files.

#### UNIX equivalent

```bash
$ ls -l | grep "something" | wc -l
```

**TODO (@jancurn):** **Move to IDEAS.md** We could have a special CLI support for creating Actor chains using pipe operator,
like this:

```
$ apify call apify/google-search-scraper | apify call apify/send-email queryTerms="aaa\nbbb"
```

Note from Marek:
Here we will need some way how to map outputs from old Actor to inputs of the following Actor, perhaps we could pipeline thru some utility like [jq](https://stedolan.github.io/jq/tutorial/)
or use some mapping like:

```
--input-dataset-id="$output.defaultDatasetId" --dataset-name="xxx"
```

Note from Ondra:
I tried to write a JS example for piping, but figured that piping is not really aligned with how actors work, because piping assumes the output of one program is immediately processed by another program. Actors can produce output like this, but they can't process input like this. Input is provided only once, when the Actor starts. Unless we consider e.g. request queue as input. We will have to think about this a bit differently.

Note from Jan:
Indeed, the flow is to start one Actor, and pass one of it's storages as default to the other newly started Actor. If we had a generic Queue, it could be used nicely for these use case. I'm adding these notes to the doc, so that we can get back to them later.

Jan: I'd get rid of the Request queue from Actor specification, and kept it as Apify's extension only.



### Charging money

TODO(@jancurn): Move the `Actor.charge()` to ideas, to keep this simple.
Mention just basic monetization in non-API section.

**STATUS: This feature is not implemented yet.**

To run an Actor on the Apify platform, the user might need
to purchase a paid plan to cover for the computing resources used,
pay a fixed monthly fee for "renting" the Actor if it's paid,
or pay a variable fee for the number of results produced by the Actor.

On top of these "static" payment options, actors will eventually support
a built-in monetization system that enables developers to charge users variable
amounts, e.g. based on returned number of results,
complexity of the input, or cost of external APIs used by the Actor.

The Actor can dynamically charge the current user a specific amount of money
by calling the `charge` function.
Users of actors can ensure they will not be charged too much by specifying
the maximum amount when starting an Actor using the `maxChargeCreditsUsd` run option.
The Actor can call the `charge` function as many times as necessary,
but once the total sum of charged credits would exceed the maximum limit,
the invocation of the function throws an error.

When a paid Actor subsequently starts another paid Actor, the charges performed
by the subsequent actors are taken from the calling Actor's credits.
This enables Actor economy, where actors hierarchically pay other actors or external APIs
to perform parts of the job.

**Rules for building actors with variable charging:**

<!-- TODO: Should be called ACTOR_MAX_CHARGE_CREDITS_USD? -->

- If your Actor is charging users, make sure at the earliest time possible  
  that the Actor is being run with sufficient credits, by checking the input
  and `APIFY_MAX_CHARGE_CREDITS_USD` environment variable (see Environment variables TODO (@jancurn)).
  If the maximum credits are not sufficient for Actor's operation with respect
  to the input (e.g. user is requesting too many results for too little money),
  fail the Actor immediately with a reasonable error status message for the user,
  and don't charge the user anything.
- Charge the users right **after** you have incurred the costs,
  not in advance. If the Actor fails in the middle or is aborted, the users
  only need to be charged for results they actually received.
  Nothing will make users of your actors angrier than charging them for something they didn't receive.

**Integration with input schema**

The Actor [Input schema](./pages/INPUT_SCHEMA.md) file can contain a special field called
`maxChargeCreditsPerUnitUsd`, which contains an information what is the maximum cost
per unit of usage specified in the input schema.
This field can be used by the Apify platform to automatically inform the user about
maximum possible charge, and automatically set `maxChargeCreditsUsd` for the Actor run.
For example,
for Google Search Scraper paid by number of pages scraped, this setting would be
added to `maxPageCount` field which limits the maximum number of pages to scrape.
Note that the Actor doesn't know in advance how many pages it will be able to fetch,
hence the pricing needs to be set on the maximum, and the cost charged dynamically on the fly.

<!-- TODO: Shall we create another Actor status `CREDITS_EXCEEDED` instead of `FAILED` ?
That could provide for better UX. Probably not, it would be an overkill... -->

#### Node.js

Charge the current user of the Actor a specific amount:

```js
const chargeInfo = await Actor.charge({ creditsUsd: 1.23 });
```

Set the maximum amount to charge when starting an Actor.

```js
const run = await Actor.call(
  'bob/analyse-images',
  { imageUrls: ['...'] },
  {
      // By default, it's 0, hence actors cannot charge users unless they explicitely allow that.
      maxChargeCreditsUsd: 5,
  },
);
```


# OUTPUT_SCHEMA.json








Is a list of different output types of the actor consiting of:

- dataset defined by schema (default, some named that is being reused, in the future another unnamed linked to the run)
- key-value store defined by schema (-||-)
- request queue defined by schema (-||-)
- live-view which should say if it's HTML page or API defined by Swagger doc or other
- log (do we need it here?)
- ... maybe more in the future

With format close to Honza's https://github.com/apify/actor-specs/blob/master/Schema%20Experiments%20by%20jan/google_search_scraper/.actor/OUTPUT_SCHEMA.json


## Run UI in Apify Console

Now what is missing is the description of the main run view tab. What do we need here?

- For the majority of actors we want to see the dataset with new records being added in realtime
- For [Google Spreadsheet Import](https://apify.com/lukaskrivka/google-sheets) we want to first display Live View for user to set up OAUTH and once 
this is set up then we want to display the log next time.
- For technical actors it's log
- For [HTML to PDF convertor](https://apify.com/jancurn/url-to-pdf) it's a single record from key-value store
- For [Monitoring](https://apify.com/apify/monitoring-runner) it's log during the runtime and single HTML record in iframe in the end
- For actor that has failed it's log

So I think that ideally we need:
- Default value
- Optionally the value for different states
- Be able to pragmatically changes this using API by actor itself

I am not 100% convinced if this belongs to `OUTPUT_SCHEMA.json` or to `ACTOR.json`. But it could look like the following:

TODO





## TODOs


- Add ideas for the permission system
  - Note from Marek regarding permissision:
  - Just a note on this, I was thinking about how this could be done systematically, so dropping the notes here:
  - By default, the actor should have following permissions that the user would accept when running the actor for the first time:
      - Write to all the default + named storages linked in the output schema
      - Proxy - simply because we want all the traffic to run thru the proxy so we don't want actors scraping directly
  - In `actor.json` the actor could request additional permissions, basically anything from [permissions](https://docs.apify.com/access-rights/list-of-permissions#actor-task), for example, `DATASET.READ` to be able to read all the datasets or `SCHEDULER.WRITE` to manage schedules
  There is one tricky part:
    - If an actor needs to `.call()` other actors then basically the user must give him full permissions. Otherwise, the actor would have to list all the other actors it's going to call and the user would have to accept all the permissions needed in recursive calls.
  Extra question:
    - What to do if the new version of the actor requires more permissions? We should probably require the author to increase a major version and keep users on the old build + email them to accept the updated permissions.


- To storages, add info about atomic rename, e.g. `setName` function, and link to other operations...

- Maybe add `Actor.getThisRun()` function to return run object of the current actor. Not sure about use case...

- Figure the push/build workflow, see https://github.com/apify/actor-specs/pull/7/files#r997020215 
   / https://github.com/apify/actor-specs/pull/7#pullrequestreview-1144097598 
   how should that work with

- Would be nice to have an API that would send a message to a run and the run would get it as `.on('message', (msg) => { ... })`. Would save people from implementing their own servers in actors.
  It would make it easier to orchestrate actors. Currently it's a bit painful to create a "master" actor and then "workers" to process some workloads. But it could probably be achieved with a queue. if it were distributed and generic.
   Explain why is this better than live-view HTTP API


- NOTE: BTW we have a new API v3 doc with ideas for changes in API https://www.notion.so/apify/API-v3-6fcd240d9621427f9650b741ec6fa06b ?

- For DATASET schema, In future versions let's consider referencing schema using URL, for now let's keep it simple

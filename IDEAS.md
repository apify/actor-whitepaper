




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



- 
- To storages, add info about atomic rename, e.g. `setName` function, and link to other operations...

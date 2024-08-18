# Request queue schema file specification [work in progress]

Currently, this is neither specified nor implemented.
We think that request queue schema might be useful for two things:

- ensuring what kind of URLs might be enqueued (certain domains or subdomains, ...)
- ensure that for example each request has `userData.label`, i.e. schema of `userData` the same way as we enforce it for the Datasets

We should consider renaming `RequestQueue` to just `Queue` and make it more generic, and then it makes sense to have request schema.

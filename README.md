
# Draft of Yumon index

initial ask : 

```
Twitch

- 🟩 # of followers
- 🟩 # of subscribers
- 🟩 Av. # of viewers on 3 last streams
- 🟨 % of growth of new subscribers over the last 24 hours, 3 days, 10 days, 30 days
- 🟨 % of growth of new followers over the last 24 hours, 3 days, 10 days, 30 days
- 🟥 # of unique viewers on the 3 last streams
- 🟥 Live tipping performance
- 🟥 Velocity of chat interactions

```

Finally using only `twitchtracker.com` to get theses infos :

```
    - current # of followers
    - # of followers of last month
    - # of followers 2 months ago
    - "# of followers 3 months ago
    - Avg growth rate of new followers (%)
    - current # of subscribers
    - # of subscribers of last month
    - # of subscribers 2 months ago
    - "# of subscribers 3 months ago
    - Avg growth rate of new subscribers on 3 last months (%)
    - Avg CCr views on last stream
    - Avg CCr views on second last stream
    - Avg CCr views on third last stream
    - Av. # of viewers on 3 last streams
```
## API

Using `FastApi` to get the result of the scapper as a `json`

Api Endpoint :
`localhost:8080/:twitcher`

to debug Api or to get all different endpoints :
`localhost:8080/docs`

## local test

``` bash
make run_locally
```

## container

``` bash
make build_image
make run_image  # test with http://localhost:8080/docs or http://localhost:8080/pokimane
make push_image
make deploy_image
```

# manual commands

``` bash
gsutil ls -R gs://le-wagon-data
gsutil cp db.sqlite gs://le-wagon-data/twitch/db.sqlite
gsutil cp gs://le-wagon-data/twitch/db.sqlite .
```

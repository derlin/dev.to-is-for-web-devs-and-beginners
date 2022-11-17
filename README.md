# dev.to is for web developers and beginners, I have data to prove it

This repository contains the source code of one of my dev.to articles,
that analyses which tags are the most popular on dev.to.

The data collection was done on **November, 13 2022 at 18:52**, so the data may have
changed since then !

**Analysis ⮕ https://derlin.github.io/dev.to-is-for-web-devs-and-beginners/analysis.html**

**Article ⮕ https://dev.to/derlin/devto-is-for-webdevs-and-beginners-i-have-data-to-prove-it-54c4**

![Tag Cloud (top 10,000 articles of all time)](images/tagcloud_articles.png)
(Top 200 tags appearing most often on the top 10,000 articles of all time)

**IMPORTANT**: the notebooks do not show graphs in GitHub preview !
To preview them, please go to  
https://derlin.github.io/dev.to-is-for-web-devs-and-beginners/ instead.

## Disclaimer

I am not a data scientist and did this on my spare time.
I didn't have much time to invest, but I tried my best to stay unbiased and to
clearly explain what I am doing, so you can see the potential biases and pitfalls.

Feel free to run it yourself, improve it, and share your results !
(Just just mention my work if you write about it somewhere, and 🌟 the repo, this would be fair).

## Conclusion

*TL;DR*: **if you are not a web developer and like to write about technical, precise subjects, it will be hard to shine on dev.to**.
This doesn't mean you shouldn't contribute though ! 

The conclusions I came to are that dev.to is currently dominated by:

1. web development and web framework articles (`#javascript`, `#webdev`, `#react`, ...) - 
   they account for more than 50% of articles / reactions / comments,
2. beginner articles (`#codenewbies`, `#beginners`, ...),
3. generic articles for improving our job/position (`#career`, `#productivity`, ...),
4. generic articles on coding (`#programming`, `#computerscience`, `#algorithms`, ...)
5. technologies and tools that are used by all developers, but especially web devs (`#docker`, `#git`, `#github`, `#vscode`).

To give you a better idea, **`#webdev`, `#javascript` and `#beginners` account for more than 50% of
all the reactions, comments, and number of articles** of the top 10,000 articles published to date !
`webdev` alone covers 12% of the 10K top articles of all time, 20% of the top 5K articles of last month.

On the other hand, the following subjects may have content, but trigger fewer interactions from
the dev.to community (less comments, less positive reactions):

1. Languages and frameworks NOT related to web development (`#kotlin`, `#laravel`, `#android`, ...),
2. Specialized areas that are NOT related to web development (`#datascience`, `#machinelearning`, ...)
3. OPS-related topics (`#devops`, `#kubernetes`, `#aws`, ...).

So if you happen to like writing about those less popular subjects, but are demotivated by the sparse
reactions, don't give up ! It is "normal" for now, but it may change in the future.

## Collected data

The data were collected using the `fetch/devto.py` script, running on Python 3.10.6.
To run it locally:
```python
pip install -r requirements.txt
python3 fetch/devto.py
```

The output of the script are two json files, `top_articles.json` and `top_articles_by_tag.json`.

#### Top articles of all time

The list of the most popular 10,000 articles of all time, fetched using the `https://dev.to/search/feed_content`
endpoint.

One article has the following information:
```json
{
  "class_name": "Article",
  "id": 185402,
  "title": "9 Projects you can do to become a Frontend Master",
  "path": "/simonholdorf/9-projects-you-can-do-to-become-a-frontend-master-in-2020-n2h",
  "tag_list": [ "..." ],
  "readable_publish_date": "Oct 6 '19",
  "published_at_int": 1570393193,
  "reading_time": 7,
  "cloudinary_video_url": "...",
  "flare_tag": "",
  "video_duration_string": "00:00",
  "comments_count": 1,
  "public_reactions_count": 12687,
  "user_id": 203467,
  "user": {
    "username": "...",
    "name": "...",
    "profile_image_90": "https://..."
  }
}
```


#### Top tags and number of articles per tag

The top tags can be fetched using one of two methods:
1. by calling the API endpoint [getTags](https://developers.forem.com/api/v0#tag/tags/operation/getTags),
2. by parsing the https://dev.to/tags page.

Both methods return **different results**, and from my experience the second one is more reliable.
Using the API, I got four tags that didn't exist (anymore?) - *404 Not Found*:
`macosapps`, `southafricanews` `sportnews`, `latestnigerianewslat`.

Furthermore, the API allows for a `count` parameter but returns only `id`, `name` and colors information.
Parsing the dev.to page allows us to also get the number of posts published, as displayed on the website.
However, this number **cannot be blindly trusted**, as it is often different from (and way higher than)
the number displayed on the `https://dev.to/t/<TAG>` page.

As it is difficult to know the source of truth, the script returns both numbers.

The `top_articles_by_tag.json` has the following structure:
```json
{
    "tag": {
      "name": "webdev",
      "num_articles": 93972
    },
    "total": 55014,
    "top_articles": []
}
```

The `total` is the number of articles displayed on the individual tag page (in this example https://dev.to/t/webdev),
while `tag.num_articles` is the number of articles displayed on the tag listing page, https://dev.to/tags.
The `top_articles` are the 100 most popular articles for this tag, and are fetched using the same endpoint
as the top articles of all time (with just an additional query parameter).

## Analysis

The analysis is done in the [python notebook](https://jupyter.org) [dataviz/analysis.ipynb](dataviz/analysis.ipynb).
The notebook is exported as HTML, and is available at https://derlin.github.io/dev.to-is-for-web-devs-and-beginners/.

An additional notebook, [dataviz/difference.ipynb](dataviz/difference.ipynb), shows a bit the difference
between the top tags from the API and the website, as well as the "*Number of posts*" discrepancies between
the tag listing page and the individual tag pages on dev.to.

To run locally:
```bash
pip install -r requirements.txt
jupyter notebook
```

To convert to HTML:
```bash
jupyter nbconvert dataviz/analysis.ipynb --to html
```
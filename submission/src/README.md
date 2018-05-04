# References used to code it
* [Clustered Network](http://bl.ocks.org/GerHobbelt/3071239)
* Emoji borrowed from [emoji2vec](https://github.com/uclmr/emoji2vec)
* [Enlarging the node size in D3](http://plnkr.co/edit/MOczs02DNeUJGzXAPdMd?p=preview)

# Libraries to run k-means (skip it if you just want to see the D3 outputs)
* Python 3.X
* gensim
* scikit-learn

# How to replicate the results

## Download Data
Download the following data to run K-means algorithm.
* [EN word vector](https://drive.google.com/open?id=18pYhlVo2X2_IeD8AIA1NKrnZ4BstUVHJ)
* [EN-JP cross-lingual word vector](https://drive.google.com/open?id=1JQh80ZIHcRIKjqx4qxAaY_yYyf5Y2XND)

## Generating JSON input file to D3
```
    $ sh kmeans_en.sh // EN visualization
    $ sh kmeans_en_jp.sh // EN-JP visualization
```

## Run the server
Assuming you are using python server (i.e., `python -m http.server` for Python 3),
the visualization is at `http://localhost:8000/clustered_network.html`

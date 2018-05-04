CLUSTER=50
python3 kmeans.py \
    --w2v eng_news_2015_1M_100.txt.normalized.txt.jp-en.mapped.txt \
    --num_cluster $CLUSTER \
    --out kmean_clustered_en_$CLUSTER.json

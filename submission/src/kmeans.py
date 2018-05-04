import gensim
#from nltk.cluster import KMeansClusterer
#import nltk
from sklearn.cluster import KMeans
from collections import defaultdict
import numpy as np
import json
from scipy.spatial.distance import cosine

def read_text_emoji(model, cross_lingual):
    f = open("/Users/yoshinarifujinuma/work/emoji2vec/data/training/train.txt")
    emoji2vec = {}
    for line in f:
        description, emoji, boolean = line.strip().split("\t")
        total = np.zeros(100)
        for word in description.split():
            if cross_lingual:
                word = "eng:" + word
            if word in model.vocab:
                total += model[word]
        emoji2vec[emoji] = total/len(description.split())
    return emoji2vec
        

def get_top_words_per_centroid(model, NUM_CLUSTERS, top_n):
    X = model[model.wv.vocab]
    kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=2)
    kmeans = kmeans.fit(X)
    labels = kmeans.predict(X)
    C = kmeans.cluster_centers_
    cluster = defaultdict(list)
    labels = kmeans.predict(X)
    subsets = []
    for i, centroid in enumerate(C):
        nn = [w for w, cos_sim in model.similar_by_vector(centroid, topn=top_n)]
        print(nn)
        subsets.extend(nn)
    return subsets

def compute_node_sims(centroid_vecs):
    sims = defaultdict(list)
    for i in range(len(centroid_vecs)):
        for j in range(i+1, len(centroid_vecs)):
            cos_sim = 1 - cosine(centroid_vecs[i], centroid_vecs[j])
            if cos_sim > 0:
                sims[i].append(j)
    return sims
 

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--w2v", type=str, help="", required=True)
    parser.add_argument("--out", type=str, help="", required=True)
    parser.add_argument("--num_cluster", type=int, help="", default=40)
    parser.add_argument("--cross_lingual", action="store_true", help="", default=False)
    args = parser.parse_args()
    

    json_dic = {}
    json_dic["nodes"] = []
    json_dic["links"] = []
    NUM_CLUSTERS=args.num_cluster
    model = gensim.models.KeyedVectors.load_word2vec_format(args.w2v, binary=False)
    X = model[model.wv.vocab]
    kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=2)
    kmeans = kmeans.fit(X)
    labels = kmeans.predict(X)
    C = kmeans.cluster_centers_
    cluster = defaultdict(list)
    print(labels)
    print(C)
    labels = kmeans.predict(X)
    #stock = model["eng:stock"]
    #jp_closing_price = model["jpn:終値"]
    #en_salary = model["eng:salary"]
    #jp_salary = model["jpn:給与"]
    #jp_rise = model["jpn:続伸"]
    #en_disaster = model["eng:disaster"]
    #jp_disaster = model["jpn:災害"]
    #en_policy = model["eng:policy"]
    #jp_policy = model["jpn:政策"]
    #en_cabinet = model["eng:cabinet"]
    #jp_cabinet = model["jpn:組閣"]
    #print(kmeans.predict(np.array([stock, jp_closing_price, en_salary, jp_salary, jp_rise, jp_disaster, en_disaster, en_policy, jp_policy, en_cabinet, jp_cabinet])))

    node_num = 0
    centroid_nodes = []

    centroid_links = compute_node_sims(C)

    emoji2vec = read_text_emoji(model, args.cross_lingual)

    for i, centroid in enumerate(C):
        sim = -1
        centroid_emoji = ""
        for k, v in emoji2vec.items():
            cos_sim = 1 - cosine(centroid, v)
            if sim < cos_sim:
                sim = cos_sim
                centroid_emoji = k

        #node_centroid = {"name": "centroid_%i" % i, "group": i, "node_id": node_num}
        node_centroid = {"name": centroid_emoji, "group": i, "node_id": node_num}
        centroid_nodes.append(node_centroid)
        node_num += 1
        json_dic["nodes"].append(node_centroid)
        #print(i, [(w, "%.3f" % cos_sim) for w, cos_sim in model.similar_by_vector(centroid, topn=10)])
        for w, cos_sim in model.similar_by_vector(centroid, topn=10):
            node = {"name": w.replace(":", "_"), "group": i, "node_id": node_num} # assuming no duplicates
            json_dic["nodes"].append(node)
            link = {"source": node_centroid["node_id"], "target": node_num, "value": 1}
            node_num += 1
            json_dic["links"].append(link)

    for i, centroid in enumerate(C):
        # Adding cluster node links
        for target in centroid_links[i]:
            link = {"source": node_centroid["node_id"], "target": centroid_nodes[target]["node_id"], "value": 1}
            json_dic["links"].append(link)


    # adding links between clusters

    outfile = open(args.out, "w")
    json.dump(json_dic, outfile)


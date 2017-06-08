import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn

def srs_likes(df):
    return pd.Series([i[0] if i else None for i in df["lnds"]])

def srs_dislikes(df):
    return pd.Series([i[1] if i else None for i in df["lnds"]])

def srs_like_sent_ratio(df):
    return pd.Series([i[2] if i else None for i in df["lnds"]])

def srs_total_sents(df): # could be faster if done state-wise
    return pd.Series([i[0] + i[1] if i else None for i in df["lnds"]])

if __name__ == '__main__':
    df = pd.DataFrame(pd.read_pickle("data_store"))
    df["likes"] = srs_likes(df)
    df["dislikes"] = srs_dislikes(df)
    df["like_sent_ratio"] = srs_like_sent_ratio(df)
    df["total_sents"] = srs_total_sents(df)
    plt.figure(0)
    sn.distplot(df["like_sent_ratio"], hist=False, norm_hist=True)
    plt.title("distribution of likes/total_sents")
    plt.xlabel("x = likes/total_sents")
    plt.ylabel("y = p(x)")
    sn.distplot(df["like_sent_ratio"][df["views"] > 1000], hist=False, norm_hist=True)
    plt.show()

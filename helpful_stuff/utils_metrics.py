from collections import defaultdict

"""
Util methods for evaluation of predictions.
"""


def precision_recall_at_k_4df(df, k=10, threshold=3.5):
    """
    Calculate recall@M and precision@M for predictions in pandas DataFrame.
    :param df:
    :param k:
    :param threshold:
    :return:
    """
    user_est_true = defaultdict(list)
    for uid, true_r, est in df[['reviewerID', 'overall', 'value']].values:
        user_est_true[uid].append((est, true_r))

    return precision_recall_at_k(user_est_true, k, threshold)


def precision_recall_at_k_4ds(predictions, k=10, threshold=3.5):
    """
    Calculate recall@M and precision@M  for predictions in surprise DataFrame.
    :param predictions:
    :param k:
    :param threshold:
    :return:
    """
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    return precision_recall_at_k(user_est_true, k, threshold)


def precision_recall_at_k(user_est_true, k=10, threshold=3.5):
    """
    General precision@M and recall@M function.
    :param user_est_true:
    :param k:
    :param threshold:
    :return:
    """
    precisions = dict()
    recalls = dict()

    for uid, user_ratings in user_est_true.items():
        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)

        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

        # Number of recommended items in top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                              for (est, true_r) in user_ratings[:k])

        # Precision@K: Proportion of recommended items that are relevant
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 1

        # Recall@K: Proportion of relevant items that are recommended
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 1

    return precisions, recalls




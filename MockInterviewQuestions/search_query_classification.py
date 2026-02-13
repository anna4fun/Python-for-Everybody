from __future__ import annotations

import re
from typing import Dict


query_domain_pairs = {
    "you": "youtube.com",
    "f": "facebook.com",
    "garden rose": "bloomingmore.com",
    "what is lynnwood weather": "accuweather.com",
    "nfl tickets":"www.ticketmaster.com/"
}


def clean_domain(domain: str) -> str:
    """
    Return a "cleaned" domain by removing leading 'www' and trailing '.com'.

    Examples:
      - 'www.youtube.com' -> 'youtube'
      - 'youtube.com' -> 'youtube'
    """
    cleaned = domain.strip().lower()

    cleaned = re.sub(r"^[a-z][a-z0-9+\-.]*://", "", cleaned)  # drop scheme (http/https)
    cleaned = cleaned.lstrip("/")  # drop leftover '//' if present
    cleaned = cleaned.split("/", 1)[0]  # drop any path/query fragments

    if cleaned.startswith("www."):
        cleaned = cleaned[4:]
    if cleaned.endswith(".com"):
        cleaned = cleaned[:-4]

    return cleaned.strip(".")


def levenshtein_distance(left: str, right: str) -> int:
    """
    Compute Levenshtein edit distance between two strings (insert/delete/substitute).
    """
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)

    # Ensure 'right' is the shorter string to reduce memory.
    if len(right) > len(left):
        left, right = right, left

    previous_row = list(range(len(right) + 1))
    for i, left_char in enumerate(left, start=1):
        current_row = [i]
        for j, right_char in enumerate(right, start=1):
            insert_cost = current_row[j - 1] + 1
            delete_cost = previous_row[j] + 1
            substitute_cost = previous_row[j - 1] + (left_char != right_char)
            current_row.append(min(insert_cost, delete_cost, substitute_cost))
        previous_row = current_row

    return previous_row[-1]


def normalized_levenshtein_distance(left: str, right: str) -> float:
    """
    levenshtein_distance(left, right) / max(len(left), len(right))
    """
    denominator = max(len(left), len(right))
    if denominator == 0:
        return 0.0
    return levenshtein_distance(left, right) / denominator


def query_domain_similarities(
    query_domain_pair: Dict[str, str],
) -> Dict[str, float]:
    """
    For each (search_query -> domain) pair, compute:
      normalized_levenshtein_distance(search_query, clean_domain(domain))

    Returns a dict keyed by search_query.
    """
    similarities: Dict[str, float] = {}
    for query, domain in query_domain_pair.items():
        query_norm = query.strip().lower()
        cleaned = clean_domain(domain)
        similarities[query] = normalized_levenshtein_distance(query_norm, cleaned)
    return similarities


def cleaned_query_domain_pairs(query_domain_pair: Dict[str, str]) -> Dict[str, str]:
    """
    Map each search query to its cleaned domain.
    """
    return {query: clean_domain(domain) for query, domain in query_domain_pair.items()}


if __name__ == "__main__":
    cleaned = cleaned_query_domain_pairs(query_domain_pairs)
    sims = query_domain_similarities(query_domain_pairs)
    for query, cleaned_domain in cleaned.items():
        print(f"{query!r} -> {cleaned_domain!r}  similarity={sims[query]:.3f}")

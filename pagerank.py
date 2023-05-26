import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution  = dict()
    links  = corpus[page]
    N = len(corpus)
    num_links  = len(links)
    # the page has no outgoing links
    if num_links == 0:
       for key in corpus: 
               probability_distribution[key] =  1 / N
               
    # the page has outgoing links
    else:
        for key in corpus:
            probability_distribution[key] = (1 - damping_factor) / N
            if key in links:
                probability_distribution[key] += (damping_factor / num_links ) 
               
               
    return probability_distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visit_counts  = {page: 0 for page in corpus}
    # Choose a random page 
    random_page = random.choice(list(corpus.keys())) 
    visit_counts[random_page] += 1
    
    for i in range(1,n):
           probability_distribution = transition_model(corpus,random_page,damping_factor)
           random_page = random.choices(list(probability_distribution.keys()), weights= list(probability_distribution.values()) , k=1)[0]
           visit_counts[random_page] += 1
             
    page_ranks = {page: visit_counts[page] /  n  for page in corpus}
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    page_ranks  = {page: 1 / N for page in corpus}

    while True :
        new_page_ranks = {}
        difference = 0
        for page in corpus:
            sum_prob = 0
            for p in corpus:
               if page in corpus[p]:
                  sum_prob += page_ranks[p] / len(corpus[p])
            
            new_page_ranks[page]  = ((1 - damping_factor) / N) + (damping_factor  * sum_prob)
            difference += abs(new_page_ranks[page]  - page_ranks[page])
            
        #This process should repeat until no PageRank value changes by more than 0.001
        if not difference >  0.001:
                break
            
        page_ranks = new_page_ranks
   
    # Normalize the page ranks so they sum to 1
    total_page_ranks = sum(page_ranks.values())
    page_ranks = {page: rank / total_page_ranks for page, rank in page_ranks.items()}
    return page_ranks
    

if __name__ == "__main__":
    main()

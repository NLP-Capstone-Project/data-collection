import json


def extract_pdf_urls_from_json(semantic_scholar_json_path):
    """
    Collects urls to all research papers with PDFs readily available.

    Returns a list of ID, pdfURL pairs.

    :param semantic_scholar_json_path: file path
        Path to the Semantic Scholar data
    :return: string list of all urls collectible
    """

    semantic_scholar_json = open(semantic_scholar_json_path, 'r')
    json_objs = []
    for paper in semantic_scholar_json.readlines():
        json_objs.append(json.loads(paper))

    pdfUrls = []
    for i, json_obj in enumerate(json_objs):
        json_obj_urls = json_obj['pdfUrls']

        # We only need one copy per publication.
        if len(json_obj_urls) >= 1:
            paper_id = json_obj['id']
            paper_url = json_obj_urls[0]
            if i < 10:
                print(paper_url)
            pdfUrls.append((paper_id, paper_url))

    return pdfUrls


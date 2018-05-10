import argparse
import json
import os
import shutil
import sys

from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    project_root = os.path.abspath(os.path.realpath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)))))

    parser.add_argument("--semantic-scholar-data-path", type=str,
                        help="Path to the Semantic Scholar data.")
    parser.add_argument("--save-dir", type=str,
                        default=os.path.join(
                            project_root, "data"),
                        help="Directory to save the paper IDs.")
    args = parser.parse_args()

    if not os.path.exists(args.semantic_scholar_data_path):
        raise ValueError("Semantic Scholar data path needed for collection.")

    # Collect urls of all research papers
    print("Processing Semantic Scholar JSON...")
    count = 0
    semantic_scholar_json = open(args.semantic_scholar_data_path, 'r')
    s2_ids = open(os.path.join(args.save_dir,
                               args.semantic_scholar_data_path + ".txt"), 'w')
    ids = set()
    for paper in tqdm(semantic_scholar_json):
        json_obj = json.loads(paper)
        sources = json_obj["sources"]
        pubmed = json_obj["pmid"]
        if "Medline" in sources or pubmed:
            paper_id = json_obj['id']
            if paper_id not in ids:
                ids.add(paper_id)
                print(paper_id, file=s2_ids)
                count += 1

    print()
    print(count, "research IDs collected!")


if __name__ == "__main__":
    main()

import argparse
import os
import shutil
import sys

from tqdm import tqdm

from collection_utils import extract_pdf_content, extract_pdf_urls_from_json


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    project_root = os.path.abspath(os.path.realpath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)))))

    parser.add_argument("--semantic-scholar-data-path", type=str,
                        help="Path to the Semantic Scholar data.")
    parser.add_argument("--save-dir", type=str,
                        default=os.path.join(
                            project_root, "data", "papers"),
                        help="Directory to save research content as"
                             "JSON files.")
    args = parser.parse_args()

    if not os.path.exists(args.semantic_scholar_data_path):
        raise ValueError("Semantic Scholar data path needed for collection.")

    try:
        if os.path.exists(args.save_dir):
            # save directory already exists, do we really want to overwrite?
            input("Directory for paper data {} already exists. Press <Enter> "
                  "to clear, overwrite and continue , or "
                  "<Ctrl-c> to abort.".format(args.save_dir))
            shutil.rmtree(args.save_dir)
        os.makedirs(args.save_dir)
    except KeyboardInterrupt:
        print()
        sys.exit(0)

    # Collect urls of all research papers
    print("Processing Semantic Scholar JSON...")
    count = 0
    semantic_scholar_json = open(args.semantic_scholar_data_path, 'r')
    for paper in semantic_scholar_json:
        json_obj = json.loads(paper)
        json_obj_urls = json_obj['pdfUrls']

        # We only need one copy per publication.
        if len(json_obj_urls) >= 1:
            paper_id = json_obj['id']
            paper_url = json_obj_urls[0]

            try:
                content = extract_pdf_content(paper_url)
                if content is not None:
                    paper_json_path = os.path.join(args.save_dir, paper_id + ".json")
                    with open(paper_json_path, 'w') as f:
                        f.write(content)
                        count += 1
            except KeyboardInterrupt:
                print("Stopping collection early.")
                break
            except:
                pass  # Ignore malformed data.

        print("\rPapers collected: {}".format(count), end="")
        sys.stdout.flush()
        count += 1

    print()
    print(count, "research papers collected!")


if __name__ == "__main__":
    main()

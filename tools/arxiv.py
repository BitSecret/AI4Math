import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tools.utils import load_json, save_json, keywords
header = {"User-Agent": UserAgent().random}


def selected(date, start, end):
    json_data = load_json("../data/{}.json".format(date))
    keys = [key for key in json_data["selected"]]
    print()
    print("### {} papers from arxiv about \"AI for Math\" from {} to {}".format(len(keys), start, end))
    for k in keys:
        print("- **{}**, arXiv:{} [[paper]({})]".format(
            json_data["selected"][k]["title"],
            json_data["selected"][k]["source"].split("/")[-1],
            json_data["selected"][k]["source"]))
    print()


def search(date):
    urls = {
        "AI": "https://arxiv.org/list/cs.AI/pastweek?show=2000",
        "CL": "https://arxiv.org/list/cs.CL/pastweek?show=2000",
        "ML": "https://arxiv.org/list/cs.LG/pastweek?show=2000"
    }
    json_data = {
        "all": {},
        "selected": {}
    }
    added = []
    data_count = 1

    for cat in urls:
        html = requests.get(urls[cat], headers=header)
        soup = BeautifulSoup(html.text, 'html.parser')
        dls = soup.findAll("dl")
        for dl in dls:
            contents = list(dl.children)
            for i in range(int(len(contents) / 4)):
                html = "https://arxiv.org" + contents[i * 4 + 1].find("a", {"title": "Abstract"})["href"]
                title = contents[i * 4 + 3].find(
                    "div", {"class": "list-title mathjax"}).text.replace("Title: ", "").replace("\n", "")
                if title not in added:
                    json_data["all"][str(data_count)] = {
                        "title": title,
                        "source": html,
                        "cat": cat
                    }
                    title_lower = title.lower()
                    for k in keywords:
                        if k in title_lower:
                            json_data["selected"][str(data_count)] = {
                                "title": title,
                                "source": html,
                                "cat": cat,
                                "keyword": k
                            }
                            break
                    added.append(title)
                    data_count += 1

    save_json(json_data, "../data/{}.json".format(date))


def main():
    date = "23-08-20"
    start = "14 Aug"
    end = "18 Aug"
    search(date)
    input("input 1 when you selected:")
    selected(date, start, end)


if __name__ == '__main__':
    main()

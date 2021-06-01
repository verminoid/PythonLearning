from bs4 import BeautifulSoup
import unittest

def parse(path_to_file):    

    f = open(path_to_file, "r", encoding="utf-8")
    soup = BeautifulSoup(f, "html.parser")
    f.close()

    all_img = soup.find(id="bodyContent").find_all("img")
    imgs = 0
    for image in all_img:
        if 'width' in image.attrs:
            if (int(image.get("width"))>=200):
                imgs += 1
    

    all_head = soup.find(id="bodyContent").find_all(["h1","h2","h3","h4","h5","h6"])
    headers = 0
    for head in all_head:
        if (('C' in head.text[0])or('T' in head.text[0])or('E' in head.text[0])):
            headers += 1
    

    body = soup.find(id="bodyContent") #возможно не отрабатывает наличие тега внутри ссылки
    # FIXME переделать с next siblings
    links = []
    count = 0
    for tag in body.descendants:
        if tag.name is not None:
            if tag.name == "a":
                count += 1
            else:
                links.append(count)
                count = 0
    linkslen = max(links)

    count = 0
    for ls in body.find_all(['ol','ul']):
        if not ls.find_parent(['ol','ul']):
            count += 1
    lists = count

    return [imgs, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()
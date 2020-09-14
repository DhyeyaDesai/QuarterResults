from requests_html import HTMLSession

def findnth(haystack, needle, n):
	parts= haystack.split(needle, n+1)
	if len(parts)<=n+1:
		return -1
	return len(haystack)-len(parts[-1])-len(needle)


def update(df, url, year):
	session = HTMLSession()
	url2 = url[0:findnth(url, "/", 3)+1]
	r = session.get(url)
	r.html.render(sleep=3, timeout=20)

	all_links = r.html.find('a')

	for a in all_links:
		UncleanedData = ""
		Links = ""
		LinkLabel = ""
		LinkInfo = ""
		try:
			if year in a.attrs['href']:
				link = a.attrs['href']
				if ".com" not in link:
					link = url + "/" + link
				link.replace("//", "/").replace("https:/", "https://").replace("http:/", "http://")
				Links = link
				LinkInfo = link[link.rfind('/')+1: len(link)]
				LinkLabel = a.text
				row = {'Year': year, 
					'Links': Links, 
					'LinkLabel': LinkLabel, 
					'LinkInfo': LinkInfo}
				df = df.append(row, ignore_index=True)
		except KeyError:
			continue
	return df



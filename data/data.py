class Data:
    def getUrl(pageNum):
        url = f"https://ws-public.interpol.int/notices/v1/red?'page={pageNum}&resultPerPage=160"
        return url


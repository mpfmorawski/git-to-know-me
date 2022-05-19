from ...common import gen_url, get_endpoint_data
""" Aggregator base class; this file was create to separate base class from the agregator classes for future purpose """


class AggregationBaseClass():
    gtkm_cookie = None

    def __init__(self):
        pass

    async def _execute_collecting_data(self, URL: str):
        if self.gtkm_cookie:
            particular_data = await get_endpoint_data(gen_url(URL),
                                                      cookie=self.gtkm_cookie)

        return particular_data.json()

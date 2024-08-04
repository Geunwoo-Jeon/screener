from api_client import APIClient


if __name__ == '__main__':
    client = APIClient()
    json = client.income_statement()
    import ipdb
    ipdb.set_trace()

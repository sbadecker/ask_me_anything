from typing import List, Optional, Union

from elasticsearch import Elasticsearch, RequestsHttpConnection
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore


class ElasticsearchDocumentStoreFixed(ElasticsearchDocumentStore):
    def _init_elastic_client(
        self,
        host: Union[str, List[str]],
        port: Union[int, List[int]],
        username: str,
        password: str,
        api_key_id: Optional[str],
        api_key: Optional[str],
        scheme: str,
        ca_certs: Optional[str],
        verify_certs: bool,
        timeout: int,
        aws4auth=None
    ) -> Elasticsearch:
        # Create list of host(s) + port(s) to allow direct client connections to multiple elasticsearch nodes
        if isinstance(host, list):
            if isinstance(port, list):
                if not len(port) == len(host):
                    raise ValueError(
                        "Length of list `host` must match length of list `port`")
                hosts = [{"host": h, "port": p} for h, p in zip(host, port)]
            else:
                hosts = [{"host": h, "port": port} for h in host]
        else:
            hosts = [{"host": host, "port": port}]

        if (api_key or api_key_id) and not (api_key and api_key_id):
            raise ValueError(
                "You must provide either both or none of `api_key_id` and `api_key`")

        if api_key:
            # api key authentication
            client = Elasticsearch(
                hosts=hosts,
                api_key=(api_key_id, api_key),
                scheme=scheme,
                ca_certs=ca_certs,
                verify_certs=verify_certs,
                timeout=timeout,
            )
        elif aws4auth:
            # aws elasticsearch with IAM
            # see https://elasticsearch-py.readthedocs.io/en/v7.12.0/index.html?highlight=http_auth#running-on-aws-with-iam
            client = Elasticsearch(
                hosts=hosts,
                http_auth=aws4auth,
                connection_class=RequestsHttpConnection,
                use_ssl=True,
                verify_certs=True,
                timeout=timeout,
            )
        else:
            # standard http_auth
            client = Elasticsearch(
                hosts=[host],
                port=port,
                http_auth=(username, password),
                scheme=scheme,
                ca_certs=ca_certs,
                verify_certs=verify_certs,
                timeout=timeout,
            )

        # Test connection
        try:
            # ping uses a HEAD request on the root URI. In some cases, the user might not have permissions for that,
            # resulting in a HTTP Forbidden 403 response.
            if username in ["", "elastic"]:
                status = client.ping()
                if not status:
                    raise ConnectionError(
                        f"Initial connection to Elasticsearch failed. Make sure you run an Elasticsearch instance "
                        f"at `{hosts}` and that it has finished the initial ramp up (can take > 30s)."
                    )
        except Exception:
            raise ConnectionError(
                f"Initial connection to Elasticsearch failed. Make sure you run an Elasticsearch instance at `{hosts}` and that it has finished the initial ramp up (can take > 30s)."
            )
        return client

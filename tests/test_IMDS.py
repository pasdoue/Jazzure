from unittest import TestCase

from jazzure.imds import imds

class TestIMDS(TestCase):


    """
        The tests bellow are for version checks.
        As online doc is susceptible of evolving, only test subset of version list. The online doc should be always the bigger set of versioning
    """
    def test_parse_online_doc_scheduled_events_versions(self):

        actual_online_doc_versions = ["2020-07-01","2019-08-01","2019-04-01","2019-01-01","2017-11-01","2017-08-01","2017-03-01"]
        versions = imds.IMDS.parse_online_doc_scheduled_events_versions()
        self.assertTrue(set(versions).issubset(set(actual_online_doc_versions)))

    def test_parse_online_doc_loadbalancer_versions(self):
        actual_online_doc_versions = ["2020-10-01"]
        versions = imds.IMDS.parse_online_doc_loadbalancer_versions()
        self.assertTrue(set(versions).issubset(set(actual_online_doc_versions)))

    def test_parse_online_doc_instance_versions(self):
        actual_online_doc_versions = ["2021-11-01","2019-02-01","2020-12-01","2021-03-01","2021-03-01","2021-11-15","2021-11-15","2020-06-01","2020-09-01","2017-04-02","2017-04-02","2017-04-02","2020-07-15","2020-07-15","2020-10-01","2017-04-02","2023-11-15","2017-08-01","2018-04-02","2017-04-02","2017-04-02","2021-10-01","2020-12-01","2018-10-01","2018-04-02","2017-04-02","2017-08-01","2019-03-11","2017-04-02","2020-06-01","2020-06-01","2021-11-01","2021-12-13","2019-06-01","2017-08-01","2017-08-01","2019-06-04","2021-01-01","2017-04-02","2017-12-01","2017-04-02","2017-12-01"]
        versions = imds.IMDS.parse_online_doc_instance_versions()
        self.assertTrue(set(versions).issubset(set(actual_online_doc_versions)))

    def test_parse_online_doc_attested_data_versions(self):
        actual_online_doc_versions = ["2020-09-01","2018-10-01","2018-10-01","2018-20-01","2018-10-01","2018-10-01","2019-04-30","2019-11-01"]
        versions = imds.IMDS.parse_online_doc_attested_data_versions()
        self.assertTrue(set(versions).issubset(set(actual_online_doc_versions)))
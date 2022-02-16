import unittest
from check_aws_rds_tfstates import check_contents
from check_aws_rds_tfstates import get_rds_instances

class tfstateQueryTest(unittest.TestCase):

    def test_check_contents(self):
        self.assertTrue(check_contents('test-files/SQL_HD_RDS_2019.tfstate_test', 'ms-usbcpewkchpsrhv'))
        self.assertFalse(check_contents('test-files/ModelDBServer.tfstate_test', 'ms-usbcpewkchpsrhv'))

    def test_get_rds_instances(self):
        self.assertGreater(len(get_rds_instances('myapp-')), 0)
        self.assertEqual(len(get_rds_instances('moose-')),0)
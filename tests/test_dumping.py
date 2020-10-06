import os
import config
import unittest
from dumper import Dumper, db


class TestDumpingDatabases(unittest.TestCase):
    def test_dumping(self):
        dump_handler = Dumper(config.backups_path, db.get_connection())
        dumps = dump_handler.dump()

        self.assertEqual(True, len(dumps) > 0, 'Dumps paths list is empty')

        self.assertEqual(
            True,
            len(os.listdir(config.backups_path)) > 0,
            '%s dir must be contains backups' % config.backups_path
        )

        dump_handler.clear()


if __name__ == '__main__':
    unittest.main()

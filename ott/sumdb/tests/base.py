try:
    import unittest2 as unittest
except ImportError:
    import unittest


import logging
log = logging.getLogger(__name__)


class TestBase(object):
    db = None
    do_print = False
    sql_db_name = 'curr'

    @classmethod
    def load_sqlite(cls):
        def get_test_file_uri(test_file):
            """ will send back proper file:////blah/test_file.zip """
            dir_path = get_test_directory_path()
            file_path = "file://{0}".format(os.path.join(dir_path, test_file))
            file_path = file_path.replace('\\', '/')
            return file_path

        if cls.db is None:
            #import pdb; pdb.set_trace()
            gtfs_file = get_test_file_uri('multi-date-feed.zip')
            url = util.make_temp_sqlite_db_uri(cls.sql_db_name)
            cls.db = database_load(gtfs_file, url=url, current_tables=True)
        return cls.db

    @classmethod
    def load_pgsql(cls):
        """ To run this test, do the following:
         x) bin/test  gtfsdb.tests.test_current

         You might also have to do the following:
         a) emacs setup.py - uncomment install_requires='psycopg2'
         b) buildout  # need psychopg2 in bin/test script
         c) comment out "#SKIP_TESTS = True" below
         d) psql -d postgres -c "CREATE DATABASE test WITH OWNER ott;"
         e) bin/test gtfsdb.tests.test_current
        """
        if cls.db is None:
            # import pdb; pdb.set_trace()
            #url = "postgresql://ott@maps7:5432/ott"
            url = "postgresql://ott@localhost/ott"
            schema = "current_test"
            gtfs_file = get_test_file_uri('multi-date-feed.zip')
            cls.db = database_load(gtfs_file, url=url, schema=schema, is_geospatial=True, current_tables=True)
        return cls.db

    @classmethod
    def print_list(cls, list):
        for i in list:
            print(i.__dict__)

    @classmethod
    def check_counts(cls, list1, list2, id='stop_id'):
        """ check first that lists both have content; then chekc that either the lists are diff in size or content """
        # import pdb; pdb.set_trace()
        ret_val = False
        if cls.do_print:
            print_list(list1)
            print_list(list2)
        if len(list1) > 0 and len(list2) > 0:
            if len(list1) != len(list2):
                ret_val = True
            else:
                for i, e1 in enumerate(list1):
                    v1 = getattr(e1, id)
                    v2 = getattr(list2[i], id)
                    if v1 != v2:
                        ret_val = True
                        if cls.do_print:
                            print("{} VS. {}".format(v1, v2))
                        break
        return ret_val

    def check_query_counts(self, clz1, clz2):
        n1 = self.db.session.query(clz1).all()
        n2 = self.db.session.query(clz2).all()
        return self.check_counts(n1, n2)

import _winreg
from com.malhunt.agent.backend.db.ElasticsearchController import ESController


class registry_api:
    file_name = 'registry_db.txt'
    key_path_pairs = [
        (_winreg.HKEY_CURRENT_USER, "Computer\\HKEY_CURRENT_USER"),
        (_winreg.HKEY_CLASSES_ROOT, "Computer\\HKEY_CLASSES_ROOT"),
        (_winreg.HKEY_PERFORMANCE_DATA, "Computer\\HKEY_PERFORMANCE_DATA"),
        (_winreg.HKEY_CURRENT_CONFIG, "Computer\\HKEY_CURRENT_CONFIG"),
        (_winreg.HKEY_USERS, "Computer\\HKEY_USERS")
    ]
    es_handle = ESController()

    def __init__(self):
        pass

    def add_registry(self, registry_key):
        """
        Adds registry entries to database

        registry_key: registry key to be stored
        """

        print(self.es_handle.insertItem(name=registry_key, type='reg', id=registry_key))

    def rem_registry(self, registry_key):
        """
        Adds registry entries to database

        registry_key: registry key to be stored
        """

        try:
            print self.es_handle.purgeItem(name=registry_key, type='reg', id=registry_key)
        except Exception:
            print "Couldn't remove process {}".format(registry_key)

    def check_registry(self, registry_key):
        """
        Queries in a database and checks if process name exists

        """

        # TODO Change to elastic search
        print(registry_key)
        return self.es_handle.fuzzyGetItem(regex=registry_key, type='registry')

    def list_all_keys(self, key, key_name):
        """
        list_all_keys: list<string>

        key : opened key handle, closed after recursion
        key_name: string name of key
        """

        ctr = 0
        while True:
            try:
                subkey = _winreg.EnumKey(key, ctr)
                if subkey == 'Classes':
                    ctr += 1
                    continue
                subkey_name = "{}\\{}".format(key_name, subkey)
                self.add_registry(subkey_name)
                key_handle = _winreg.OpenKey(key, subkey)
                self.list_all_keys(key_handle, subkey_name)
                key_handle.Close()
                ctr += 1
            except OSError as err:
                break

    def fill_keys(self):
        """
        Enumerates all the currently existing processes and adds to db

        """

        for key, path in self.key_path_pairs:
            self.list_all_keys(key, path)
        key_handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE")
        self.list_all_keys(key_handle, 'Computer\\HKEY_LOCAL_MACHINE\\SOFTWARE')

    def add_rem_key_callback(self):
        """
        Watches for registries added or removed
        """
        pass

    def mod_key_callback(self):
        """
        Watches for registry values modified
        """
        pass

    def registry_api(self):
        """
        Starts up the entire process filling and updating task

        """

        self.fill_keys()
        # self.add_rem_key_callback()


if __name__ == '__main__':
    registry_obj = registry_api()
    registry_obj.registry_api()

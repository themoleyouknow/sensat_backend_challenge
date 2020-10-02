import ruamel.yaml
from options import Options


class DBConfiguror(object):
    options = Options(
        host='interviews.ctsaq8pbcych.eu-west-2.rds.amazonaws.com',
        user='admin',
        password='sensatinterview',
        port=3306,
        db='interviews'
    )

    def __init__(self, config_yaml_file=None):
        if config_yaml_file:
            self.configure_options_with_yaml(config_yaml_file=config_yaml_file)

    def _parse_yaml_file_to_dictionary(self, yaml_filepath):
        # Open yaml file and extract dictionary:
        with open(yaml_filepath, 'r') as f:
            argument_dictionary = ruamel.yaml.safe_load(f)
        # Return concatenated string of key-value arguments:
        return argument_dictionary

    def _process_options_input(self, options_dictionary):
        new_dict = {}
        for key, value in options_dictionary.items():
            if key in self.options.keys():
                new_dict[key] = value
        return new_dict

    def configure_options_with_yaml(self, config_yaml_file):
        options_dictionary = self._parse_yaml_file_to_dictionary(config_yaml_file)
        self.options.set(**self._process_options_input(options_dictionary))

    def get_host(self):
        return self.options['host']
    def get_user(self):
        return self.options['user']
    def get_password(self):
        return self.options['password']
    def get_port(self):
        return self.options['port']
    def get_db(self):
        return self.options['db']

if __name__ == '__main__':
    database = DBConfiguror()
    print(database.get_db())


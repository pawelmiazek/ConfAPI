from django.core.management.base import BaseCommand
import json
from nested_lookup import get_all_keys, nested_lookup, nested_update


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("base_file", type=str, help="File which contains base configuration")
        parser.add_argument("params_file", type=str, help="File which contains parameters for new configuration files")

    def handle(self, *args, **options):
        try:
            with open(options["base_file"]) as base_file:
                base_data = json.load(base_file)
            with open(options["params_file"]) as params_file:
                params_data = json.load(params_file)
        except Exception as e:
            return(e)
        
        base_keys = get_all_keys(base_data)
        params_keys = get_all_keys(params_data)

        not_found_params = [param for param in params_keys if param not in base_keys]
        if not_found_params:
            return f"Wrong params config file. These params do not exist in base file: {not_found_params}"
        
        changed_key_values = [key for key in params_keys if isinstance(nested_lookup(key, params_data)[0], list)]

        for key in changed_key_values:
            for value in nested_lookup(key, params_data)[0]:

                new_configuration = nested_update(base_data, key=key, value=value)

                with open(f"configuration_{key}_{value}.json", "w") as outfile:
                    json.dump(new_configuration, outfile)
        
        return "Successfully generated configurations"


        

        

        

        


        
        

        
        

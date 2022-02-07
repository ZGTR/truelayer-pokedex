from ssm_parameter_store import EC2ParameterStore


class ParameterStore(EC2ParameterStore):
    def get_parameters_by_path(self, path, decrypt=True, recursive=True, strip_path=True, strip_root=True):
        parameters = super().get_parameters_by_path(path, decrypt, recursive, strip_path)

        if strip_root:
            new_parameters = dict()

            length = len(path)

            for key in parameters.keys():
                new_parameters[key[length:]] = parameters[key]

            parameters = new_parameters

        return parameters

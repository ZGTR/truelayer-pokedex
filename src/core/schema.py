from flask import request
from marshmallow import Schema, validate
from munch import Munch


class BaseSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    def decorator(self):
        def method_wrapper(method):
            def resource_wrapper(*args, **kwargs):
                available_data = (request.json or dict()).copy()

                form_data = request.form.to_dict()
                available_data.update(form_data)

                query_params = request.args.to_dict()
                available_data.update(query_params)

                # add url user-defined segments to the awesome validation
                available_data.update(kwargs)

                data = self.load(available_data)

                # not passing *args and **kwargs to the method but query parameters and url segments
                # are passed to marshmallow which is nice in validation
                return method(validated_data=Munch(data))

            return resource_wrapper

        return method_wrapper

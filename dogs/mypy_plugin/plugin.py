from mypy.plugin import Plugin


def callback(context):
    # breakpoint()
    return context


class DogsPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str):
        # see explanation below
        # if "dogs.hkt.kind.Kind" == fullname:
        #     return callback
        ...


def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return DogsPlugin

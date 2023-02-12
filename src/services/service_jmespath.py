import jmespath


class ServiceJMESpath:

    def expression(self, query, json):
        engine = jmespath.compile(query)
        return engine.search(json)

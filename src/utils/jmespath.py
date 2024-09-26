import jmespath


class UtilsJMESpath:

    def expression(self, query, json):
        engine = jmespath.compile(query)
        return engine.search(json)

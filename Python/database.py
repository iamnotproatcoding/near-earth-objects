class NEODatabase:
    def __init__(self, neos, approaches):
        self._neos = neos # object produced by the load_neos and load_approaches functions of the extract module
        self._approaches = approaches # represents a collection of CloseApproaches
        self._pdes_to_index = {neo.designation: index for index, neo in enumerate(self._neos)}

        for approach in self._approaches:
            if approach.designation in self._pdes_to_index.keys():
                approach.neo = self._neos[self._pdes_to_index[approach.designation]]
                self._neos[self._pdes_to_index[approach.designation]].approaches.append(approach)
                
        self._des_to_neo = {neo.designation: neo for neo in self._neos}
        self.name_to_neo = {neo.name: neo for neo in self._neos}

    def get_neo_by_designation(self, designation):
        # Used instead of loops
        return self._des_to_neo.get(designation.upper(), None)

    def get_neo_by_name(self, name):
        # Used instead of loops
        return self.name_to_neo.get(name.capitalize(), None)

    def query(self, filters=()):
        if filters:
            for approach in self._approaches:
                if all(map(lambda f: f(approach), filters)):
                    yield approach
        else:
            for approach in self._approaches:
                yield approach
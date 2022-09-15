class NodeNotFound(Exception):
    def __init__(self, id):
        super().__init__(f"Node with id: {id} not found")

class Context:
    """Represents types scope in a python program.

    Attributes:
        types_map ({str, Type}): a dict mapping variable names to their inferred types.
    """

    def __init__(self, parent_context=None):
        self.types_map = {}
        self.parent_context = parent_context
        self.children_contexts = []

        if parent_context:
            parent_context.children_contexts.append(self)

    def get_type(self, var_name):
        if var_name in self.types_map:
            return self.types_map[var_name]
        if self.parent_context is None:
            raise NameError("Name {} is not defined.".format(var_name))
        return self.parent_context.get_type(var_name)

    def set_type(self, var_name, var_type):
        """Sets the type of a variable in this context."""
        self.types_map[var_name] = var_type

    def delete_type(self, var_name):
        if var_name in self.types_map:
            del self.types_map[var_name]
        elif self.parent_context is None:
            raise NameError("Name {} is not defined.".format(var_name))
        else:
            self.parent_context.delete_type(var_name)

    def has_variable(self, var_name):
        if var_name in self.types_map:
            return True
        if self.parent_context is None:
            return False
        return self.parent_context.has_variable(var_name)

    def has_var_in_children(self, var_name):
        """Check if the variable exists in this context or in children contexts"""
        if var_name in self.types_map:
            return True
        for child in self.children_contexts:
            if child.has_var_in_children(var_name):
                return True
        return False

    def get_var_from_children(self, var_name):
        """Get variable type from this context or from children contexts"""
        if var_name in self.types_map:
            return self.types_map[var_name]
        for child in self.children_contexts:
            try:
                return child.get_var_from_children(var_name)
            except NameError:
                continue
        raise NameError("Name {} is not defined".format(var_name))

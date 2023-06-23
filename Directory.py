class Directory:

    def __init__(self):
        self.current_dir = []

    def go_in(self, dir):
        self.current_dir.append(dir)

    def go_in(self):
        self.go_in("")

    def go_out(self):
        if self.current_dir:
            self.current_dir.pop()

    def get_path(self):
        return "/".join(filter(lambda x: x, self.current_dir))
    
    def get_path_with_slash(self):
        # Returns the path with a slash at the end, if the path is not the root
        path_without_slash = self.get_path()
        if path_without_slash:
            return path_without_slash + "/"
        else:
            return path_without_slash
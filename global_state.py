class GlobalState:
    __instance = None
    current_user_id = None

    @staticmethod
    def get_instance():
        if GlobalState.__instance is None:
            GlobalState.__instance = GlobalState()
        return GlobalState.__instance

    def get_current_user_id(self):
        return self.current_user_id

    def set_current_user_id(self, user_id):
        self.current_user_id = user_id

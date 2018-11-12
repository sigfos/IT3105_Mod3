class Settings():

    # Øyv må se over at det stemmer med verdier vs lister og sette default values i config.txt
    def __init__(self):
        self.anet_dim = []
        self.anet_batch_size = None
        self.root_board_dim = None
        self.verbose = False
        self.games = None
        self.simulations = None
        self.input_act = None
        self.output_act = None
        self.anet_init = None
        self.epochs = None
        self.anet_verbose = None
        self.loss = None
        self.optimizer = None
        self.save_interval = None
        self.anet1_file = None
        self.anet2_file = None
        self.tournament = None


def read_file(input_file):
    config = Settings()
    file_obj = open(input_file, 'r')
    for line in file_obj.readlines():
        line_vec = line.split(':')
        label = line_vec[0]
        val_is_set = False
        if line_vec[1] != "\n":
            val = line_vec[1:]
            val_is_set = True

        if label.lower().strip() == "anet_dim":
            if val_is_set:
                anet_dim = []
                for i in range(0, len(val)):
                    anet_dim.append(int(val[i]))
                config.anet_dim = anet_dim

        elif label.lower().strip() == "anet_batch_size":
            config.anet_batch_size = int(val[0].strip())

        elif label.lower().strip() == "root_board_dim":
            config.root_board_dim = int(val[0].strip())

        elif label.lower().strip() == "verbose":
            config.verbose = int(val[0].strip())

        elif label.lower().strip() == "games":
            config.games = int(val[0].strip())

        elif label.lower().strip() == "simulations":
            config.simulations = int(val[0].strip())

        elif label.lower().strip() == "input_act":
            config.input_act = str(val[0].strip())

        elif label.lower().strip() == "output_act":
            config.output_act = str(val[0].strip())

        elif label.lower().strip() == "anet_init":
            config.anet_init = str(val[0].strip())

        elif label.lower().strip() == "epochs":
            config.epochs = int(val[0].strip())

        elif label.lower().strip() == "anet_verbose":
            config.anet_verbose= int(val[0].strip())

        elif label.lower().strip() == "loss":
            config.loss = str(val[0].strip())

        elif label.lower().strip() == "optimizer":
            config.optimizer = str(val[0].strip())

        elif label.lower().strip() == "save_interval":
            config.save_interval = int(val[0].strip())

        elif label.lower().strip() == "anet1_file":
            config.anet1_file = str(val[0].strip())

        elif label.lower().strip() == "anet2_file":
            config.anet2_file = str(val[0].strip())

        elif label.lower().strip() == "tournament":
            config.tournament= int(val[0].strip())
    return config

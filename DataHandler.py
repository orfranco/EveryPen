from Client import Client


class DataHandler:
    """
    this class will handle the data from the client by calculating the
    velocity, acceleration and position according to the data from the client.
    """
    def __init__(self, host, port, param_names, threshold):
        self.client = Client(host, port, self.update_values)
        self.__px, self.__vx, self.__ax, self.__timestamp = 0, 0, 0, None
        self.__param_names = param_names
        self.__threshold = threshold
        self.__pos_vals, self.__vel_vals, self.__acc_vals = [], [], []

    def update_values(self, data):
        """
        this method will update the values of the parameters. should be
        called on every new data from the client.
        :param data: data from client.
        """
        for param_name in self.__param_names:
            # Extract data:
            curr_param = data[data.find(param_name) + len(param_name):]
            curr_param = curr_param[:curr_param.find('\n')]
            timestamp_name = "timestamp:"
            curr_timestamp = data[
                             data.find(timestamp_name) + len(timestamp_name):]
            curr_timestamp = curr_timestamp[:curr_timestamp.find(',')]
            # Calculate new Values:
            if self.__timestamp is not None:
                dt = (float(curr_timestamp) - float(
                    self.__timestamp)) / 1000000
            else:
                dt = 0
            curr_ax = float("{:.7f}".format(float(curr_param)))
            curr_vx = float("{:.7f}".format(self.__vx + curr_ax * dt))
            curr_px = self.__px + curr_vx * dt

            # assign new Values:
            self.__ax = curr_ax
            self.__vx = 0 if (self.__threshold > curr_vx > -self.__threshold) \
                else curr_vx
            self.__px = curr_px
            self.__timestamp = curr_timestamp

            # Update Graph:
            # TODO: realize which scaling factor needed:
            self.__pos_vals.append(self.__px * 10)
            self.__vel_vals.append(self.__vx)
            self.__acc_vals.append(self.__ax)

    def get_values(self):
        """
        this method returns the values of the parameters.
        :return: list of values.
        """
        return [self.__pos_vals, self.__vel_vals, self.__acc_vals]
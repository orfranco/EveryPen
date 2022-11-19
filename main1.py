from KalmanDataHandler import DataHandler
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate(frame, xs, yss, values, lines, ax):
    xs.append(frame)
    for i, ys in enumerate(yss):
        ys.append(values[i][-1])
        x = xs[-40:]
        y = ys[-40:]
        lines[i].set_xdata(x)
        lines[i].set_ydata(y)
    ax.set_xlim(min(x) - 1, max(x) + 1)
    ax.set_ylim(min(yss[0][-40:]) - 2, max(yss[0][-40:]) + 2)
    return lines


if __name__ == "__main__":
    host, port = "localhost", 3001
    param_names = ["acc_x:"]
    threshold = 0.05
    dataHandler = DataHandler(host, port, param_names, threshold)

    fig, ax = plt.subplots()
    xs, ys_pos, ys_vel, ys_acc = [], [], [], []
    pos_vals, vel_vals, acc_vals = [0], [0], [0]
    line_pos, = ax.plot(xs, ys_pos, 'r-')
    line_vel, = ax.plot(xs, ys_vel, 'g-')
    line_acc, = ax.plot(xs, ys_acc, 'b-')
    ax.set_xlim(0, 100)
    ax.set_ylim(-100, 100)
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.title('Live Graph')
    ani = animation.FuncAnimation(fig, animate,
                                  fargs=(xs, [ys_pos, ys_vel, ys_acc],
                                         dataHandler.get_values(),
                                         [line_pos, line_vel, line_acc],
                                         ax), interval=1)
    plt.show()

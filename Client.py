import socketio
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# standard Python
sio = socketio.Client()

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
xs = []
ys = []
curr = [0]
line, = ax1.plot(xs, ys)
plt.xlabel('Time')
plt.ylabel('acc_z')
plt.title('Live Graph')


def animate(frame, xs, ys):
    xs.append(frame)
    ys.append(curr[-1])
    x = xs[-40:]
    y = ys[-40:]
    line.set_xdata(x)
    line.set_ydata(y)
    ax1.set_xlim(min(x) - 1, max(x) + 1)
    ax1.set_ylim(min(y) - 10, max(y) + 10)
    ax1.set_xticks(list(range(min(x), max(x) + 1)))
    return line


@sio.event
def message(data):
    print('I received a message!')


@sio.on('recieve-data')
def on_message(data):
    global curr
    param_name = "quaternion_w:"
    next_param = "quaternion_x:"
    param_with_name = data[data.find(param_name):data.find(next_param)]
    # print(data[data.find("acc_z:"):data.find("gyr_x:")])
    param = param_with_name[len(param_name):]
    curr.append(float(param))


@sio.event
async def message(data):
    print('I received a message!')


@sio.on('*')
def catch_all(event, data):
    pass


@sio.on('*')
async def catch_all(event, data):
    pass


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")
    exit()


sio.connect('http://localhost:3001')

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)
plt.show()

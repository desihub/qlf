from bokeh.plotting import figure, output_file, curdoc
from bokeh.models import ColumnDataSource, LabelSet, Label
from bokeh.driving import count
import configparser

from dashboard.bokeh.helper import get_last_process

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

try:
    cfg.read('%s/qlf/config/qlf.cfg' % qlf_root)
    scratch = cfg.get('namespace', 'scratch')
except Exception as error:
    print(error)
    print("Error reading  %s/qlf/config/qlf.cfg" % qlf_root)

process = get_last_process()

print(process)

process = process.pop()
PROCESSID = process.get("id")
EXPOSURE = process.get("exposure")

bars = list()
label_name = list()
cameras = dict()
listColor = list()

# AF: height of the bars in the bokeh chart
barsHeight = list()

for num in range(30):
    # AF: add bars
    bars.append(num)
    listColor.append('#0000FF')
    barsHeight.append(0.5)
    # AF: add labels for cameras and processing steps

    if 'z9' not in label_name:
        cameras['z' + str(num)] = Label(x=-6.5, y=num - .3, text='z' + str(num))
        cameras['stagez' + str(num)] = Label(x=50, y=num - .3, text='Initializing ', background_fill_color='white',
                                             background_fill_alpha=0.7)
        label_name.append('z' + str(num))
    elif 'r9' not in label_name:
        cameras['r' + str(num - 10)] = Label(x=-6.5, y=num - .3, text='r' + str(num - 10))
        cameras['stager' + str(num - 10)] = Label(x=50, y=num - .3, text='Initializing ',
                                                  background_fill_color='white', background_fill_alpha=0.7)
        label_name.append('r' + str(num - 10))
    elif 'g9' not in label_name:
        cameras['g' + str(num - 20)] = Label(x=-6.5, y=num - .3, text='g' + str(num - 20))
        cameras['stageg' + str(num - 20)] = Label(x=50, y=num - .3, text='Initializing ', render_mode='css',
                                                  background_fill_color='white', background_fill_alpha=0.7)
        label_name.append('g' + str(num - 20))

title = "Process ID: %i ~ Exposure ID: %i" % (PROCESSID, EXPOSURE)

plot = figure(title=title, height=900, x_range=(-9, 120))
for cam in cameras:
    plot.add_layout(cameras[cam])

# AF: Move plot style configuration to theme.yaml
plot.xaxis.visible = False
plot.yaxis.visible = False

sourceBar = ColumnDataSource(dict(y=[0], right=[0], height=[0], color=['#0000FF']))
plot.hbar(y='y', right='right', height='height', color='color', source=sourceBar)
curdoc().add_root(plot)


@count()
def update(t):
    barsRight = list()

    for num in range(30):
        barsRight.append(0)

    process = get_last_process().pop()

    if process.get('id') != PROCESSID or process.get('exposure') != EXPOSURE:
        PROCESSID = process.get('id')
        EXPOSURE = process.get('exposure')
        plot.title = "Process ID: %i ~ Exposure ID: %i" % (PROCESSID, EXPOSURE)

    # AF: loop over cameras
    for cam in cameras:
        if cam[:5] != 'stage':
            log = list()
            try:
                for item in process.get("jobs"):
                    if cam == item.get("camera"):
                        #TODO
                        cameralog = ""
                arq = open('../test/log/' + cam + '.log', 'r')
                log = arq.readlines()
            except Exception as e:
                e
            if cam[:1] == 'z':
                barsRight[int(cam[1:])] = len(log)
            if cam[:1] == 'r':
                barsRight[int(cam[1:]) - 20] = len(log)
            if cam[:1] == 'g':
                barsRight[int(cam[1:]) - 10] = len(log)

            # AF: currrent line

            for line in log[::-1]:
                if 'Pipeline completed' in line:
                    cameras['stage' + cam].text = 'Pipeline completed'
                    break
                elif 'Sky Subtraction' in line:
                    cameras['stage' + cam].text = 'Sky Subtraction'
                    break
                elif 'Boxcar Extraction' in line:
                    cameras['stage' + cam].text = 'Boxcar Extraction'
                    break
                elif 'Preprocessing' in line:
                    cameras['stage' + cam].text = 'Preprocessing'
                    break
                elif 'Initializing' in line:
                    cameras['stage' + cam].text = 'Initializing'
                    break

    new_datat = dict(y=bars, right=barsRight, height=barsHeight, color=listColor)
    sourceBar.stream(new_datat, 30)


curdoc().add_periodic_callback(update, 100)

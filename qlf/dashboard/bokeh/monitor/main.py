from bokeh.plotting import figure, output_file, curdoc
from bokeh.models import ColumnDataSource, LabelSet, Label
from bokeh.driving import count
import random


bars_list = list()
label_name = list()
labels_dict = dict()
listColor=list()

# AF: height of the bars in the bokeh chart
heightList=list()



for i in range(30):
    # AF: not used below
    n = random.randint(1,7)
    listColor.append('#0000FF')
    heightList.append(0.5)
    
for i in range(30):
    # AF: add bars
    bars_list.append(i)
   
    # AF: add labels for camera and processing steps
    
    if 'z9' not in label_name:
        labels_dict['z' + str(i)] = Label(x=-6.5, y = i -.3, text='z' + str(i))
        labels_dict['stagez' + str(i)] = Label(x=50, y = i -.3, text='start ' + str(i), background_fill_color='white', background_fill_alpha=0.7)
        label_name.append('z' + str(i))
    elif 'r9' not in label_name:
        labels_dict['r' + str(i - 10)] = Label(x=-6.5, y = i -.3, text='r' + str(i - 10))
        labels_dict['stager' + str(i - 10)] = Label(x=50, y = i -.3, text='start ' + str(i), background_fill_color='white', background_fill_alpha=0.7)
        label_name.append('r' + str(i - 10))
    elif 'g9' not in label_name:
        labels_dict['g' + str(i - 20)] = Label(x=-6.5, y = i -.3, text='g' + str(i - 20))
        labels_dict['stageg' + str(i - 20)] = Label(x=50, y = i -.3, text='start ' + str(i), render_mode='css', background_fill_color='white', background_fill_alpha=0.7)
        label_name.append('g' + str(i - 20))

# AF: y is not being used anywhere
y = bars_list

plot = figure(title="Monitor", height=900, x_range=(-9, 120))
for i in labels_dict:
    plot.add_layout(labels_dict[i]) 

# AF: Move plot style configuration to theme.yaml
plot.xaxis.visible = False
plot.yaxis.visible = False

sourceBar = ColumnDataSource(dict(y=[0], right=[0], height=[0], color=['#0000FF']))
plot.hbar(y='y', right='right', height='height', color='color', source=sourceBar)
curdoc().add_root(plot)

@count()
def update(t):
    lista = []
    # AF: not being used
    urls_dict = dict()
    
    # AF: ?
    name = 'Running'
    
    for i in range(30):
        lista.append(0)
        
    try:
        
        # AF: loop over cameras 
        for i in labels_dict:
            if i[:5] != 'stage':            
                # AF: add example of log files in qlf/test/logs and use a relative path here
                arq = open('/home/rafael/qlf-17/qlf/dashboard/bokeh/monitor/teste_log/'+i+'.log', 'r')
                log = arq.readlines()
                if i[:1] == 'z':
                    lista[int(i[1:])] = len(log)
                if i[:1] == 'r':
                    lista[int(i[1:]) - 20] = len(log)
                if i[:1] == 'g':
                    lista[int(i[1:]) - 10] = len(log)
                
                # AF: currrent line
                stage = log[len(log) -1]
                
                if 'QuickLook INFO' in stage:
                    
                    # AF: replace this by a search for the processing steps defined in the design
                    if stage.split(':')[3].split()[0] == 'Running' or stage.split(':')[3].split()[0] == 'Pipeline':
                        name = stage.split(':')[3].split()[0] +' '+ stage.split(':')[3].split()[1]
                        labels_dict['stage'+ i].text = name
                        
    except Exception as e:
        for i in labels_dict:
            if i[:5] != 'stage':
                labels_dict['stage'+ i].text = 'Log not found'
    new_datat = dict(y=y, right=lista, height=heightList, color=listColor)
    sourceBar.stream(new_datat, 30)

curdoc().add_periodic_callback(update, 100)

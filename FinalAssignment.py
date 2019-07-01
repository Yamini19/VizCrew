import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import matplotlib.pyplot as plt
import flask

A = np.fromfile("slice150.raw", dtype='int16')

Array2D = np.reshape(A, (512, 512))

plt.imshow(Array2D,cmap= "gray")
plt.title ("Original Image")
plt.savefig("OriginalImage.png")

def median(value, str):

    MedianFilter = np.zeros(shape=(len(Array2D), len(Array2D)))
    x = ((2 * value) + 1) ** 2
    for i in range(value, len(Array2D) - value):
        for j in range(value, len(Array2D) - value):

            arr = np.reshape((Array2D[i - value:i + value+1, j - value:j + value+1]), x)
            arr = np.sort(arr)
            MedianFilter[i][j] = arr[int((x-1)/2)]


    ax,fig = plt.subplots()
    fig.imshow(MedianFilter, cmap="gray")
    fig.set_title("Image with Median Filter")
    ax.savefig(str)


image_directory = '/Users/yamini/PycharmProjects/freshstart/'
static_image_route = '/'

def smooth(value, str):
    Smoothing = np.zeros(shape=(len(Array2D), len(Array2D)))

    for i in range(value, len(Array2D) - value):
        for j in range(value, len(Array2D) - value):
            Smoothing[i][j] = np.mean(Array2D[i - value:i + value+1, j - value:j + value+1])
    ax6, fig6 = plt.subplots()
    fig6.imshow(Smoothing, cmap="gray")
    fig6.set_title("Image with Smoothing Filter")
    ax6.savefig(str)

def transform(value,str):
    minA = min(A)
    maxA = max(A)
    NonLinearTrans = np.zeros(shape=(len(Array2D), len(Array2D)))
    for i in range(0, len(Array2D)):
        for j in range(0, len(Array2D)):
            if value == "square":
                NonLinearTrans[i][j] = 0 + ((4 * ((Array2D[i][j] - minA) ** 2) / (4 * ((maxA - minA) ** 2))) * (255))
            if value == "log":
                NonLinearTrans[i][j] = 0 + np.log(Array2D[i][j] + 1)
            if value == "cubic":
                NonLinearTrans[i][j] = 0 + ((4 * ((Array2D[i][j] - minA) ** 3) / (4 * ((maxA - minA) ** 2))) * 255)
            if value == "Square root":
                NonLinearTrans[i][j] = 0 + ((4 * ((Array2D[i][j] - minA) ** 0.5) / (4 * ((maxA - minA) ** 2))) * (255))
    ax5, fig5 = plt.subplots()
    fig5.imshow(NonLinearTrans, cmap="gray")
    fig5.set_title("Image for " + value + " Transformation")
    ax5.savefig(str)

def contrast(value,str):
    minA = min(A)
    maxA = max(A)
    for i in range(0, len(Array2D)):
        for j in range(0, len(Array2D)):
            Array2D[i][j] = 0 + (((Array2D[i][j] - minA) / (maxA - minA)) * (255 - 0))
    if value == 1 :
        plt.imshow(Array2D, cmap=plt.cm.gray, vmin= 45, vmax=200)
    if value == 2 :
        plt.imshow(Array2D, cmap=plt.cm.gray, vmin= 60, vmax=190)
    if value == 3 :
        plt.imshow(Array2D, cmap=plt.cm.gray, vmin= 75, vmax=180)
    if value == 4 :
        plt.imshow(Array2D, cmap=plt.cm.gray, vmin= 95, vmax=160)
    plt.title("Image with Contrast")
    plt.savefig(str)

#  Smoothening


# smooth(1,"Smoothing0.png")
# smooth(3,"Smoothing1.png")
# smooth(5,"Smoothing2.png")
# smooth(7,"Smoothing3.png")
#
# #  Transformation
#
#
# transform("square","Transformation0.png")
# transform("log","Transformation1.png")
# transform("cubic","Transformation2.png")
# transform("Square root","Transformation3.png")
#
# #  Median Filter
#
# median(1,"Medianfilter0.png")
# median(3,"Medianfilter1.png")
# median(5,"Medianfilter2.png")
# median(7,"Medianfilter3.png")
#
#
# #  Contour
#
# contrast(1,"Contrast0.png")
# contrast(2,"Contrast1.png")
# contrast(3,"Contrast2.png")
# contrast(4,"Contrast3.png")

app = dash.Dash()

app.layout = html.Div([

    html.Div([
        html.H2("Vis-Crew"),
        html.Img(src="/assets/logo.png")],className='banner'),

    html.Div([
        html.Div([
                    html.Div([
                        dcc.RadioItems(
                            id="RadioButton",
                            options=[
                                {'label': 'Smoothening', 'value': 'Smoothing'},
                                {'label': 'Transformation', 'value': 'Transformation'},
                                {'label': 'Median Filter', 'value': 'Medianfilter'},
                                {'label': 'Contrast', 'value': 'Contrast'}
                            ],
                            value='Smoothing'
                        ,labelStyle={'display':'inline-block','margin-left':'60px'})
                    ],className="rdobtn")
                    ],className="containerOuter")
            ,

            html.Div([
                dcc.Slider(
                    id="slider",
                min=0,
                max=3,


                value=0,


            )],style={ 'margin':5, 'textAlign': 'center', 'padding':'25px','label':'200px','background':'#f9f9f9'
                       ,'padding-left':'40px','border-radius': '25px'}

            ),


        html.Div([

            html.Div([
                html.Img(id='image1',src="http://127.0.0.1:8050/OriginalImage.png", height=400,width=400)

            ],className="six columns"),
            html.Div([
                html.Img(id='image', height=400,width=400),

            ],className="six columns")


        ],className='Image box')



    ])


])



@app.callback(
    dash.dependencies.Output('slider','marks'),
    [dash.dependencies.Input('RadioButton', 'value')])

def update_slider(value):
    marks={}
    if(value=='Smoothing'):

        marks = {0: 'Low',
                 1 : 'Medium',
                 2: 'High',
                 3: 'Very High'}

    if(value=='Transformation'):
        marks = {0: 'Square',
                 1: 'Log',
                 2: 'Cubic',
                 3: 'Square-root'}

    if(value=='Medianfilter'):
        marks = {0: 'Low',
                 1: 'Medium',
                 2: 'High',
                 3: 'Very High'}

    if (value == 'Contrast'):
        marks = {0: 'Level 1',
                 1: 'Level 2',
                 2: 'Level 3',
                 3: 'Level 4'}
    return marks


@app.callback(
    dash.dependencies.Output('image','src'),
    [dash.dependencies.Input('slider', 'value'),
     dash.dependencies.Input('RadioButton', 'value')])

def update_image_src(value1,value2):
    return value2 + str(value1) + ".png"

@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)

    return flask.send_from_directory(image_directory, image_name)

if __name__ == '__main__':
    app.run_server(debug=True)


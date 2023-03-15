import tkinter as tk
from tkinter import *
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from matplotlib.widgets import Slider, Button

def getval():
    global res1
    global res2
    res1=np.float64(val1.get())
    res2=np.float64(val2.get())

def vis():
    global t,f,RMSE
    t = np.linspace(0,3.01,num=len(data))

    init_tao = res1
    init_Tn = res2
    f=np.vectorize(Ht)
    fig, ax = plt.subplots(figsize=(12, 6))

    line, = plt.plot(t,data, lw=2)
    line, = plt.plot(t,f(init_tao, init_Tn, t), lw=2)
    ax.set_xlabel('time [s]')
    ax.set_ylabel("H(t)")

    plt.subplots_adjust(left=0.25, bottom=0.25)

    plt.grid()
    axtao = plt.axes([0.25, 0.1, 0.65, 0.03])

    tao_slider = Slider(
        ax=axtao,
        label='Damping Ratio (Tao)',
        valmin=0,
        valmax=4,
        valinit=init_tao,
    )

    axTn = plt.axes([0.25, 0, 0.65, 0.03])
    Tn_slider = Slider(
        ax=axTn,
        label="Free Oscillation Period (Tn)",
        valmin=0,
        valmax=4,
        valinit=init_Tn,

    )

    def update(val):
        global sp1,sp2,RMSE
        line.set_ydata(f(tao_slider.val, Tn_slider.val,t))
        sp1=tao_slider.val
        sp2=Tn_slider.val

        fig.canvas.draw_idle()
        cal1 = []
        obs1 = []

        for a in range(len(t)):
            cal1.append(f(optimal_tao, optimal_Tn, t[a]))
            obs1.append(f(sp1, sp2, t[a]))
        diff = np.subtract(cal1, obs1)
        square = np.square(diff)
        MSE = square.mean()
        RMSE = str(round((np.sqrt(MSE)).real*100,4))
        var.set(RMSE)

        ax.set_title("RMS (%) :"+RMSE)

    tao_slider.on_changed(update)
    Tn_slider.on_changed(update)

    resetax = plt.axes([0.8, 0.125, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')


    def reset(event):
        tao_slider.reset()
        Tn_slider.reset()

    button.on_clicked(reset)

    plt.show()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()


def saved_plot():

    fig = plt.figure(figsize=(4, 4))

    t = np.arange(0,3.01,0.01)

    f=np.vectorize(Ht)
    plt.plot(t,f(sp1,sp2,t))

    plt.grid()
    plt.xlabel('time [s]')
    plt.ylabel("H(t)")
    plt.title("Tao :"+str(round(sp1,3))+" Tn :"+ str(round(sp2,3)))

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()


    canvas.get_tk_widget().grid(row=3, column=1, sticky=tk.EW,
                                   columnspan=4, rowspan=3, padx=1, pady=5)

    toolbarFrame = tk.Frame(master=root)
    toolbarFrame.grid(row=9, column=1, sticky=tk.EW,columnspan=4, rowspan=1, padx=2, pady=5)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

def Ht(tao,Tn,t):
    wn=(np.pi*2)/Tn
    c1=(wn* math.exp(-tao*wn*t))
    c2=np.power((1-np.power(tao,2,dtype=complex).real),(1/2),dtype=complex).real
    c3=np.sin(wn * t * np.power((1-np.power(tao,2,dtype=complex).real),(1/2),dtype=complex).real)
    c4=((c1)/c2)*c3
    return c4

if __name__ == "__main__":
    cal=0
    obs=0
    var1=10
    var2=10
    data = np.genfromtxt(r'C:\Users\xboxm\vs_workspace\github_projects\seismometer_function_program\private_data.dat',
                         skip_header=1,
                         skip_footer=1,
                         names=True,
                         dtype=None,
                         delimiter=' ')
    optimal_tao=0.707
    optimal_Tn=1

    df = None
    output = None
    root = tk.Tk()
    root.geometry('655x640')
    root.title("Seismometer")
    root["bg"]="#5F9EA0"
    style=ttk.Style(root)
    style.theme_use("clam")
    var=IntVar()


    img = PhotoImage(file=r"C:\Users\xboxm\vs_workspace\github_projects\seismometer_function_program\logo.png")
    img1 = img.subsample(1,1 )

    Label(root, image=img1).grid(row=3, column=1, sticky=tk.E,
                                   columnspan=3, rowspan=2, padx=5, pady=5)

    L1 = Label(root,height=1,width=15, text="Initial Tao:",bg="#E0FFFF")
    L1.grid(column=0, row=1, sticky=tk.E,pady=2)

    L_name = Label(root,height=2,width=30, text="Seismometer Damping Function",bg="#E0FFFF")
    L_name.grid(column=1, row=0, sticky=tk.E,pady=2)

    val1 = tk.Entry(root, width=20,bg="#E0FFFF")
    val1.grid(column=1, row=1, sticky=tk.W,columnspan=2,pady=2)

    L2 = Label(root, height=1, width=15, text="Initial Tn:",bg="#E0FFFF")
    L2.grid(column=0, row=2, sticky=tk.E,pady=2)

    val2 = tk.Entry(root, width=20,bg="#E0FFFF")
    val2.grid(column=1, row=2, sticky=tk.W,columnspan=2, pady=2)

    b = tk.Button(root,height=1,width=10, text='Enter values',bg="#E0FFFF", command=getval)
    b.grid(column=2, row=1, sticky=tk.W,columnspan=1,pady=5)

    b1 = tk.Button(root,height=1,width=10, text='Determinate',bg="#E0FFFF", command=vis)
    b1.grid(column=3, row=1, sticky=tk.W,columnspan=1,pady=5)

    err = Label(root, textvariable=var,bg="#E0FFFF")  # shows as text in the window
    err.grid(column=4, row=2, sticky=tk.E,pady=2)

    Label_err = Label(root,height=1,width=15, text="RMS (%) :",bg="#E0FFFF")
    Label_err.grid(column=3, row=2, sticky=tk.E,pady=2)

    b2 = tk.Button(root,height=1,width=10, text='Show graph',bg="#E0FFFF", command=saved_plot)
    b2.grid(column=4, row=1, sticky=tk.W,columnspan=2,pady=5)

    root.mainloop()
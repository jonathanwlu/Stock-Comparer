import os.path as op
import pyodbc
import pandas as pd
from pandas.io.sql import DatabaseError
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pylab as pl
import matplotlib.dates as mdates

sqlFile = 'query'


def plot(sym, sym2, date):
    with open(sqlFile + '.sql', 'r') as f:
        sql = f.read().replace('SYM1', sym.upper()).replace('SYM2', sym2.upper()).replace('DATE', date)

    df = pd.read_sql(sql, cnxn, index_col=['TradeDate'])
    if df.empty:
        raise ValueError()

    ax = axes[0]
    ax.clear()
    df.iloc[:, :2].plot(ax=ax, legend=False, xticks=[])
    ax.set_ylabel('Px')
    ax.set_title(sym.upper() + '-' + sym2.upper())

    ax2 = axes[1]
    ax2.clear()
    df.iloc[:, 2:].plot(ax=ax2, xticks=[])
    ax2.legend(df.columns[:2], loc='best', shadow=True, prop={'size': 6})
    ax2.set_xlabel('')
    ax2.set_ylabel('IV')

    ax2.xaxis.set_tick_params(reset=True)
    ax2.xaxis.set_major_locator(mdates.YearLocator(1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.minorticks_off()

    fig.autofmt_xdate(ha='center')

    fig.tight_layout()

cnxn = pyodbc.connect("Driver={SQL Server};Server=[server];UID=[user];PWD=[pw];Database=stocks;")

fig, axes = pl.subplots(nrows=2, ncols=1, sharex='all')

# control panel #
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


def update():
    textbox.selectAll()
    textbox.setFocus()
    try:
        plot(textbox.text(), textbox2.text(), textbox3.text())
        print('updating')
        fig.canvas.draw_idle()
        return True
    except (DatabaseError, ValueError):
        print('one or more entries are invalid')
        return False


def next_box():
    textbox2.selectAll()
    textbox2.setFocus()


def next_box_2():
    textbox3.selectAll()
    textbox3.setFocus()


def save_pic():
    if update():
        fig.savefig(op.join('out', textbox.text().upper() + '-' + textbox2.text().upper() + '.png'))


root = fig.canvas.manager.window
panel = QtWidgets.QWidget()
hbox = QtWidgets.QHBoxLayout(panel)

textbox = QtWidgets.QLineEdit(parent=panel)
textbox.returnPressed.connect(next_box)
hbox.addWidget(textbox)
hbox.addSpacing(10)

textbox2 = QtWidgets.QLineEdit(parent=panel)
textbox2.returnPressed.connect(next_box_2)
hbox.addWidget(textbox2)
hbox.addSpacing(10)

textbox3 = QtWidgets.QLineEdit(parent=panel)
textbox3.returnPressed.connect(update)
hbox.addWidget(textbox3)
hbox.addSpacing(10)

but1 = QtWidgets.QPushButton('Plot', parent=panel)
but1.clicked.connect(update)
hbox.addWidget(but1)
hbox.addSpacing(10)

but2 = QtWidgets.QPushButton('Save', parent=panel)
but2.clicked.connect(save_pic)
hbox.addWidget(but2)

panel.setLayout(hbox)

dock = QtWidgets.QDockWidget(parent=root)
dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
root.addDockWidget(Qt.BottomDockWidgetArea, dock)
dock.setWidget(panel)

toolbar = root.findChild(QtWidgets.QToolBar)
toolbar.setVisible(False)

root.setFixedSize(1024, 768)
root.statusBar().setSizeGripEnabled(False)
######################

textbox.setText('QQQ')
textbox2.setText('SPY')
textbox3.setText('1/1/11')
textbox.selectAll()
textbox.setFocus()

plot('QQQ', 'SPY', '1/1/11')
pl.show()

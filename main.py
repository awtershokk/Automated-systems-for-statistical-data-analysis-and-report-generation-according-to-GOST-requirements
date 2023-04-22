import sys
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog


# Определяем класс MainWindow, который наследуется от класса MainWindow
class MainWindow(QMainWindow):
    # Задаем парамертры окна
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #C5DDD8")
        self.setWindowTitle('Automation system')

        self.select_file_btn = QPushButton('Выбрать файл', self)
        self.select_file_btn.setGeometry(50, 50, 200, 50)
        self.select_file_btn.setFont(QtGui.QFont('Verdana', 12, QtGui.QFont.Bold))
        self.select_file_btn.setStyleSheet("background-color: #CECB8D")
        self.select_file_btn.clicked.connect(self.select_file)

        self.select_save_path_btn = QPushButton('Сохранить как', self)
        self.select_save_path_btn.setGeometry(50, 120, 200, 50)
        self.select_save_path_btn.setFont(QtGui.QFont('Verdana', 12, QtGui.QFont.Bold))
        self.select_save_path_btn.setStyleSheet("background-color: #CECB8D")
        self.select_save_path_btn.clicked.connect(self.select_save_path)

        self.start_btn = QPushButton('Старт', self)
        self.start_btn.setGeometry(50, 190, 200, 50)
        self.start_btn.setFont(QtGui.QFont('Verdana', 12, QtGui.QFont.Bold))
        self.start_btn.setStyleSheet("background-color: #CECB8D")
        self.start_btn.clicked.connect(self.start)

        self.selected_file_label = QLabel('Выберите файл', self)
        self.selected_file_label.setGeometry(270, 50, 1500, 50)
        self.selected_file_label.setFont(QtGui.QFont('Verdana', 12, QtGui.QFont.Bold))

        self.selected_save_path_label = QLabel('Выберите путь для сохранения', self)
        self.selected_save_path_label.setGeometry(270, 120, 1500, 50)
        self.selected_save_path_label.setFont(QtGui.QFont('Verdana', 12, QtGui.QFont.Bold))

        self.setGeometry(100, 100, 700, 290)
        self.show()

    # Обработчик кнопки "Выберите файл"
    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', 'All Files (*.*)')
        if file_name:
            self.selected_file_label.setText(file_name)
            self.current_file = file_name

    # Обработчик кнопки "Сохранить как"
    def select_save_path(self):
        file_path = QFileDialog.getExistingDirectory(self, 'Выберите путь для сохранения')
        if file_path:
            self.selected_save_path_label.setText(file_path)
            self.save_path = file_path

    # Обработчик кнопки "Старт"
    def start(self):
        if hasattr(self, 'current_file') and hasattr(self, 'save_path'):
            import shutil
            import os
            file_name = self.current_file
            dest_path = os.path.join(self.save_path, os.path.basename(file_name))

            # Считывание файла
            with open(file_name) as f:
                x = np.genfromtxt(f, delimiter=',')

            # Задаем размеры нашей будущей таблицы
            m = len(x) // 3
            n = 3

            # Задаем параметры документа
            s = '\\documentclass[utf8x, 12pt]{G7-32} \n'
            s += '\\begin{document} \n'
            s += '\\setcounter{table}{0} \n'
            s += r'\renewcommand{\thetable}{\arabic{table}} ' + '\n'
            s += r'\renewcommand{\theequation}{\arabic{equation}} ' + '\n'

            # Создаем таблицу и наполняем ее данными из считанного файла
            s += '\\begin{table} \n'
            s += '\\centering \n'
            s += '\\caption{Экспериментальные данные} \n'
            s += '\\begin{tabular}{|c|c||c|c||c|c|} \n'
            s += '\\hline \n'
            names = " & ".join(['№', '$x$'] * 3)
            s += f'{names} \\\  \n'
            s += '\\hline \n'
            for i in range(m):
                for j in range(n):
                    if j: s += ' & '
                    s += str(i + j * m + 1) + ' & ' + '{0:.2f}'.format(x[i + j * m])
                s += ' \\\\ \n\\hline \n'
            s += '\\end{tabular} \n'
            s += '\\end{table} \n'

            # Проводим все вычичсления и записываем их в переменную s
            s += 'Вычислим среднее арифметическое случайной величины $X$ по формуле (1): \n'
            s += '\\begin{equation} \n'
            mean = '{0:.2f}'.format(np.mean(x))
            s += '\\bar{x}=\\frac{1}{n} \sum_{i=1}^n x_i =' + f'{mean} \n'
            s += '\\end{equation} \n'
            s += '\n'
            s += 'Далее вычислим среднее квадратическое отклонение $S$  случайной величины $x$ по формуле (2): \n'
            s += '\\begin{equation} \n'
            sred = '{0:.2f}'.format(np.std(x))
            s += '\\sigma_X=\sqrt{\\frac{\sum_{i=1}^n\left(x_i-\\bar{x}\\right)^2}{n-1}} = ' + f'{sred} \n'
            s += '\\end{equation} \n'
            s += '\n'
            s += 'Вычислим среднее квадратическое отклонение среднего арифмитического для случайной величины $x$ по формуле (3): \n'
            s += '\\begin{equation} \n'
            sredarifm = '{0:.2f}'.format(float(sred) / n * 0.5)
            s += '\\sigma_{\\bar{X}}=\\frac{\sigma_X}{\sqrt{n}} = ' + f'{sredarifm} \n'
            s += '\\end{equation} \n'
            s += '\n'
            s += 'Доверительные границы неисключенной систематической погрешности $\\sigma_{\\theta}$ заданы паспортом термодатчика DS18B20: \n'
            s += '\\begin{equation} \n'
            s += '\\sigma_\\theta=0.5^{\circ} \mathrm{C} \n'
            s += '\\end{equation} \n'
            s += '\n'
            s += 'Теперь вычислим суммаруню погрешность имзеряемой величины по формуле (5): \n'
            s += '\\begin{equation} \n'
            pogr = '{0:.2f}'.format((0.5 ** 2 + float(sredarifm) ** 2) * 0.5)
            s += '\\Delta=\sqrt{\sigma_\\theta^2+\sigma_{\\bar{X}}^2} = ' + f'{pogr} \n'
            s += '\\end{equation} \n'
            s += '\n'
            s += 'В итоге, используя формулы (1) и (6), получим: \n'
            s += '\\begin{equation} \n'
            s += '\\mathrm{X}=\\bar{X} \pm \Delta = ' + f'{mean}' + '\pm' + f'{pogr} \n'
            s += '\\end{equation} \n'
            s += '\end{document}'

            #Создаем папку с обработанным и всеми сопуутсвующими файлами и копируем их в выбранную пользователем директорию
            with open('tex/otchet.tex', 'w', encoding='utf-8') as f:
                f.write(s)

            dst = self.save_path
            src = 'tex/'
            file_names = [
                'G2-105.sty',
                'G7-32.cls',
                'G7-32.sty',
                'GostBase.clo',
                'otchet.tex'
            ]

            result_folder = os.path.join(dst, 'result')

            if not os.path.exists(result_folder):
                os.mkdir(result_folder)

            for name in file_names:
                shutil.copy(os.path.join(src, name), os.path.join(result_folder, name))

            os.system(f'cd {result_folder} && pdflatex otchet.tex && exit')

            #Вывод сообщения о успешной обработке файла
            self.selected_file_label.setText('Файл успешно обработан')
            self.selected_save_path_label.setText('Результат сохранен в ' + self.save_path)

        else:
            self.selected_file_label.setText('Выберите файл')
            self.selected_save_path_label.setText('Выберите путь для сохранения')

#Запуск программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
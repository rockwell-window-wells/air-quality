'''exportmethods.py: Classes and functions for producing the desired PDF report
after a plot has been generated.

'''

from fpdf import FPDF
import os

class SingleDayPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def header(self):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`

        # Check the name of the current folder. Navigate to the place where the logo is accessible.
        if os.path.basename(os.getcwd()) == "dist":
            path_parent = os.path.dirname(os.getcwd())
            print("Changing directories to {}".format(path_parent))
            os.chdir(path_parent)
        elif os.path.basename(os.getcwd()) == "AirQualityApp":
            print("Currently in AirQualityApp directory")

        self.image('assets/RockwellFullLogo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'Styrene Report', 0, 0, 'R')
        self.ln(20)

        # # Go back to the dist folder
        # os.chdir("dist")

    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 5, 'Generated by Styrene Analysis Tool', 0, 1, 'C')
        self.cell(0, 5, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, date, tstart, tend, plot, twa, peak, ste, employee):
        datetext = "Date:\t{}".format(str(date))
        timetext = "Time:\t{}-{}".format(tstart, tend)
        employeetext = "Employee:\t{}".format(employee)
        twatext = "TWA:\t{} ppm".format(twa)
        peaktext = "Peak:\t{} ppm".format(peak)
        stetext = "Max STE:\t{} ppm (15 minutes)".format(ste)

        self.set_margins(25, 25, 25)

        self.image(plot, 15, 25, self.WIDTH - 30)
        self.cell(0,self.HEIGHT-150, "", 0, 1, 'L')
        self.set_font('Arial', 'B', 12)
        self.cell(40, 6, "Metrics:", 0, 1, 'L')
        self.set_font('Arial', '', 11)
        self.cell(40, 6, datetext, 0, 1, 'L')
        self.cell(40, 6, timetext, 0, 1, 'L')
        self.cell(40, 6, employeetext, 0, 1, 'L')
        self.cell(40, 6, twatext, 0, 1, 'L')
        self.cell(40, 6, peaktext, 0, 1, 'L')
        self.cell(40, 6, stetext, 0, 1, 'L')


    def print_page(self, date, tstart, tend, plot, twa, peak, ste, employee):
        # Generates the report
        self.add_page()
        self.page_body(date, tstart, tend, plot, twa, peak, ste, employee)


class MultiDayPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def header(self):
        # Custom logo and positioning

        # Check the name of the current folder. Navigate to the place where the logo is accessible.
        if os.path.basename(os.getcwd()) == "dist":
            path_parent = os.path.dirname(os.getcwd())
            print("Changing directories to {}".format(path_parent))
            os.chdir(path_parent)
        elif os.path.basename(os.getcwd()) == "AirQualityApp":
            print("Currently in AirQualityApp directory")

        self.image('assets/RockwellFullLogo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'Styrene Report', 0, 0, 'R')
        self.ln(20)

    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 5, 'Generated by Styrene Analysis Tool', 0, 1, 'C')
        self.cell(0, 5, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, dstart, dend, tstart, tend, plot, twa, peak, ste, employee):
        datetext = "Dates:\t{}-{}".format(str(dstart), str(dend))
        timetext = "Time:\t{}-{}".format(tstart, tend)
        employeetext = "Employee:\t{}".format(employee)
        twatext = "TWA:\t{} ppm".format(twa)
        peaktext = "Peak:\t{} ppm".format(peak)
        stetext = "Max STE:\t{} ppm (15 minutes)".format(ste)

        self.set_margins(25, 25, 25)

        self.image(plot, 15, 25, self.WIDTH - 30)
        self.cell(0,self.HEIGHT-150, "", 0, 1, 'L')
        self.set_font('Arial', 'B', 12)
        self.cell(40, 6, "Metrics:", 0, 1, 'L')
        self.set_font('Arial', '', 11)
        self.cell(40, 6, datetext, 0, 1, 'L')
        self.cell(40, 6, timetext, 0, 1, 'L')
        self.cell(40, 6, employeetext, 0, 1, 'L')
        self.cell(40, 6, twatext, 0, 1, 'L')
        self.cell(40, 6, peaktext, 0, 1, 'L')
        self.cell(40, 6, stetext, 0, 1, 'L')


    def print_page(self, dstart, dend, tstart, tend, plot, twa, peak, ste, employee):
        # Generates the report
        self.add_page()
        self.page_body(dstart, dend, tstart, tend, plot, twa, peak, ste, employee)


def generatesinglePDF(date, tstart, tend, plot, twa, peak, ste, employee, filename, exportpath):
    pdf = SingleDayPDF()
    pdf.print_page(date, tstart, tend, plot, twa, peak, ste, employee)
    exportfilepath = exportpath + '/' + filename
    pdf.output(exportfilepath, 'F')

def generatemultiPDF(dstart, dend, tstart, tend, plot, twa, peak, ste, employee, filename, exportpath):
    pdf = MultiDayPDF()
    pdf.print_page(dstart, dend, tstart, tend, plot, twa, peak, ste, employee)
    exportfilepath = exportpath + '/' + filename
    pdf.output(exportfilepath, 'F')
